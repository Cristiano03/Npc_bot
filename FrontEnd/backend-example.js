// Esempio di endpoint backend per /api/chats
// Questo file mostra come dovrebbe essere strutturato l'endpoint del backend

// Endpoint: GET /api/chats
// Response example:

const exampleResponse = {
  "chats": [
    {
      "id": "aedryan",
      "name": "Aedryan",
      "avatar": "🧙‍♂️",
      "description": "Saggio mago esperto",
      "lastMessage": "Come posso aiutarti oggi?",
      "time": "12:30",
      "unread": 0,
      "status": "online"
    },
    {
      "id": "thorin",
      "name": "Thorin",
      "avatar": "⚔️",
      "description": "Guerriero coraggioso",
      "lastMessage": "Pronto per la battaglia!",
      "time": "11:45",
      "unread": 2,
      "status": "online"
    },
    {
      "id": "elara",
      "name": "Elara",
      "avatar": "🏹",
      "description": "Ranger elfica",
      "lastMessage": "La natura mi chiama",
      "time": "10:20",
      "unread": 0,
      "status": "offline"
    },
    {
      "id": "grommash",
      "name": "Grommash",
      "avatar": "🪓",
      "description": "Orco guerriero",
      "lastMessage": "FOR THE HORDE!",
      "time": "09:15",
      "unread": 1,
      "status": "online"
    },
    {
      "id": "merlin",
      "name": "Merlin",
      "avatar": "🔮",
      "description": "Mago potente",
      "lastMessage": "La magia è ovunque",
      "time": "08:30",
      "unread": 0,
      "status": "online"
    },
    {
      "id": "aragorn",
      "name": "Aragorn",
      "avatar": "👑",
      "description": "Re di Gondor",
      "lastMessage": "Il re ritorna",
      "time": "07:45",
      "unread": 3,
      "status": "online"
    }
  ],
  "total": 6,
  "timestamp": "2024-01-15T12:30:00Z"
};

// Struttura dei dati per ogni chat:
// - id: identificativo univoco del bot
// - name: nome visualizzato del bot
// - avatar: emoji o icona del bot
// - description: descrizione breve del bot
// - lastMessage: ultimo messaggio inviato dal bot
// - time: timestamp dell'ultimo messaggio (formato "HH:MM")
// - unread: numero di messaggi non letti
// - status: stato del bot ("online", "offline", "away")

// Esempio di implementazione in Express.js:
/*
app.get('/api/chats', async (req, res) => {
  try {
    // Recupera le chat dal database
    const chats = await Chat.find({}).sort({ lastMessageTime: -1 });
    
    // Formatta i dati per il frontend
    const formattedChats = chats.map(chat => ({
      id: chat.botId,
      name: chat.botName,
      avatar: chat.avatar,
      description: chat.description,
      lastMessage: chat.lastMessage,
      time: formatTime(chat.lastMessageTime),
      unread: chat.unreadCount,
      status: chat.status
    }));
    
    res.json({
      chats: formattedChats,
      total: formattedChats.length,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({ error: 'Errore nel recupero delle chat' });
  }
});

function formatTime(date) {
  return new Date(date).toLocaleTimeString('it-IT', { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
}
*/ 