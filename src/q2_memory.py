import json
import re
from typing import List, Tuple
from collections import Counter

def q2_memory(file_path: str) -> List[Tuple[str, int]]:
  
    # Expresión regular para extraer emojis
    emoji_pattern = re.compile(
        "[" 
        "\U0001F600-\U0001F64F"  # Emoticonos
        "\U0001F300-\U0001F5FF"  # Símbolos y pictogramas
        "\U0001F680-\U0001F6FF"  # Transporte y símbolos de mapas
        "\U0001F1E0-\U0001F1FF"  # Banderas (iOS)
        "\U00002700-\U000027BF"  # Símbolos de Dingbats
        "\U000024C2-\U0001F251"  # Otros símbolos
        "]+",
        flags=re.UNICODE
    )
    
    # Contador de emojis
    emoji_counts = Counter()
    
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
                    # Usar finditer para reducir el uso de memoria
                    for match in emoji_pattern.finditer(text):
                        emoji = match.group()
                        emoji_counts.update([emoji])
            except json.JSONDecodeError:
                continue  # Saltar líneas con JSON inválido
            except Exception:
                continue  # Saltar cualquier otro error
    
    top_10_emojis = emoji_counts.most_common(10)
    return top_10_emojis
