import os

# Файл со стихами (откуда брался текст для видео)
INPUT_FILE = "facts.txt"
# Куда сохраним готовые названия и описания
OUTPUT_FILE = "youtube_metadata.txt"

# Базовые теги для ниши Dark Aesthetic / Poetry
TAGS = "dark aesthetic, sad quotes, deep thoughts, poetry, aesthetic status, heartbreak, life quotes, sad aesthetic, deep quotes, midnight thoughts"

def create_metadata():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as file:
            poems = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"❌ Ошибка: Файл '{INPUT_FILE}' не найден.")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_file:
        out_file.write("📄 МЕТАДАННЫЕ ДЛЯ ЗАГРУЗКИ YOUTUBE SHORTS 📄\n")
        out_file.write("="*50 + "\n\n")

        for index, poem in enumerate(poems):
            video_filename = f"aesthetic_{str(index+1).zfill(3)}.mp4" 
            # --- ФОРМИРУЕМ НАЗВАНИЕ ---
            # Берем первые 4-5 слов из стиха для интригующего названия + добавляем эмодзи и хештег
            words = poem.split()
            short_snippet = " ".join(words[:5]).rstrip(".,;:") # Берем первые 5 слов и убираем точки на конце
            title = f"{short_snippet}...  #shorts #quotes"

            # --- ФОРМИРУЕМ ОПИСАНИЕ ---
            description = (
                f"{poem}\n\n"
                f"🖤 Subscribe for more deep thoughts & dark aesthetic poetry.\n\n"
                f"#darkaesthetic #poetry #sadquotes #deepthoughts #aesthetic #quotes"
            )

            # --- ЗАПИСЫВАЕМ В ФАЙЛ ---
            out_file.write(f"🎬 ФАЙЛ: {video_filename}\n")
            out_file.write(f"📌 НАЗВАНИЕ (Title):\n{title}\n\n")
            out_file.write(f"📝 ОПИСАНИЕ (Description):\n{description}\n\n")
            out_file.write(f"🏷 ТЕГИ (Tags - скопируй через запятую):\n{TAGS}\n")
            out_file.write("-" * 50 + "\n\n")

    print(f"✅ Готово! Открой файл '{OUTPUT_FILE}'. Там названия и теги для всех {len(poems)} видео.")

if __name__ == "__main__":
    create_metadata()
  
   