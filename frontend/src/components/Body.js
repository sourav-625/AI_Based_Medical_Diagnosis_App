import React, { useState } from 'react';

const Chat = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const handleSend = async () => {
        if (input.trim() === '') return;

        const userMessage = { sender: 'User', text: input };
        setMessages([...messages, userMessage]);

        try {
            const response = await fetch('http://127.0.0.1:5000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: input }),
            });
            const data = await response.json();
            const botMessage = { sender: 'Bot', text: data.response };
            setMessages((prevMessages) => [...prevMessages, botMessage]);
        } catch (error) {
            const errorMessage = { sender: 'Bot', text: 'Error: Unable to connect to the server.' };
            setMessages((prevMessages) => [...prevMessages, errorMessage]);
        }

        setInput('');
    };

    return (
        <div className="container mt-4">
            <link
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
                rel="stylesheet"
                integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
                crossOrigin="anonymous"
            />
            <script
                src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
                integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
                crossOrigin="anonymous"
            ></script>
            <div className="card">
                <div className="card-header text-bg-primary">Chat with MediBot</div>
                <div
                    className="card-body"
                    style={{
                        height: '400px',
                        overflowY: 'scroll',
                        backgroundColor: '#f8f9fa',
                    }}
                >
                    <span className="badge bg-secondary">Please tell me your Problems</span>
                    {messages.map((msg, index) => (
                        <div
                            key={index}
                            className={`mb-2 ${
                                msg.sender === 'User' ? 'text-end' : 'text-start'
                            }`}
                        >
                            <span
                                className={`badge ${
                                    msg.sender === 'User' ? 'bg-primary' : 'bg-secondary'
                                }`}
                            >
                                {msg.sender}: {msg.text}
                            </span>
                        </div>
                    ))}
                </div>
                <div className="card-footer">
                    <div className="input-group">
                        <input
                            type="text"
                            className="form-control"
                            placeholder="Type your message..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter') handleSend();
                            }}
                        />
                        <button className="btn btn-primary" onClick={handleSend}>
                            Send
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Chat;