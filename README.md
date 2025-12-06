# CancerCare Bot

![Project Version](https://img.shields.io/badge/version-2.0.0-blue.svg?style=flat-square)
![Python](https://img.shields.io/badge/python-3.8%2B-yellow.svg?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)

> **A privacy-first, CPU-optimized AI assistant for cancer-related information, powered by Intel's Neural Chat LLM.**

---

## Overview

**CancerCare Bot** is a personal AI project developed collaboratively by **Aditya Kulkarni**, **Rasika Rakhewar**, and **Vedika Lohiya**. Our goal was to build a state-of-the-art chatbot that provides accurate, concise, and helpful answers to cancer-related queries using Retrieval-Augmented Generation (RAG) technology.

Designed with accessibility in mind, this project demonstrates how powerful AI applications can be optimized to run **locally on standard CPUs**, ensuring data privacy without the need for expensive GPU hardware.

### Key Features

-   **Intel Neural Chat LLM**: High-performance 7B parameter model optimized for Intel CPUs.
-   **Privacy First**: All data processing and inference happen locally on your machine.
-   **RAG Technology**: Uses personal/medical documents (PDFs) to provide context-aware answers.
-   **Glassmorphism UI**: A beautiful, modern, and responsive interface designed from scratch.
-   **CPU Optimized**: Runs efficiently on standard hardware (8GB+ RAM recommended).

---

## Architecture

The system uses a modern open-source stack:

-   **LLM**: `neural-chat-7b-v3-1.Q4_K_M.gguf` (Quantized for CPU)
-   **Embeddings**: `BAAI/bge-large-en`
-   **Vector Store**: Chroma DB
-   **Orchestration**: LangChain & CTransformers
-   **Backend**: Flask (Python)
-   **Frontend**: HTML5, CSS3 (Glassmorphism), Vanilla JS

---

## Getting Started

### Prerequisites

-   Python 3.8 or higher
-   8GB RAM (Minimum)
-   5GB Disk Space (for the model)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Aditya19110/Team_Sentinals_Unnati-2024
    cd Team_Sentinals_Unnati-2024
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

---

## Developers

| Name | Role | Contact |
| :--- | :--- | :--- |
| **Aditya Kulkarni** | Full Stack Developer | [LinkedIn](https://www.linkedin.com/in/aditya191103) |
| **Rasika Rakhewar** | AI Researcher & Developer | [LinkedIn](https://www.linkedin.com/in/rasika-rakhewar-2a5158256/) |
| **Vedika Lohiya** | AI & LLM Specialist | [LinkedIn](https://www.linkedin.com/in/vedika2203) |

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<p align="center">
  Built with ❤️ for the AI community
</p>
