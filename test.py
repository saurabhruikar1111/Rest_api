from multiprocessing import connection
import sqlite3
from venv import create
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = 'CREATE TABLE users(id int, username text, password text)'
cursor.execute(create_table)

insert_q = 'INSERT INTO users VALUES(?,?,?)'
users=[
    (1,'ross','ben'),
    (2,'rachel','break'),
    (3,'monica','clean')
]

cursor.executemany(insert_q,users)
select_q = 'SELECT * FROM users'
for row in cursor.execute(select_q):
    print(row)


connection.commit()
connection.close()
