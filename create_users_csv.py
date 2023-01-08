import random
import string
import names


def randString(size):
    s=''
    for j in range(size): s+=random.choice(string.ascii_lowercase)
    return s

def createcsv(filename,start):
    f = open (filename,"w",encoding="utf-8")
    if "uploader" in filename: f.write("user_id,password,fname,lname,email,phone,company_afm\n")
    else: f.write("user_id,password,fname,lname,email,phone\n")
    for i in range(500):
        user=str(start+i)      
        password=randString(10)
        fname=names.get_first_name()
        lname=names.get_last_name()
        email=(fname+'_'+lname+"@example.com").lower()
        phone=str(6900000000+random.randint(0,99999999))
        afm=''
        if "uploader" in filename:
            if(random.random()<0.06): # 6% mesites stous uploaders
                afm=random.choice(["123456789","987654321"])
            f.write((f"{user},{password},{fname},{lname},{email},{phone},{afm}\n"))
            continue
        f.write(f"{user},{password},{fname},{lname},{email},{phone}\n")
    f.close()
    print(f".csv file with random users created {filename}")

if __name__=="__main__":
    createcsv("data\\uploader.csv",100000)
    createcsv("data\\endiaferomenos.csv",500000)