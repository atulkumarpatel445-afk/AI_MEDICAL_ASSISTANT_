from rag import retrieve
from search import search_web
from google import genai
import os

# Gemini API Key (read from environment variable `GENAI_API_KEY`)
# Falls back to a literal value if the env var is not set.
api_key=os.getenv("GENAI_API_KEY")
client = genai.Client(api_key=api_key)

# Generate response using Gemini
def generate_answer(prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# Main function
def get_answer(question):

    try:
        # Search in ChromaDB first
        docs = retrieve(question)

        # If we have vector DB results and the top score indicates relevance, use RAG
        if docs and len(docs) > 0 and docs[0][1] < 0.5:
            context = "\n".join([doc[0].page_content for doc in docs])

            prompt = f"""
You are an AI Medical Assistant.

Answer using ONLY the provided medical context.

Context:
{context}

Question:
{question}
"""

            return generate_answer(prompt)

        # Otherwise fall back to an internet search
        web_results = search_web(question)
        web_context = "\n".join([str(result) for result in web_results])

        prompt = f"""
You are an AI Medical Assistant.

Use the following internet information to answer.

Internet Data:
{web_context}

Question:
{question}
"""

        return generate_answer(prompt)

    except Exception as e:
        # On unexpected errors, fallback to internet search and include the error in logs
        print(f"medical_assistant.get_answer error: {e}")
        web_results = search_web(question)
        web_context = "\n".join([str(result) for result in web_results])

        prompt = f"""
You are an AI Medical Assistant.

Use the following internet information to answer. An internal retrieval error occurred.

Internet Data:
{web_context}

Question:
{question}
"""

        return generate_answer(prompt)