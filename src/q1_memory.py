import json
from typing import List, Tuple
from datetime import datetime, date
from collections import Counter, defaultdict

def q1_memory(file_path: str) -> List[Tuple[date, str]]:
    # Primera pasada: Contar tweets por fecha
    date_counts = Counter()

    with open(file_path, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue  # Saltar líneas vacías
            try:
                tweet = json.loads(line)
                date_str = tweet.get('date')
                if date_str:
                    tweet_date = datetime.fromisoformat(date_str).date()
                    date_counts[tweet_date] += 1
            except json.JSONDecodeError:
                continue  # Saltar líneas con JSON inválido
            except Exception:
                continue  # Saltar cualquier otro error

    # Obtener las 10 fechas con más tweets
    top_10_dates = set(date for date, _ in date_counts.most_common(10))

    # Segunda pasada: Encontrar el usuario con más tweets en las top 10 fechas
    user_counts_per_date = defaultdict(Counter)

    with open(file_path, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                tweet = json.loads(line)
                date_str = tweet.get('date')
                user = tweet.get('user', {}).get('username', '')
                if date_str and user:
                    tweet_date = datetime.fromisoformat(date_str).date()
                    if tweet_date in top_10_dates:
                        user_counts_per_date[tweet_date][user] += 1
            except json.JSONDecodeError:
                continue
            except Exception:
                continue

    # Construir el resultado
    result = []

    # Ordenar las fechas por cantidad de tweets de manera descendente
    sorted_top_dates = sorted(top_10_dates, key=lambda d: date_counts[d], reverse=True)

    for tweet_date in sorted_top_dates:
        user_counts = user_counts_per_date[tweet_date]
        top_user = user_counts.most_common(1)[0][0]
        result.append((tweet_date, top_user))

    return result
