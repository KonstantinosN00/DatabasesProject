import requests
import json
import random

def translate(txt):
    if txt=="Υπνοδωμάτια": return 2
    elif txt=="Μπάνια": return 3
    elif txt=="Όροφος": return 9
    elif txt=="Έτος κατασκευής": return 7
    elif txt=="Ενεργειακή Κλάση": return 15
    elif txt=="Τέντες": return 16
    elif txt=="Θέρμανση": return 10
    elif txt=="Μέσο θέρμανσης": return 14
    elif txt=="Έτος ανακαίνισης": return 8
    elif txt=="Θέα": return 17
    elif txt=="Κλιματισμός": return 13
    elif txt=="Κουφώματα αλουμινίου": return 12
    elif txt=="Πόρτα ασφαλείας": return 11
    elif txt=="Επιτρέπονται κατοικίδια": return 30
    elif txt=="Σχέδιο πόλης": return 29
    elif txt=="Οικοδομήσιμο": return 24
    elif txt=="Κήπος": return 5
    elif txt=="Ηλιακός θερμοσίφωνας": return 18
    elif txt=="Συντελεστής δόμησης": return 25
    elif txt=="Συντελεστής κάλυψης": return 26
    elif txt=="Πρόσοψη σε μέτρα": return 27
    elif txt=="Ρεύμα": return 23
    elif txt=="Parking": return 21
    elif txt=="Με αποθήκη": return 22
    elif txt=="Τζάκι": return 19
    elif txt=="Επιπλωμένο": return 20
    return -1

def performSearch(pages):
    IDs=[]
    transactions=["rent","buy"]
    categs=["re_residence","re_prof","re_land"]
    for categ in categs:
        for tr in transactions:
            for i in range(1,pages):
                res=requests.get(f"https://www.xe.gr/property/results/map_search?transaction_name={tr}&item_type={categ}&geo_place_ids[]=ChIJLe0kpZk1XhMRoIy54iy9AAQ&page={i}")
                j=json.loads(res.text)
                for ad in j["results"]:
                    IDs.append([ad["id"],tr])
    return IDs

def getDetails(id):
    url=f"https://www.xe.gr/property/results/single_result?result_id={id}"
    res=requests.get(url)
    return json.loads(res.text)["result"]

def extractInfo(R):
    adfile=open("ads.csv","a",encoding="utf-8")
    paroxes=open("paroxes.csv","a",encoding="utf-8")
    adfile.write("ad_id,publisher_id,type,location,purpose,price,title,description\n")
    paroxes.write("ad_id,char_code,value\n")
    i=0
    for xe_id,tr in R:
        i+=1
        if xe_id=='': continue
        ad=getDetails(xe_id)
        ad_id=str(i)
        publisher=random.randint(100000,100499)
        price=int(ad["price"].strip(" €").replace('.', '')) #shmantiko!! topothetountai non-breaking space
        typos=ad["item_type"][3:]
        purpose=tr
        title=ad["title"]
        location=ad["address"]
        desc=ad["publication_text"].replace(',', '')
        adfile.write(f"{ad_id},{publisher},{typos},{location},{purpose},{str(price)},{title},{desc}\n")
        #------------------------------------------------------#
        area=ad["size_with_square_meter"].replace('.','').strip(' τμ')
        paroxes.write(f"{ad_id},1,{area}\n")
        for detail in ad["characteristics_list"]:
            txt=detail["text"]
            value=str(detail["value"]).replace(',','')
            code=translate(txt)
            if code>0: paroxes.write(f"{ad_id},{str(code)},{value}\n")
    adfile.close()
    paroxes.close()

if __name__=="__main__":
    results=performSearch(2)
    print (results)
    extractInfo(results)