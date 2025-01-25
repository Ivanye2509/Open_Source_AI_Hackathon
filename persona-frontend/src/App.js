import React, { useState } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim() !== "") {
      setMessages([...messages, { text: input, sender: "You" }]);
      setInput("");
      // Simulating a bot response
      setTimeout(() => {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: "This is a bot response!", sender: "Bot" },
        ]);
      }, 1000);
    }
  };

  return (
    <div className="chat-window">
      <header className="chat-header">
        <h1>Chat Application</h1>
      </header>
      <div className="messages-container">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.sender === "You" ? "you" : "bot"}`}
          >
            <span className="message-sender">{message.sender}:</span>
            <span className="message-text">{message.text}</span>
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          className="chat-input"
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message here..."
        />
        <button className="send-button" onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}

export default App;
