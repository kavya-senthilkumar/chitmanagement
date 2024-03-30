import mysql.connector as md,sys
import random

def prt():
    print('\n'*3)


#CREATING MAIN TABLE
def createmain():
    global n
    global tname
    query="create table "+tname+'main (sno int primary key,name char(15) )'
    cur.execute(query)
    db.commit()
    for i in range(1,n+1):
        na=input("enter name:")
        q="insert into "+tname+"main values({},'{}')".format(i,na)
        cur.execute(q)
    ti='interest'
    t='total'
    num=n+1
    tt='-----'
    q="insert into "+tname+"main values ({},'{}')".format(num,tt)
    cur.execute(q)
    q="insert into "+tname+"main values ({},'{}')".format(num+1,ti)
    cur.execute(q)
    q="insert into "+tname+"main values ({},'{}')".format(num+2,tt)
    cur.execute(q)
    q="insert into "+tname+"main values ({},'{}')".format(num+3,t)
    cur.execute(q)
    db.commit()


#CREATING ALREADY TAKEN TABLE
def createtaken():
    global tname
    q="create table "+tname+"taken (name char(20))"
    cur.execute(q)
    db.commit()


#CREATING INFORMATION TABLE
def createinfo():
    global chit_amount
    global n
    global ctype
    global tname    
    no=3
    tname=input("enter the table name: ")
    if ctype[-2:]=='wc':
        c=int(input("enter the commission amount: "))
        query="create table "+tname+'info (chitamount int,members int,perhead int,ctype char(15),commision int)'
        cur.execute(query)
        db.commit()
        per_head=chit_amount/n
        q="insert into "+tname+"info values({},{},{},'{}',{})".format(chit_amount,n,per_head,ctype,c)
        cur.execute(q)
        db.commit()
    else:
        query="create table "+tname+'info (chitamount int,members int,perhead int,ctype char(15))'
        cur.execute(query)
        db.commit()
        per_head=chit_amount/n
        q="insert into "+tname+"info values({},{},{},'{}')".format(chit_amount,n,per_head,ctype)
        cur.execute(q)
        db.commit()

        
#CREATING A NEW CHIT
def new():
    global ctype
    global chit_amount
    global n
    chit_amount=int(input("enter chit amount: "))
    n=int(input("enter number of member : "))
    print("enter whether do you want to conduct the chit funds")
    inte=input("\tas interest for all (y/n): ")
    if inte.upper()=='N':
        inte="inte for not taken"
    else:
        inte="inte for all"
    com=input("\twith comission for you(y/n): ")
    if com.upper()=='N':
        com="without comission"
    else:
        com="with comission"
    if inte=="inte for all":
        if com=="with comission":
            ctype="ia wc"
        else:
            ctype="ia woc"
    else:
        if com=="with comission":
            ctype="in wc"
        else:
            ctype="in woc"
    createinfo()   
    createmain()
    createtaken()


#CHECKING WHETHER TABLE'S EXISTANCE
def check(tn,ne):
    r='show tables'
    cur.execute(r)
    data=cur.fetchall()
    s=()
    s1=[]
    for i in range(len(data)):
        s+=data[i]
    for i in s:
        if i[-4:]=='main':
            s1.append(i)
    l=len(s1)
    j=0
    while j<l:
        if s1[j][:-4]==tn:
            yellam(tn,ne)
            break
        else:
            j+=1
    else:
        sys.stderr.write("     no such table exist :(   \n")
        

#CHECKING THE KIND OF CHIT
def yellam(tn,ne):
    q='select * from '+tn+'info'
    cur.execute(q)
    data=cur.fetchall()
    if len(data[0])==4:
        for row in data:
            ca,n,ph,ctype=row[0],row[1],row[2],row[3]
            if ctype[:2]=='ia':
                ia_woc(ca,n,ph,ne,tn)
            else:
                in_woc(ca,n,ph,ne,tn)
    else:
        for row in data:
            ca,n,ph,ctype,c=row[0],row[1],row[2],row[3],row[4]
        if ctype[:2]=="ia":
            ia_wc(ca,n,ph,c,ne,tn)
        else:
            in_wc(ca,n,ph,c,ne,tn)


#ADDING THE NAME OF THE PERSON TAKEN
def add(n,tn):
    q="insert into "+tn+"taken values ('"+n+"')"
    cur.execute(q)
    db.commit()

    
