import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}, sqlite version: {sqlite3.version}")
    except Error as e:
        print(e)

    return conn

def create_connection_in_memory():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(":memory:")
        print(f"Connected, sqlite version: {sqlite3.version}")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def execute_sql(conn, sql):
    """ Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e) 

def add_project(conn , project):
    sql = """
    INSERT INTO projects(nazwa, start_date, end_date)
    VALUES (? , ? , ?);"""
    c = conn.cursor()
    c.execute(sql , project)
    conn.commit()
    return c.lastrowid

def add_task(conn , task):
    sql = """
    INSERT INTO tasks(projekt_id , nazwa , opis , status , start_date , end_date)
    VALUES (? , ? , ? , ? , ? , ?);"""
    c = conn.cursor()
    c.execute(sql , task)
    conn.commit()
    return c.lastrowid

def select_task_by_status(conn, status):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param status:
    :return:
    """
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE status=?", (status,))
    rows = c.fetchall()
    return rows    

def select_all(conn, table):
    """
    Query all rows in the table
    :param conn: the Connection object
    :return:
    """
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table}")
    rows = c.fetchall()

    return rows

def select_where(conn, table, **query):
    """
    Query tasks from table with data from **query dict
    :param conn: the Connection object
    :param table: table name
    :param query: dict of attributes and values
    :return:
    """
    c = conn.cursor()
    qs = []
    values = ()
    for k, v in query.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)
    c.execute(f"SELECT * FROM {table} WHERE {q}", values)
    rows = c.fetchall()
    return rows

def update(conn, table, id, **kwargs):
    c = conn.cursor()
    qs = []
    values = ()
    for k, v in kwargs.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = ", ".join(qs)
    sql = f"UPDATE {table} SET {q} WHERE id={id}"
    c.execute(sql, values)
    conn.commit()
    return "OK"

def delete_where(conn, table, **query):
    c = conn.cursor()
    qs = []
    values = ()
    for k, v in query.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)
    sql = f"DELETE FROM {table} WHERE {q}"
    c.execute(sql, values)
    conn.commit()
    return "DELETED"

create_projects_sql = """
-- projects table
CREATE TABLE IF NOT EXISTS projects (
  id integer PRIMARY KEY,
  nazwa text NOT NULL,
  start_date text,
  end_date text
);
"""

create_tasks_sql = """
-- zadanie table
CREATE TABLE IF NOT EXISTS tasks (
  id integer PRIMARY KEY,
  projekt_id integer NOT NULL,
  nazwa VARCHAR(250) NOT NULL,
  opis TEXT,
  status VARCHAR(15) NOT NULL,
  start_date text NOT NULL,
  end_date text NOT NULL,
  FOREIGN KEY (projekt_id) REFERENCES projects (id)
);
"""                

conn = create_connection(r"database.db")
    #   create_connection_in_memory()

execute_sql(conn , create_projects_sql)
execute_sql(conn , create_tasks_sql)

add_project(conn , ('nazwa' , 'start_date' , 'end_date'))

add_task(conn, (1 , 'pierwszy' , 'pierwszy task' , 'w trakcie' , 'poniedziałek' , 'wtorek'))

update(conn, 'tasks' , 3 , nazwa='Nowanazwa', status='Robisię', end_date='piątek')

print(delete_where(conn, 'tasks', status='nie chcę'))

#print(select_task_by_status(conn , 'w trakcie'))

#print(select_where(conn , 'tasks' , status='w trakcie' , projekt_id= 1 , start_date= 'środa'))

conn.close()

#with create_connection('datebase.db') as conn:
#    execute_sql(conn , create_projects_sql)
#    execute_sql(conn , create_tasks_sql)