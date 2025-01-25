import React, { useState, useRef, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css"; // Import Bootstrap CSS
import "./App.css"; // Custom CSS for additional styling

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  // Auto-scroll to the bottom when new messages are added
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle sending messages
  const handleSend = () => {
    if (input.trim() !== "") {
      setMessages([...messages, { text: input, sender: "You" }]);
      setInput("");
      // Simulate a bot response after 1 second
      setTimeout(() => {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: "This is a bot response!", sender: "Bot" },
        ]);
      }, 1000);
    }
  };

  // Handle "Enter" key press to send messages
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  return (
    <div className="container-fluid vh-100 d-flex flex-column bg-dark text-light">
      {/* Chat Header */}
      <header className="bg-dark text-white text-center py-4 border-bottom border-secondary">
        <h1 className="mb-0">Chat Application</h1>
        <p className="text-muted mb-0">A modern dark-themed chat app</p>
      </header>

      {/* Messages Container */}
      <div className="flex-grow-1 overflow-auto p-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`d-flex mb-3 ${
              message.sender === "You" ? "justify-content-end" : "justify-content-start"
            }`}
          >
            <div
              className={`p-3 rounded ${
                message.sender === "You"
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
          <button
            className="btn btn-primary"
            onClick={handleSend}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;