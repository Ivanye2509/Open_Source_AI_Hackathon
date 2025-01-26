# RAG-based Persona Chatbot 🤖

> A Retrieval-Augmented Generation system that learns and mimics personal communication styles from chat history.

## 🏗 System Architecture

```mermaid
graph TD
    subgraph Data Ingestion
        CH[Chat History] --> Parser[Chat Parser]
        Parser --> QA[Q&A Pairs]
        QA --> VE[Vector Embeddings]
    end

    subgraph Vector Storage
        VE --> VS[(Chroma DB)]
        VS --> IC[Index Collection]
        IC --> MT[Metadata Tags]
    end

    subgraph Persona Analysis
        QA --> PA[Personality Analyzer]
        PA --> PT[Traits Extraction]
        PA --> PS[Style Analysis]
        PA --> PP[Phrase Patterns]
    end

    subgraph RAG Engine
        UQ[User Query] --> SR[Semantic Retrieval]
        SR --> VS
        VS --> RC[Relevant Context]
        RC --> RG[Response Generator]
        PT --> RG
        PS --> RG
        PP --> RG
    end

    subgraph Response Pipeline
        RG --> RM[Response Matching]
        RM --> EX[Exact Match]
        RM --> SM[Similar Match]
        EX --> FR[Final Response]
        SM --> FR
    end
```

## ✨ Features
    
🧠 Intelligent Persona Analysis

- Extracts personality traits
- Learns communication style
- Identifies common phrases
- Maps topic interests

🎯 Context-Aware Responses

- RAG-powered generation
- Historical context matching
- Style-consistent replies
- Exact response matching

## 🚀 Quick Start
Prerequisites
```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Setup
1. Set OpenAI API key
```
set OPENAI_API_KEY=your-api-key
```

2. Run application
```
python app.py
```
3. Access interface

- Open browser to http://localhost:5000
- Upload chat history file
- Start conversation

## 💻 Technologies
- Frontend: Bootstrap 5, Socket.IO
- Backend: Flask, Flask-SocketIO
- AI/ML: LangChain, OpenAI GPT-4
- Vector Store: ChromaDB
- Embeddings: OpenAI Ada

## 📁 Project Structure
```
Open_Source_AI_Hackathon/
├── app.py              # Flask server
├── persona_chatbot.py  # Core RAG logic
├── templates/          # Frontend
│   └── index.html     # Chat interface
├── requirements.txt    # Dependencies
└── README.md          # Documentation
```

## 📄 License
MIT License - See LICENSE for details

## 👥 Team
Developed for Open Source AI Hackathon 2024 by Data Doppelgangers (GitHub: @ivanye2509, @prabhatmenon, @patelmanan96, @solkit70)

## 🙏 Acknowledgments
- OpenAI
- LangChain Framework
- Flask Community
- Kaggle CommunityGit
