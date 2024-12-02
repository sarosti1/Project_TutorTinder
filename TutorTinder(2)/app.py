from flask import Flask, request, jsonify
import smtplib
from datetime import datetime

app = Flask(__name__)

# Sample tutor schedule (replace with a database for production)
TUTORS = [
    {"name": "John Doe", "subject": "Math", "available": ["2024-12-05 14:00", "2024-12-06 10:00"]},
    {"name": "Jane Smith", "subject": "Physics", "available": ["2024-12-05 16:00", "2024-12-06 14:00"]}
]

@app.route("/api/suggest_questions", methods=["POST"])
def suggest_questions():
    """Process the input problem and suggest questions or videos."""
    data = request.json
    problem = data.get("problem")
    # Placeholder logic: Replace with AI API (e.g., OpenAI)
    suggested_questions = [
        f"What is the fundamental principle behind {problem}?",
        f"Can you provide examples to apply {problem} in real life?"
    ]
    videos = ["https://example.com/video1", "https://example.com/video2"]
    return jsonify({"questions": suggested_questions, "videos": videos})

@app.route("/api/check_availability", methods=["POST"])
def check_availability():
    """Match student availability with tutor schedules."""
    data = request.json
    name = data.get("name")
    subject = data.get("subject")
    availability = data.get("availability")
    
    # Match student and tutor availability
    matches = []
    for tutor in TUTORS:
        if tutor["subject"].lower() == subject.lower():
            tutor_slots = set(tutor["available"])
            student_slots = set(availability)
            common_slots = tutor_slots & student_slots
            if common_slots:
                matches.append({"tutor": tutor["name"], "slots": list(common_slots)})
    
    return jsonify(matches)

@app.route("/api/book_session", methods=["POST"])
def book_session():
    """Book a session and send confirmation email."""
    data = request.json
    email = data.get("email")
    tutor = data.get("tutor")
    slot = data.get("slot")

    # Send email (replace with production email server)
    try:
        smtp_server = smtplib.SMTP("smtp.example.com", 587)
        smtp_server.starttls()
        smtp_server.login("youremail@example.com", "yourpassword")
        message = f"Subject: Booking Confirmation\n\nYour session with {tutor} at {slot} is confirmed!"
        smtp_server.sendmail("youremail@example.com", email, message)
        smtp_server.quit()
        return jsonify({"status": "success", "message": "Booking confirmed and email sent!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
