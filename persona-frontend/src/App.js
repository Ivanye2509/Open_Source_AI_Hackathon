import React, { useState, useEffect, useRef } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  // Fetch messages from the Flask server
  const fetchMessages = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/messages");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setMessages(data.messages);
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  };

  // Send a message to the Flask server
  const sendMessage = async () => {
    if (input.trim() !== "") {
      try {
        const response = await fetch("http://127.0.0.1:5000//api/send", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: input }),
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setMessages(data.messages); // Update messages with the response
        setInput(""); // Clear the input field
      } catch (error) {
        console.error("Error sending message:", error);
      }
    }
  };

  // Auto-scroll to the bottom when new messages are added
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Fetch messages when the component mounts
  useEffect(() => {
    fetchMessages();
  }, []);

  // Scroll to the bottom when messages are updated
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle "Enter" key press
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div className="container-fluid vh-100 d-flex flex-column bg-dark text-light">
      {/* Chat Header */}
      <header className="bg-dark text-white text-center py-4 border-bottom border-secondary">
        <h1 className="mb-0">Persona AI</h1>
        <p className="text-muted mb-0">Integrated with Flask and Jupyter Notebook</p>
      </header>

      {/* Messages Container */}
      <div className="flex-grow-1 overflow-auto p-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`d-flex mb-3 ${
              message.sender === "user" ? "justify-content-end" : "justify-content-start"
            }`}
          >
            <div
              className={`p-3 rounded ${
                message.sender === "user"
                  ? "bg-primary text-white"
                  : "bg-secondary text-light"
              }`}
              style={{ maxWidth: "70%" }}
            >
              <strong>{message.sender}:</strong> {message.text}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Container */}
      <div className="bg-dark p-3 border-top border-secondary">
        <div className="input-group">
          <input
            type="text"
            className="form-control bg-dark text-light border-secondary"
            placeholder="Type your message here..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <button className="btn btn-primary" onClick={sendMessage}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;