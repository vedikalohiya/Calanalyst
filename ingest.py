import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader

if not os.path.exists('Data/'):
    print("Error: 'Data/' directory not found!")
    print("Please make sure the Data directory exists and contains PDF files.")
    exit(1)

pdf_files = []
for root, dirs, files in os.walk('Data/'):
    for file in files:
        if file.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(root, file))

if not pdf_files:
    print("Warning: No PDF files found in the Data directory!")
    print("Please add PDF files to the Data directory before running this script.")
    exit(1)

print(f"Found {len(pdf_files)} PDF files to process...")

model_name = "BAAI/bge-large-en"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

print("Initializing embeddings model...")
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

print("Loading documents...")
loader = DirectoryLoader('Data/', glob="**/*.pdf", show_progress=True, loader_cls=PyPDFLoader)
documents = loader.load()

if not documents:
    print("Error: No documents were loaded!")
    exit(1)

print(f"Loaded {len(documents)} document pages...")
print("Splitting documents into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
texts = text_splitter.split_documents(documents)

print(f"Created {len(texts)} text chunks...")
print("Creating vector store (this may take a while)...")
vector_store = Chroma.from_documents(
    texts, 
    embeddings, 
    collection_metadata={"hnsw:space": "cosine"}, 
    persist_directory="stores/medical_cosine"
)

print("Vector Store Created Successfully!")
print(f"Processed {len(documents)} documents into {len(texts)} chunks.")