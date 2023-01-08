import sqlite3

def createTables(database,filename):
    with open(filename, 'r') as sql_file:
        sql_script = sql_file.read()
    cursor = database.cursor()
    cursor.executescript(sql_script)
    print("Tables created from sql file",filename)

if __name__=="__main__":
    db = sqlite3.connect('database\\realestate.db')
    createTables(db,'database\\create_tables.sql')
    db.commit()
    db.close()