#INTEREST-ALL WITHOUT-COMMISSION
def ia_woc(ca,n,ph,ne,tn):
    discount=int(input("enter discount: "))
    name=input("enter the name of the person who had taken the chit: ")
    r="select * from "+tn+"taken"
    cur.execute(r)
    data=cur.fetchall()
    le=len(data)
    s=[]
    for i in range(le):
        s+=data[i]
    for i in range(le):
        if data[i][0]==name:
            print("the person had already taken the chit  :)")
            break
    else:
        rn=input("enter the row name: ")
        add(name,tn)
        winner=(ca-(discount+ph))
        interest=discount//(n-1)
        amp=ph-interest
        q="alter table "+tn+"main add "+rn+" char(20)"
        cur.execute(q)
        q="update "+tn+"main set "+rn+"="+str(amp)+" where name!='-----'"
        cur.execute(q)
        db.commit()
        q="update "+tn+"main set "+rn+"="+str(winner)+" where name='total'"
        cur.execute(q)
        db.commit()
        q="update "+tn+"main set "+rn+"='-----'where name='-----'"
        cur.execute(q)
        db.commit()
        q="update "+tn+"main set "+rn+"="+str(interest)+" where name='interest'"
        cur.execute(q)
        db.commit()
        q="update "+tn+"main set "+rn+"='-----'where name='"+name+"'"
        cur.execute(q)
        db.commit()        
    
    db.commit()


#INTEREST-ALL WITH-COMMISSION
def ia_wc(ca,n,ph,c,ne,tn):
    discount=int(input("enter discount: "))
    name=input("enter the name of the person who had taken the chit: ")
    r="select * from "+tn+"taken"
    cur.execute(r)
    data=cur.fetchall()
    le=len(data)
    s=[]
    for i in range(le):
        s+=data[i]
    for i in range(le):
        if data[i][0]==name:
            print("the person had already taken the chit  :)")
            break
    else:
        rn=input("enter the row name: ")
        add(name,tn)
        winner=(ca-(discount+ph))
        interest=(discount-c)//(n-1)
        amp=ph-interest
        q="alter table "+tn+"main add "+rn+" char(20)"
        cur.execute(q)
        q="update "+tn+"main set "+rn+"="+str(amp)+" where name!='-----'"
        cur.execute(q)
        db.commit()
        q="update "+tn+"main set "+rn+"="+str(winner)+" where name='total'"
        cur.execute(q)
        db.commit()
        q="update "+tn+"main set "+rn+"='-----'where name='-----'"
        cur.execute(q)
        db.commit()
        q="update "+tn+"main set "+rn+"="+str(interest)+" where name='interest'"
        cur.execute(q)
        db.commit()
        q="update "+tn+"main set "+rn+"='-----'where name='"+name+"'"
        cur.execute(q)
        db.commit()        
    db.commit()


#INTEREST-NOTALL WITHOUT-COMMISSION
def in_woc(ca,n,ph,ne,tn):
    discount=int(input("enter discount: "))
    name=input("enter the name of the person who had taken the chit: ")
    r="select * from "+tn+"taken"
    cur.execute(r)
    data=cur.fetchall()
    le=len(data)
    s=[]
    for i in range(le):
        s+=data[i]
    for i in range(le):
        if data[i][0]==name:
            print("the person had already taken the chit  :)")
            break
    else:
        rn=input("enter the row name: ")
        add(name,tn)
        winner=(ca-(discount+ph))
        interest=(discount)//(n-ne)
        amp=ph-interest
        q="alter table "+tn+"main add "+rn+" char(20)"
        cur.execute(q)
        q="update "+tn+"main set "+rn+"="+str(amp)+" where name!='-----'"
        cur.execute(q)
        db.commit()
        q="update "+tn+"main set "+rn+"="+str(winner)+" where name='total'"
        cur.execute(q)
        db.commit()
        q="update "+tn+"main set "+rn+"='-----'where name='-----'"
        cur.execute(q)
        db.commit()
        q="update "+tn+"main set "+rn+"="+str(interest)+" where name='interest'"
        cur.execute(q)
        db.commit()
        q="update "+tn+"main set "+rn+"='-----'where name='"+name+"'"
        cur.execute(q)
        db.commit()
        for i in s:
            q="update "+tn+"main set "+rn+"="+str(ph)+" where name='"+i+"'"
            cur.execute(q)
            db.commit()    
    db.commit()


