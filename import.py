import csv
import os

from flask import Flask, session, render_template, url_for, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

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

file = open('books.csv')
books = csv.reader(file)

count = 0

for (isbn,title,author,year) in books:
	if count != 0:		
		# print(f"\n{isbn}, {title}, {author}, {year}")
		db.execute("INSERT INTO books (title, author, year, isbn) VALUES (:title,:author,:year,:isbn)"
			,{"title":title,"author":author,"year":year,"isbn":isbn})
		
		print(f"\nTitle:{title}, Author:{author}, Year:{year}, ISBN:{isbn}")
		
	count += 1
db.commit()
	
