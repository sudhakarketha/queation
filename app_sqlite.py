from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from services.ai_answer_generator import generate_answer_and_explanation
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Use SQLite for easier setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize database
db = SQLAlchemy(app)

# Question Model
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    choice_a = db.Column(db.String(255))
    choice_b = db.Column(db.String(255))
    choice_c = db.Column(db.String(255))
    choice_d = db.Column(db.String(255))
    predicted_answer = db.Column(db.String(1))
    explanation = db.Column(db.Text)
    user_correction = db.Column(db.String(255), nullable=True)

    def __init__(self, question_text, choice_a, choice_b, choice_c, choice_d, predicted_answer, explanation, user_correction=None):
        self.question_text = question_text
        self.choice_a = choice_a
        self.choice_b = choice_b
        self.choice_c = choice_c
        self.choice_d = choice_d
        self.predicted_answer = predicted_answer
        self.explanation = explanation
        self.user_correction = user_correction

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question_text,
            "choices": [self.choice_a, self.choice_b, self.choice_c, self.choice_d],
            "answer": self.predicted_answer,
            "explanation": self.explanation,
            "user_correction": self.user_correction
        }

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "message": "Question Answer API is running (SQLite)",
        "version": "1.0.0"
    }), 200

@app.route('/upload', methods=['POST'])
def upload_question():
    """Upload a new question with choices and get AI-generated answer."""
    try:
        data = request.get_json(silent=True) or {}
        question_text = data.get('question')
        choices = data.get('choices')

        # Validate input
        if not question_text or not isinstance(choices, list) or len(choices) != 4:
            return jsonify({
                "error": "Invalid input. 'question' and exactly 4 'choices' are required."
            }), 400

        # Check for empty choices
        if any(not choice.strip() for choice in choices):
            return jsonify({
                "error": "All choices must be non-empty."
            }), 400

        logger.info(f"Processing question: {question_text[:50]}...")

        # Generate answer and explanation
        result = generate_answer_and_explanation(question_text, choices)

        # Create new question record
        new_question = Question(
            question_text=question_text,
            choice_a=choices[0],
            choice_b=choices[1],
            choice_c=choices[2],
            choice_d=choices[3],
            predicted_answer=result['answer'],
            explanation=result['explanation']
        )

        db.session.add(new_question)
        db.session.commit()

        logger.info(f"Question saved with ID: {new_question.id}")

        return jsonify({
            "message": "Question saved successfully",
            "result": result,
            "question_id": new_question.id
        }), 201

    except Exception as e:
        logger.error(f"Error saving question: {str(e)}")
        db.session.rollback()
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

@app.route('/questions', methods=['GET'])
def get_questions():
    """Retrieve all questions from the database."""
    try:
        questions = Question.query.order_by(Question.id.desc()).all()
        return jsonify([q.to_dict() for q in questions])
    except Exception as e:
        logger.error(f"Error fetching questions: {str(e)}")
        return jsonify({
            "error": "Failed to retrieve questions",
            "details": str(e)
        }), 500

@app.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    """Retrieve a specific question by ID."""
    try:
        question = Question.query.get_or_404(question_id)
        return jsonify(question.to_dict())
    except Exception as e:
        logger.error(f"Error fetching question {question_id}: {str(e)}")
        return jsonify({
            "error": "Failed to retrieve question",
            "details": str(e)
        }), 500

@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    """Delete a specific question by ID."""
    try:
        question = Question.query.get_or_404(question_id)
        db.session.delete(question)
        db.session.commit()
        return jsonify({"message": "Question deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error deleting question {question_id}: {str(e)}")
        db.session.rollback()
        return jsonify({
            "error": "Failed to delete question",
            "details": str(e)
        }), 500

@app.route('/questions/<int:question_id>/report', methods=['POST'])
def report_wrong_answer(question_id):
    """Allow user to report/correct the answer for a question."""
    try:
        data = request.get_json(silent=True) or {}
        correction = data.get('correction')
        if not correction or correction not in ['A', 'B', 'C', 'D']:
            return jsonify({"error": "Correction must be one of 'A', 'B', 'C', or 'D'."}), 400
        question = Question.query.get_or_404(question_id)
        question.user_correction = correction
        db.session.commit()
        return jsonify({"message": "Correction saved.", "user_correction": correction}), 200
    except Exception as e:
        logger.error(f"Error saving correction: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Failed to save correction.", "details": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        logger.info("SQLite database created/verified")
    
    logger.info("🚀 Flask API running at http://localhost:5000 (SQLite)")
    logger.info("📊 Health check: http://localhost:5000/health")
    logger.info("📝 Upload questions: POST http://localhost:5000/upload")
    logger.info("📋 Get questions: GET http://localhost:5000/questions")
    
    app.run(debug=True, port=5000, host='0.0.0.0') 