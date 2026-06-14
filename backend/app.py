from flask import Flask, request, jsonify
from flask_cors import CORS
from medical_assistant import get_answer

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {
        "message": "AI Medical Assistant is Running"
    }

@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.get_json()

        question = data.get("question")

        if not question:
            return jsonify({
                "error": "Question is required"
            }), 400

        answer = get_answer(question)

        return jsonify({
            "question": question,
            "answer": answer
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
@app.route(
    "/analyze-report",
    methods=["POST"]
)
def analyze_report():

    file = request.files["file"]

    filename = file.filename

    return jsonify({
        "analysis":
        f"Report uploaded successfully: {filename}"
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )