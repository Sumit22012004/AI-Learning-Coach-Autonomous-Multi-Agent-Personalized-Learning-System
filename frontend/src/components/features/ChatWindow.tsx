"use client";

import React, { useState, useRef, useEffect } from 'react';
import { agentApi } from '@/lib/api';
import { Send, User as UserIcon, Bot } from 'lucide-react';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

export default function ChatWindow() {
    const [messages, setMessages] = useState<Message[]>([
        { role: 'assistant', content: 'Hello! I am your AI Learning Coach. How can I help you today?' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Auto-scroll
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMsg = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
        setIsLoading(true);

        try {
            // Hardcoded user_id for Phase 3 demo
            const result = await agentApi.interact({
                user_id: "demo-user-123",
                message: userMsg
            });

            setMessages(prev => [...prev, { role: 'assistant', content: result.response }]);
        } catch (error) {
            console.error("Chat error:", error);
            setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I encountered an error connecting to my brain." }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-[600px] w-full max-w-2xl border rounded-xl shadow-lg bg-white overflow-hidden">
            {/* Header */}
            <div className="p-4 bg-slate-800 text-white flex items-center gap-2">
                <Bot className="w-6 h-6" />
                <h2 className="font-semibold">AI Coach Chat</h2>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`flex items-start max-w-[80%] gap-2 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                            <div className={`p-2 rounded-full ${msg.role === 'user' ? 'bg-blue-600' : 'bg-green-600'} text-white`}>
                                {msg.role === 'user' ? <UserIcon size={16} /> : <Bot size={16} />}
                            </div>
                            <div className={`p-3 rounded-lg ${msg.role === 'user'
                                    ? 'bg-blue-600 text-white rounded-tr-none'
                                    : 'bg-white border shadow-sm text-slate-800 rounded-tl-none'
                                }`}>
                                <p className="text-sm">{msg.content}</p>
                            </div>
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="flex items-center gap-2 bg-white border p-3 rounded-lg rounded-tl-none shadow-sm">
                            <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" />
                            <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-75" />
                            <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-150" />
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 bg-white border-t">
                <div className="flex gap-2">
                    <input
                        type="text"
                        className="flex-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Type your answer or question..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                        disabled={isLoading}
                    />
                    <button
                        onClick={handleSend}
                        disabled={isLoading || !input.trim()}
                        className="p-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 transition-colors"
                    >
                        <Send size={20} />
                    </button>
                </div>
            </div>
        </div>
    );
}
