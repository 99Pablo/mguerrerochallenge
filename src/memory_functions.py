import os
import pandas as pd
from datetime import datetime
from typing import List, Tuple

from datetime import datetime
from typing import List, Tuple
from collections import defaultdict
import ujson as json

import os
import pandas as pd
import emoji
from datetime import datetime
from collections import Counter
from typing import List, Tuple

import ujson as json
from collections import Counter
from typing import List, Tuple
import emoji

import ujson as json
import re


#Se define la funcion que nos devolvera la top 10 fechas con mas tweets y se menciona el usuario con mas tweets en estas fechas con enfoque en optimizacion de la memoria en uso
def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    
    # Diccionario para mantener el conteo de tweets por fecha
    date_counts = defaultdict(int)
    # Diccionario para mantener el conteo de tweets de usuario por fecha
    user_date_counts = defaultdict(lambda: defaultdict(int))
    
    with open(file_path, "r") as file:
        for line in file:
            tweet = json.loads(line)
            # Se extrae la date del tweet y la convertimos a datetime.date
            tweet_date = datetime.strptime(tweet['date'].split("T")[0], '%Y-%m-%d').date()
            # Se actualiza el conteo de tweets para esa fecha
            date_counts[tweet_date] += 1
            # Se actualiza el conteo de tweets de usuario para esa fecha
            user_date_counts[tweet_date][tweet['user']['username']] += 1

    # Se ordena las fechas por numero de tweets de forma descendente y se guarda el top 10
    top_dates = sorted(date_counts, key=date_counts.get, reverse=True)[:10]
    # Para cada fecha, se obtiene el usuario con mas tweets
    result = []
    for date in top_dates:
        #Se obtiene el usuario con mas tweets para cada fecha
        top_user = max(user_date_counts[date], key=user_date_counts[date].get)
        result.append((date, top_user))
    
    return result

#Se define la funcion que nos devolvera la lista de los 10 emojis mas usados con enfoque en optimizacion de la memoria en uso
def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    
    # Se crea un counter para contar la frecuencia de cada emoji
    emoji_counts = Counter()
    
    # Se abre el archivo json y se itera sobre cada tweet
    with open(file_path, 'r') as file:
        for line in file:
            # Se convierte la linea en un diccionario
            tweet = json.loads(line)
            # Se extrae el contenido del tweet
            content = tweet.get('content', '')
            # Se extraen los emojis del contenido
            emojis_in_content = [entry['emoji'] for entry in emoji.emoji_list(content)]
                
            # Se actualiza el counter con los emojis encontrados
            emoji_counts.update(emojis_in_content)

    # Se obtienen los top 10 emojis más utilizados
    top_emojis = emoji_counts.most_common(10)
    
    return top_emojis

#Se define la funcion que nos devolvera la lista de los 10 usuarios mas mencionados en tweets con enfoque en la optimizacion de la memoria en uso
def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    
    # Se crea un counter para contar la frecuencia de cada mención
    mention_counts = Counter()
    
    # Se abre el archivo json y se itera sobre cada tweet
    with open(file_path, 'r') as file:
        for line in file:
            tweet = json.loads(line)
            content = tweet.get('content', '')
            # Se extraen las menciones del contenido
            mentions = re.findall(r'@(\w+)', content)
            # Se actualiza el counter con las menciones encontradas
            mention_counts.update(mentions)
            
    # Obtener los top 10 usuarios más mencionados
    top_mentions = mention_counts.most_common(10)
    
    return top_mentions