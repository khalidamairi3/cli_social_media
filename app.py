import dbcreds
import mariadb
from social_media import social_media

conn = None
cursor = None
try:
    conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password, host=dbcreds.host,port=dbcreds.port, database=dbcreds.database)
    cursor = conn.cursor()
    social_media(conn,cursor)
except mariadb.OperationalError as e:
    print("Error connecting to MariaDB Platform: {e}")
except:
    print("an unanticipated error has occurred")
finally:
    if(cursor != None):
        cursor.close()
    if(conn != None):
        conn.rollback()
        conn.close()
