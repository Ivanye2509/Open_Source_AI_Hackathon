from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
import gradio as gr
import json
from typing import List, Dict, Any
from langchain_core.documents import Document

# Constants
DATA_FILE = "human_chat.txt"
PERSIST_DIR = "./human1_db"
TARGET_USER = "Human 1"
MODEL_NAME = "gpt-4"
TEMPERATURE = 0.7
MAX_HISTORY = 100

# Initialize models
try:
    embeddings = OpenAIEmbeddings()
    llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)
except Exception as e:
    raise Exception(f"Failed to initialize models: {str(e)}")

def parse_chat_data(file_path: str) -> List[Document]:
    documents = []
    current_conversation = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            lines = f.readlines()
    
    for line in lines:
        if line.strip():
            if "Human 2:" in line or "Human 1:" in line:
                speaker, message = line.split(":", 1)
                current_conversation.append((speaker.strip(), message.strip()))
                
                if len(current_conversation) >= 2:
                    if current_conversation[-2][0] == "Human 2" and current_conversation[-1][0] == TARGET_USER:
                        documents.append(Document(
                            page_content=f"Question: {current_conversation[-2][1]}\nAnswer: {current_conversation[-1][1]}",
                            metadata={
                                "question": current_conversation[-2][1],
                                "answer": current_conversation[-1][1],
                                "speaker": TARGET_USER
                            }
                        ))
    return documents

def analyze_persona(docs: List[Document]) -> Dict[str, Any]:
    try:
        prompt = """Analyze the personality and respond in JSON format with:
        - traits: list of personality traits
        - style: communication style
        - phrases: common phrases used
        - interests: key topics discussed"""
        
        response = ChatOpenAI(temperature=0).invoke(prompt)
        return json.loads(response.content)
    except Exception as e:
        print(f"Error analyzing persona: {str(e)}")
        return {
            "traits": ["friendly", "casual"],
            "style": "conversational",
            "phrases": ["how are you", "that's cool"],
            "interests": ["general conversation"]
        }

# Rest of the code remains the same...

def initialize_retriever() -> Chroma:
    """Initialize vector store with chat history"""
    docs = parse_chat_data(DATA_FILE)
    return Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )

class PersonaChatbot:
    def __init__(self):
        self.vector_store = initialize_retriever()
        self.persona = analyze_persona(parse_chat_data(DATA_FILE))
        self.history: List[str] = []
        self.last_context: str = ""  # Add context tracking
    
    def get_last_context(self) -> str:
        """Return the last retrieved context"""
        return self.last_context
    
    def clear_context(self) -> None:
        """Clear the stored context"""
        self.last_context = ""
    
    def generate_response(self, query: str) -> str:
        if len(self.history) > MAX_HISTORY:
            self.history = self.history[-MAX_HISTORY:]

        # Search for exact or similar questions
        retrieved = self.vector_store.similarity_search(
            query,
            k=3
        )
        
        # Extract relevant Q&A pairs
        relevant_contexts = []
        exact_match = None
        
        for doc in retrieved:
            if doc.metadata.get("question", "").lower().strip() == query.lower().strip():
                exact_match = doc.metadata.get("answer")
                break
            relevant_contexts.append(doc.page_content)
        
        self.last_context = "\n".join(relevant_contexts)
        
        if exact_match:
            response = exact_match
        else:
            prompt = f"""You are Human 1. ONLY use the provided examples to respond.
            If no relevant examples exist, use the personality traits and style.
            DO NOT make up information not present in the context.

            Human 1's Traits: {', '.join(self.persona['traits'])}
            Style: {self.persona['style']}
            
            Relevant Examples:
            {self.last_context}
            
            Question: {query}
            Answer:"""
            
            response = llm.invoke(prompt).content
        
        self.history.append(f"User: {query}")
        self.history.append(f"Human 1: {response}")
        return response

def create_ui() -> gr.Blocks:
    chatbot = PersonaChatbot()
    
    with gr.Blocks(title="Persona Chatbot") as interface:
        gr.Markdown(f"## {TARGET_USER} Persona Chatbot")
        
        chatbot_ui = gr.Chatbot(label="Conversation")
        msg = gr.Textbox(label="Your Message", placeholder="Type your message here...")
        clear = gr.Button("Clear History")
        
        def respond(message: str, chat_history: List) -> tuple:
            bot_response = chatbot.generate_response(message)
            chat_history.append((message, bot_response))
            return "", chat_history
        
        msg.submit(respond, [msg, chatbot_ui], [msg, chatbot_ui])
        clear.click(lambda: None, None, chatbot_ui, queue=False)
    
    return interface

if __name__ == "__main__":
    print("Initializing persona chatbot...")
    print(f"Analyzing data from {DATA_FILE}")
    try:
        ui = create_ui()
        ui.launch(share=False)
    except Exception as e:
        print(f"Error launching UI: {str(e)}")