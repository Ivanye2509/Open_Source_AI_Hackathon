# Open_Source_AI_Hackathon

## System Architecture

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

## To run
### 1. Save your chat data in human_chat.txt
### 2. Install requirements:
 pip install gradio langchain chromadb tiktoken
### 3. Set your OpenAI API key:

 export OPENAI_API_KEY="your-api-key"
### 4. Run the chatbot:

 python persona_chatbot.py