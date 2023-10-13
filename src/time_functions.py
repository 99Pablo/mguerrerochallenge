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

import os
import pandas as pd
from datetime import datetime
from collections import Counter
from typing import List, Tuple


#Se define la funcion que nos devolvera la top 10 fechas con mas tweets y se menciona el usuario con mas tweets en estas fechas con enfoque en optimizacion del tiempo de ejecucion
def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    
    #Se ajusta ruta de lectura de archivo json a .parquet para futuras lecturas
    parquet_file = file_path.replace('.json', '.parquet')
    
    #Se verifica si el archivo .parquet existe, si existe se lee, si no se crea
    if os.path.exists(parquet_file):
        df = pd.read_parquet(parquet_file)
    else:
        df = pd.read_json(file_path, lines=True)
        df.to_parquet(parquet_file, index=False)
    

    #Se convierte la columna date a datetime de pandas y extraemos solo la fecha
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    #Se extrae el nombre de usuario de la columna user
    df['username'] = df['user'].apply(lambda x: x.get('username'))
    
    #Se elimina la columna user
    del df['user']

    #Se agrupa el DataFrame por fecha y nombre de usuario y se cuenta el número de tweets para cada combinación
    grouped = df.groupby(['date', 'username']).size().reset_index(name='count')

    #Se obtiene las 10 fechas con el mayor número de tweets.
    top_dates_df = df['date'].value_counts().nlargest(10).reset_index()

    # Se obtiene el usuario con mas tweets para cada una de las 10 fechas
    result = []
    for _, row in top_dates_df.iterrows():
        date = row['date']
        top_user_df = grouped[grouped['date'] == date].nlargest(1, 'count')
        top_user = top_user_df['username'].iloc[0]
        result.append((date, top_user))
    
    return result

# Se define la funcion que nos devolvera la lista de los 10 emojis mas usados con enfoque en optimizacion del tiempo de ejecucion
def q2_time(file_path: str) -> List[Tuple[str, int]]:
    
    # Se ajusta ruta de lectura de archivo json a .parquet para futuras lecturas
    parquet_file = file_path.replace('.json', '.parquet')
    
    # Se verifica si el archivo .parquet existe, si existe se lee, si no se crea
    if os.path.exists(parquet_file):
        df = pd.read_parquet(parquet_file)
    else:
        df = pd.read_json(file_path, lines=True)
        df.to_parquet(parquet_file, index=False)
    
    # Se extraen todos los emojis de la columna 'content' y se cuenta su frecuencia
    all_emojis = []
    for content in df['content']:
        emojis_in_content = [entry['emoji'] for entry in emoji.emoji_list(content)]
        all_emojis.extend(emojis_in_content)
    # Se cuenta la frecuencia de cada emoji
    emoji_counts = Counter(all_emojis)

    # Se obteniene los top 10 emojis más utilizados
    top_emojis = emoji_counts.most_common(10)
    
    return top_emojis

#Se define la funcion que nos devolvera la lista de los 10 usuarios mas mencionados en tweets con enfoque en la optimizacion del tiempo de ejecucion
def q3_time(file_path: str) -> List[Tuple[str, int]]:
    
    #Se ajusta ruta de lectura de archivo json a .parquet para futuras lecturas
    parquet_file = file_path.replace('.json', '.parquet')
    
    #Se verifica si el archivo .parquet existe, si existe se lee, si no se crea
    if os.path.exists(parquet_file):
        df = pd.read_parquet(parquet_file)
    else:
        df = pd.read_json(file_path, lines=True)
        df.to_parquet(parquet_file, index=False)
    
    
    #Se extraen todas las menciones por cada tweet
    df['mentions'] = df['content'].str.findall(r'@(\w+)')

    # Se aplana la lista de menciones, ya que cada tweet puede tener más de una mención
    mentions_flat = []
    for sublist in df['mentions'].dropna():
        for mention in sublist:
            mentions_flat.append(mention)
    # Se cuenta la frecuencia de cada mención en la lista aplanada
    mention_counts = Counter(mentions_flat)
    # Obtener los top 10 usuarios más mencionados
    top_mentions = mention_counts.most_common(10)
    
    return top_mentions