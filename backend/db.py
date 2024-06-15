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
#todo: replace 1 with users chose 
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM user_info WHERE id_location = 1
                       """)
        
        rows = cursor.fetchall()  # Fetch all rows from the result set
        
        listOfPeople = ""
        for row in rows:
            listOfPeople +=f"{row}\n"
        print(f"List of locations:{listOfLocs}")
        
        print("[info] Data added")
#showing all locations
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM locations")
        
        rows = cursor.fetchall()  # Fetch all rows from the result set
        
        
        listOfLocs = ""
        for row in rows:
            listOfLocs +=f"{row}\n"
        print(f"List of locations:{listOfLocs}")
        
        print("[info] Data added")
  
except Exception as _ex:
    print("[info] error while working with procedure", _ex)
    
finally:
    if connection:
        connection.close()
        print("[info] connection closed")