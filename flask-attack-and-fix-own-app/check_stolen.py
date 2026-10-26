import sqlite3
print(sqlite3.connect('stolen.db').execute('select username,password from users').fetchall())
