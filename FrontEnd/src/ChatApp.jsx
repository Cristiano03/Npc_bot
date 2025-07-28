import React, { useState, useEffect } from "react";
import Sidebar from "./Sidebar";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedChat, setSelectedChat] = useState("aedryan");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [conversationHistory, setConversationHistory] = useState({});

  // Carica lo storico della conversazione quando cambia la chat selezionata
  useEffect(() => {
    if (selectedChat) {
      loadConversationHistory(selectedChat);
    }
  }, [selectedChat]);

  const loadConversationHistory = async (npcId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/conversation/${npcId}/history?user_id=default_user&limit=50`);
      if (response.ok) {
        const data = await response.json();
        
        // Converti lo storico in formato compatibile con il frontend
        const formattedMessages = data.history.map(msg => ({
          sender: msg.sender === 'user' ? 'user' : 'bot',
          text: msg.content,
          timestamp: msg.timestamp
        }));

        // Imposta i messaggi (anche se vuoto, non mostra messaggio di benvenuto)
        setMessages(formattedMessages);

        // Salva lo storico nel cache locale
        setConversationHistory(prev => ({
          ...prev,
          [npcId]: formattedMessages
        }));
      } else {
        console.error('Errore nel caricamento dello storico:', response.statusText);
        setMessages([]);
      }
    } catch (error) {
      console.error('Errore nel caricamento dello storico:', error);
      setMessages([]);
    }
  };

  async function handleSend() {
    if (!inputText.trim() || loading) return;

    const userMessage = { sender: "user", text: inputText };
    setMessages(prev => [...prev, userMessage]);
    setInputText("");
    setLoading(true);

    try {
      const response = await fetch(`http://localhost:8000/api/${selectedChat}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: inputText,
          user_id: "default_user",
          include_history: true
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const botMessage = { sender: "bot", text: data.reply };
        setMessages(prev => [...prev, botMessage]);
      } else {
        const errorMessage = { sender: "bot", text: "Errore nella comunicazione con il server." };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error("Errore:", error);
      const errorMessage = { sender: "bot", text: "Errore nella comunicazione con il server." };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  }

  const handleChatSelect = (chatId) => {
    setSelectedChat(chatId);
    // Lo storico viene caricato automaticamente tramite useEffect
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div style={{ height: '100vh', width: '100vw', backgroundColor: '#0f172a', display: 'flex', overflow: 'hidden' }}>
      {/* Sidebar Component */}
      <Sidebar
        selectedChat={selectedChat}
        onChatSelect={handleChatSelect}
        sidebarOpen={sidebarOpen}
        onToggleSidebar={toggleSidebar}
      />

      {/* Main Chat Area */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0 }}>
        {/* Chat Header */}
        <div style={{
          backgroundColor: '#1e293b',
          padding: '12px 16px',
          borderBottom: '1px solid #334155',
          flexShrink: 0
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <button
              onClick={toggleSidebar}
              style={{
                color: '#94a3b8',
                background: 'none',
                border: 'none',
                padding: '4px',
                cursor: 'pointer'
              }}
            >
              ☰
            </button>
            <div style={{
              width: '40px',
              height: '40px',
              backgroundColor: '#475569',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '20px'
            }}>
              🤖
            </div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <h2 style={{ color: 'white', fontWeight: '500', margin: 0, fontSize: '16px' }}>
                Chat con {selectedChat}
              </h2>
              <p style={{ color: '#94a3b8', fontSize: '14px', margin: 0 }}>
                Bot disponibile
              </p>
            </div>
          </div>
        </div>

        {/* Messages Container */}
        <div style={{
          flex: 1,
          overflowY: 'auto',
          padding: '16px',
          display: 'flex',
          flexDirection: 'column',
          gap: '12px'
        }}>
          {messages.length === 0 && !loading && (
            <div style={{
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              height: '100%',
              color: '#94a3b8',
              fontSize: '16px',
              textAlign: 'center'
            }}>
              <div>
                <div style={{ fontSize: '48px', marginBottom: '16px' }}>💬</div>
                <div>Inizia una conversazione con {selectedChat}</div>
                <div style={{ fontSize: '14px', marginTop: '8px', opacity: 0.7 }}>
                  Scrivi un messaggio per iniziare
                </div>
              </div>
            </div>
          )}
          
          {messages.map((message, index) => (
            <div
              key={index}
              style={{
                display: 'flex',
                justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                marginBottom: '8px'
              }}
            >
              <div
                style={{
                  maxWidth: '70%',
                  padding: '12px 16px',
                  borderRadius: message.sender === 'user' ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
                  backgroundColor: message.sender === 'user' ? '#0ea5e9' : '#334155',
                  color: 'white',
                  wordWrap: 'break-word',
                  fontSize: '14px',
                  lineHeight: '1.4'
                }}
              >
                {message.text}
                {message.timestamp && (
                  <div style={{
                    fontSize: '11px',
                    opacity: 0.7,
                    marginTop: '4px',
                    textAlign: message.sender === 'user' ? 'right' : 'left'
                  }}>
                    {new Date(message.timestamp).toLocaleTimeString('it-IT', {
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </div>
                )}
              </div>
            </div>
          ))}
          {loading && (
            <div style={{
              display: 'flex',
              justifyContent: 'flex-start',
              marginBottom: '8px'
            }}>
              <div style={{
                padding: '12px 16px',
                borderRadius: '18px 18px 18px 4px',
                backgroundColor: '#334155',
                color: 'white',
                fontSize: '14px'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <div style={{
                    width: '16px',
                    height: '16px',
                    border: '2px solid #94a3b8',
                    borderTop: '2px solid transparent',
                    borderRadius: '50%',
                    animation: 'spin 1s linear infinite'
                  }}></div>
                  Sta scrivendo...
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div style={{
          backgroundColor: '#1e293b',
          padding: '16px',
          borderTop: '1px solid #334155',
          flexShrink: 0
        }}>
          <div style={{
            display: 'flex',
            gap: '12px',
            alignItems: 'flex-end'
          }}>
            <div style={{
              flex: 1,
              backgroundColor: '#334155',
              borderRadius: '20px',
              padding: '8px 16px',
              minHeight: '40px',
              maxHeight: '120px',
              overflowY: 'auto'
            }}>
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Scrivi un messaggio..."
                style={{
                  width: '100%',
                  minHeight: '24px',
                  maxHeight: '96px',
                  backgroundColor: 'transparent',
                  border: 'none',
                  outline: 'none',
                  color: 'white',
                  fontSize: '14px',
                  resize: 'none',
                  fontFamily: 'inherit'
                }}
                rows={1}
              />
            </div>
            <button
              onClick={handleSend}
              disabled={!inputText.trim() || loading}
              style={{
                backgroundColor: inputText.trim() && !loading ? '#0ea5e9' : '#475569',
                color: 'white',
                border: 'none',
                borderRadius: '50%',
                width: '40px',
                height: '40px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: inputText.trim() && !loading ? 'pointer' : 'not-allowed',
                fontSize: '18px'
              }}
            >
              ➤
            </button>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}