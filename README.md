# 🎬 AI Shorts Automation Factory

An automated video production pipeline that generates vertical short-form videos (YouTube Shorts, TikTok, Reels) from text files. This tool eliminates manual video editing by programmatically combining background footage, audio, and dynamic text overlays, complete with SEO metadata generation.

## 🚀 Business Value
Manual creation of text-based short videos takes approximately 10-15 minutes per video. This script generates dozens of ready-to-publish videos in minutes, automatically calculating optimal reading duration, cropping assets to 9:16 vertical format, and rendering a flawless typewriter text effect.

## ✨ Key Features
* **Smart Video Processing:** Automatically crops landscape videos to 9:16 vertical format.
* **Dynamic Duration:** Calculates video length based on the word count of the text.
* **Custom Text Rendering:** Uses `Pillow` to generate a frame-by-frame typewriter effect without flickering, featuring dynamic font sizing and text wrapping.
* **Audio Mixing:** Automatically loops or trims background music to match video duration and applies volume scaling.
* **SEO Generation:** Includes a standalone script (`generate_seo.py`) to generate optimized YouTube titles, descriptions, and tags based on the video content.

## 🛠️ Tech Stack
* **Python 3.x**
* **MoviePy** (Video/Audio compositing and manipulation)
* **Pillow (PIL)** (Frame-by-frame text rendering and typography)

## 📁 Project Structure
```text
├── Background_Videos/   # Place your raw background clips here (.mp4, .mov)
├── Background_Music/    # Place your audio tracks here (.mp3, .wav)
├── 3_Ready_Shorts/      # Output directory for rendered videos
├── facts.txt            # Input text file (one quote/fact per line)
├── font.ttf             # Custom TrueType font for the text overlay
├── step_aesthetic.py    # Main video generation engine
└── generate_seo.py      # SEO metadata generator
