import random
import datetime


        
def createFavCsv(user_count,ad_count):
    fav=open("data\\favourites.csv","w",encoding="utf-8")
    fav.write("user_id,ad_id\n")
    for user_id in range(500000,500000+user_count):
        # Antistoixish se kathe user 0-3 agaphmenes aggelies
        favads=[]
        for j in range(random.randint(0,3)):
            ad_id=random.randint(1,ad_count)
            if ad_id in favads: continue
            favads.append(ad_id)
            fav.write(f"{user_id},{ad_id}\n")
    fav.close()

def createCommCsv(user_count,ad_count):
    commfile=open("data\\comments.csv","w",encoding="utf-8")
    commfile.write("ad_id,user_id,comment,comm_date,rating\n")
    for ad_id in range(1,ad_count):
        # Antistoixish se kathe aggelia 0-4 sxolia
        userscomm=[]
        for i in range(random.randint(0,5)):
            user_id=random.randint(500000,500000+user_count)
            if user_id in userscomm:continue
            userscomm.append(user_id)
            txt=".   "*random.randint(10,100)
            rating=random.randint(4,10)
            startdate=datetime.date(2016,1,1)
            date=str(startdate+datetime.timedelta(random.randint(1,2500)))
            commfile.write(f"{ad_id},{user_id},{txt},{date},{rating}\n")
    commfile.close()

def createProtCsv(user_count):
    prot=open("data\\protimiseis.csv","w",encoding="utf-8")
    prot.write("user_id,location,type,purpose\n")
    for user_id in range(500000,500000+user_count):
        typos=random.choice(["residence","prof","land"])
        purpose=random.choice(["buy","rent"])
        prot.write(f"{user_id},Πάτρα,{typos},{purpose}\n")
    prot.close()


if __name__=="__main__":
    USERS=500
    createFavCsv(USERS,200)
    createCommCsv(USERS,200)
    createProtCsv(USERS)