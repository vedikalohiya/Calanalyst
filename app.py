import flask
from flask import Flask, request, jsonify, render_template
import os
import sys
import logging
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

def check_prerequisites():
    """Check if all required files and directories exist."""
    issues = []
    
    # Check model file
    local_llm = "neural-chat-7b-v3-1.Q4_K_M.gguf"
    if not os.path.exists(local_llm):
        issues.append(f"Model file '{local_llm}' not found!")
    
    # Check vector store
    if not os.path.exists("stores/medical_cosine"):
        issues.append("Vector store directory 'stores/medical_cosine' not found!")
    
    # Check if vector store has data
    if os.path.exists("stores/medical_cosine"):
        store_files = os.listdir("stores/medical_cosine")
        if not store_files:
            issues.append("Vector store directory is empty!")
    
    return issues

# Check prerequisites before starting
issues = check_prerequisites()
if issues:
    print("Setup Issues Found:")
    for issue in issues:
        print(f"   - {issue}")
    print("\nSolutions:")
    print("   1. Run: python setup.py (to download the model)")
    print("   2. Run: python ingest.py (to create the vector store)")
    print("   3. Make sure the Data/ directory contains PDF files")
    sys.exit(1)

logger.info("All prerequisites check passed!")

local_llm = "neural-chat-7b-v3-1.Q4_K_M.gguf"

config = {
    'max_new_tokens': 512,  # Reduced from 1024 for memory efficiency
    'repetition_penalty': 1.1,
    'temperature': 0.2,
    'top_k': 40,  # Reduced from 50
    'top_p': 0.9,
    'stream': False,  # Changed to False for better compatibility
    'threads': max(1, min(2, int(os.cpu_count() / 2))),  # Limit threads for low memory
    'context_length': 1024,  # Reduced context length
    'batch_size': 1  # Process one at a time
}

logger.info("Initializing LLM...")
try:
    # Try different library configurations for Apple Silicon compatibility
    lib_options = ["basic", "metal", None]  # Remove avx2 for ARM compatibility
    
    llm = None
    for lib in lib_options:
        try:
            config_copy = config.copy()
            if lib:
                config_copy['lib'] = lib
            elif 'lib' in config_copy:
                del config_copy['lib']
            
            llm = CTransformers(
                model=local_llm,
                model_type="mistral",
                **config_copy
            )
            logger.info(f"LLM Initialized successfully with lib='{lib}'!")
            break
        except Exception as e:
            logger.warning(f"Failed with lib='{lib}': {str(e)[:100]}")
            continue
    
    if llm is None:
        raise Exception("Failed to initialize LLM with any library configuration")
        
except Exception as e:
    logger.error(f"Failed to initialize LLM: {e}")
    print("Try these solutions:")
    print("   1. Install ARM64 compatible ctransformers: pip uninstall ctransformers && pip install ctransformers --no-cache-dir")
    print("   2. Or try: pip install ctransformers[metal] for Apple Silicon")
    print("   3. Ensure you have enough RAM (4GB+ minimum)")
    sys.exit(1)

prompt_template = """Use the following pieces of information to answer the user's question about cancer.
If you don't know the answer based on the provided context, just say that you don't know, don't try to make up an answer.
Please provide a clear, helpful, and medically accurate response.

Context: {context}
Question: {question}

Helpful answer:
"""

model_name = "BAAI/bge-large-en"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

logger.info("Initializing embeddings...")
try:
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    logger.info("Embeddings initialized successfully!")
except Exception as e:
    logger.error(f"Failed to initialize embeddings: {e}")
    print("Try installing required packages: pip install sentence-transformers")
    sys.exit(1)

prompt = PromptTemplate(template=prompt_template,
                        input_variables=['context', 'question'])

logger.info("Loading vector store...")
try:
    load_vector_store = Chroma(
        persist_directory="stores/medical_cosine", 
        embedding_function=embeddings
    )
    retriever = load_vector_store.as_retriever(search_kwargs={"k": 2})  # Reduced from 3 for memory efficiency
    
    # Test the vector store
    test_results = retriever.invoke("cancer")
    if not test_results:
        raise ValueError("Vector store appears to be empty or corrupted")
    
    logger.info(f"Vector store loaded successfully! Found {len(test_results)} test documents.")
