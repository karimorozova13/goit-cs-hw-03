import psycopg2

        
def create_db():
    
    conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="13091989morozova",
            host="localhost",
            port="5432"
        )
    cursor = conn.cursor()
    
    try:
        
        
        with conn:
            with open('./task1/tasks.sql', 'r') as f:
                sql = f.read()

            cursor.execute(sql)
            conn.commit()
        
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL database:", e)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed.")
     

if __name__ =="__main__":
    create_db()
