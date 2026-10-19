from client import search_long_videos
from analyzer import analyze_trends

if __name__ == "__main__":
    topic = "machine learning tutorial"  # Можно заменить на ввод пользователя
    print(f"Анализ трендов по теме: {topic}")
    
    videos = search_long_videos(topic, max_results=20)
    df = analyze_trends(videos)
    
    if not df.empty:
        print("\nТоп видео по просмотрам:")
        print(df.sort_values("views", ascending=False).head(10)[["title", "views", "likes"]])
    else:
        print("Видео не найдены.")