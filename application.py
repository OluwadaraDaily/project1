import os, psycopg2, requests, json 
from flask import Flask, session, render_template, url_for, request, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

app.secret_key = os.urandom(24)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://ogqqjcwefzosbk:d75911845b37de0c2f14bd6f56d75a3a82b262e4ad7d8afef25e5cbb037871e8@ec2-18-215-99-63.compute-1.amazonaws.com:5432/d151lk5g150ori")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "GET":
		return render_template("register.html")

	# Get data from form
	username = request.form.get("username")
	password = request.form.get("password")
	
	# Check if user exists
	check_user = ("SELECT * FROM users WHERE username=:username}", {"username":username})
	
	if check_user:
		return render_template("error.html", message = "Already a user")
	
	# If user does not exist, insert into DB and let in
	db.execute("INSERT INTO users (username,password) VALUES (:username, :password)"
				, {"username":username, "password":password})
	db.commit()
	
	if db.commit is True:
		return redirect(url_for("home"))

@app.route("/login", methods=["GET","POST"])
def login():
	if request.method == "GET":
		return render_template("login.html")

	# Pop any user id in the session to create a new user id after login
	session.pop("user_id", None)

	# Get credentials from form
	username = request.form.get("username")
	password = request.form.get("password")
	
	# Query
	sql = db.execute("SELECT * FROM users WHERE username=:username AND password=:password"
			,{"username":username, "password":password}).fetchone()	

	if sql is None:
		return redirect(url_for("login"))

	# Store id in the session to be used later
	session["user_id"] = sql.id
	return redirect(url_for('home'))

@app.route("/home", methods=["GET","POST"])
def home():
	# Check if logged in
	if session.get("user_id"):
		if request.method == "GET":
			return render_template("home.html")

		if session.get("books") is None:
			session["books"] = []
		
		# Get search query
		search = request.form.get("search")

		# Match strings
		matchString = (f"%{search}%")

		# Query statement
		sql = db.execute("SELECT * FROM books WHERE title LIKE :x OR author LIKE :y OR isbn LIKE :z"
				,{"x":matchString, "y":matchString, "z":matchString}).fetchall()

		# Every row to be appended to the books array for each session
		for row in sql:
			session["books"].append(row)		

		if len(session["books"]) == 0:
			return render_template("error.html", message="No matches found")

		return render_template("results.html", books=session["books"], search=search)
	
	return redirect(url_for("login"))

@app.route("/book/<int:book_id>")
def book(book_id):
	if session.get("user_id"):
		# Make sure book exists
		book = db.execute("SELECT * FROM books WHERE id = :id",{"id":book_id}).fetchone()
		reviews = db.execute("SELECT * FROM reviews WHERE book_id = :id",{"id":book_id}).fetchall()
		
		res = requests.get("https://www.goodreads.com/book/review_counts.json"
			, params={"key": "zZmCQn1urZAcdyRvfeRCg", "isbns": book.isbn})
			
		data = res.text

		parsed = json.loads(data)


		for review in reviews:
			user = db.execute("SELECT * FROM users WHERE id=:id", {"id":review.user_id}).fetchone()
		
		if book is None:
			return render_template("error.html", message="Invalid ID")

		return render_template("book.html", book=book, reviews=reviews, user=user, parsed=parsed)
	
	return redirect(url_for("login"))

@app.route("/reviews/<int:book_id>", methods=["GET", "POST"])
def reviews(book_id):
	if session.get("user_id"):
		rating = request.form.get("rating")
		content = request.form.get("review")
		
		try: 
			db.execute("INSERT INTO reviews (content, book_id, user_id, rating) VALUES (:content, :book_id, :user_id, :rating)"
		,{"content": content, "book_id":book_id, "user_id":session["user_id"], "rating": rating})
			db.commit()

			if db.commit() is False:
				return render_template("error.html", message="Failed to insert")
			
			return render_template("success.html", message="Review recorded")
		except KeyError:
			return redirect(url_for("login"))

	return redirect(url_for("login"))

@app.route("/api/<string:isbn>")
def book_api(isbn):
	# Return details about a book with ISBN number specified
	if session.get("user_id"):
		
		# Check if book exists
		book = db.execute("SELECT * FROM books WHERE isbn=:isbn",{"isbn":isbn}).fetchone()

		if book is None:
			return render_template("404.html")
		
		# Get review_count and average_score required
		count = db.execute("SELECT COUNT(*) FROM reviews")
		avg = db.execute("SELECT AVG(rating) FROM reviews")

		results = {
			"title": book.title,
          	"author": book.author,
          	"year": book.year,
          	"isbn": book.isbn,
		}
		
		for rowproxy in count:
		    # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
		    for column, value in rowproxy.items():
		        a = value

		for rowproxy in avg:
		    # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
		    for column, value in rowproxy.items():
		        b = value

		    results.update({"review_count": str(a)})
		    results.update({"average_score": str(b)})

		return jsonify(results)

	return redirect(url_for('login'))

@app.route('/logout')
def logout():
	session.pop("user_id")
	return redirect(url_for('index'))