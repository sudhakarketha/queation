from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/questions', methods=['GET'])
def get_questions():
    return jsonify({"message": "Route is working"}), 200

if __name__ == '__main__':
    app.run(debug=True)
