import json
from typing import List, Tuple
from datetime import datetime, date
from collections import defaultdict, Counter

def q1_time(file_path: str) -> List[Tuple[date, str]]:

    # Diccionarios para contar tweets por fecha y por usuario en cada fecha
    date_counts = Counter()
    user_counts_per_date = defaultdict(Counter)

    # Abrir el archivo y procesarlo línea por línea
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue  # Saltar líneas vacías
            try:
                tweet = json.loads(line)  # Cargar cada línea como un objeto JSON
                date_str = tweet.get('date')  # Obtener la cadena de fecha
                user = tweet.get('user', {}).get('username', '')  # Obtener el nombre de usuario
                if date_str and user:
                    # Convertir la cadena de fecha a un objeto datetime.date
                    tweet_date = datetime.fromisoformat(date_str).date()
                    # Actualizar conteo de tweets por fecha
                    date_counts[tweet_date] += 1
                    # Actualizar conteo de tweets por usuario en la fecha
                    user_counts_per_date[tweet_date][user] += 1
            except json.JSONDecodeError as e:
                # Puedes comentar la siguiente línea para evitar imprimir errores y mejorar aún más el rendimiento
                # print(f"Error al decodificar JSON en la línea {line_number}: {e}")
                continue  # Saltar líneas que no son JSON válidos
            except Exception as e:
                # print(f"Error inesperado en la línea {line_number}: {e}")
                continue  # Saltar cualquier otro error

    # Obtener las 10 fechas con más tweets
    top_10_dates = [date for date, count in date_counts.most_common(10)]

    result = []

    # Para cada fecha, encontrar el usuario con más tweets ese día
    for tweet_date in top_10_dates:
        user_counts = user_counts_per_date[tweet_date]
        # Obtener el usuario con más tweets en la fecha
        top_user = user_counts.most_common(1)[0][0]
        # Añadir la tupla al resultado
        result.append((tweet_date, top_user))

    return result
