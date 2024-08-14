from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Set up the database URI (using SQLite in this example)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    personality_type = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/", methods=["GET", "POST"])
def index():
    questions = [
        "I enjoy social gatherings and meeting new people.",
        "I am detail-oriented and always try to complete tasks with precision.",
        "I often empathize with others and try to understand their emotions.",
        "I am open to trying new experiences and stepping out of my comfort zone.",
        "I prefer to plan everything in advance rather than acting spontaneously.",
        "I often take the lead in group situations and enjoy being in charge.",
        "I handle stress and pressure well and remain calm in difficult situations.",
        "I am creative and enjoy coming up with new ideas and solutions.",
        "I am highly motivated and always strive to achieve my goals.",
        "I am considerate of others' feelings and avoid conflicts whenever possible.",
        "I enjoy analyzing problems and solving puzzles or complex tasks.",
        "I am punctual and value timeliness in both my personal and professional life.",
        "I adapt easily to changes and new environments.",
        "I am independent and prefer working alone rather than in a team.",
        "I am trustworthy and people often confide in me."
    ]
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        # Collect responses
        responses = [request.form.get(f"question_{i}") for i in range(1, len(questions) + 1)]
        # Here you would normally process the responses to determine the personality type and score
        personality_type = "Type A"  # Example value
        score = 85  # Example score
        
        # Save to database
        new_user = User(name=name, age=age, personality_type=personality_type, score=score)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('result', name=name, age=age, personality_type=personality_type, score=score))
    
    return render_template("index.html", questions=questions)

@app.route("/result")
def result():
    name = request.args.get('name')
    age = request.args.get('age')
    personality_type = request.args.get('personality_type')
    score = request.args.get('score')
    return render_template("result.html", name=name, age=age, personality_type=personality_type, score=score)

@app.route("/history")
def history():
    users = User.query.all()
    return render_template("history.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)
