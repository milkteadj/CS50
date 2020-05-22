import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, success

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/", methods=["GET"])
@login_required
def index():
    """Show portfolio of stocks"""

    #username
    username = session["username"]

    #get the user cash amount
    user_cash = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])

    #get the stock information
    stocks = db.execute("SELECT * FROM owned WHERE id = :id", id=session["user_id"])

    #make dicts that can pair values with the symbols in the array, and their usd format for display
    quotes = {}
    quotes_usd = {}
    values = {}
    values_usd = {}

    #total value of the porfolio
    porfolio_value = user_cash[0]["cash"]

    #interate through the stocks and save their quotes into two dicts for reference in index
    for stock in stocks:
        symbol = stock["symbol"]
        shares = int(stock["shares"])
        #search for stock price using lookup, then turn into usd format for display (this implementation takes more space tho...)
        quotes[stock["symbol"]] = lookup(stock["symbol"])
        quotes_usd[stock["symbol"]] = usd(quotes[stock["symbol"]]["price"])
        #calculate the total price for the stocks, then turn into usd format for display
        values[stock["symbol"]] = quotes[stock["symbol"]]["price"] * shares
        values_usd[stock["symbol"]] = usd(values[stock["symbol"]])

        #total value of the porfolio
        porfolio_value += float(values[stock["symbol"]])


    #gotta remember to add your dicts to render_template!
    return render_template("index.html",
        username=username,
        user_cash=usd(user_cash[0]["cash"]),
        porfolio_value = usd(porfolio_value),
        stocks = stocks,
        quotes = quotes,
        quotes_usd = quotes_usd,
        values_usd = values_usd)


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    symbol = request.form.get("symbol")

    if request.method == 'POST':
        if not request.form.get("symbol"):
            return apology("Can you type?")

        #use lookup, and if symbol is made up, aplogize
        quote = lookup(symbol)
        if quote == None:
            return apology("Invalid Symbol")

        return render_template("quoted.html",
        name =quote["name"], price=usd(quote["price"]), sym=quote["symbol"])

    return render_template("quote.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == 'POST':

        #set shares as shares and symbol and symbol
        shares = int(request.form.get("shares"))
        symbol = request.form.get("symbol").upper()

        #if no symbol then scold
        if not request.form.get("symbol"):
            return apology("Sorry what are you buying?")

        #use lookup, and if symbol is made up, aplogize
        quote = lookup(symbol)
        if quote == None:
            return apology("{} is not a real company".format(symbol))

        #if no shares then scold
        if not request.form.get("shares"):
            return apology("How much you want from me?")

        #just in case bad # of shares
        if shares <= 0:
            return apology("Sorry you can't buy this # of shares")

        #total amount of the purchase:
        cost = float(int(shares) * quote["price"])

        #locate the user transactions and transfer into a dict
        results = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

        #compare user amount with the cost
        leftover = float(results[0]["cash"] - cost)
        if leftover >= 0:

            #put in the transaction, which is a general table for all users
            db.execute("INSERT INTO user_transaction('id', 'TransType', 'symbol', 'company', 'shares', 'share_price', 'total_transaction') VALUES(:id, :TransType, :symbol, :company, :shares, :share_price, :total_transaction)",
                id=session["user_id"], TransType="Bought", symbol=symbol, company=quote["name"], shares=shares, share_price=quote["price"], total_transaction=cost)

            #put into total owned stocks of that user
            #first check if stock exists already
            exists = db.execute("SELECT * FROM owned WHERE id = :id AND symbol = :symbol", id=session["user_id"], symbol=symbol)

            #if exists, update the number of shares
            if len(exists) > 0:
                db.execute("UPDATE owned SET shares= :shares WHERE id= :id AND symbol= :symbol",
                 id=session["user_id"], shares=shares+exists[0]["shares"], symbol=symbol)
            #if doesn't exist, insert it in
            else:
                db.execute("INSERT INTO owned('id', 'symbol', 'shares') VALUES(:id, :symbol, :shares)",
                id=session["user_id"], symbol=symbol, shares=shares)

            #deduct the cash amount from the user
            db.execute("UPDATE users SET cash = :leftover WHERE id = :id", leftover=leftover, id = session["user_id"])

        #if the user's left over doesn't have enough
        else:
            #TODO ADD HOW MUCH SHORT
            return apology("sorry... you're broke")

    return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("Come back later-- Jiawei")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == 'POST':

        #set shares as shares and symbol and symbol
        shares = int(request.form.get("shares"))
        symbol = request.form.get("symbol").upper()

        #if no symbol then scold
        if not request.form.get("symbol"):
            return apology("Sorry what are you selling?")

        #use lookup, and if symbol is made up, aplogize
        quote = lookup(symbol)
        if quote == None:
            return apology("{} is not a real company".format(symbol))

        #if no shares then scold
        if not request.form.get("shares"):
            return apology("How much you want from me?")

        #just in case bad # of shares
        if shares <= 0:
            return apology("Sorry you can't sell this # of shares")

        #see the number of shares the user has of the stock
        userowned = db.execute("SELECT shares FROM owned WHERE id = :id AND symbol = :symbol", id=session["user_id"], symbol=symbol)
        if len(userowned) < 1:
            return apology("you don't own this stock")

        #check if the user owns this many shares that was selected to sell. If yes, reduce owned # by chosen amount.
        if userowned[0]["shares"] >= shares:
            db.execute("UPDATE owned SET shares = :shares WHERE id = :id AND symbol = :symbol", shares=userowned[0]["shares"]-shares, id=session["user_id"], symbol=symbol)
        else:
            return apology("You don't own this many shares")

        #select from the user the amount of cash before transaction
        before = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        #total amount for the transaction
        profit = float(int(shares) * quote["price"])
        #total amount of user cash after the purchase:
        cash_after = float(before[0]["cash"] + profit)
        #update new cash amount after purchase
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = cash_after, id=session["user_id"])

        #if the user sold all of their shares of the stock, delete the column from owned
        after = db.execute("SELECT shares FROM owned WHERE id = :id AND symbol = :symbol", id=session["user_id"], symbol=symbol)
        if after[0]["shares"] == 0:
            db.execute("DELETE FROM owned WHERE id = :id AND symbol = :symbol", id=session["user_id"], symbol=symbol)

        #put transaction into user_transaction
        db.execute("INSERT INTO user_transaction('id', 'TransType', 'symbol', 'company', 'shares', 'share_price', 'total_transaction') VALUES(:id, :TransType, :symbol, :company, :shares, :share_price, :total_transaction)",
                id=session["user_id"], TransType="Sold", symbol=symbol, company=quote["name"], shares=shares, share_price=quote["price"], total_transaction=profit)

    return render_template("sell.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    #username
    username = session["username"]
    #get the user cash amount
    user_cash = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])

    #get the transactions information
    transactions = db.execute("SELECT * FROM user_transaction WHERE id = :id", id=session["user_id"])

    #gotta remember to add your dicts to render_template!
    return render_template("history.html",
        username=username,
        user_cash=usd(user_cash[0]["cash"]),
        transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    #copying code from the login, pretty similar except we need to append new user here

    # Forget any user_id
    session.clear()

    if request.method == 'POST':
        #insure username is submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        #insure password is submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        elif not request.form.get("confirm_password"):
            return apology("must confirm password", 403)
        #insure password are the same:
        elif request.form.get("password") != request.form.get("confirm_password"):
            return apology("password must match!", 403)

        #get password data for turning into hash
        password = request.form.get("password")

        #check if username is already taken in the database:
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        if len(rows) >=1:
            return apology("username is already taken", 403)

        #get password data for turning into hash
        password = request.form.get("password")
        #generate hash
        hash = generate_password_hash(password)

        #add user into database
        new_user = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=hash)

        #return an alert declaring success
        return success()

    return render_template("register.html")

"""#can use either success() or this route
@app.route("/registered_success", methods=["GET"])
def registered_sucess():
    return render_template("registered_success.html")
"""

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
