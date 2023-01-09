from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from PIL import Image, ImageTk
#pip install pillow
import queries

import sqlite3

WIDTH=1000
HEIGHT=600
count=0
db=sqlite3.connect('database\\realestate.db')

def printComments(adid):
    c=db.cursor()
    result =  c.execute(f"SELECT user_id,comm_date,rating,comment FROM SXOLIO WHERE ad_id={adid}").fetchall()
    for comm in result:
        print(f"User {comm[0]} on {comm[1]} commented:")
        print("Rating:",comm[2])
        print(comm[3])
        print("___________________")
    db.commit()

def printstats():
    c=db.cursor()
    result = queries.statsbytype(c)
    print("____STATS_____")
    print("Type, Purpose, Average Price")
    for row in result:
        print(f"{row[0]}   {row[1]}   {row[2]}")

def getAllAds():
    c=db.cursor()
    result =  c.execute("SELECT ad_id,title,location,purpose,price,contact_number FROM AGGELIA")
    db.commit()
    return result
    
class Login(Tk):
    def __init__(self):
        super().__init__()
        #Window Parameters
        self.title("Login to Database")
        self.iconbitmap("img\\icon.ico")
        self.geometry("500x600")
        self.configure(background='lightblue',padx=20)
        self.resizable(False,False)

        self.container=LabelFrame(width=300,height=300,background='lightblue',border=10)

        self.header=Label(self.container,text="LOGIN",font="TkDefaultFont 30 bold",fg='#797EF6',background='lightblue').pack()

        #Username form
        self.l1 = Label(self.container, text="Username:",font='10',background='lightblue').pack(pady=(60,0))
        self.user = StringVar()
        self.userInput = Entry(self.container, textvariable=self.user,font='12').pack()  

        #Password form
        self.l2 = Label(self.container,text="Password:",font='10',background='lightblue').pack() 
        self.password = StringVar()
        self.passwordInput = Entry(self.container, textvariable=self.password,font=12, show='*')
        self.passwordInput.pack()
        self.passwordInput.bind("<Return>", lambda e:self.validateUser())  
        #Login button
        self.loginButton = Button(self.container, text="ENTER",font='12',padx=20,command=self.validateUser).pack(pady=30) 
        self.container.pack(fill='both',padx=100,pady=100)

        self.newUplBtn = Button(self, text="New Uploader Profile",font='12',command=lambda: self.newUser("UPLOADER")).pack(side=LEFT,padx=50)
        self.newEndBtn = Button(self, text="New Visitor Profile",font='12',command=lambda: self.newUser("ENDIAFEROMENOS")).pack(side=LEFT,padx=20)

        
    def newUser(self,prof):
        c=db.cursor()
        ids=c.execute(f"SELECT user_id FROM {prof}").fetchall()
        newid=max(ids)[0]+1
        psw=input("Set Password: ")
        fname=input("First Name: ")
        lname=input("Last Name: ")
        email=input("Email: ")
        ph=input("Telephone Number: ")
        c.execute(f"""INSERT INTO {prof}(user_id,password,fname,lname,email,phone)
        VALUES ({newid},'{psw}','{fname}','{lname}','{email}',{ph})""")
        db.commit()

    def validateUser(self):
        u=self.user.get()
        p=self.password.get()
        if u=='admin' and p=='admin':
            self.destroy()
            App('admin')
            return
        try:upl=db.execute(f'SELECT user_id FROM UPLOADER WHERE user_id={u}').fetchone()
        except: pass
        try:end=db.execute(f'SELECT user_id FROM ENDIAFEROMENOS WHERE user_id={u}').fetchone()
        except: messagebox.showwarning(title="Error", message="Wrong credentials!\nTry again.").center()
        if upl!=None: 
            self.destroy()
            App("uploader",upl[0])
        elif end!=None: 
            self.destroy()
            App("endiaferomenos",end[0])
        db.commit()
        


