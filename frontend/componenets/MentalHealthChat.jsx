import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User } from 'lucide-react';

const Card = ({ children, className }) => (
  <div className={`bg-white rounded-lg shadow-lg ${className}`}>{children}</div>
);

const CardHeader = ({ children }) => (
  <div className="p-4 border-b bg-gradient-to-r from-blue-500 to-blue-600">
    {children}
  </div>
);

const CardTitle = ({ children, className }) => (
  <h2 className={`text-xl font-bold text-white ${className}`}>{children}</h2>
);

const CardContent = ({ children, className }) => (
  <div className={`p-4 ${className}`}>{children}</div>
);

const Alert = ({ children, variant = "default" }) => (
  <div className={`p-4 rounded-lg mb-4 ${
    variant === "destructive" ? "bg-red-100 text-red-900" : "bg-gray-100"
  }`}>
    {children}
  </div>
);

const AlertDescription = ({ children }) => (
  <div className="ml-2 inline-block">{children}</div>
);

const ChatMessage = ({ message, type }) => (
  <div className={`flex items-start space-x-2 mb-4 ${type === 'user' ? 'justify-end' : 'justify-start'}`}>
    {type === 'bot' && (
      <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
        <Bot className="w-5 h-5 text-blue-500" />
      </div>
    )}
    <div className={`max-w-[70%] rounded-2xl p-4 ${
      type === 'user' 
        ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-br-none' 
        : 'bg-gray-100 rounded-bl-none'
    }`}>
      {message}
    </div>
    {type === 'user' && (
      <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center">
        <User className="w-5 h-5 text-white" />
      </div>
    )}
  </div>
);

const ErrorState = ({ message }) => (
  <Alert variant="destructive" className="mb-4">
    <AlertDescription>{message}</AlertDescription>
  </Alert>
);

const MentalHealthChat = () => {
  const [messages, setMessages] = useState([
    { type: 'bot', content: "Hi, I'm here to support you. How are you feeling today?" }
  ]);
  const [input, setInput] = useState('');
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    try {
      setIsLoading(true);
      setError(null);
      
      const userMessage = input.trim();
      setMessages(prev => [...prev, { type: 'user', content: userMessage }]);
      setInput('');

      const response = await fetch('http://localhost:5001/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        mode: 'cors',
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();
      setMessages(prev => [...prev, { type: 'bot', content: data.response }]);
    } catch (err) {
      console.error('Error:', err);
      setError('Failed to get response. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-3xl mx-auto h-[700px] flex flex-col">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Bot className="w-8 h-8 text-white" />
          Mental Health Support Chat
        </CardTitle>
      </CardHeader>
      
      <CardContent className="flex-1 overflow-hidden flex flex-col bg-gray-50">
        <div className="flex-1 overflow-y-auto p-6">
          {error && <ErrorState message={error} />}
          
          {messages.map((msg, idx) => (
            <ChatMessage 
              key={idx} 
              message={msg.content} 
              type={msg.type} 
            />
          ))}
          
          {isLoading && (
            <div className="flex justify-start mb-4">
              <div className="ml-10 bg-gray-100 rounded-2xl p-4 rounded-bl-none">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-100" />
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce delay-200" />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="p-4 bg-white border-t">
          <form onSubmit={handleSubmit}>
            <div className="flex flex-col gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message..."
                className="w-full p-4 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-50"
                disabled={isLoading}
              />
              <button 
                type="submit" 
                disabled={isLoading || !input.trim()}
                className="w-full p-4 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl hover:from-blue-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                <span>Send Message</span>
                <Send className="w-5 h-5" />
              </button>
            </div>
          </form>
        </div>
      </CardContent>
    </Card>
  );
};

export default MentalHealthChat;