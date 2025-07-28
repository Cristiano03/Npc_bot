# 🤖 NPC Bot - Backend

Sistema di chat con NPC intelligenti basato su database SQLite e Ollama.

## 📋 Caratteristiche

- **Database SQLite**: Gestione completa degli NPC e conversazioni
- **Memoria persistente**: Gli NPC ricordano le conversazioni precedenti
- **API RESTful**: Interfaccia completa per frontend e integrazioni
- **Gestione NPC**: Aggiunta, modifica, eliminazione degli NPC
- **Ollama Integration**: Utilizzo di modelli LLM locali
- **Statistiche**: Monitoraggio conversazioni e utilizzo

## 🗄️ Struttura Database

### Tabella `npcs`
- `id` (TEXT PRIMARY KEY): Identificativo univoco dell'NPC
- `name` (TEXT): Nome visualizzato dell'NPC
- `avatar` (TEXT): Emoji o simbolo dell'NPC
- `description` (TEXT): Descrizione breve
- `status` (TEXT): Stato online/offline
- `prompt` (TEXT): Prompt che definisce la personalità
- `last_message` (TEXT): Ultimo messaggio inviato
- `last_message_time` (TEXT): Timestamp ultimo messaggio
- `unread_count` (INTEGER): Contatore messaggi non letti
- `created_at` (TIMESTAMP): Data creazione
- `updated_at` (TIMESTAMP): Data ultimo aggiornamento

### Tabella `conversations`
- `id` (INTEGER PRIMARY KEY): ID conversazione
- `npc_id` (TEXT): Riferimento all'NPC
- `user_id` (TEXT): ID utente
- `title` (TEXT): Titolo conversazione
- `message_count` (INTEGER): Numero messaggi
- `created_at` (TIMESTAMP): Data creazione
- `updated_at` (TIMESTAMP): Data ultimo aggiornamento

### Tabella `messages`
- `id` (INTEGER PRIMARY KEY): ID messaggio
- `conversation_id` (INTEGER): Riferimento conversazione
- `sender` (TEXT): 'user' o 'npc'
- `content` (TEXT): Contenuto messaggio
- `timestamp` (TIMESTAMP): Data invio

## 🚀 Installazione

1. **Clona il repository**:
   ```bash
   git clone <repository-url>
   cd Npc_Bot/Backend
   ```

2. **Installa le dipendenze**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Avvia Ollama** (in un terminale separato):
   ```bash
   ollama serve
   ```

4. **Avvia il server**:
   ```bash
   python api_server.py
   ```

## 🛠️ Gestione NPC

### Interfaccia a Righe di Comando

Utilizza il gestore NPC integrato:

```bash
python npc_manager.py
```

**Funzionalità disponibili**:
- 📝 Aggiungi nuovo NPC
- 👁️ Visualizza tutti gli NPC
- 🔍 Cerca NPC per ID
- ✏️ Modifica NPC esistente
- 🗑️ Elimina NPC
- 📊 Statistiche sistema

### Import/Export

**Importa NPC da JSON**:
```bash
python import_npcs.py import npcs.json
```

**Esporta NPC a JSON**:
```bash
python import_npcs.py export backup.json
```

**Backup automatico**:
```bash
python import_npcs.py backup
```

### Esempio di Creazione NPC

```python
from shared import npc_manager

npc_data = {
    "id": "merlin",
    "name": "Merlin il Mago",
    "avatar": "🔮",
    "description": "Mago potente e saggio",
    "status": "online",
    "prompt": "Tu sei Merlin, un mago potente e saggio..."
}

success = npc_manager.add_npc(npc_data)
```

## 🌐 API Endpoints

### NPC Management

- `GET /api/npcs` - Lista tutti gli NPC
- `GET /api/npc/{npc_id}` - Dettagli NPC specifico
- `POST /api/npc` - Crea nuovo NPC
- `PUT /api/npc/{npc_id}` - Aggiorna NPC
- `DELETE /api/npc/{npc_id}` - Elimina NPC

