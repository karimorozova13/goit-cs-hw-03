import faker
from random import randint
import psycopg2

NUMBER_USERS = 30
NUMBER_TASKS = 75
NUMBER_STATUS = 3

def generate_fake_data(number_users, number_tasks):
    fake_users = []
    fake_status =  ['new', 'in progress','completed']
    fake_tasks = []
    
    fake_data = faker.Faker()
    
    for _ in range(number_users):
        fake_users.append((fake_data.name(), fake_data.email()))
    
    for _ in range(number_tasks):
        fake_tasks.append((fake_data.sentence(nb_words=4), fake_data.paragraph(nb_sentences=3)))
    
    return fake_users, fake_status, fake_tasks

def prepare_data(users, status, tasks):
    for_users =users
    for_status = [(s,) for s in status]
    for_tasks = [
        task + (randint(1, NUMBER_STATUS), randint(1, NUMBER_USERS))
        for task in tasks
    ]
    
    return for_users, for_status, for_tasks

def insert_data_to_db(users, status, tasks):
    
    conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="13091989morozova",
            host="localhost",
            port="5432"
        )
    try:
        with conn:
            cur = conn.cursor()
            
            sql_users = "INSERT INTO users(fullname, email) VALUES(%s, %s)"
            cur.executemany(sql_users, users)
            
            sql_status = "INSERT INTO status(name) VALUES(%s)"
            cur.executemany(sql_status, status)
            
            sql_tasks= "INSERT INTO tasks(title, description, status_id, user_id) VALUES(%s,%s,%s,%s)"
            cur.executemany(sql_tasks, tasks)
            
            conn.commit()
    except psycopg2.Error as e:
        print("Error:", e)
        conn.rollback() 
    
    finally:
        conn.commit()  
        cur.close()  
        conn.close()  

if __name__ =="__main__":
    users, status, tasks = prepare_data(*generate_fake_data(NUMBER_USERS, NUMBER_TASKS))
    insert_data_to_db(users, status, tasks)
