import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def analyze_trends(videos: list) -> pd.DataFrame:
    """Извлекает ключевые слова и кластеризует видео по темам."""
    if not videos:
        return pd.DataFrame()

    # Просто создаём DataFrame из списка словарей
    df = pd.DataFrame(videos)
    
    # Переименуем колонки для единообразия с вашим старым кодом
    # (если вы хотите сохранить совместимость с БД)
    df = df.rename(columns={'view_count': 'views', 'like_count': 'likes'})
    
    # Оставляем только те видео, у которых есть заголовок
    df = df.dropna(subset=['title'])
    
    if df.empty:
        return pd.DataFrame()

    # Простая кластеризация заголовков (как было раньше)
    vectorizer = TfidfVectorizer(stop_words="english", max_features=50)
    X = vectorizer.fit_transform(df["title"])
    
    n_clusters = min(3, len(df))
    if n_clusters >= 2:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        df["cluster"] = kmeans.fit_predict(X)
        
        order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names_out()
        for i in range(n_clusters):
            top_terms = [terms[ind] for ind in order_centroids[i, :5]]
            print(f"Кластер {i} (тема): {', '.join(top_terms)}")
    
    return df