from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "vector_db",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever(
    search_kwargs={"k":3}
)

while True:

    question = input("\nQuestion : ")

    if question.lower() == "exit":
        break

    docs = retriever.invoke(question)

    print("\nRetrieved Documents\n")

    for i, doc in enumerate(docs, start=1):

        print("="*50)
        print(f"Document {i}")
        print("="*50)

        print(doc.page_content)