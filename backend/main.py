import psycopg2
from config import host,user,password,db_name

connection = None

try:
    #connect to db
    connection = psycopg2.connect(
        host=host,
        user=user,
        password= password,
        database= db_name
    )

    connection.autocommit = True

    cursor = connection.cursor()

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )

        print (f"Serever version:{cursor.fetchone()}")

except Exception as _ex:
    print("[info] error while working with procedure", _ex)
    
finally:
    if connection:
        connection.close()
        print("[info] connection closed")