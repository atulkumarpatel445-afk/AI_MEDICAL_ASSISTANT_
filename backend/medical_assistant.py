from rag import retrieve
from search import search_web
import os

# Gemini API Key (read from environment variable `GENAI_API_KEY`)
api_key = os.getenv("GENAI_API_KEY")

# Try to import Google GenAI client. If unavailable, provide a safe fallback.
try:
    from google import genai

    client = genai.Client(api_key=api_key)

    def generate_answer(prompt):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        # Some client responses expose `text`, others may stringify.
        return getattr(response, "text", str(response))

except Exception as e:
    print(f"google genai import/config failed: {e}. Falling back to web-only responder.")

    def generate_answer(prompt):
        # Fallback: perform a web search and return a brief aggregated placeholder.
        try:
            web_results = search_web(prompt)
            snippets = [str(r) for r in web_results[:3]]
            return "Fallback (GenAI not configured). Top web snippets:\n" + "\n- " + "\n- ".join(snippets)
        except Exception:
            return "GenAI not configured and web search failed."


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