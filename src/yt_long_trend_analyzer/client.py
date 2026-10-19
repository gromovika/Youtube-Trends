import yt_dlp
from typing import List, Dict, Any

def get_video_metadata(video_urls: List[str]) -> List[Dict[str, Any]]:
    """
    Извлекает метаданные для списка URL видео с помощью yt-dlp.
    Возвращает список словарей с нужными полями.
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False, # Нужны полные метаданные (просмотры и т.д.)
        'skip_download': True, # Не скачивать само видео
    }

    results = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in video_urls:
            try:
                info = ydl.extract_info(url, download=False)
                # Извлекаем нужные для анализа поля
                results.append({
                    'id': info.get('id'),
                    'title': info.get('title'),
                    'view_count': info.get('view_count', 0),
                    'like_count': info.get('like_count', 0),
                    'duration': info.get('duration', 0), # в секундах
                    'upload_date': info.get('upload_date'), # YYYYMMDD
                    'url': info.get('webpage_url', url),
                })
            except Exception as e:
                print(f"Не удалось получить данные для {url}: {e}")
    
    return results

def filter_long_videos(videos: List[Dict[str, Any]], min_duration_seconds: int = 1200) -> List[Dict[str, Any]]:
    """Фильтрует видео, оставляя только длинные (по умолчанию > 20 минут)."""
    return [v for v in videos if v.get('duration', 0) >= min_duration_seconds]