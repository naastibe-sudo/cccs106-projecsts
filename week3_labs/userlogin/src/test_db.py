import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="nasser1234",
        database="fletapp"
    )
    print("Connected to database successfully!")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    result = cursor.fetchall()
    print("Users:", result)
    conn.close()
except mysql.connector.Error as e:
    print("Database error:", e)
