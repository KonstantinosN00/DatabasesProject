import pandas as pd
import sqlite3

def addDataFromCsv(database,table,filename):
    data=pd.read_csv(filename)
    data.to_sql(table,database,if_exists='append',index=False)
    print(f"Table {table} filled with data from file: {filename}")


if __name__=="__main__":
    db = sqlite3.connect('database\\realestate.db')
    addDataFromCsv(db,'XARAKTIRISTIKO','data\\characteristics_list.csv')
    addDataFromCsv(db,'UPLOADER','data\\uploader.csv')
    addDataFromCsv(db,'ENDIAFEROMENOS','data\\endiaferomenos.csv')
    addDataFromCsv(db,'AGGELIA','data\\ads.csv')
    addDataFromCsv(db,'PAREXEI','data\\paroxes.csv')
    addDataFromCsv(db,'AGAPIMENA','data\\favourites.csv')
    addDataFromCsv(db,'SXOLIO','data\\comments.csv')
    addDataFromCsv(db,'PROTIMISI','data\\protimiseis.csv')
    addDataFromCsv(db,'MESITIKI','data\\companies.csv')



    #data=pd.read_csv("data\\south_houses.csv")[["ad_id","publisher_id","type","location","price","contact_number","description",#"purpose"]]
    #try: data.to_sql('AGGELIA',db,if_exists='append',index=False)
    #except sqlite3.IntegrityError: print("Already exists!")
    #print(data)

    db.commit()
    db.close()