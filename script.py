# -*- coding: utf-8 -*-

import pandas as pd
import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'port': 3307,
    'password': 'root',
    'database': 'loldb'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

df = pd.read_csv('players_stats.csv')

# Troca valores vazios por 0
df.fillna(0, inplace=True)

def insert_get(table_name, value):
    cursor.execute("SELECT {}_id FROM {} WHERE nome = %s".format(table_name, table_name), (value,))
    result = cursor.fetchone()

    if result:
        return result[0]
    
    cursor.execute("INSERT INTO {} (nome) VALUES (%s)".format(table_name), (value,))
    conn.commit()
    return cursor.lastrowid

try:
    for index, row in df.iterrows():
        place_id = insert_get('Place', row.get('event'))
        team_id = insert_get('Team', row.get('team'))
        player_id = insert_get('Player', row.get('player'))
        
        # Insere os dados 
        cursor.execute(
            """
            INSERT INTO Performance (
                season_id, place_id, team_id, player_id,
                games_played, wins, loses, kills, deaths, assists,
                creep_score, gold, damage
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """.format(
                row.get('season'), place_id, team_id, player_id,
                row.get('games_played'), row.get('wins'), row.get('loses'),
                row.get('kills'), row.get('deaths'), row.get('assists'),
                row.get('creep_score'), row.get('gold'), row.get('damage')
            )
        )
    conn.commit()

# Desfaz a alteração em caso de erro
except Exception as e:
    conn.rollback()
    print("erro:", e)

cursor.close()
conn.close()
