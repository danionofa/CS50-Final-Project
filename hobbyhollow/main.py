from flask import Blueprint, redirect, render_template, request, session, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from hobbyhollow.database import db_session, User, Hobby
from hobbyhollow.helpers import login_required, lookup, suggest


bp = Blueprint('main', __name__, url_prefix='/')

@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        return render_template("login.html")


@bp.route("/sources", methods=["GET", "POST"])
def sources():
    return render_template("sources.html")


@bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    else:
        hobby = request.form.get("hobby").strip()
        type = request.form.get("type")
        if not hobby:
            flash("You must enter a title!")
            return redirect("/upload")
        if not type:
            flash("Please specify entertainment type.")
            return redirect("/upload")
        # Remove duplicate spaces from input and replace remaining spaces with "+"
        query = (" ".join(hobby.split())).replace(" ", "+")
        info = lookup(query, type)
        if not info:
            flash("Title not included in our database.")
            return redirect("/upload")
        hobby_id = info["id"]
        image = info["image"]
        name = info["name"]
        hobby_genres = info["genres"]
        overview = info["overview"]
        results = db_session.execute("SELECT * FROM hobbies WHERE hobby_id = :h AND user_id = :h",{'h': hobby_id,'u':session["user_id"]}).first()
        if not results:
            db_session.execute(
                "INSERT INTO hobbies (name, overview, img, hobby_id, user_id, genres) VALUES (:n, :o, :i, :h, :u, :g)",{'n':name,'o':overview,'i':image,'h':hobby_id,'u':session['user_id'],'g':str(hobby_genres)})
            db_session.commit()
        else:
            flash("You've already chosen this title!")
            return redirect("/upload")
    flash("Successfully uploaded!")
    return render_template("upload.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Username and password required.")
            return redirect("/login")

        rows = db_session.execute("SELECT * FROM users WHERE username = :u", {'u': username}).first()

        if not rows or not check_password_hash(rows["password"],password):
            flash("Invalid username and/or password.")
            return redirect("/login")
        
        session["user_id"] = rows["id"]
        return redirect("/home")


@bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    session.clear()
    return redirect("/")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

    if not (username and password and confirmation):
        flash("Fill all fields to register.")
        return redirect("/register")

    results = db_session.execute("SELECT * FROM users WHERE username = :u",{'u':username}).first()

    if results:
        flash("Username is taken.")
        return redirect("/register")

    if password != confirmation:
        flash("Passwords must match.")
        return redirect("/register")

    user = User(username=username, password=generate_password_hash(password))

    db_session.add(user)
    db_session.commit()

    flash("Success! Login to your new account.")
    return redirect("/login")


@bp.route("/home", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "GET":
        hobbies = db_session.execute("SELECT name, overview, img FROM hobbies WHERE user_id = :u",{'u':session['user_id']}).all()
        for hobby in hobbies:
            hobby = list(hobby)
            overview = hobby[1]
            description = (overview[:125] + '...') if len(overview) > 125 else overview
            hobby.append(description)
        return render_template("home.html", hobbies=hobbies)
    else:
        hobbies = db_session.execute("SELECT name, overview, img, hobby_id FROM hobbies WHERE user_id = :u",{'u':session['user_id']}).all()
        hobby = request.form.get("delete")
        db_session.execute("DELETE FROM hobbies WHERE name = :h AND user_id = :u",{'h':hobby,'u':session['user_id']})
        db_session.commit()
        flash("Hobby deleted!")
        return redirect("/home")


@bp.route("/explore", methods=["GET", "POST"])
@login_required
def explore():
    if request.method == "GET":
        genres = db_session.execute("SELECT genres FROM hobbies WHERE user_id = :u",{'u':session['user_id']}).all()
        my_hobbies = db_session.execute("SELECT hobby_id FROM hobbies WHERE user_id = :u",{'u':session['user_id']}).all()
        hobbies = []
        for hobby in my_hobbies:
            hobby = str(hobby)
            check = int(hobby.replace('(','').replace(')','').replace(',',''))
            hobbies.append(check)
        queries = []
        for genre in genres:
            query = genre[0].replace('[', '').replace(']','').replace(', ','%2C%20')
            queries.append(query)
        type = ["tv", "movie"]
        suggestions = []
        for query in queries:
            info = suggest(type[0], query) + suggest(type[1], query)
            for suggestion in info:
                if suggestion in suggestions:
                    info.remove(suggestion)
                elif suggestion["id"] in hobbies:
                    info.remove(suggestion)
                elif suggestion["overview"] == '':
                    info.remove(suggestion)
                else:
                    pass
            suggestions += info
        return render_template("explore.html", genres=genres, suggestions=suggestions)
    else:
        hobby = request.form.get("add")
        query = (" ".join(hobby.split())).replace(" ", "+")
        type = ["tv", "movie"]
        info = lookup(query, type[0])
        if not info:
            flash("Title not included in our database.")
            return redirect("/explore")
        hobby_id = info["id"]
        image = info["image"]
        name = info["name"]
        hobby_genres = info["genres"]
        overview = info["overview"]
        
        results = db_session.query(Hobby).filter_by(id=hobby_id).first()
        if not results:
            db_session.execute(
                "INSERT INTO hobbies (name, overview, img, hobby_id, user_id, genres) VALUES (:n, :o, :i, :h, :u, :g)",{'n':name,'o':overview,'i':image,'h':hobby_id,'u':session['user_id'],'g':str(hobby_genres)})
            db_session.commit()
        else:
            flash("You've already chosen this title!")
            return redirect("/upload")
    flash("Successfully added!")
    return redirect("/explore")
