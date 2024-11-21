import json
import re
from typing import List, Tuple
from collections import Counter

def q3_time(file_path: str) -> List[Tuple[str, int]]:

    # Expresión regular para extraer menciones (@username)
    mention_pattern = re.compile(r'@(\w+)', flags=re.UNICODE)
    
    mention_counts = Counter()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue  # Saltar líneas vacías
            try:
                tweet = json.loads(line)
                # Ajusta según el campo que contenga el texto
                text = tweet.get('text') or tweet.get('content') 
                if text:
                    mentions = mention_pattern.findall(text)
                    mention_counts.update(mentions)
            except json.JSONDecodeError:
                continue  # Saltar líneas con JSON inválido
            except Exception as e:
                # Opcional: imprime el error para depuración
                # print(f"Error en línea {line_number}: {e}")
                continue  # Saltar cualquier otro error
    
    top_10_users = mention_counts.most_common(10)
    return top_10_users
