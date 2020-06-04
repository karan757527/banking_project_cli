

from datetime import datetime
import pickle
import getpass
import os

def load_db(f):
    with open(f,'rb') as file:
        db=pickle.load(file)
    return db

def update_db(obj,f): 
    with open(f, 'wb') as fp: 
        d=pickle.dump(obj, fp) 
        fp.close()

def sign_up():
    from datetime import datetime
    now = datetime.now()
    time = now.strftime("%H:%M:%S->%D")
    db=load_db("bank.pkl")
    title("Sign Up Menu")
    name=input("Enter Full Name:").upper()
    pwd=getpass.getpass("Enter Password:")
    bal=float(input("Enter Balance:"))
    bal=round(bal,2)
    acc="RJAC"+str(int(max(db.keys())[4:])+1)
    print("\nYour Account Number is:",acc)
    value={'name': name, 'password': pwd, 'balance': bal}
    db.update([(acc,value)])
    x=load_db("transaction.pkl")
    x[acc]=[("initial bal",bal,time)]
    print("\nCongratulations!!! Your Account has been created")   
    print("\nPress 1: To sign-in\nPress 2: To go to Main Menu\nEnter Your Choice: ")
    update_db(x,"transaction.pkl")
    update_db(db,"bank.pkl")
    i=input()
    while i:
        if i=='1':
            sign_in()
            break
        elif i=='2':
            break
        else:
            print("Incorrect Input, Try Again!!!")

def debit(acc):
    t_db=load_db("transaction.pkl")
    b_db=load_db("bank.pkl")
    flag=True
    while flag:
        title("Debit Window")
        amt=float(input("\nEnter amount to withdraw:"))
        amt=round(amt,2)
        if amt>b_db[acc]["balance"]:
            print("Insufficient Amount!!!!\n")
            i=input("Press 1: To try again\nPress 2: To Exit the Transaction\nEnter Your Choice: ")
            if i=='1':
                flag=True
            else:
                break
        else:
            now = datetime.now()
            time = now.strftime("%H:%M:%S->%D")
            t_db[acc].append(("debit",amt,time))
            b_db[acc]["balance"]-=amt
            print("Amount Debited Successfully!!!")
            update_db(t_db,"transaction.pkl")
            update_db(b_db,"bank.pkl")
            i=input("\nPress 1: To go to previous menu\nPress 2: To Logout\nEnter Your Choice: ")
            while i:
                if i=='1':
                    return False
                elif i=='2':
                    return True
                else:
                    print("Incorrect Input, Try Again")

def credit(acc):
    title("Credit Window")
    amt=float(input("Enter amount to add:"))
    amt=round(amt,2)
    t_db=load_db("transaction.pkl")
    b_db=load_db("bank.pkl")
    now = datetime.now()
    time = now.strftime("%H:%M:%S->%D")
    t_db[acc].append(("credit",amt,time))
    b_db[acc]["balance"]+=amt
    print("Amount Credited Successfully!!!")
    update_db(t_db,"transaction.pkl")
    update_db(b_db,"bank.pkl")
    i=input("\nPress 1: To go to previous menu\nPress 2: To Logout\nEnter Your Choice: ")
    while i:
        if i=='1':
            return False
        elif i=='2':
            return True
        else:
            print("Incorrect Input, Try Again")

def statement(acc):
    t_db=load_db("transaction.pkl")
    b_db=load_db("bank.pkl")
    title("E-Passbook Window")
    now = datetime.now()
    time = now.strftime("%H:%M:%S->%D")
    print("-"*101)
    print(f"A/C No.: {acc}".center(101))
    print(("Name: "+(b_db[acc]["name"])).center(101))
    print(("Available Balance: "+str(b_db[acc]["balance"])).center(101))
    print(f"Time: {time}".center(101))
    print("-"*101)
    print("|","S.No.".center(24),"|","Date & Time".center(24),"|","Transaction Type".center(24),"|","Amount".center(24),"|",sep="")
    print("|","-"*24,"|","-"*24,"|","-"*24,"|","-"*24,"|",sep="")
    c=1
    for i in t_db[acc]:
        t,a,d=i
        print("|",str(c).center(24),"|",d.center(24),"|",t.center(24),"|",str(a).center(24),"|",sep="")
        c+=1
    print("-"*101)

    i=input("\nPress 1: To go to previous menu\nPress 2: To Logout\nEnter Your Choice: ")
    while i:
        if i=='1':
            return False
        elif i=='2':
            return True
        else:
            print("Incorrect Input, Try Again")


