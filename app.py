# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from question_model import db, Question
# from services.ai_answer_generator import generate_answer_and_explanation

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:yourpassword@localhost/questiondb'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CORS(app)
# db.init_app(app)

# # @app.route('/upload', methods=['POST'])
# # def upload_question():
# #     data = request.json
# #     question_text = data.get('question')
# #     choices = data.get('choices')

# #     result = generate_answer_and_explanation(question_text, choices)
# #     new_question = Question(
# #         question_text=question_text,
# #         choice_a=choices[0],
# #         choice_b=choices[1],
# #         choice_c=choices[2],
# #         choice_d=choices[3],
# #         predicted_answer=result['answer'],
# #         explanation=result['explanation']
# #     )
# #     db.session.add(new_question)
# #     db.session.commit()
# #     return jsonify({"message": "Question saved", "result": result})


# @app.route('/upload', methods=['POST'])
# def upload_question():
#     data = request.json or {}  # ✅ safe fallback

#     question_text = data.get('question')
#     choices = data.get('choices')

#     if not question_text or not choices or len(choices) != 4:
#         return jsonify({"error": "Invalid input"}), 400

#     result = generate_answer_and_explanation(question_text, choices)

#     new_question = Question(
#         question_text=question_text,
#         choice_a=choices[0],
#         choice_b=choices[1],
#         choice_c=choices[2],
#         choice_d=choices[3],
#         predicted_answer=result['answer'],
#         explanation=result['explanation']
#     )
#     db.session.add(new_question)
#     db.session.commit()

#     return jsonify({"message": "Question saved", "result": result})


# @app.route('/questions', methods=['GET'])
# def get_questions():
#     questions = Question.query.all()
#     return jsonify([q.to_dict() for q in questions])

# if __name__ == '__main__':
#     app.run(debug=True)












from flask import Flask, request, jsonify
from flask_cors import CORS
from question_model import db, Question
from services.ai_answer_generator import generate_answer_and_explanation
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Use configuration
app.config['SQLALCHEMY_DATABASE_URI'] = Config.get_database_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize database
db.init_app(app)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "message": "Question Answer API is running",
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        logger.info("Database tables created/verified")
    
    logger.info("🚀 Flask API running at http://localhost:5000")
    logger.info("📊 Health check: http://localhost:5000/health")
    logger.info("📝 Upload questions: POST http://localhost:5000/upload")
    logger.info("📋 Get questions: GET http://localhost:5000/questions")
    
    app.run(debug=Config.DEBUG, port=5000, host='0.0.0.0')


