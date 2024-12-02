from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import random
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Replace with your actual OpenAI API key
openai.api_key = "your-openai-api-key"

# Simulated database of tutors
tutors = [
    {"id": 1, "name": "Alice", "subject": "Math"},
    {"id": 2, "name": "Bob", "subject": "Science"},
    {"id": 3, "name": "Charlie", "subject": "English"},
]

@app.route('/suggest_questions', methods=['POST'])
def suggest_questions():
    """
    Generate suggested questions based on the user's problem using OpenAI's GPT-3.
    """
    problem = request.json['problem']
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Given the problem: '{problem}', suggest 3 questions to deepen understanding:",
            max_tokens=100
        )
        suggested_questions = response.choices[0].text.strip().split('\n')
        return jsonify({"questions": suggested_questions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/available_slots', methods=['GET'])
def available_slots():
    """
    Generate random available time slots for tutors.
    In a real application, this would fetch from a database.
    """
    slots = []
    start_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    for _ in range(10):  # Generate 10 random slots
        tutor = random.choice(tutors)
        slot_date = start_date + timedelta(days=random.randint(0, 6), hours=random.randint(0, 8))
        slots.append({
            "tutor_id": tutor["id"],
            "tutor_name": tutor["name"],
            "subject": tutor["subject"],
            "datetime": slot_date.isoformat()
        })
    return jsonify(slots)

@app.route('/book_tutor', methods=['POST'])
def book_tutor():
    """
    Book a tutor session. In a real application, this would update a database
    and potentially send emails.
    """
    booking_data = request.json
    # Here you would typically save the booking to a database
    # and send confirmation emails
    return jsonify({"message": "Booking confirmed", "booking": booking_data})

if __name__ == '__main__':
    app.run(debug=True)