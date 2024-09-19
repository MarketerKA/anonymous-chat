import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css'

const API_URL = 'http://127.0.0.1:8000'; // URL of your FastAPI server

function App() {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [counter, setCounter] = useState(0);
  const socketRef = useRef(null);

  useEffect(() => {
    fetchMessages();
    fetchCounter();

    const ws = new WebSocket(`ws://${API_URL.split('http://')[1]}/ws`);
    socketRef.current = ws;

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages((prevMessages) => [...prevMessages, message]);
      setCounter((prevCounter) => prevCounter + 1);
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed');
    };

    return () => {
      ws.close();
    };
  }, []);

  const fetchMessages = async () => {
    try {
      const response = await axios.get(`${API_URL}/messages`);
      setMessages(response.data);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  const fetchCounter = async () => {
    try {
      const response = await axios.get(`${API_URL}/messages/count`);
      setCounter(response.data.count);
    } catch (error) {
      console.error('Error fetching counter', error);
    }
  };

  const handleSendMessage = async () => {
    if (!newMessage.trim()) return;
    try {
      await axios.post(`${API_URL}/messages`, { text: newMessage });
      setNewMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleSendMessage();
    }
  };

  return (
    <div className="chat-container">
      <h1>Anonymous Chat</h1>
      <p>Current number of messages: {counter}</p>
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index} className="message">
            <span>{msg.text}</span>
            <small>{new Date(msg.timestamp).toLocaleTimeString()}</small>
          </div>
        ))}
      </div>
      <input
        type="text"
        value={newMessage}
        onChange={(e) => setNewMessage(e.target.value)}
        onKeyDown={handleKeyDown} // Add this line
        placeholder="Type your message..."
      />
      <button onClick={handleSendMessage}>Send</button>
    </div>
  );
}

export default App;