#INTEREST-NOTALL WITH-COMMISSION
def in_wc(ca,n,ph,c,ne,tn):
    discount=int(input("enter discount: "))
    name=input("enter the name of the person who had taken the chit: ")
    r="select * from "+tn+"taken"
    cur.execute(r)
    data=cur.fetchall()
    le=len(data)
    s=[]
    for i in range(le):
        s+=data[i]
    for i in range(le):
        if data[i][0]==name:
            print("the person had already taken the chit  :)")
            break
    else:
        rn=input("enter the row name: ")
        add(name,tn)
        winner=(ca-(discount+ph))
        interest=(discount-c)//(n-ne)
        amp=ph-interest
        q="alter table "+tn+"main add "+rn+" char(20)"
        cur.execute(q)
        q="update "+tn+"main set "+rn+"="+str(amp)+" where name!='-----'"
        cur.execute(q)
        db.commit()
        q="update "+tn+"main set "+rn+"="+str(winner)+" where name='total'"
        cur.execute(q)
        db.commit()
        q="update "+tn+"main set "+rn+"='-----'where name='-----'"
        cur.execute(q)
        db.commit()
        q="update "+tn+"main set "+rn+"="+str(interest)+" where name='interest'"
        cur.execute(q)
        db.commit()
        q="update "+tn+"main set "+rn+"='-----'where name='"+name+"'"
        cur.execute(q)
        db.commit()
        for i in s:
            q="update "+tn+"main set "+rn+"="+str(ph)+" where name='"+i+"'"
            cur.execute(q)
            db.commit()
    db.commit()


#TO DISPLAY THE NAMES OF CHITS
def display():
    r='show tables'
    cur.execute(r)
    data=cur.fetchall()
    s=()
    s1=[]
    for i in range(len(data)):
        s+=data[i]
    for i in s:
        if i[-4:]=='main':
            s1.append(i)
    print("lists of chits:\n")
    for i in range(len(s1)):
        print('\t',i+1, s1[i][:-4])


#TO DISPLAY THE CHIT
def dist():
    name=input("enter the name of the table to be displayed:")
    r='show tables'
    cur.execute(r)
    data=cur.fetchall()
    s=()
    s1=[]
    for i in range(len(data)):
        s+=data[i]
    for i in s:
        if i[-4:]=='main':
            s1.append(i[:-4])
    print()

    if name in s1:
        q="select * from "+name+"main"
        cur.execute(q)
        data=cur.fetchall()
        l=len(data)
        q="select * from "+name+"main"
        cur.execute(q)
        for i in range(l):
            data=cur.fetchone()
            for i in range(len(data)):
                print(data[i],end='  \t  ')
            print()
            
        
    else:
        sys.stderr.write("     no such table exist :(   \n")


#CREATING A NEW CHIT-LOTTERY
def newl():
    global ctypel
    global chit_amountl
    global nl
    chit_amountl=int(input("enter chit amount: "))
    nl=int(input("enter number of member : "))
    createinfol()
    createmainl()
    createtakenl()
    

#CREATING INFORMATION TABLE-LOTTERY
def createinfol():
    global chit_amountl
    global nl
    global tnamel    
    no=3
    tnamel=input("enter the table name: ")
    cl=int(input("enter the commission amount: "))
    query="create table "+tnamel+'info (chitamount int,members int,perhead int,commision int)'
    cur.execute(query)
    db.commit()
    per_headl=chit_amountl/nl
    q="insert into "+tnamel+"info values({},{},{},{})".format(chit_amountl,nl,per_headl,cl)
    cur.execute(q)
    db.commit()

#CREATING MAIN TABLE-LOTTERY
def createmainl():
    global nl
    global tnamel
    query="create table "+tnamel+'main (sno int primary key,name char(15) )'
    cur.execute(query)
    db.commit()
    for i in range(1,nl+1):
        na=input("enter name:")
        q="insert into "+tnamel+"main values({},'{}')".format(i,na)
        cur.execute(q)
    ti='intrst'
    t='total'
    num=nl+1
    tt='-----'
    q="insert into "+tnamel+"main values ({},'{}')".format(num,tt)
    cur.execute(q)
    q="insert into "+tnamel+"main values ({},'{}')".format(num+1,ti)
    cur.execute(q)
    q="insert into "+tnamel+"main values ({},'{}')".format(num+2,tt)
    cur.execute(q)
    q="insert into "+tnamel+"main values ({},'{}')".format(num+3,t)
    cur.execute(q)
    db.commit()


