# 🩺 RAG Clinical Support API – Ophthalmology

## Overview
This project implements a **Retrieval-Augmented Generation (RAG) API** designed to support **clinical decision-making in ophthalmology**, with an initial focus on **retinal diseases in adults**, particularly **Age-related Macular Degeneration (AMD / DMAE)**.

The API provides **fast, consistent, and evidence-based answers** to clinical questions by retrieving information **exclusively from officially validated medical guidelines** and generating structured responses using a Large Language Model (LLM).

The solution was developed as part of the **Get Talent 2025 – Final Challenge**.

---

## Problem Statement
In clinical practice, diagnostic and treatment criteria may vary between doctors due to experience, training, or resource availability. This variability can lead to:

- Inconsistent medical messages for the same patient
- Increased patient uncertainty and reduced trust
- Difficulty standardizing clinical criteria in hospitals and training centers

Additionally, authoritative clinical guidelines:
- Are usually **long and complex**
- Are **written in English**, creating a language barrier
- Are impractical to consult repeatedly during daily clinical workflows

---

## Objective
To design an **API-based clinical assistant** using **Retrieval-Augmented Generation (RAG)** that:

- Uses **only high-quality, official medical sources**
- Provides **standardized, reproducible answers**
- Allows **natural language queries in Spanish**
- Returns **clinically reliable responses** aligned with international guidelines

---

## Target Users

- **Ophthalmologists** making diagnostic and treatment decisions
- **Ophthalmology residents**, both in clinical training and academic study
- **Healthcare institutions**, benefiting indirectly from:
  - Improved quality of care
  - Standardized clinical criteria
  - Adoption of cutting-edge AI solutions

---

## Data Sources

The system is grounded in guidelines from the **American Academy of Ophthalmology (AAO)**, the most prestigious global authority in ophthalmology.

- Source documents: **Preferred Practice Patterns (PPP)**
- Characteristics:
  - Expert-reviewed
  - Periodically updated
  - Widely adopted in clinical practice

For this implementation, the knowledge base includes the **PPP on Age-related Macular Degeneration**, publicly available on the AAO website.

---

## Technical Stack

### Environment & Libraries
A Python virtual environment was created with the following key dependencies:

- `PyMuPDF`
- `langchain` / `langchain-community`
- `cohere`
- `chromadb`
- `python-dotenv`
- `fastapi`
- `uvicorn`

---

## Data Processing Pipeline

### PDF Text Extraction
- Source documents are provided as **PDF files**
- Text is extracted using **PyMuPDF**, chosen for its superior handling of:
  - Tables
  - Multi-column layouts
- Page numbers are preserved to enable **source citation in responses**

Key functions:
- `extract_text_from_pdf`
- `process_all_pdfs`

---

### Chunking
- Implemented using **RecursiveCharacterTextSplitter (LangChain)**
- Preserves semantic coherence by progressively splitting from larger units to smaller ones

---

### Embeddings & Vector Database

- Embeddings generated using **Cohere – embed-multilingual-v3.0**
- Enables **cross-lingual retrieval**:
  - User queries in Spanish
  - Source documents in English
  - Answers returned in Spanish

- Vectors stored in **ChromaDB**
- Similarity metric: **Cosine similarity**
- **Persistence enabled**, avoiding repeated preprocessing across app restarts

---

## RAG Architecture

### Reranked Retriever
To improve retrieval quality in long clinical documents:

- Initial retrieval: `top_n = 20`
- Final selection: `top_k = 5`
- Reranking performed with **Cohere** using the same multilingual embedding model

This approach improves recall for concepts distributed throughout the document rather than confined to a single section.

---

### RAG Answer Generation
The RAG flow:

1. User submits a natural language question
2. Query is embedded and searched in ChromaDB
3. Relevant chunks are reranked
4. Top 5 chunks are combined into a context
5. Response is generated using Cohere LLM

Model configuration:

- Model: `command-r-plus-08-2024`
- Temperature: `0.0`
  - Ensures **deterministic and reproducible** answers
  - Essential for medical use cases

---

## API Design

### Schemas
- Both request (`query`) and response (`answer`) are defined as `string` types

### Orchestrator
To optimize system behavior:

- Common conversational inputs (e.g., greetings, thanks) are intercepted
- Predefined responses are returned via `get_generic_responses`
- Only relevant clinical queries are routed to the RAG pipeline

This prevents unnecessary LLM usage and improves user experience.

---

### Router

- Central integration point
- Defines API routes and HTTP methods
- Receives user queries and calls `orchestrated_answer`
- Built using **FastAPI**

---

### API Entry Point

- Initializes the FastAPI application
- Includes routers
- Provides a `GET` endpoint for health checks
- Executed using **Uvicorn**

---

## Frontend

A simple web-based chat interface was created using:

- HTML
- CSS
- JavaScript

The UI was designed with the assistance of **Claude AI**, focusing on usability and clarity for medical professionals.

---

## Future Improvements

- Expand the knowledge base with additional PPPs and other ophthalmic diseases
- Enhance the orchestrator to:
  - Route out-of-scope questions to a general LLM (without RAG)
  - Use a secondary prompt for non-clinical queries
- Store conversation history for:
  - Quality control
  - Usage analytics
- Improve frontend with:
  - Protocol filters when multiple guidelines are available
  - Faster and more targeted vector searches

---

## Disclaimer

This system is intended as a **clinical decision support tool** and **does not replace professional medical judgment**. All outputs should be interpreted within the context of individual patient care and institutional policies.