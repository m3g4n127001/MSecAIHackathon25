import React, { useState } from 'react';
import axios from 'axios';
import './ChatBox.css';

function ChatBox() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const handleSendMessage = async () => {
        if (input.trim()) {
            const newMessages = [...messages, { text: input, sender: 'User' }];
            setMessages(newMessages);
            setInput('');

            try {
                const response = await axios.post('http://localhost:5000/api/chat', { query: input });
                setMessages([...newMessages, { text: response.data.filters, sender: 'Bot' }]);
            } catch (error) {
                console.error('Error sending message:', error);
                setMessages([...newMessages, { text: 'Error connecting to the backend. Please try again.', sender: 'Bot' }]);
            }
        }
    };

    return (
        <div className="chatbox">
            <h2>Copilot Chat</h2>
            <div className="chat-messages">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.sender}`}>
                        {msg.text}
                    </div>
                ))}
            </div>
            <div className="chat-input">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask me anything..."
                />
                <button onClick={handleSendMessage}>Send</button>
            </div>
        </div>
    );
}

export default ChatBox;