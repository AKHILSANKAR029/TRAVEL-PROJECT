
#from unicodedata import name
from flask import *
import sqlite3
import mail
import random

app  = Flask(__name__)

@app.route('/')

def index():
    return render_template("login_pg.html")

@app.route('/register_pg')

def register():
    with sqlite3.connect("Register.db") as con:  
        con.execute('''CREATE TABLE IF NOT EXISTS tourist (
            aadhar int not null,
            name varchar(20) not null,
            age int not null,
            phno int not null,
            email varchar(20) not null,
            password varchar(20) not null
            )''')
        con.commit()
    with sqlite3.connect("Register.db") as con:  
        con.execute('''CREATE TABLE IF NOT EXISTS guide (
            city varchar(50) not null,
            guide_name varchar(20) not null,
            restaurant varchar(20) not null,
            hotel varchar(20) not null,
            days int not null,
            people int not null
            )''')
        con.commit()
    with sqlite3.connect("Register.db") as con:  
        con.execute('''CREATE TABLE IF NOT EXISTS payment (
            Transaction_id varchar(50) not null,
            bank_name varchar(20) not null,
            person name varchar(20) not null,
            card number int not null,
            cvv int not null,
            expiry int not null
            )''')
        con.commit()
    return render_template("register_pg.html") 

@app.route('/otp',methods = ['POST'])
def otp():
    global otp1
    if request.method == "POST":
        gmail = request.form["gmail"]  
        password = request.form["pswd"]  
        name = request.form["name"] 
        age = request.form['age']
        aadhar = request.form['aadhar']
        phone = request.form['phno']
    with sqlite3.connect("Register.db") as con:
        con.execute(
        "INSERT into tourist (email, password, name, age, aadhar, phno) values (?,?,?,?,?,?)",(gmail, password, name, age, aadhar, phone))
    otp1 = random.randint(1000,9999)
    mail.email(gmail,otp1)
    return render_template("otp.html")

@app.route('/verify',methods = ['post'])
def verify():
    if request.method == 'POST':
        if str(otp1) == request.form['otp']:
            return render_template("login_pg.html")
        else:
            return "wrong Otp"
    else:
        redirect("/")

@app.route('/home',methods = ["POST","GET"])
def home():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        con = sqlite3.connect("Register.db")
        #con.execute("SELECT email,password FROM tourist")
        cursor_obj = con.cursor()
        cursor_obj.execute("SELECT email,password FROM tourist")
        data = cursor_obj.fetchall()
        list_data = []
        data_dict = dict()
        for i in data:
            list_data.append(list(i))
        for i in list_data:
            data_dict[i[0]] = i[1]
        for i in list_data:
            if data_dict[email] != password:
                return  "Wrong password or invalid Mail id"
            else:
                return render_template("home_pg.html")
    else:
        return render_template("login_pg.html")

@app.route('/guide_pg')
def guide():
    return render_template("guide_pg.html")
@app.route('/payment',methods = ['POST'])
def payment():
    if request.method == "POST":
        city = request.form["city"]  
        guide_name = request.form["guide_name"]  
        restaurant = request.form["restaurant"] 
        hotel = request.form['hotel']
        days = request.form['days']
        people = request.form['people']
        with sqlite3.connect("Register.db") as con:
            con.execute(
            "INSERT into guide (city, guide_name, restaurant, hotel, days, people) values (?,?,?,?,?,?)",(city, guide_name, restaurant, hotel, days, people))
        return render_template('pay_pg.html')

@app.route("/success_pg", methods = ["post"])
def success():
    global transaction_id   
    if request.method == "post":
        bank = request.form["bank_name"]
        name = request.form["name"]
        card = request.form["card"]
        expiry =request.form["expiry"]
        cvv = request.form["cvv"]
        transaction_id = random.randint(100000,999999)
        with sqlite3.connect("Register.db") as con:
            con.execute(
            "INSERT into payment (Transaction_id,bank_name, name, card, expiry, cvv) values (?,?,?,?,?,?)",(transaction_id,bank, name, card, expiry, cvv))
        return render_template("success_pg.html")
    else:
        bank = request.form["bank_name"]
        name = request.form["name"]
        card = request.form["card"]
        expiry =request.form["expiry"]
        cvv = request.form["cvv"]
        transaction_id = random.randint(100000,999999)
        with sqlite3.connect("Register.db") as con:
            con.execute(
            "INSERT into payment (Transaction_id,bank_name, person, card, expiry, cvv) values (?,?,?,?,?,?)",(transaction_id,bank, name, card, expiry, cvv))
        return render_template("success_pg.html")
if __name__ == "__main__":
    app.run(debug = True)



    