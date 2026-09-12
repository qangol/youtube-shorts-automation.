import os
import random
import textwrap
import traceback
import shutil
from PIL import Image, ImageDraw, ImageFont
from moviepy import (
    VideoFileClip,
    AudioFileClip,
    ColorClip,
    CompositeVideoClip,
    ImageClip,
    concatenate_videoclips,
    concatenate_audioclips
)

print("🍷 Factory 'Dark Aesthetic' (Stable Typewriter Edition)")
print("---------------------------------------------------------")

# --- FOLDER SETTINGS ---
BG_DIR = "Background_Videos"
MUSIC_DIR = "Background_Music"
OUTPUT_DIR = "3_Ready_Shorts"
FONT_PATH = "font.ttf"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- HELPER FUNCTIONS ---
def get_media_files(folder, extensions):
    files = []
    for f in os.listdir(folder):
        if f.startswith("."):
            continue
        if f.lower().endswith(tuple(ext.lower() for ext in extensions)):
            full_path = os.path.join(folder, f)
            if os.path.isfile(full_path):
                files.append(f)
    return files

def create_typing_text_clip(text, width, height, duration, font_path, index):
    """Creates a video clip with a typewriter text effect (no flickering)"""
    max_text_height = height * 0.50
    max_text_width = width * 0.70
    font_size = 60
    min_font_size = 30
    
    # Adjust font size dynamically
    while font_size >= min_font_size:
        try:
            font = ImageFont.truetype(font_path, font_size)
        except Exception:
            font = ImageFont.truetype("/Library/Fonts/Arial Bold.ttf", font_size)

        lines = textwrap.wrap(text, width=24)
        if not lines:
            lines = [text]

        line_spacing = int(font_size * 0.3)
        total_block_height = 0
        widest_line_width = 0
        
        for line in lines:
            bbox = font.getbbox(line)
            widest_line_width = max(widest_line_width, bbox[2] - bbox[0])
            total_block_height += bbox[3] - bbox[1] + line_spacing
        total_block_height -= line_spacing

        if total_block_height <= max_text_height and widest_line_width <= max_text_width:
            break
        font_size -= 2

    total_chars = sum(len(line) for line in lines)
    typing_duration = duration * 0.6 
    time_per_char = typing_duration / max(1, total_chars)
    
    # Create a unique temp folder for the frames of this specific video
    temp_dir = f"temp_typing_frames_{index}"
    os.makedirs(temp_dir, exist_ok=True)
    
    frame_clips = []
    
    # Generate frames
    for i in range(total_chars + 1):
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        y_text = (height - total_block_height) / 2
        current_char_count = 0
        
        for line in lines:
            bbox = font.getbbox(line)
            line_w = bbox[2] - bbox[0]
            line_h = bbox[3] - bbox[1]
            x_text = (width - line_w) / 2 
            
            chars_allowed_here = max(0, i - current_char_count)
            visible_text = line[:chars_allowed_here]
            
            if visible_text:
                draw.text((x_text, y_text), visible_text, font=font, fill=(0, 0, 0, 255), stroke_width=4, stroke_fill=(0, 0, 0, 255))
                draw.text((x_text, y_text), visible_text, font=font, fill="white", stroke_width=1, stroke_fill="white")
            
            y_text += line_h + line_spacing
            current_char_count += len(line)
            
        frame_path = os.path.join(temp_dir, f"frame_{i}.png")
        img.save(frame_path)
        
        if i == total_chars:
            clip_duration = duration - typing_duration
        else:
            clip_duration = time_per_char
            
        # Load the frame and set duration (start time is calculated automatically)
        frame_clip = ImageClip(frame_path).with_duration(clip_duration)
        frame_clips.append(frame_clip)
        
    # Flawless frame concatenation without gaps
    return concatenate_videoclips(frame_clips, method="compose")

# --- MAIN LOGIC ---
try:
    with open("facts.txt", "r", encoding="utf-8") as file:
        poems = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    print("❌ Error: File 'facts.txt' not found!")
    raise SystemExit(1)

bg_files = get_media_files(BG_DIR, [".mp4", ".mov", ".m4v"])
music_files = get_media_files(MUSIC_DIR, [".mp3", ".wav", ".m4a", ".aac"])

