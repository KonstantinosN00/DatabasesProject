import sqlite3
semi='''
SELECT * FROM AGGELIA
'''
stats=f'''
SELECT type,purpose,ROUND(AVG(price),2) FROM ({semi}) as A,PAREXEI
WHERE A.ad_id=PAREXEI.ad_id AND char_code=1 AND CAST(value AS INTEGER)>100
GROUP BY type,purpose
'''

def searchbyString(c,key):
    query=f'''    
    SELECT * FROM AGGELIA WHERE title LIKE '%{key}%' 
    OR description LIKE '%{key}%' ;
    '''
    return c.execute(query)
def filterCharacteristics(c,location,type,purpose='both',min_price=0,max_price=1e10,min_sq=0,max_sq=1e5):
    query=f'''
    SELECT AGGELIA.ad_id,AGGELIA.price FROM AGGELIA,PAREXEI AS P1,PAREXEI AS P2
    WHERE location='Πάτρα' AND type='residence'
    AND purpose='rent' AND (price BETWEEN {min_price} AND {max_price})
    AND AGGELIA.ad_id=P1.ad_id AND P2.ad_id=AGGELIA.ad_id
    AND P2.char_code=2 AND CAST(P2.value AS INTEGER) BETWEEN 1 AND 2
    AND P1.char_code=1 AND CAST(P1.value AS INTEGER) BETWEEN {min_sq} AND {max_sq}
    '''
    return c.execute(query)


def userRecommedations(c,user_id):
    query=f'''
    SELECT ad_id FROM AGGELIA NATURAL JOIN PROTIMISI WHERE user_id={user_id}
    '''
    return c.execute(query)


db=sqlite3.connect("database\\realestate.db")
c=db.cursor()
#for i in searchbyString(db.cursor(),'ΟΙΚΟΠΕΔΟ'):
#for i in filterCharacteristics(c,'Πάτρα','residence',max_price=340):
for i in userRecommedations(c,500000):
    print(i)