### Chat

- `GET /api/chats` - Lista chat disponibili
- `POST /api/{npc_id}` - Invia messaggio a NPC
- `GET /api/conversation/{npc_id}/history` - Storico conversazione

### Statistiche

- `GET /api/stats` - Statistiche generali
- `GET /api/conversations/stats` - Statistiche conversazioni
- `GET /api/health` - Health check

## 💬 Esempio di Utilizzo API

### Invia messaggio a NPC

```bash
curl -X POST "http://localhost:8000/api/aedryan" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Ciao Re Aedryan, come stai?",
    "user_id": "user123",
    "include_history": true
  }'
```

### Ottieni storico conversazione

```bash
curl "http://localhost:8000/api/conversation/aedryan/history?user_id=user123&limit=10"
```

### Aggiungi nuovo NPC via API

```bash
curl -X POST "http://localhost:8000/api/npc" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "gandalf",
    "name": "Gandalf il Grigio",
    "avatar": "🧙‍♂️",
    "description": "Mago Istari",
    "status": "online",
    "prompt": "Tu sei Gandalf il Grigio..."
  }'
```

## 🔧 Configurazione

### Variabili d'Ambiente

- `OLLAMA_URL`: URL server Ollama (default: `http://localhost:11434/api/generate`)
- `OLLAMA_MODEL`: Modello LLM da utilizzare (default: `openhermes`)

### Database

Il database SQLite viene creato automaticamente al primo avvio. Per reimpostare:

```bash
rm chat_history.db
python api_server.py
```

## 📊 Monitoraggio

### Statistiche Disponibili

- **NPC**: Totale, online, offline, messaggi non letti
- **Conversazioni**: Totale, messaggi totali, media per conversazione
- **Performance**: Tempo di risposta, errori

### Log

Il sistema registra automaticamente:
- Creazione/modifica NPC
- Conversazioni e messaggi
- Errori e eccezioni
- Statistiche utilizzo

## 🔒 Sicurezza

- **Validazione input**: Tutti gli input vengono validati
- **SQL Injection**: Prevenuto tramite prepared statements
- **CORS**: Configurato per frontend specifico
- **Rate Limiting**: Implementabile tramite middleware

## 🧪 Testing

### Test API

```bash
python test_api.py
```

### Test Conversazioni

```bash
python test_conversation_history.py
```

## 📝 Esempi NPC

### Re Aedryan (Default)
- **ID**: `aedryan`
- **Ruolo**: Re decadente di Virelund
- **Personalità**: Regale, amareggiato, determinato

### Thorin (Default)
- **ID**: `thorin`
- **Ruolo**: Guerriero coraggioso
- **Personalità**: Determinato, coraggioso, esperto

### Elara (Default)
- **ID**: `elara`
- **Ruolo**: Ranger elfica
- **Personalità**: Graziosa, saggia, connessa alla natura

## 🚨 Risoluzione Problemi

### Ollama non raggiungibile
```bash
# Verifica che Ollama sia in esecuzione
ollama list
ollama serve
```

### Database corrotto
```bash
# Backup e ricreazione
python import_npcs.py backup
rm chat_history.db
python api_server.py
```

### NPC non trovato
```bash
# Verifica NPC nel database
python npc_manager.py
# Scegli opzione 2 per visualizzare tutti gli NPC
```

## 📞 Supporto

Per problemi o domande:
1. Controlla i log del server
2. Verifica la connessione a Ollama
3. Controlla la struttura del database
4. Consulta questo README

## 🔄 Changelog

### v2.0 - Database Migration
- ✅ Migrazione da JSON a SQLite
- ✅ Gestione NPC completa
- ✅ Interfaccia CLI per gestione
- ✅ Import/Export funzionalità
- ✅ API endpoints aggiornati
- ✅ Statistiche avanzate

### v1.0 - Initial Release
- ✅ Sistema base con JSON
- ✅ Integrazione Ollama
- ✅ API RESTful
- ✅ Frontend React 