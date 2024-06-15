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

    with connection.cursor() as cursor:
        cursor.execute(
            """ CREATE TABLE tester(
                    id_tester serial primary key,
                    name varchar(20) not null,
                    pp int not null
                )"""
        )

    with connection.cursor() as cursor:
        cursor.execute(
            """INSERT into  tester (name,pp) values ('testor','123')"""
        )

        print("[info] data addaed")

except Exception as _ex:
    print("[info] error while working with procedure", _ex)
    
finally:
    if connection:
        connection.close()
        print("[info] connection closed")