if not poems or not bg_files or not music_files:
    print("❌ Error: Check 'facts.txt', backgrounds, and music files!")
    raise SystemExit(1)

random.shuffle(bg_files)
random.shuffle(music_files)

print(f"📝 Quotes found: {len(poems)}")
print(f"🎥 Backgrounds found: {len(bg_files)}")
print(f"🎵 Music tracks found: {len(music_files)}")
print("---------------------------------------------------------")

for index, text in enumerate(poems):
    out_name = f"aesthetic_{str(index + 1).zfill(3)}.mp4"
    out_path = os.path.join(OUTPUT_DIR, out_name)

    music_clip = None
    final_audio = None
    bg_clip = None
    dark_overlay = None
    text_overlay = None
    final_visuals = None
    final_video = None

    try:
        print(f"\n🎬 Creating {out_name}...")
        print(f"   TEXT: {text[:80]!r}")

        # Timing: minimum 7 seconds
        word_count = len(text.split())
        video_duration = max(7.0, (word_count / 2.5) + 2.0)

        # Music setup
        current_music_name = music_files[index % len(music_files)]
        current_music_path = os.path.join(MUSIC_DIR, current_music_name)
        music_clip = AudioFileClip(current_music_path)

        if music_clip.duration <= 0:
            raise ValueError(f"Invalid audio duration: {current_music_name}")

        if music_clip.duration < video_duration:
            repeats = int(video_duration // music_clip.duration) + 1
            music_clip = concatenate_audioclips([music_clip] * repeats)

        m_start = random.uniform(0, max(0, music_clip.duration - video_duration))
        final_audio = music_clip.subclipped(m_start, m_start + video_duration).with_volume_scaled(0.3)

        # Background video setup
        current_bg_name = bg_files[index % len(bg_files)]
        current_bg_path = os.path.join(BG_DIR, current_bg_name)
        bg_clip = VideoFileClip(current_bg_path)

        if bg_clip.duration <= 0:
            raise ValueError(f"Invalid video duration: {current_bg_name}")

        if bg_clip.duration < video_duration:
            repeats = int(video_duration // bg_clip.duration) + 1
            bg_clip = concatenate_videoclips([bg_clip] * repeats).subclipped(0, video_duration)
        else:
            v_start = random.uniform(0, max(0, bg_clip.duration - video_duration))
            bg_clip = bg_clip.subclipped(v_start, v_start + video_duration)

        # Crop to 9:16 ratio
        w, h = bg_clip.w, bg_clip.h
        target_ratio = 9 / 16

        if (w / h) > target_ratio + 0.05:
            new_w = int(h * target_ratio)
            bg_clip = bg_clip.cropped(
                x1=int(w / 2 - new_w / 2),
                y1=0,
                x2=int(w / 2 + new_w / 2),
                y2=h
            )
            w = new_w

        # Dark overlay
        dark_overlay = ColorClip(size=(w, h), color=(0, 0, 0)).with_opacity(0.4).with_duration(video_duration)

        # Typewriter text effect (passing index for unique temp folder)
        text_overlay = create_typing_text_clip(text, w, h, video_duration, FONT_PATH, index)

        # Final composition
        final_visuals = CompositeVideoClip([bg_clip, dark_overlay, text_overlay])
        final_video = final_visuals.with_audio(final_audio)

        print(f"   Rendering to: {out_path}")
        final_video.write_videofile(
            out_path,
            codec="libx264",
            audio_codec="aac",
            fps=30,
            logger="bar"
        )
        print(f"✅ Success: {out_name}")

    except Exception as e:
        print(f"❌ Error on video {index + 1}: {out_name}")
        print(f"   TEXT: {text!r}")
        print(f"   ERROR: {e}")
        traceback.print_exc()

    finally:
        # Memory cleanup
        for clip in [final_video, final_visuals, text_overlay, dark_overlay, bg_clip, final_audio, music_clip]:
            try:
                if clip is not None:
                    clip.close()
            except Exception:
                pass
                
        # Remove the temp folder containing frames for this specific video
        temp_dir = f"temp_typing_frames_{index}"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)

print("---------------------------------------------------------")
print("🍷 Batch processing completed successfully!")
