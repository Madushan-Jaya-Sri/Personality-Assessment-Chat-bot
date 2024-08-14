from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///personality_assessment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the UserHistory model
class UserHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    personality_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

# Define the questions and possible responses
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

# Define the scoring criteria
scoring = {
    "Strongly Agree": 5,
    "Agree": 4,
    "Neutral": 3,
    "Disagree": 2,
    "Strongly Disagree": 1
}

# Define personality types based on total score
personality_types = [
    (75, 80, "Extraverted Leader", "Highly sociable, confident, and enjoys taking charge in group settings."),
    (67, 74, "Conscientious Planner", "Detail-oriented, methodical, and prefers structured environments."),
    (59, 66, "Empathetic Supporter", "Compassionate, empathetic, and values helping others."),
    (51, 58, "Adventurous Innovator", "Open to new experiences, creative, and enjoys coming up with novel ideas."),
    (43, 50, "Calm Problem Solver", "Analytical, calm under pressure, and enjoys solving complex problems."),
    (35, 42, "Adaptable Collaborator", "Flexible, team-oriented, and easily adapts to new environments."),
    (27, 34, "Independent Thinker", "Prefers working independently, values autonomy, and often introspective."),
    (15, 26, "Reserved Listener", "Introverted, reserved, and prefers listening over speaking.")
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user data
        name = request.form["name"]
        age = request.form["age"]

        # Get responses and calculate the score
        total_score = 0
        for i in range(len(questions)):
            response = request.form.get(f"question_{i+1}")
            total_score += scoring.get(response, 0)  # Default to 0 if response is not found

        # Determine personality type
        personality_type = "Unknown"
        personality_description = "No description available."
        for min_score, max_score, personality, description in personality_types:
            if min_score <= total_score <= max_score:
                personality_type = personality
                personality_description = description
                break

        # Save to database
        user_history = UserHistory(name=name, age=age, score=total_score, personality_type=personality_type, description=personality_description)
        db.session.add(user_history)
        db.session.commit()

        # Render result
        return render_template("result.html", name=name, age=age, personality_type=personality_type, description=personality_description, score=total_score)

    return render_template("index.html", questions=questions)

@app.route("/history")
def history():
    # Fetch user history from the database
    histories = UserHistory.query.order_by(UserHistory.date_created.desc()).all()
    return render_template("history.html", histories=histories)

if __name__ == "__main__":
    app.run(debug=True)
