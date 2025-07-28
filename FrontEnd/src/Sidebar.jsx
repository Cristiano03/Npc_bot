import React, { useState, useEffect } from "react";

export default function Sidebar({ selectedChat, onChatSelect, sidebarOpen, onToggleSidebar }) {
  const [chats, setChats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch chats from backend
  useEffect(() => {
    fetchChats();
  }, []);

  const fetchChats = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/chats', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setChats(data.chats || []);
    } catch (error) {
      console.error('Error fetching chats:', error);
      setError('Errore nel caricamento delle chat');
      // Fallback to default chats if backend is not available
      setChats([
        { id: "aedryan", name: "Aedryan", avatar: "🧙‍♂️", lastMessage: "Come posso aiutarti oggi?", time: "12:30", unread: 0, description: "Saggio mago esperto" },
        { id: "thorin", name: "Thorin", avatar: "⚔️", lastMessage: "Pronto per la battaglia!", time: "11:45", unread: 2, description: "Guerriero coraggioso" },
        { id: "elara", name: "Elara", avatar: "🏹", lastMessage: "La natura mi chiama", time: "10:20", unread: 0, description: "Ranger elfica" },
        { id: "grommash", name: "Grommash", avatar: "🪓", lastMessage: "FOR THE HORDE!", time: "09:15", unread: 1, description: "Orco guerriero" },
        { id: "merlin", name: "Merlin", avatar: "🔮", lastMessage: "La magia è ovunque", time: "08:30", unread: 0, description: "Mago potente" },
        { id: "aragorn", name: "Aragorn", avatar: "👑", lastMessage: "Il re ritorna", time: "07:45", unread: 3, description: "Re di Gondor" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleChatClick = (chatId) => {
    onChatSelect(chatId);
  };

  const handleRefresh = () => {
    fetchChats();
  };

  return (
    <div style={{ 
      width: sidebarOpen ? '320px' : '0px', 
      backgroundColor: '#1e293b', 
      borderRight: '1px solid #334155',
      display: 'flex',
      flexDirection: 'column',
      transition: 'width 0.3s ease',
      overflow: 'hidden'
    }}>
      {/* Sidebar Header */}
      <div style={{ 
        backgroundColor: '#1e293b', 
        padding: '12px 16px', 
        borderBottom: '1px solid #334155',
        flexShrink: 0
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <h2 style={{ color: 'white', fontWeight: '600', fontSize: '18px', margin: 0 }}>NPC Bots</h2>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button
              onClick={handleRefresh}
              disabled={loading}
              style={{ 
                color: '#94a3b8', 
                background: 'none', 
                border: 'none', 
                padding: '4px',
                cursor: loading ? 'not-allowed' : 'pointer',
                fontSize: '16px'
              }}
              title="Aggiorna chat"
            >
              🔄
            </button>
            <button
              onClick={onToggleSidebar}
              style={{ 
                color: '#94a3b8', 
                background: 'none', 
                border: 'none', 
                padding: '4px',
                cursor: 'pointer'
              }}
            >
              ✕
            </button>
          </div>
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div style={{ 
          padding: '20px', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          color: '#94a3b8'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div style={{ 
              width: '16px', 
              height: '16px', 
              border: '2px solid #334155', 
              borderTop: '2px solid #10b981', 
              borderRadius: '50%', 
              animation: 'spin 1s linear infinite' 
            }}></div>
            Caricamento chat...
          </div>
        </div>
      )}

      {/* Error State */}
      {error && !loading && (
        <div style={{ 
          padding: '16px', 
          color: '#ef4444', 
          fontSize: '14px',
          textAlign: 'center'
        }}>
          {error}
          <button
            onClick={handleRefresh}
            style={{ 
              marginLeft: '8px',
              color: '#10b981',
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              textDecoration: 'underline'
            }}
          >
            Riprova
          </button>
        </div>
      )}

      {/* Chats List */}
      {!loading && !error && (
        <div style={{ flex: 1, overflowY: 'auto' }}>
          {chats.length === 0 ? (
            <div style={{ 
              padding: '20px', 
              textAlign: 'center', 
              color: '#94a3b8',
              fontSize: '14px'
            }}>
              Nessuna chat disponibile
            </div>
          ) : (
            chats.map((chat) => (
              <div
                key={chat.id}
                onClick={() => handleChatClick(chat.id)}
                style={{
                  padding: '12px 16px',
                  cursor: 'pointer',
                  backgroundColor: selectedChat === chat.id ? '#334155' : 'transparent',
                  borderLeft: selectedChat === chat.id ? '4px solid #10b981' : 'none',
                  transition: 'background-color 0.2s ease',
                  borderBottom: '1px solid #334155'
                }}
                onMouseEnter={(e) => {
                  if (selectedChat !== chat.id) {
                    e.target.style.backgroundColor = '#334155';
                  }
                }}
                onMouseLeave={(e) => {
                  if (selectedChat !== chat.id) {
                    e.target.style.backgroundColor = 'transparent';
                  }
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <div style={{ 
                    width: '48px', 
                    height: '48px', 
                    backgroundColor: '#475569', 
                    borderRadius: '50%', 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center',
                    fontSize: '20px',
                    flexShrink: 0
                  }}>
                    {chat.avatar || '🤖'}
                  </div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '4px' }}>
                      <h3 style={{ 
                        color: 'white', 
                        fontWeight: '500', 
                        margin: 0, 
                        fontSize: '14px',
                        whiteSpace: 'nowrap',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis'
                      }}>
                        {chat.name}
                      </h3>
                      <span style={{ 
                        color: '#94a3b8', 
                        fontSize: '12px',
                        flexShrink: 0,
                        marginLeft: '8px'
                      }}>
                        {chat.time}
                      </span>
                    </div>
                    <p style={{ 
                      color: '#94a3b8', 
                      fontSize: '12px', 
                      margin: '0 0 4px 0',
                      whiteSpace: 'nowrap',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis'
                    }}>
                      {chat.description}
                    </p>
                    <p style={{ 
                      color: '#64748b', 
                      fontSize: '11px', 
                      margin: 0,
                      whiteSpace: 'nowrap',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis'
                    }}>
                      {chat.lastMessage}
                    </p>
                  </div>
                  {chat.unread > 0 && (
                    <div style={{ 
                      backgroundColor: '#10b981', 
                      color: 'white', 
                      fontSize: '12px', 
                      borderRadius: '50%', 
                      width: '20px', 
                      height: '20px', 
                      display: 'flex', 
                      alignItems: 'center', 
                      justifyContent: 'center',
                      flexShrink: 0
                    }}>
                      {chat.unread}
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Footer */}
      <div style={{ 
        padding: '12px 16px', 
        borderTop: '1px solid #334155',
        backgroundColor: '#1e293b',
        flexShrink: 0
      }}>
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'space-between',
          fontSize: '12px',
          color: '#64748b'
        }}>
          <span>{chats.length} chat disponibili</span>
          <span>v1.0</span>
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