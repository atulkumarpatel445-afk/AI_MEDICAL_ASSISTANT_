import pandas as pd

df = pd.read_csv("data/Diseases.csv")
df = pd.read_csv("data/medical.csv")
documents = []

for _, row in df.iterrows():
    text = " ".join(str(x) for x in row.values)
    documents.append(text)

print(documents[:5])
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma.from_texts(
    documents,
    embedding=embedding,
    persist_directory="chroma_db"
)

print("Data stored successfully!")