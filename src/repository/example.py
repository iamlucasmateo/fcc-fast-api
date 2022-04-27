import psycopg2

from app.utils.config import ConfigParser


# connection
config = ConfigParser()
env = config.get_env()
connection_data = config.get_data(paths=["DATABASE", env, "CONNECTION"])
conn = psycopg2.connect(**connection_data)

# retrieval
try:
    cursor = conn.cursor()
    query = "SELECT * FROM main.posts;"
    cursor.execute(query)
    data = cursor.fetchall()
    print(data)
except:
    conn.rollback()

# cleanup
cursor.close()
conn.commit()
conn.close()