import os

# Input file containing the poems/quotes used for videos
INPUT_FILE = "facts.txt"
# Output file for the generated titles and descriptions
OUTPUT_FILE = "youtube_metadata.txt"

# Base tags for the Dark Aesthetic / Poetry niche
TAGS = "dark aesthetic, sad quotes, deep thoughts, poetry, aesthetic status, heartbreak, life quotes, sad aesthetic, deep quotes, midnight thoughts"

def create_metadata():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as file:
            poems = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"❌ Error: File '{INPUT_FILE}' not found.")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_file:
        out_file.write("📄 YOUTUBE SHORTS METADATA 📄\n")
        out_file.write("="*50 + "\n\n")

        for index, poem in enumerate(poems):
            video_filename = f"aesthetic_{str(index+1).zfill(3)}.mp4" 
            # --- FORMAT TITLE ---
            # Take the first 4-5 words from the poem for an intriguing title + add emojis and hashtags
            words = poem.split()
            short_snippet = " ".join(words[:5]).rstrip(".,;:") # Take first 5 words and strip trailing punctuation
            title = f"{short_snippet}...  #shorts #quotes"

            # --- FORMAT DESCRIPTION ---
            description = (
                f"{poem}\n\n"
                f"🖤 Subscribe for more deep thoughts & dark aesthetic poetry.\n\n"
                f"#darkaesthetic #poetry #sadquotes #deepthoughts #aesthetic #quotes"
            )

            # --- WRITE TO FILE ---
            out_file.write(f"🎬 FILE: {video_filename}\n")
            out_file.write(f"📌 TITLE:\n{title}\n\n")
            out_file.write(f"📝 DESCRIPTION:\n{description}\n\n")
            out_file.write(f"🏷 TAGS (Comma separated):\n{TAGS}\n")
            out_file.write("-" * 50 + "\n\n")

    print(f"✅ Done! Open '{OUTPUT_FILE}'. It contains titles and tags for all {len(poems)} videos.")

if __name__ == "__main__":
    create_metadata()
