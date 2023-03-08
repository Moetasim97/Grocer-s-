from flask import Flask,render_template,request,session,redirect,url_for

from werkzeug.security import check_password_hash,generate_password_hash
from flask_session import Session
from helper import login_required
import sqlite3

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.run(debug=True)


app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d



db=sqlite3.connect("datahub.db",check_same_thread=False)
db.row_factory = dict_factory
connector=db.cursor()
#Now, I'm going to create the first table in the database
connector.execute('''CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    hash TEXT NOT NULL,
    registration_time TEXT NOT NULL);''')


name=""

@app.route("/",methods=["GET","POST"])
@login_required
def home():
    umbrella_user = connector.execute("SELECT * FROM users;")
    for user in umbrella_user:
        if session["user_id"]==user["id"]:
            name=user["name"]
            return render_template("home.html",name=name)

@app.route("/queryfruit",methods=["GET"])
@login_required
def queryfunc():
    fruitquery="%"+request.args.get("fruit")+"%"
    if fruitquery:
        fruit_data = connector.execute("SELECT * FROM fru_veg WHERE name LIKE ?",(fruitquery,))
        fruit_data=fruit_data.fetchall()
    else:
        fruit_data=[]
    return render_template("fruit.html",results=fruit_data)

#meat query path
@app.route("/querymeat", methods=["GET"])
@login_required
def querymeatfunc():
    meatquery = "%"+request.args.get("meat")+"%"
    if meatquery:
        meat_data = connector.execute(
            "SELECT * FROM meat WHERE product_type LIKE ?", (meatquery,))
        meat_data = meat_data.fetchall()
    else:
        meat_data = []
    return render_template("meat.html", meat_results=meat_data)

# frozen products query path
@app.route("/queryfrozen", methods=["GET"])
@login_required
def queryfrozenfunc():
    frozenquery = "%"+request.args.get("froze")+"%"
    if frozenquery:
        frozen_data = connector.execute(
            "SELECT * FROM frozen WHERE product_type LIKE ?", (frozenquery,))
        frozen_data = frozen_data.fetchall()
    else:
        frozen_data = []
    return render_template("frozen.html", frozen_results=frozen_data)

# dairy products query path
@app.route("/querydairy", methods=["GET"])
@login_required
def querydairy():
    dairyquery = "%"+request.args.get("dairyEggs")+"%"
    if dairyquery:
        dairy_data = connector.execute(
            "SELECT * FROM dairy_eggs WHERE product_type LIKE ?", (dairyquery,))
        dairy_data = dairy_data.fetchall()
    else:
        dairy_data = []
    return render_template("dairy.html", dairy_results=dairy_data)

#food cupboard query path
@app.route("/querycupboard", methods=["GET"])
@login_required
def querycupboard():
    cupboardquery = "%"+request.args.get("cupb")+"%"
    if cupboardquery:
        cupboard_data = connector.execute(
            "SELECT * FROM food_cupboard WHERE product_type LIKE ?", (cupboardquery,))
        cupboard_data = cupboard_data.fetchall()
    else:
        cupboard_data = []
    return render_template("food_cupboard.html", cupboard_results=cupboard_data)

# snacks query path
@app.route("/querysnacks", methods=["GET"])
@login_required
def querysnacks():
    snackquery = "%"+request.args.get("snack")+"%"
    if snackquery:
        snack_data = connector.execute(
            "SELECT * FROM snacks WHERE product_type LIKE ?", (snackquery,))
        snack_data = snack_data.fetchall()
    else:
        snack_data = []
    return render_template("snacks.html", snacks_results=snack_data)

# beverages query path


@app.route("/querybeverages", methods=["GET"])
@login_required
def querybeverages():
    beveragequery = "%"+request.args.get("beverage")+"%"
    if beveragequery:
        beverage_data = connector.execute(
            "SELECT * FROM beverages WHERE product_type LIKE ?", (beveragequery,))
        beverage_data = beverage_data.fetchall()
    else:
        beverage_data = []
    return render_template("beverages.html", beverage_results=beverage_data)


@app.route("/querydetergents", methods=["GET"])
@login_required
def querydetergents():
    detergentquery = "%"+request.args.get("detergent")+"%"
    if detergentquery:
        detergent_data = connector.execute(
            "SELECT * FROM laundry_detergents WHERE product_type LIKE ?", (detergentquery,))
        detergent_data = detergent_data.fetchall()
    else:
        detergent_data = []
    return render_template("detergents.html", detergent_results=detergent_data)






@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        register_id = 0
        password = request.form.get("password")
        pass_confirmation = request.form.get("confirmation")
# I'm going to create a register_id variable and store in it the value of the string that the user inputted if it already exists in the database(or not)
        users = db.execute("SELECT * FROM users;")
        users=users.fetchall()
        for user in users:
            if username == str(user["name"]):
                register_id = user["id"]

        if not username or register_id != 0:
            message = "Invalid username"
            return render_template("apology.html",message=message)
        else:
            if not password or password != pass_confirmation:
                message = "Invalid"
                return render_template("apology.html",message=message)
            else:
                new_hash = generate_password_hash(password, method="plain")
                db.execute(
                    "INSERT INTO users (name,hash,registration_time) VALUES(?,?,datetime('now'))", (username, new_hash))
                db.commit()
                return render_template("login.html")

    return render_template("registration.html")

#The following code was taken from the staff's implementation of the log in route in the finance app.
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html",message="Please enter a username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html",message="Please enter a password")

        # Query database for username

        rows = connector.execute('''SELECT * FROM users WHERE name = ?''',
                          (request.form.get("username"),))
        rows=rows.fetchall()

        # Ensure username exists and password is correct
        if len(rows) !=1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("apology.html",message="Invalid password or usename")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/transactions")
@login_required
def history():
   

    transactions = connector.execute(
        " SELECT * FROM daily_transactions")
    transactions=transactions.fetchall()

    return render_template("transaction_receipt.html", goods_sold=transactions)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")




db.commit()