#CREATING ALREADY TAKEN TABLE-LOTTERY
def createtakenl():
    global tnamel
    q="create table "+tnamel+"taken (name char(20))"
    cur.execute(q)
    db.commit()


#CHECKING THE EXISTANCE OF TABLE
def checkl(tnl,nel):
    r='show tables'
    cur.execute(r)
    data=cur.fetchall()
    s=()
    s1=[]
    for i in range(len(data)):
        s+=data[i]
    for i in s:
        if i[-4:]=='main':
            s1.append(i)
    l=len(s1)
    j=0
    while j<l:
        if s1[j][:-4]==tnl:
            yellaml(tnl,nel)
            break
        else:
            j+=1
    else:
        sys.stderr.write("     no such table exist :(   \n")


#RETREVING INFO
def yellaml(tnl,nel):
    q='select * from '+tnl+'info'
    cur.execute(q)
    data=cur.fetchall()
    for row in data:
        cal,nl,phl,cl=row[0],row[1],row[2],row[3]
    conduct(cal,nl,phl,cl,nel,tnl)


#CONDUCTING YELLAM
def conduct(cal,nl,phl,cl,nel,tnl):
    discount=(((nl-nel)+1)/100)*cal
    r="select * from "+tnl+"taken"
    cur.execute(r)
    data=cur.fetchall()
    le=len(data)
    s=[]
    for i in range(le):
        s+=data[i]
    while True:
        r=random.randint(1,nl)
        q="select name from "+tnl+"main where sno="+str(r)
        cur.execute(q)
        data1=cur.fetchall()
        if (data1[0][0]) in s:
            continue
        else:
            name=data1[0][0]
            rn=input("enter the row name: ")
            add(name,tnl)
            winner=(cal-(discount+phl))
            interest=(discount-cl)//(nl-nel)
            amp=phl-interest
            q="alter table "+tnl+"main add "+rn+" char(20)"
            cur.execute(q)
            q="update "+tnl+"main set "+rn+"="+str(amp)+" where name!='-----'"
            cur.execute(q)
            db.commit()
            q="update "+tnl+"main set "+rn+"="+str(winner)+" where name='total'"
            cur.execute(q)
            db.commit()
            q="update "+tnl+"main set "+rn+"='-----'where name='-----'"
            cur.execute(q)
            db.commit()
            q="update "+tnl+"main set "+rn+"="+str(interest)+" where name='interest'"
            cur.execute(q)
            db.commit()
            q="update "+tnl+"main set "+rn+"='-----'where name='"+name+"'"
            cur.execute(q)
            db.commit()
            for i in s:
                q="update "+tnl+"main set "+rn+"="+str(phl)+" where name='"+i+"'"
                cur.execute(q)
                db.commit()
            db.commit()
            break

#MAIN PROGRAM
print()
sys.stderr.write("\t\t\tCHIT MANAGEMENT SYSTEM\n")

db=md.connect(host='localhost',user='root',passwd='Kavya@200412',database='chitproject')
cur=db.cursor()