class App(Tk):
    # Modes: admin / uploader / endiaferomenos
    def __init__(self,mode,user_id=500005):
        super().__init__()
        self.style=ttk.Style(self)
        self.style.theme_create( "custom_theme", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 0, 2, 0]}},
        "TNotebook.Tab": {
            "configure": {"padding": [20, 20], "background": "#B1D4E0" },
            "map":       {"background": [("selected", "#2E8BC0")],
                          "expand": [("selected", [10, 1, 1, 0])] } } } )
        self.style.theme_use("custom_theme")
        self.style.configure("Treeview",background="#D3D3D3",foreground="black",rowheight=25,fieldBackground="#D3D3D3")
        self.style.map("Treeview",background=[('selected',"#347083")])

        self.mode=mode
        self.user=user_id
        self.viewed_ad=0
        self.updating_ad=0
        

        #Window Parameters
        self.title("Real Estate DB Manager")
        self.iconbitmap("img\\icon.ico")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.resizable(False,False)

        #Create Menu Tabs
        self.tabs=ttk.Notebook(self,width=200,height=600)
        self.allAdsTab=Frame(self.tabs,background="lightgrey")
        self.myAdsTab=Frame(self.tabs,background='lightblue')
        self.viewAdTab=Frame(self.tabs,background="lightgrey")
        self.alterAdTab=Frame(self.tabs,background="lightgrey")
        self.searchTab=Frame(self.tabs,background="lightgrey")
        self.allAdsTab.pack()
        self.myAdsTab.pack()
        self.viewAdTab.pack()
        self.alterAdTab.pack()
        self.searchTab.pack()
        #Append Tabs
        self.tabs.add(self.allAdsTab,text="Main Menu")
        self.tabs.add(self.myAdsTab,text="My Advertisements",state='hidden')
        self.tabs.add(self.viewAdTab,text="View Advertisement",state='hidden')
        self.tabs.add(self.alterAdTab,text="Update Advertisement",state='hidden')
        self.tabs.add(self.searchTab,text="Search Advertisements")
        self.tabs.pack(fill='both') 
        #----------------------------------------------#
        Button(self.myAdsTab,text="Click to print recommended Advertisements to command line...",command=self.printRecomm).pack(padx=100,pady=100)
        #----------------------------------------------#
        #ALL ADS TAB
        #Treeview container
        self.treeFrame=Frame(self.allAdsTab)
        self.treeFrame.pack(pady=25)

        #Scrollbar setting
        self.scr=Scrollbar(self.treeFrame)
        self.scr.pack(side=RIGHT,fill=Y)

        #Treeview
        self.tree=ttk.Treeview(master=self.treeFrame,height=15,yscrollcommand=self.scr.set,selectmode="extended")
        self.tree.pack()
        self.scr.config(command=self.tree.yview)

        headers=("Ad_id","Title","Location","Purpose","Price","Contact Number")
        
        self.tree['columns']=headers
        self.tree.column("#0",width=0,stretch=NO)
        self.tree.column(headers[0],anchor=CENTER,width=50,minwidth=100)
        self.tree.column(headers[1],anchor=CENTER,width=300,minwidth=100)
        self.tree.column(headers[2],anchor=CENTER,width=150,minwidth=100)
        self.tree.column(headers[3],anchor=CENTER,width=100,minwidth=100)
        self.tree.column(headers[4],anchor=CENTER,width=100,minwidth=100)
        self.tree.column(headers[5],anchor=CENTER,width=150,minwidth=100)
        self.tree.heading("#0",text="",anchor=W)
        self.tree.heading(headers[0],text=headers[0],anchor=CENTER)
        self.tree.heading(headers[1],text=headers[1],anchor=CENTER)
        self.tree.heading(headers[2],text=headers[2],anchor=CENTER)
        self.tree.heading(headers[3],text=headers[3],anchor=CENTER)
        self.tree.heading(headers[4],text=headers[4],anchor=CENTER)
        self.tree.heading(headers[5],text=headers[5],anchor=CENTER)
        self.tree.tag_configure('oddrow',background='white')
        self.tree.tag_configure('evenrow',background="lightblue")
        #Fill the table
        self.rows=getAllAds()
        count=0
        for row in self.rows:
            if count%2==0:
                self.tree.insert(parent='',index='end',iid=count,text='',values=(row[0],row[1],row[2],row[3],str(row[4])+' €',row[5]),tags=('evenrow',))
            else:
                self.tree.insert(parent='',index='end',iid=count,text='',values=(row[0],row[1],row[2],row[3],str(row[4])+' €',row[5]),tags=('oddrow',))
            count+=1
        
        self.actionBtnsContainer=LabelFrame(self.allAdsTab,text="Action Buttons",padx=20,pady=5,background='lightgrey')
        self.actionBtnsContainer.pack()
        #Action Buttons
        Button(self.actionBtnsContainer,text='+',font="TkDefaultFont 16",command=self.newAd,padx=10,pady=3,background='lightgreen').pack(side=LEFT,padx=[20,10],anchor=W)
        self.viewAdbtn=Button(self.actionBtnsContainer,text="View Advertisement",command=self.selectAd,padx=10,pady=10,background='lightblue')
        self.viewAdbtn.pack(side=LEFT,padx=[40,10],anchor=W)
        self.deleteAdbtn=Button(self.actionBtnsContainer,text="Delete Advertisement",command=self.deleteAd,padx=10,pady=10,background='lightblue')
        self.deleteAdbtn.pack(side=LEFT,padx=[40,10],anchor=W)
        self.updateAdbtn=Button(self.actionBtnsContainer,text="Modify Advertisement",command=self.updateAd,padx=10,pady=10,background='lightblue')
        self.updateAdbtn.pack(side=LEFT,padx=[40,40],anchor=W)
        #--------------------------------------------------------------#
    #SEARCH ADS TAB
        #1
        self.search1=StringVar()
        self.searchFr1=LabelFrame(self.searchTab,background='lightgrey',padx=20,pady=20,text="Search by keyword",font="TkDefaultFont 10")
        Entry(self.searchFr1,font="TkDefaultFont 12",textvariable=self.search1).pack(side=LEFT)
        Button(self.searchFr1,text="Search...",padx=10,pady=2,command=self.printAdsbyString).pack(side=LEFT,padx=[20,0])
        self.searchFr1.pack(pady=[40,0])

        #2
        [self.type,self.purpose,self.location,self.pricemin,self.pricemax]=[StringVar(),StringVar(),StringVar(),StringVar(),StringVar()]
        self.searchFr2=LabelFrame(self.searchTab,background='lightgrey',padx=20,pady=20,text="Search by keyword",font="TkDefaultFont 10")
        Label(self.searchFr2,background='lightgrey',text="Type: ").pack(side=LEFT)
        Entry(self.searchFr2,width=5,font="TkDefaultFont 12",textvariable=self.type).pack(side=LEFT,padx=[0,15])
        Label(self.searchFr2,background='lightgrey',text="Purpose: ").pack(side=LEFT)
        Entry(self.searchFr2,width=5,font="TkDefaultFont 12",textvariable=self.purpose).pack(side=LEFT,padx=[0,15])
        Label(self.searchFr2,background='lightgrey',text="Location: ").pack(side=LEFT)
        Entry(self.searchFr2,width=5,font="TkDefaultFont 12",textvariable=self.location).pack(side=LEFT,padx=[0,15])
        Label(self.searchFr2,background='lightgrey',text="Min Price: ").pack(side=LEFT)
        Entry(self.searchFr2,width=5,font="TkDefaultFont 12",textvariable=self.pricemin).pack(side=LEFT,padx=[0,15])
        Label(self.searchFr2,background='lightgrey',text="Max Price: ").pack(side=LEFT)
        Entry(self.searchFr2,width=5,font="TkDefaultFont 12",textvariable=self.pricemax).pack(side=LEFT,padx=[0,15])
        Button(self.searchFr2,background='lightgrey',text="Search...",padx=10,pady=2,command=self.printFiltered).pack(side=LEFT,padx=[20,0])
        self.searchFr2.pack(pady=[40,0])

        #stats
        self.statsFr=LabelFrame(self.searchTab,background='lightgrey',padx=20,pady=15,text="Stats",font="TkDefaultFont 10")
        Button(self.statsFr,text="Print Stats...",padx=10,pady=2,command=printstats).pack(side=LEFT)
        self.statsFr.pack(pady=[40,0])
        #--------------------------------------------------------------#
        if self.mode!='admin': 
            self.deleteAdbtn['state']=DISABLED
            self.updateAdbtn['state']=DISABLED
        if self.mode=='endiaferomenos':
            self.tabs.tab(self.myAdsTab,state='normal')

    def newAd(self):return
       
    def updateAd(self):
        selected=self.tree.focus()
        values=self.tree.item(selected,'values') 
        if values=='': return

        for child in self.alterAdTab.winfo_children(): child.destroy()
        #Move to Update Tab
        self.tabs.tab(self.alterAdTab,state='normal')
        self.updating_ad=int(values[0])
        self.tabs.select(self.alterAdTab)

    #Form Frame
        self.updateFormFrame=LabelFrame(self.alterAdTab,padx=20,pady=20)
        self.updateFormFrame.columnconfigure(0,weight=1)
        self.updateFormFrame.columnconfigure(1,weight=3)

        Label(self.updateFormFrame,padx=50, justify=LEFT,font="TkDefaultFont 11", text="ad_id").grid(row=0,column=0,stick=W,pady=(0,15))
        Label(self.updateFormFrame,padx=50, justify=LEFT,font="TkDefaultFont 11", text="Title").grid(row=1,column=0,stick=W,pady=(0,15))
        Label(self.updateFormFrame,padx=50, justify=LEFT,font="TkDefaultFont 11", text="Location").grid(row=2,column=0,stick=W,pady=(0,15))
        Label(self.updateFormFrame,padx=50, justify=LEFT,font="TkDefaultFont 11", text="Price").grid(row=3,column=0,stick=W,pady=(0,15))
        Label(self.updateFormFrame,padx=50, justify=LEFT,font="TkDefaultFont 11", text="Contact Number").grid(row=4,column=0,stick=W,pady=(0,15))
        Label(self.updateFormFrame,padx=50, justify=LEFT,font="TkDefaultFont 11", text="Description").grid(row=5,column=0,stick=W,pady=(0,15))
        [self.newid,self.newtitle,self.newloc,self.newprice,self.newphone]=[StringVar(),StringVar(),StringVar(),StringVar(),StringVar()]
        self.id_field = Entry(self.updateFormFrame,width=35,font="TkDefaultFont 13",textvariable=self.newid)
        self.title_field = Entry(self.updateFormFrame,width=35,font="TkDefaultFont 13",textvariable=self.newtitle)
        self.loc_field = Entry(self.updateFormFrame,width=35,font="TkDefaultFont 13",textvariable=self.newloc)
        self.price_field = Entry(self.updateFormFrame,width=35,font="TkDefaultFont 13",textvariable=self.newprice)
        self.phone_field = Entry(self.updateFormFrame,width=35,font="TkDefaultFont 13",textvariable=self.newphone)
        self.desc_field = scrolledtext.ScrolledText(self.updateFormFrame,font="TkDefaultFont 10",width=55,height=10)
        self.id_field.grid(row=0,column=1,pady=(0,15))
        self.title_field.grid(row=1,column=1,pady=(0,15))
        self.loc_field .grid(row=2,column=1,pady=(0,15))
        self.price_field.grid(row=3,column=1,pady=(0,15))
        self.phone_field.grid(row=4,column=1,pady=(0,15))
        self.desc_field.grid(row=5,column=1,pady=(15,15))
        c=db.cursor()
        (ad_id,title,desc,loc,phone,price)=c.execute(f"SELECT ad_id,title,description,location,contact_number,price FROM AGGELIA WHERE ad_id={self.updating_ad}").fetchone()
        #Set current ad info
        self.id_field.insert(0,ad_id)
        self.title_field.insert(0,title)
        self.loc_field.insert(0,loc)
        self.price_field.insert(0,price)
        self.phone_field.insert(0,phone)
        self.desc_field.insert('1.0',desc)
        
        
        self.updateFormFrame.pack(pady=(50,0))

    #Buttons Layout
        self.updateBtnFrame=Frame(self.alterAdTab,background="lightgrey")
        self.confirmChangesButton=Button(self.updateBtnFrame,padx=20,pady=10,text="Confirm",command=self.confirmUpdate).pack(padx=20,pady=10,side=LEFT)
        self.discardChangesButton=Button(self.updateBtnFrame,padx=20,pady=10,text="Discard",command=self.discardChanges).pack(pady=10,side=LEFT)
        self.updateBtnFrame.pack()

    def discardChanges(self):
        self.tabs.tab(self.alterAdTab,state='hidden')
        for child in self.alterAdTab.winfo_children(): child.destroy()
        self.tabs.select(self.allAdsTab)

    def confirmUpdate(self):
        if self.newid.get().isnumeric()==False : 
            print("Select an integer as ID of the advertisement!")
            return
        desc=''
        c=db.cursor()
        c.execute(f"""UPDATE AGGELIA 
        SET ad_id={self.newid.get()},title='{self.newtitle.get()}',description='{desc}',location='{self.newloc.get()}',contact_number='{self.newphone.get()}',price='{self.newprice.get()}'
        WHERE ad_id={self.updating_ad}
        """)
        db.commit()
        self.tabs.select(self.allAdsTab)
        self.refreshAll()
        self.tabs.tab(self.alterAdTab,state='hidden')

    def viewAd(self):
        c=db.cursor()
        result=c.execute(f"SELECT type FROM AGGELIA WHERE ad_id={self.viewed_ad}").fetchone()
        if result==None: 
            self.tabs.select(self.allAdsTab)
            self.tabs.tab(self.viewAdTab,state='hidden')
            return
        typos=result[0]
        #CLEAR PREVIOUS CONTENT
        for child in self.viewAdTab.winfo_children():
            child.destroy()

    #Top Frame
        self.topAdFrame=Frame(self.viewAdTab,background="lightgrey")
        self.topAdFrame.pack()
        if typos=="residence": self.img = ImageTk.PhotoImage(Image.open("img\\house.png"))
        elif typos=="prof": self.img = ImageTk.PhotoImage(Image.open("img\\office.png"))
        else: self.img = ImageTk.PhotoImage(Image.open("img\\land.png"))
        self.adImg=Label(self.topAdFrame,image=self.img,borderwidth=5, relief="ridge")
        self.adImg.image=self.img
        self.adImg.grid(row=0,column=0,rowspan=10,columnspan=3,padx=[60,20],pady=[50,20])
        # Ad Details
        (title,desc,loc,purp,price)=c.execute(f"SELECT title,description,location,purpose,price FROM AGGELIA WHERE ad_id={self.viewed_ad}").fetchone()
        rating=c.execute(f"SELECT ROUND(AVG(rating),1) FROM SXOLIO WHERE ad_id={self.viewed_ad};").fetchone()
        rating=str(rating[0])
        if purp=="rent": purp="Ενοικίαση"
        else: purp="Προς Πώληση"

        self.adTitle=Label(self.topAdFrame,text=title.upper(),font="TkDefaultFont 25",background='lightgrey').grid(row=0,column=3,padx=30,pady=[40,10],sticky=W)
        self.adPurpLocPrice=Label(self.topAdFrame,text=purp+': '+str(price)+' €\n\n'+"Τοποθεσία: "+loc+'\nΜέση Βαθμολογία χρηστών: '+rating+'/10',font="TkDefaultFont 15",background='lightgrey',justify=LEFT).grid(row=1,column=3,padx=30,sticky=W)
        self.commBtn=Button(self.topAdFrame,text="Comments",padx=8,command=lambda: printComments(self.viewed_ad)).grid(row=7,column=3,padx=30,sticky=E)
        self.detailsBtn=Button(self.topAdFrame,text="Details",padx=20,command=self.detailsBox).grid(row=8,column=3,padx=30,sticky=E)

    #Bottom Frame
        self.descContainer=LabelFrame(self.viewAdTab,text="Description")
        self.adDesc=Label(self.descContainer,text=desc,font="TkDefaultFont 10",background='lightgrey',wraplength=850,justify=LEFT).pack()
        self.descContainer.pack()
        db.commit()

    def selectAd(self):
        selected=self.tree.focus()
        values=self.tree.item(selected,'values') 
        if values=='': return

        self.tabs.tab(self.viewAdTab,state='normal')
        self.viewed_ad=int(values[0])
        self.tabs.select(self.viewAdTab)
        self.viewAd()
    
    def deleteAd(self):
        selected=self.tree.focus()
        values=self.tree.item(selected,'values') 
        if values=='': return
        #If Ad is open, close adView Tab
        if int(values[0])==self.viewed_ad: self.tabs.tab(self.viewAdTab,state='hidden')
        if int(values[0])==self.updating_ad: self.tabs.tab(self.alterAdTab,state='hidden')
        del_ad=int(values[0])
        db.execute(f"DELETE FROM AGGELIA WHERE ad_id={del_ad}")
        db.commit()
        self.refreshAll()
    
    def detailsBox(self):
        c=db.cursor()
        detailsquery=f'''
        SELECT XARAKTIRISTIKO.code,XARAKTIRISTIKO.name,PAREXEI.value 
        FROM PAREXEI,XARAKTIRISTIKO 
        WHERE ad_id={self.viewed_ad} AND PAREXEI.char_code=XARAKTIRISTIKO.code
        '''
        res=c.execute(detailsquery).fetchall()
        num_rows=len(res)
        self.detWin=Toplevel(self)
        self.detWin.geometry(f"400x{num_rows*32+60}")
        self.detWin.title("Details for Ad with id: "+str(self.viewed_ad))

        self.detailrows=[] #code,stingvar,entrybox
        countrows=0
        for (code,key,value) in res:
            if code==1: value+=' τ.μ.'
            tempvar=StringVar()
            self.keyLabel=Label(self.detWin,text=key,wraplength=150).grid(row=countrows,column=0,sticky=W,padx=10,pady=5)
            self.valueBox=Entry(self.detWin,textvariable=tempvar,font="TkDefaultFont 10",width=34)
            self.valueBox.insert(0,value)
            self.valueBox.config(state=DISABLED)
            self.valueBox.grid(row=countrows,column=1,sticky=W,padx=10)
            #Keep track of details displayed
            self.detailrows.append([code,tempvar,self.valueBox])
            countrows+=1
        db.commit()
        if self.mode=='admin':
            Button(self.detWin,text="Update Details",command=self.updateDetails).grid(row=countrows,column=0,columnspan=2,padx=[10,0],pady=20)
            for [i,j,vb] in self.detailrows:
                vb.config(state=NORMAL)
    
    def updateDetails(self):
        c=db.cursor()
        updatequery='''
        UPDATE PAREXEI SET value=?1
        WHERE ad_id=?2 AND char_code=?3
        '''
        for [code,var,vb] in self.detailrows:
            value=var.get()
            if code==1: value=value.replace('τ.μ.','').replace(' ','')
            c.execute(updatequery,(value,self.viewed_ad,code))
        self.detWin.destroy()

    #Refresh Ads Display
    def refreshAll(self):
        self.rows=getAllAds()
        count=0
        for child in self.tree.get_children(): self.tree.delete(child)
        for row in self.rows:
            if count%2==0:
                self.tree.insert(parent='',index='end',iid=count,text='',values=(row[0],row[1],row[2],row[3],str(row[4])+' €',row[5]),tags=('evenrow',))
            else:
                self.tree.insert(parent='',index='end',iid=count,text='',values=(row[0],row[1],row[2],row[3],str(row[4])+' €',row[5]),tags=('oddrow',))
            count+=1           

    def printRecomm(self):
        c=db.cursor()
        print("ad_id,publisher_id,type,location,purpose,price,title")
        for ad in queries.userRecommedations(c,self.user):
            print(ad[0],ad[1],ad[2],ad[3],ad[4],ad[5],ad[6])

    def printAdsbyString(self):
        c=db.cursor()
        print("\n\nSearching for:",self.search1.get())
        print("ad_id,publisher_id,type,location,purpose,price,title")
        for ad in queries.searchbyString(c,self.search1.get()):
            print(ad[0],ad[1],ad[2],ad[3],ad[4],ad[5],ad[6])

    def printFiltered(self):
        query="SELECT ad_id,publisher_id,type,location,purpose,price,title FROM AGGELIA WHERE 1=1 "
        field=self.type.get().strip(' ')
        if (field!=''):
            query+=f"AND type='{field}' "
        field=self.purpose.get().strip(' ')
        if (field!=''):
            query+=f"AND purpose='{field}' "
        field=self.location.get().strip(' ')
        if (field!=''):
            query+=f"AND location='{field}' "
        field=self.pricemin.get().strip(' ')
        if (field!=''):
            query+=f"AND price>={field} "
        field=self.pricemax.get().strip(' ')
        if (field!=''):
            query+=f"AND price<={field} "
        c=db.cursor()
        result = c.execute(query)
        print("ad_id,publisher_id,type,location,purpose,price,title")
        for ad in result:
            print(ad[0],ad[1],ad[2],ad[3],ad[4],str(ad[5])+"€",ad[6])
        

if __name__ == '__main__':
    Login().mainloop()
    #App('endiaferomenos').mainloop()