except Exception as e:
    logger.error(f"Failed to load vector store: {e}")
    print("Try recreating the vector store: python ingest.py")
    sys.exit(1)


@app.route('/')
def index():
    logger.info("Serving main page")
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "model": "neural-chat-7b-v3-1.Q4_K_M.gguf",
        "vector_store": "ready"
    })

@app.route('/get_response', methods=['POST'])
def get_responses():
    start_time = logger.info("Processing query...")
    
    try:
        # Get and validate query
        query = request.form.get('query')
        if not query:
            raise ValueError("No query provided")
        
        query = query.strip()
        if len(query) < 2:
            raise ValueError("Query is too short (minimum 2 characters)")
        
        if len(query) > 1000:
            raise ValueError("Query is too long (maximum 1000 characters)")
        
        logger.info(f"Query: {query[:100]}{'...' if len(query) > 100 else ''}")
        
        # Retrieve relevant documents
        logger.info("Searching for relevant documents...")
        relevant_docs = retriever.invoke(query)
        
        if not relevant_docs:
            logger.warning("No relevant documents found")
            return jsonify({
                "answer": "I couldn't find any relevant information in my knowledge base to answer your question. Please try rephrasing your question or ask about general cancer topics.",
                "source_document": "No relevant documents found",
                "doc": "Unknown"
            })
        
        logger.info(f"Found {len(relevant_docs)} relevant documents")
        
        # Create QA chain
        chain_type_kwargs = {"prompt": prompt}
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,  
            return_source_documents=True,
            chain_type_kwargs=chain_type_kwargs,
            verbose=False  # Reduce verbosity
        )

        logger.info("Generating response...")
        response = qa.invoke(query)
        
        # Extract response data
        if 'result' in response:
            answer = response['result'].strip()
        else:
            answer = 'No answer found'
        
        if 'source_documents' in response and response['source_documents']:
            source_document = response['source_documents'][0].page_content
            doc = response['source_documents'][0].metadata.get('source', 'Unknown')
            # Clean up the document path
            if doc != 'Unknown':
                doc = os.path.basename(doc)
        else:
            source_document = 'No source document found'
            doc = 'Unknown'
        
        # Clean up the answer
        if answer and len(answer.strip()) > 0:
            # Remove any unwanted prefixes/suffixes
            answer = answer.replace("Helpful answer:", "").strip()
        else:
            answer = "I couldn't generate a proper response. Please try rephrasing your question."
        
        response_data = {
            "answer": answer,
            "source_document": source_document[:1000] + "..." if len(source_document) > 1000 else source_document,
            "doc": doc
        }
        
        logger.info("Response generated successfully")
        return jsonify(response_data)
    
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error processing request: {error_msg}")
        
        # Provide helpful error messages
        if "CUDA" in error_msg or "GPU" in error_msg:
            error_msg = "GPU/CUDA error detected. This application is designed to run on CPU only."
        elif "memory" in error_msg.lower() or "ram" in error_msg.lower():
            error_msg = "Insufficient memory. Please close other applications and try again."
        elif "model" in error_msg.lower():
            error_msg = "Model loading error. Please check if the model file is corrupted."
        
        response_data = {
            "answer": "I encountered an error while processing your request. Please try again with a different question.",
            "source_document": f"Error details: {error_msg}",
            "doc": "Error"
        }
        
        return jsonify(response_data), 500



if __name__ == '__main__':
    port = 5001  # Changed from 5000 to avoid AirPlay conflict on macOS
    logger.info("Starting CancerCareBot Flask application...")
    logger.info(f"Server will be available at: http://localhost:{port}")
    logger.info(f"Health check endpoint: http://localhost:{port}/health")
    logger.info("Press Ctrl+C to stop the server")
    
    try:
        app.run(debug=False, host='0.0.0.0', port=port, threaded=True)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        print("Try these solutions:")
        print(f"   1. Check if port {port} is already in use")
        print(f"   2. Run: lsof -ti:{port} | xargs kill -9")
        print("   3. Try a different port: app.run(port=5002)")
