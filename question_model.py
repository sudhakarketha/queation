from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    choice_a = db.Column(db.String(255))
    choice_b = db.Column(db.String(255))
    choice_c = db.Column(db.String(255))
    choice_d = db.Column(db.String(255))
    predicted_answer = db.Column(db.String(1))
    explanation = db.Column(db.Text)

    def __init__(self, question_text, choice_a, choice_b, choice_c, choice_d, predicted_answer, explanation):
        self.question_text = question_text
        self.choice_a = choice_a
        self.choice_b = choice_b
        self.choice_c = choice_c
        self.choice_d = choice_d
        self.predicted_answer = predicted_answer
        self.explanation = explanation

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question_text,
            "choices": [self.choice_a, self.choice_b, self.choice_c, self.choice_d],
            "answer": self.predicted_answer,
            "explanation": self.explanation
        }




# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# class Question(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     question_text = db.Column(db.Text, nullable=False)
#     choice_a = db.Column(db.String(255))
#     choice_b = db.Column(db.String(255))
#     choice_c = db.Column(db.String(255))
#     choice_d = db.Column(db.String(255))
#     predicted_answer = db.Column(db.String(1))
#     explanation = db.Column(db.Text)

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "question": self.question_text,
#             "choices": [
#                 self.choice_a,
#                 self.choice_b,
#                 self.choice_c,
#                 self.choice_d
#             ],
#             "answer": self.predicted_answer,
#             "explanation": self.explanation
#         }
