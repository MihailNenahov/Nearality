import psycopg2

# variabiles for connecting
dbname = 'your_database_name'
user = 'your_username'
password = 'your_password'
host = 'localhost'  # or ip
port = '5432'  # post for connecting PostgreSQL

# connecting db
try:
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    print("successful connecting to PostgreSQL")
except psycopg2.Error as e:
    print("error with connecting PostgreSQL:", e)

# examples of  SQL-comands
try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM your_table;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
except psycopg2.Error as e:
    print("error:", e)
finally:
    if conn:
        conn.close()
        print("connecting closed")