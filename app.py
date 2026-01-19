import os
from flask import Flask, render_template, request, jsonify
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

app = Flask(__name__)

# --- GLOBAL AI SETUP (Runs once when app starts) ---
print("Initializing RightsMate AI... Please wait.")

# 1. Setup Model
model = ChatOllama(model="ibm/granite4:micro", temperature=0)

# 2. Load & Split Data
pdf_path = "labor_laws.pdf" 
if not os.path.exists(pdf_path):
    print(f"ERROR: {pdf_path} not found. Please put the PDF in the folder.")
else:
    print(f"Loading {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)

    # 3. Create Embeddings
    print("Embedding")
    embeddings = HuggingFaceEmbeddings(model_name="ibm-granite/granite-embedding-30m-english")
    
    # This creates a folder named 'chroma_db' to store your data
    vector_db = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory="./chroma_db" 
    )
    retriever = vector_db.as_retriever()
    print("Loaded")

    # 4. Build the RAG Chain
    template = """You are RightsMate, a helpful legal assistant for workers. 
    Answer the question based ONLY on the following context. Keep it simple.
    
    Context: {context}
    
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n".join([d.page_content for d in docs])

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

# --- FLASK ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        response = rag_chain.invoke(user_input)
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Sorry, I encountered an error processing your request."})

@app.route('/summarize', methods=['GET'])
def summarize():
    try:
        query = "Summarize the key rights for workers mentioned in this document in 3 bullet points."
        response = rag_chain.invoke(query)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": "Could not generate summary."})

if __name__ == '__main__':
    app.run(debug=True, port=5000)