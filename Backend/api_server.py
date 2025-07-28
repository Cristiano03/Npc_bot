from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from shared import (
    query_ollama, get_chats, npc_manager, 
    get_conversation_history, get_user_conversations,
    delete_conversation, get_conversation_stats
)
from typing import Dict, List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # solo il front-end in dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    message: str
    user_id: str = "default_user"
    include_history: bool = True

class NPCData(BaseModel):
    id: str
    name: str
    avatar: str
    description: str
    status: str = "online"
    prompt: str
    lastMessage: str = ""
    lastMessageTime: str = ""
    unread: int = 0

# Endpoint per ottenere la lista delle chat
@app.get("/api/chats")
def get_chats_endpoint():
    """Ottiene la lista di tutte le chat disponibili"""
    return get_chats()

# Endpoint per parlare con un NPC specifico
@app.post("/api/{npc_id}")
def talk_to_npc(npc_id: str, data: UserInput):
    """Parla con un NPC specifico con supporto per lo storico"""
    try:
        reply = query_ollama(
            data.message, 
            npc_id, 
            data.user_id, 
            data.include_history
        )
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nella comunicazione con l'NPC: {str(e)}")

# Endpoint legacy per compatibilità
@app.post("/api/aedryan")
def talk_to_king(data: UserInput):
    """Endpoint legacy per Re Aedryan"""
    return talk_to_npc("aedryan", data)

# Endpoint per ottenere un NPC specifico
@app.get("/api/npc/{npc_id}")
def get_npc(npc_id: str):
    """Ottiene i dati di un NPC specifico"""
    npc = npc_manager.get_npc(npc_id)
    if not npc:
        raise HTTPException(status_code=404, detail="NPC non trovato")
    return npc

# Endpoint per aggiungere un nuovo NPC
@app.post("/api/npc")
def add_npc(npc_data: NPCData):
    """Aggiunge un nuovo NPC"""
    success = npc_manager.add_npc(npc_data.dict())
    if not success:
        raise HTTPException(status_code=400, detail="NPC già esistente o dati non validi")
    return {"message": "NPC aggiunto con successo", "npc": npc_data.dict()}

# Endpoint per aggiornare un NPC
@app.put("/api/npc/{npc_id}")
def update_npc(npc_id: str, npc_data: NPCData):
    """Aggiorna un NPC esistente"""
    if npc_id != npc_data.id:
        raise HTTPException(status_code=400, detail="ID non corrispondente")
    
    success = npc_manager.update_npc(npc_id, npc_data.dict())
    if not success:
        raise HTTPException(status_code=404, detail="NPC non trovato")
    return {"message": "NPC aggiornato con successo", "npc": npc_data.dict()}

# Endpoint per eliminare un NPC
@app.delete("/api/npc/{npc_id}")
def delete_npc(npc_id: str):
    """Elimina un NPC"""
    success = npc_manager.delete_npc(npc_id)
    if not success:
        raise HTTPException(status_code=404, detail="NPC non trovato")
    return {"message": "NPC eliminato con successo"}

# Endpoint per ottenere tutti gli NPC
@app.get("/api/npcs")
def get_all_npcs():
    """Ottiene tutti gli NPC dal database"""
    try:
        npcs = npc_manager.get_all_npcs()
        return {
            "npcs": npcs,
            "total": len(npcs),
            "timestamp": get_chats()["timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nel recupero degli NPC: {str(e)}")

# Endpoint per ottenere lo storico di una conversazione
@app.get("/api/conversation/{npc_id}/history")
def get_conversation_history_endpoint(
    npc_id: str, 
    user_id: str = "default_user", 
    limit: int = 50
):
    """Ottiene lo storico di una conversazione specifica"""
    try:
        history = get_conversation_history(npc_id, user_id, limit)
        return {
            "npc_id": npc_id,
            "user_id": user_id,
            "history": history,
            "total_messages": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nel recupero dello storico: {str(e)}")

# Endpoint per ottenere tutte le conversazioni di un utente
@app.get("/api/user/{user_id}/conversations")
def get_user_conversations_endpoint(user_id: str, limit: int = 20):
    """Ottiene tutte le conversazioni di un utente"""
    try:
        conversations = get_user_conversations(user_id, limit)
        return {
            "user_id": user_id,
            "conversations": conversations,
            "total": len(conversations)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nel recupero delle conversazioni: {str(e)}")

# Endpoint per eliminare una conversazione
@app.delete("/api/conversation/{npc_id}")
def delete_conversation_endpoint(npc_id: str, user_id: str = "default_user"):
    """Elimina una conversazione specifica"""
    try:
        success = delete_conversation(npc_id, user_id)
        if success:
            return {"message": "Conversazione eliminata con successo"}
        else:
            raise HTTPException(status_code=404, detail="Conversazione non trovata")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nell'eliminazione della conversazione: {str(e)}")

# Endpoint per ottenere statistiche sulle conversazioni
@app.get("/api/conversations/stats")
def get_conversation_stats_endpoint(npc_id: str = None):
    """Ottiene statistiche sulle conversazioni"""
    try:
        stats = get_conversation_stats(npc_id)
        return {
            "npc_id": npc_id,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nel recupero delle statistiche: {str(e)}")

# Endpoint per ottenere statistiche
@app.get("/api/stats")
def get_stats():
    """Ottiene statistiche sugli NPC e conversazioni"""
    npcs = npc_manager.get_all_npcs()
    online_count = sum(1 for npc in npcs if npc.get("status") == "online")
    total_unread = sum(npc.get("unread", 0) for npc in npcs)
    
    # Statistiche conversazioni
    conv_stats = get_conversation_stats()
    
    return {
        "npcs": {
            "total_npcs": len(npcs),
            "online_npcs": online_count,
            "offline_npcs": len(npcs) - online_count,
            "total_unread": total_unread
        },
        "conversations": conv_stats,
        "timestamp": get_chats()["timestamp"]
    }

# Endpoint di health check
@app.get("/api/health")
def health_check():
    """Health check dell'API"""
    return {
        "status": "healthy",
        "npcs_loaded": len(npc_manager.get_all_npcs()),
        "timestamp": get_chats()["timestamp"]
    }
