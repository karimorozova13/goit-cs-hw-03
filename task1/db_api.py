import psycopg2

def execute_query(sql, params):
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
            
            cur.execute(sql, params)
        return cur.fetchall()
    except psycopg2.Error as e:
        print("Error:", e)
        conn.rollback() 
    
    finally:
        conn.commit()  
        cur.close()  
        conn.close()  

def update_db(sql, params):
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
            
            cur.execute(sql, params)
            print('Change successfully')
    except psycopg2.Error as e:
        print("Error:", e)
        conn.rollback() 
    
    finally:
        conn.commit()  
        cur.close()  
        conn.close()  

all_tasks_by_user_id = """
SELECT t.title, t.description, s.name AS status_name
FROM tasks AS t
LEFT JOIN status AS s ON t.status_id = s.id
WHERE t.user_id = %s;
"""
all_tasks_by_status = """
SELECT t.title, t.description, s.name AS status_name
FROM tasks AS t
LEFT JOIN status AS s ON t.status_id = s.id
WHERE s.name = %s;
"""
status_id_by_name = "SELECT id FROM status WHERE name = %s;"
status_id = execute_query(status_id_by_name, ('in progress', ))
change_task_status = """
    UPDATE tasks SET status_id = %s WHERE id = %s;
    """
select_users_without_tasks = """
SELECT fullname
FROM users
WHERE id NOT IN (
    SELECT DISTINCT user_id
    FROM tasks
);
"""
insert_task_to_user = """
INSERT INTO tasks (title, description, status_id, user_id)
VALUES (%s, %s, %s, %s);
"""
all_tasks_in_progress = """
SELECT * FROM tasks
WHERE status_id != 3;
"""
delete_task_by_id = """DELETE FROM tasks WHERE id = %s;"""
select_user_by_email = """SELECT * FROM users WHERE email LIKE %s;"""
update_user_name = "UPDATE users SET fullname = %s WHERE id = %s;"
tasks_count_by_status = """
SELECT s.name AS status_name, COUNT(t.id) AS task_count
FROM tasks AS t
INNER JOIN status AS s ON t.status_id = s.id
GROUP BY s.name;
"""
users_tasks_by_domain = """
SELECT t.title, t.description, s.name AS status_name, u.fullname AS assigned_user
FROM tasks AS t
INNER JOIN users AS u ON t.user_id = u.id
INNER JOIN status AS s ON t.status_id = s.id
WHERE u.email LIKE %s;
"""
tasks_without_description = """
SELECT *
FROM tasks
WHERE description IS NULL;
"""
users_tasks_by_status = """
SELECT u.fullname, t.title, t.description
FROM users AS u
INNER JOIN tasks AS t ON u.id = t.user_id
INNER JOIN status AS s ON t.status_id = s.id
WHERE s.name = 'in progress';
"""
count_of_users_and_tasks = """
SELECT u.fullname, COUNT(t.id) AS task_count
FROM users AS u
LEFT JOIN tasks AS t ON u.id = t.user_id
GROUP BY u.fullname
ORDER BY u.fullname;
"""

print(execute_query(all_tasks_by_user_id, (2,)))
print(execute_query(all_tasks_by_status, ('completed',)))
print(execute_query(select_users_without_tasks, ()))
print(execute_query(all_tasks_in_progress, ()))
print(execute_query(select_user_by_email, ('%net%', )))
print(execute_query(tasks_count_by_status, ()))
print(execute_query(users_tasks_by_domain, ('%net%',)))
print(execute_query(tasks_without_description, ()))
print(execute_query(users_tasks_by_status, ()))
print(execute_query(count_of_users_and_tasks, ()))


update_db(change_task_status, (status_id[0][0], 17))
update_db(insert_task_to_user, ('Kari', "Works a lot", 1, 27))
update_db(delete_task_by_id, (64,))
update_db(update_user_name, ('Kari', 1))





