import os
import glob
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def load_pdf_file(data_path: str):
    pdf_files = glob.glob(os.path.join(data_path, "*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(
            "Medical_book.pdf not found in data/. Place the PDF there and restart."
        )
    documents = []
    for pdf in pdf_files:
        loader = PyPDFLoader(pdf)
        documents.extend(loader.load())
    return documents


def text_split(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    return splitter.split_documents(documents)


def get_or_create_vectorstore(data_path: str, chroma_path: str, collection_name: str) -> Chroma:
    embeddings = get_embeddings()
    client = chromadb.PersistentClient(path=chroma_path)

    try:
        collection = client.get_collection(collection_name)
        if collection.count() > 0:
            return Chroma(
                persist_directory=chroma_path,
                embedding_function=embeddings,
                collection_name=collection_name,
            )
    except Exception:
        pass

    print("Ingesting PDF, this may take a minute...")
    documents = load_pdf_file(data_path)
    chunks = text_split(documents)
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=chroma_path,
        collection_name=collection_name,
    )
