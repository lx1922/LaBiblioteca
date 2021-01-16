import os

from flask import Flask, session, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import scoped_session, sessionmaker
from flask.templating import render_template
import requests

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/library", methods=["POST", "GET"])
def library():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)",
                    {"username": username, "email": email, "password": password})
        db.commit()
        return render_template("search.html", name=username)
    else:
        return "please sign up"

@app.route("/login", methods=["GET"])
def login():
    if session.get("users") is not None:
        session["users"] = None
    return render_template("login.html")

@app.route("/welcome", methods=["POST"])
def welcome():
    if session.get("users") is None: 
        session["users"] = []
    if request.method == "POST":
        enterred_username = request.form.get("username")
        enterred_password = request.form.get("password")
        password = db.execute("SELECT * FROM users WHERE username = :username", {"username": enterred_username})
        for passw in password:
            if passw.password == enterred_password:
                session["users"].append(enterred_username)
                return render_template("welcome.html")
        msg = "Either Username or Password is Incorrect"
        return render_template("error.html", msg=msg)

@app.route("/searchresults", methods=["POST"])
def search_results():
    enterred_search = request.form.get("booksearch")
    enterred_search = "%" + enterred_search + "%"
    search_list = db.execute("SELECT * FROM books WHERE title LIKE :enterred_search OR isbn LIKE :enterred_search OR author LIKE :enterred_search", {"enterred_search": enterred_search}).fetchall()
    return render_template("searchresults.html", results=search_list)

@app.route("/searchresults/<string:isbn>")
def book(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    review = db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"isbns": isbn, "key": "uTdAwrW3HSwJV1TkmumbQ"})
    data=res.json()
    return render_template("book.html", book=book, review=review, rating_count=data['books'][0]["ratings_count"], rating=data['books'][0]["average_rating"])

@app.route("/searchresults/<string:isbn>/review", methods=["POST"])
def review(isbn):
    enterred_review = request.form.get("review")
    enterred_rating = request.form.get("rating")
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    title = book.title
    review_before = db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
    for re in review_before:
        if re.username == session["users"][0]:
            return render_template("error.html", msg="Only one review allowed per book!")
    db.execute("INSERT INTO reviews (isbn, title, rating, review, username) VALUES (:isbn, :title, :rating, :review, :username)",
            {"isbn": isbn, "title": title, "rating": enterred_rating, "review": enterred_review, "username": session["users"][0]})
    db.commit()
    review = db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"isbns": isbn, "key": "uTdAwrW3HSwJV1TkmumbQ"})
    data=res.json()
    return render_template("book.html", book=book, review=review, rating_count=data['books'][0]["work_ratings_count"], rating=data['books'][0]["average_rating"])

@app.route("/api/<string:isbn>", methods=["GET"])
def api(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if not book:
        return render_template("error.html", msg="Book not Found!")
    review_count = db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn})
    total = 0
    rating_count=0
    for re in review_count:
        total+=re.rating
        rating_count+=1
    return jsonify({
        "title":book.title,
        "author":book.author,
        "year":book.year,
        "isbn":isbn,
        "review_count":rating_count,
        "average_score":float(total/rating_count)
    })





    

