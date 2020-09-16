import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# Creates SQL table
create_table = 'CREATE TABLE users (id INT, username TEXT, password TEXT)'
cursor.execute(create_table)

# Inserts 1 row into table
user = (1, 'gibran', 'nao')
insert_query = 'INSERT INTO users VALUES (?, ?, ?)'
cursor.execute(insert_query,user)

# Inserts many rows in table
users = [
    (2, 'bob', 'asdf'),
    (3, 'dave', 'password')
]
cursor.executemany(insert_query, users)

# Returns every column (*) for all data in users
selectAll_query = 'SELECT * FROM users'
for row in cursor.execute(selectAll_query):
    print(row)

selectUser_query = 'SELECT username FROM users'
for row in cursor.execute(selectUser_query):
    print(row)

connection.commit()
connection.close()