while True:
    print("\n\n\t+********************  MAIN MENUE  *********************+")
    print("\t+\t\t\t\t\t\t\t+")
    print("\t+\t\t1.chit by lottery\t\t\t+")
    print("\t+\t\t2.chit by yellam\t\t\t+")
    print("\t+\t\t3.exit\t\t\t\t\t+")
    print("\t+\t\t\t\t\t\t\t+")
    print("\t+\t\t\t\t\t\t\t+")
    print("\t+*******************************************************+")
    prt()
    ch=int(input("enter your choice (1-3): "))

    if ch==3:
        prt()
        print('\t_       .-"--._')
        print("       / \     /   ____\ ")
        print("       ||\\   /  /'(")
        print("       || \\ _|  '``'-.")
        print("       | \_\\ `       9\              ,")
        print("        \_       9   _ '-.=      .--'|}")
        print("         |  _        \)   |     /    /}}")
        print("          \/    = \   ;_.'/    .=\.--'`\}")
        print("          |        `-`__.;---.//` '---./`")
        print("           '.____..-'`        `|      ___   _ _   ___   _  _   _  _")
        print("           _/         __.-.__/       |_ _| | | | / _ \ | \| | | |/ /")
        print("        .-'        .-'   |||          | |  |   | |   | |  ` | |   <")
        print("     .-/          /      |\\\          |_|  |_|_| |_|_| |_|\_| |_|\_\ ")
        print("    {  |         /_     /  \|               _ _   ___   _ _")
        print("     '-\           `\--;`                  | | | /   \ | | |")
        print("        '-.          |  |                  \   / | | | | | |")
        print("           )        / _/                    |_|  \___/ \___/")
        print("          /     __.'  '--.")
        print("         (       '--. ___)))")
        print("          '-..____)))")
        print("")
        print("")
        f=input("click enter to end")
        break

    while ch==1:
        q="use lotterychit"
        cur.execute(q)
        prt()
        print("\n\n\t+**************  chit by lottery MENUE  ****************+")
        print("\t+\t\t\t\t\t\t\t+")
        print("\t+\t\t1.creting new chit\t\t\t+")
        print("\t+\t\t2.conducting next yellam\t\t+")
        print("\t+\t\t3.displaying name of chits\t\t+")
        print("\t+\t\t4.displaying a chit\t\t\t+")
        print("\t+\t\t5.exit\t\t\t\t\t+")
        print("\t+\t\t\t\t\t\t\t+")
        print("\t+\t\t\t\t\t\t\t+")
        print("\t+*******************************************************+")
        prt()
        choicel=int(input("enter your choice(1-5): "))
        
        if choicel==5:
            prt()
            f=input("click enter go to main menue")
            ch=0
            
        elif choicel==1:
            ctypel=''
            chit_amountl=''
            nl=''
            tnamel=''
            newl()
            amount_perheadl=chit_amountl/nl
            prt()
            f=input("click enter to continue")
            
        elif choicel==2:
            prt()
            tnl=input("enter the name of the table: ")
            nel=int(input("enter what is the number of yellam conducted: "))
            checkl(tnl,nel)
            prt()
            f=input("click enter to continue")

        elif choicel==3:
            prt()
            display()
            prt()
            f=input("click enter to continue")

        elif choicel==4:
            prt()
            dist()
            prt()
            f=input("click enter to continue")

        else:
            prt()
            sys.stderr.write("  (: entered a wrong choice please enter choice (1-5) :) \n")
            prt()
            f=input("click enter to continue")

        
    
    while ch==2:
        q="use chitproject"
        cur.execute(q)
        prt()
        print("\n\n\t+****************  chit by yellam MENUE  ***************+")
        print("\t+\t\t\t\t\t\t\t+")
        print("\t+\t\t1.creting new chit\t\t\t+")
        print("\t+\t\t2.conducting next yellam\t\t+")
        print("\t+\t\t3.displaying name of chits\t\t+")
        print("\t+\t\t4.displaying a chit\t\t\t+")
        print("\t+\t\t5.exit\t\t\t\t\t+")
        print("\t+\t\t\t\t\t\t\t+")
        print("\t+\t\t\t\t\t\t\t+")
        print("\t+*******************************************************+")
        prt()
        choice=int(input("enter your choice(1-5): "))
        
        if choice==5:
            prt()
            f=input("click enter go to main menue")
            ch=0
            
        elif choice==1:
            ctype=''
            chit_amount=''
            n=''
            tname=''
            new()
            amount_perhead=chit_amount/n
            prt()
            f=input("click enter to continue")
            
        elif choice==2:
            prt()
            tn=input("enter the name of the table: ")
            ne=int(input("enter what is the number of yellam conducted: "))
            check(tn,ne)
            prt()
            f=input("click enter to continue")

        elif choice==3:
            prt()
            display()
            prt()
            f=input("click enter to continue")

        elif choice==4:
            prt()
            dist()
            prt()
            f=input("click enter to continue")

        else:
            prt()
            sys.stderr.write("  (: entered a wrong choice please enter choice (1-5) :) \n")
            prt()
            f=input("click enter to continue")
    else:
        print("sorry enter choice between 1-3 ")