def fund_transfer(acc):
    t_db=load_db("transaction.pkl")
    b_db=load_db("bank.pkl")
    while True:
        title("Fund Transfer Menu")
        acc_t=input("Enter the account no. to which you want to transfer fund: ").upper()
        if acc_t==acc:
            print("Amount cannot be transferred to same account\n")
        elif acc_t in b_db:
            amt=float(input("Enter the amount you want to Transfer: "))
            amt=round(amt,2)
            if amt>b_db[acc]["balance"]:
                print("Insufficient Amount!!!!")
            else:
                now = datetime.now()
                time = now.strftime("%H:%M:%S->%D")
                t_db[acc_t].append((f"Received from {acc}",amt,time))
                t_db[acc].append((f"Transferred to {acc_t}",amt,time))
                b_db[acc]["balance"]-=amt
                b_db[acc_t]["balance"]+=amt
                print("Amount Transfer Successfully!!!")

        else:
            print("No such account exist")
        i=input("\nPress 1: To Transfer again\nPress 2: To go to previous menu\nPress 3: To Logout\nEnter Your Choice: ")
        if i=='1':
            pass
        elif i=='2':
            update_db(t_db,"transaction.pkl")
            update_db(b_db,"bank.pkl")
            return False
        else:
            update_db(t_db,"transaction.pkl")
            update_db(b_db,"bank.pkl")
            return True


def view_bal(acc):
    b_db=load_db("bank.pkl")
    title("Balance Window")
    print(f"A/C No.: {acc}".center(101))
    print(("Name: "+(b_db[acc]["name"])).center(101))
    print("-"*101)
    print("\nYour Available Balance is:",b_db[acc]['balance'])
    i=input("\nPress 1: To go to previous Menu\nPress 2: To Logout\nEnter Your Choice: ")
    while i:
        if i=='1':
            return False
        elif i=='2':
            return True
        else:
            print("Incorrect Input, Try Again")     

def sign_in():
    db=load_db("bank.pkl")
    flag=True
    title("Customer Menu")
    acc_no=input("Enter Account No: ").upper()
    if acc_no in db:
        pwd=getpass.getpass("Enter Password: ")
        while flag:
            if db[acc_no]['password']==pwd:
                title("Customer Menu")
                print("WELCOME",db[acc_no]['name'])
                i=input("\nPress 1: For Credit\nPress 2: For Debit\nPress 3: To Transfer Fund\nPress 4: To view Balance\nPress 5: To view E-Passbook\nPress 6: To Logout\nEnter Your Choice: ")
                if i==str(1):
                    if credit(acc_no):
                        break
                elif i==str(2):
                    if debit(acc_no):
                        break
                elif i==str(3):
                    if fund_transfer(acc_no):
                        break
                elif i==str(4):
                    if view_bal(acc_no):
                        break
                elif i==str(5):
                    if statement(acc_no):
                        break
                else:
                    break

            else:
                print("\nWrong Password!!!\n\nPress 1: To Re-enter Password\nPress 2: To Exit\nEnter Your Choice: ")
                i=input()
                if i=='1':
                    pwd=getpass.getpass("Enter Password")
                else:
                    break
    else:
        print("No such user exist")
        i=input("Press 1: Sign Up\nPress 2: To go to Main Menu\nEnter Your Choice: ")
        if i==str(1):
            choice="3"
            sign_up()

def title(msg="Your Msg"):
    os.system("cls")
    print("-"*101)
    print(("-"*23).center(101))
    print("Rajasthan National Bank".center(101))
    print(("-"*23).center(101))
    print(msg.center(101))
    print("-"*101)
    print()

def fun():
    
    i=0
    while i!="3":
        title("Main Menu")
        print("\nPress 1: Sign In")
        print("\nPress 2: Sign Up")
        print("\nPress 3: To Exit")
        i=input()
        if i=='1':
            sign_in()
        elif i=='2':
            sign_up()
        elif i=="3":
            print("Thankyou...Visit Again!!!")
            print("This system is developed by Chirag & Karan")
            break
        else:
            print("Invalid Option")

fun()
