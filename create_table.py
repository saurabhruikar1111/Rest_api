import sqlite3
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text )"
create_item = "CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY, name text, price real )"

insert_query= 'INSERT INTO items VALUES(NULL,?,?)'

cursor.execute(create_item)
#cursor.execute(insert_query,('test',10.45))
cursor.execute(create_table)
connection.commit()
connection.close()