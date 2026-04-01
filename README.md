# CancerCare Bot

![Project Version](https://img.shields.io/badge/version-2.0.0-blue.svg?style=flat-square)
![Python](https://img.shields.io/badge/python-3.8%2B-yellow.svg?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)

> **A privacy-first, CPU-optimized AI assistant for cancer-related information, powered by Intel's Neural Chat LLM.**

---

## Overview

**CancerCare Bot** is a personal AI project developed collaboratively by **Vedika Lohiya**. Our goal was to build a state-of-the-art chatbot that provides accurate, concise, and helpful answers to cancer-related queries using Retrieval-Augmented Generation (RAG) technology.

Designed with accessibility in mind, this project demonstrates how powerful AI applications can be optimized to run **locally on standard CPUs**, ensuring data privacy without the need for expensive GPU hardware.

### Key Features

-   **Intel Neural Chat LLM**: High-performance 7B parameter model optimized for Intel CPUs.
-   **Privacy First**: All data processing and inference happen locally on your machine.
-   **RAG Technology**: Uses personal/medical documents (PDFs) to provide context-aware answers.
-   **Glassmorphism UI**: A beautiful, modern, and responsive interface designed from scratch.
-   **CPU Optimized**: Runs efficiently on standard hardware (8GB+ RAM recommended).

---

## Architecture

The CancerCare Bot operates on a sophisticated **Retrieval-Augmented Generation (RAG)** pipeline designed for offline efficiency. Here's how the components interact:

### 1. Data Ingestion & Embedding
-   **Source Documents**: Medical PDFs are loaded from the `Data/` directory.
-   **Chunking**: Documents are split into manageable chunks using `RecursiveCharacterTextSplitter`.
-   **Embedding**: Each chunk is converted into a vector representation using the **BAAI/bge-large-en** model. This captures the semantic meaning of the text.
-   **Vector Store**: These vectors are stored locally in **Chroma DB**, enabling lightning-fast similarity search.

### 2. Retrieval System
-   **User Query**: When a user asks a question, it is also converted into a vector embedding.
-   **Semantic Search**: The system queries Chroma DB to find the most relevant document chunks that match the user's intent, not just keywords.

### 3. Generative AI (LLM)
-   **Context Injection**: The retrieved information is combined with the user's original question into a structured prompt.
-   **Inference**: This prompt is fed into the **Intel Neural Chat 7B** model.
-   **Response**: The LLM generates a medically accurate, natural language response based *solely* on the provided context, minimizing hallucinations.

### 4. Application Layer
-   **Flask Backend**: Orchestrates the entire flow and serves the API.
-   **Frontend**: A responsive Glassmorphism UI provides an engaging user experience, communicating with the backend via asynchronous JavaScript fetch calls.

---

## Getting Started

### Prerequisites

-   Python 3.8 or higher
-   8GB RAM (Minimum)
-   5GB Disk Space (for the model)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Aditya19110/Calanalyst
    cd Calanalyst
    ```

2.  **Run Setup Script** (Downloads the LLM automatically)
    ```bash
    python setup.py
    ```

3.  **Create Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

4.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Ingest Data** (Process PDF documents)
    ```bash
    # Place your PDFs in the 'Data/' folder first!
    python ingest.py
    ```

### Running the App

```bash
python app.py
```
Open your browser and navigate to: [http://localhost:5001](http://localhost:5001)


## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<p align="center">
  Built with ❤️ for the AI community
</p>
