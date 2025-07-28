# 🤖 NPC Bot - Chat Intelligente con NPC

Un sistema di chat avanzato con NPC (Non-Player Characters) intelligenti, basato su database SQLite e modelli LLM locali tramite Ollama.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![React](https://img.shields.io/badge/React-18+-61dafb.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3.0+-yellow.svg)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-orange.svg)

## 🌟 Caratteristiche

- **🤖 NPC Intelligenti**: Personaggi con personalità uniche e memoria persistente
- **💾 Database SQLite**: Gestione completa di NPC e conversazioni
- **🧠 Memoria**: Gli NPC ricordano le conversazioni precedenti
- **🎨 Frontend Moderno**: Interfaccia WhatsApp-style con tema scuro
- **🔧 Gestione Completa**: Aggiunta, modifica, eliminazione NPC via CLI
- **🌐 API RESTful**: Interfaccia completa per integrazioni
- **📊 Statistiche**: Monitoraggio conversazioni e utilizzo
- **🛡️ Sicuro**: Validazione input e protezione SQL injection

## 📁 Struttura Progetto

```
Npc_Bot/
├── Backend/                 # Server FastAPI + Database
│   ├── api_server.py       # Server API principale
│   ├── database.py         # Gestione database SQLite
│   ├── shared.py           # Logica condivisa
│   ├── npc_manager.py      # CLI per gestione NPC
│   ├── import_npcs.py      # Import/Export NPC
│   ├── test_*.py           # Test suite
│   └── requirements.txt    # Dipendenze Python
├── FrontEnd/               # Client React
│   ├── src/
│   │   ├── ChatApp.jsx     # Componente principale
│   │   ├── Sidebar.jsx     # Barra laterale chat
│   │   └── App.css         # Stili
│   ├── package.json        # Dipendenze Node.js
│   └── vite.config.js      # Configurazione Vite
└── README.md              # Questo file
```

## 🚀 Installazione Rapida

### Prerequisiti

- **Python 3.8+**
- **Node.js 16+**
- **Ollama** (per modelli LLM locali)

### 1. Clona la Repository

```bash
git clone https://github.com/tuousername/Npc_Bot.git
cd Npc_Bot
```

### 2. Setup Backend

```bash
cd Backend
pip install -r requirements.txt
```

### 3. Setup Frontend

```bash
cd FrontEnd
npm install
```

### 4. Avvia Ollama

```bash
# In un terminale separato
ollama serve
```

### 5. Avvia il Sistema

```bash
# Terminale 1: Backend
cd Backend
python api_server.py

# Terminale 2: Frontend
cd FrontEnd
npm run dev
```

## 🎮 Utilizzo

### Interfaccia Web

1. Apri `http://localhost:5173` nel browser
2. Seleziona un NPC dalla barra laterale
3. Inizia a chattare!

### Gestione NPC via CLI

```bash
cd Backend
python npc_manager.py
```

**Opzioni disponibili**:
- 📝 Aggiungi nuovo NPC
- 👁️ Visualizza tutti gli NPC
- 🔍 Cerca NPC per ID
- ✏️ Modifica NPC esistente
- 🗑️ Elimina NPC
- 📊 Statistiche sistema

### API REST

```bash
# Lista NPC
curl http://localhost:8000/api/chats

# Invia messaggio
curl -X POST http://localhost:8000/api/aedryan \
  -H "Content-Type: application/json" \
  -d '{"message": "Ciao!", "user_id": "user123"}'

# Storico conversazione
curl http://localhost:8000/api/conversation/aedryan/history
```

## 🤖 NPC Predefiniti

### 👑 Re Aedryan
- **Ruolo**: Re decadente di Virelund
- **Personalità**: Regale, amareggiato, determinato
- **Storia**: Lotta per salvare il suo regno dalla pestilenza

### ⚔️ Thorin
- **Ruolo**: Guerriero coraggioso
- **Personalità**: Determinato, coraggioso, esperto
- **Storia**: Combattente esperto con molte battaglie alle spalle

### 🏹 Elara
- **Ruolo**: Ranger elfica
- **Personalità**: Graziosa, saggia, connessa alla natura
- **Storia**: Protettrice delle foreste e delle creature

## 🛠️ Sviluppo

### Aggiungere Nuovi NPC

#### Via CLI (Raccomandato)
```bash
cd Backend
python npc_manager.py
# Scegli opzione 1
```

#### Via API
```bash
curl -X POST http://localhost:8000/api/npc \
  -H "Content-Type: application/json" \
  -d '{
    "id": "gandalf",
    "name": "Gandalf il Grigio",
    "avatar": "🧙‍♂️",
    "description": "Mago Istari",
    "prompt": "Tu sei Gandalf il Grigio..."
  }'
```

### Struttura Prompt NPC

```python
prompt = """
Tu sei [Nome NPC], [descrizione ruolo].

[Background e storia del personaggio]

[Personalità e caratteristiche]

[Istruzioni per il comportamento]

Quando i personaggi ti parlano, rispondi come [Nome NPC].
Mantieni coerenza emotiva e narrativa.
"""
```

## 📊 Database Schema

### Tabella `npcs`
- `id` (TEXT PRIMARY KEY): Identificativo univoco
- `name` (TEXT): Nome visualizzato
- `avatar` (TEXT): Emoji o simbolo
- `description` (TEXT): Descrizione breve
- `prompt` (TEXT): Prompt che definisce la personalità
- `status` (TEXT): Stato online/offline
- `last_message` (TEXT): Ultimo messaggio
- `created_at` (TIMESTAMP): Data creazione

### Tabella `conversations`
- `id` (INTEGER PRIMARY KEY): ID conversazione
- `npc_id` (TEXT): Riferimento all'NPC
- `user_id` (TEXT): ID utente
- `message_count` (INTEGER): Numero messaggi
- `created_at` (TIMESTAMP): Data creazione

### Tabella `messages`
- `id` (INTEGER PRIMARY KEY): ID messaggio
- `conversation_id` (INTEGER): Riferimento conversazione
- `sender` (TEXT): 'user' o 'npc'
- `content` (TEXT): Contenuto messaggio
- `timestamp` (TIMESTAMP): Data invio

## 🔧 Configurazione

### Variabili d'Ambiente

```bash
# Backend
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=openhermes
DISCORD_TOKEN=your_discord_token_here  # Solo se usi il bot Discord

# Frontend
VITE_API_URL=http://localhost:8000
```

#### Configurazione Discord Bot (Opzionale)
Se vuoi usare il bot Discord:

1. Crea un'applicazione su [Discord Developer Portal](https://discord.com/developers/applications)
2. Crea un bot e ottieni il token
3. Imposta la variabile d'ambiente:
   ```bash
   export DISCORD_TOKEN=your_token_here
   ```
4. Avvia il bot:
   ```bash
   cd Backend
   python discord_bot.py
   ```

### Modelli Ollama Supportati

- `openhermes` (raccomandato)
- `llama2`
- `mistral`
- `codellama`
- Qualsiasi modello compatibile con Ollama

## 🧪 Testing

```bash
# Test Backend
cd Backend
python test_api.py
python test_conversation_history.py
python test_db.py

# Test Frontend
cd FrontEnd
npm test
```

## 🚨 Troubleshooting

### Ollama non raggiungibile
```bash
# Verifica che Ollama sia in esecuzione
ollama list
ollama serve
```

### Database corrotto
```bash
cd Backend
python import_npcs.py backup
rm chat_history.db
python api_server.py
```

### Frontend non si connette
```bash
# Verifica che il backend sia in esecuzione
curl http://localhost:8000/api/health
```

## 🤝 Contribuire

1. **Fork** la repository
2. **Crea** un branch per la feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** le modifiche (`git commit -m 'Add AmazingFeature'`)
4. **Push** al branch (`git push origin feature/AmazingFeature`)
5. **Apri** una Pull Request

### Linee Guida

- Segui le convenzioni di codice esistenti
- Aggiungi test per nuove funzionalità
- Aggiorna la documentazione
- Mantieni la compatibilità con l'API esistente

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.

## 🙏 Ringraziamenti

- **Ollama** per i modelli LLM locali
- **FastAPI** per il framework backend
- **React** per il framework frontend
- **SQLite** per il database leggero

## 📞 Supporto

- **Issues**: [GitHub Issues](https://github.com/tuousername/Npc_Bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tuousername/Npc_Bot/discussions)
- **Wiki**: [Documentazione Dettagliata](https://github.com/tuousername/Npc_Bot/wiki)

---

⭐ **Se questo progetto ti è utile, considera di dargli una stella su GitHub!** 