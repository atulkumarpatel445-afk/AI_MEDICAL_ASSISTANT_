from flask import Flask, request, jsonify
from flask_cors import CORS
from medical_assistant import get_answer
from pypdf import PdfReader
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {
        "message": "AI Medical Assistant is Running"
    }
@app.route("/analyze-report", methods=["POST"])
def analyze_report():

    file = request.files["file"]
    text = extract_text_from_pdf(file)
    analysis = get_report_analysis(text)
    
    return jsonify({
        "analysis": analysis
    })

@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.get_json()

        question = data.get("question")

        answer = get_answer(question)

        return jsonify({
            "answer": answer
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

def extract_text_from_pdf(file):
    """Extract text from an uploaded PDF FileStorage."""
    try:
        # Try reading from the file stream (works for Flask FileStorage)
        reader = PdfReader(file.stream)
    except Exception:
        # Fallback: try reading the file object directly
        file.stream.seek(0)
        reader = PdfReader(file)

    text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

    return "\n".join(text)


def get_report_analysis(text):
    """Generate a concise analysis for a medical report text."""
    prompt = (
        "Please analyze the following medical report and provide a concise summary of key findings, "
        "possible diagnoses, and suggested next steps:\n\n" + text
    )

    try:
        return get_answer(prompt)
    except Exception as e:
        return f"Error generating analysis: {e}"
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT",5000)),
        debug=False
    )