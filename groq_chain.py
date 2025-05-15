# groq_chain.py
import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains.question_answering import load_qa_chain

class PDFQueryAgent:
    def __init__(self, pdf_file):
        loader = PyPDFLoader(pdf_file)
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        self.docs = text_splitter.split_documents(documents)

        embeddings = HuggingFaceEmbeddings()
        self.db = FAISS.from_documents(self.docs, embeddings)

        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="gemma2-9b-it"  # or "gemma2-9b-it"
        )
        self.chain = load_qa_chain(self.llm, chain_type="stuff")

    def query(self, question):
        relevant_docs = self.db.similarity_search(question)
        return self.chain.run(input_documents=relevant_docs, question=question)
