#Deletes all entries in the table.
import sqlite3


conn = sqlite3.connect('weather.db')

sql_query = """
DELETE from City 

"""
conn.execute(sql_query)
conn.commit()
conn.close()