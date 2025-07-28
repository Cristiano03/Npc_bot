import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from database import chat_db

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "openhermes"

class NPCManager:
    def __init__(self):
        pass  # Non serve più caricare da file JSON
    
    def get_npc(self, npc_id: str) -> Optional[Dict]:
        """Ottiene un NPC specifico per ID dal database"""
        return chat_db.get_npc_by_id(npc_id)
    
    def get_all_npcs(self) -> List[Dict]:
        """Ottiene tutti gli NPC dal database"""
        return chat_db.get_all_npcs()
    
    def update_npc_last_message(self, npc_id: str, message: str):
        """Aggiorna l'ultimo messaggio di un NPC nel database"""
        chat_db.update_npc_last_message(npc_id, message)
    
    def add_npc(self, npc_data: Dict) -> bool:
        """Aggiunge un nuovo NPC al database"""
        return chat_db.create_npc(npc_data)
    
    def update_npc(self, npc_id: str, npc_data: Dict) -> bool:
        """Aggiorna un NPC esistente nel database"""
        return chat_db.update_npc(npc_id, npc_data)
    
    def delete_npc(self, npc_id: str) -> bool:
        """Elimina un NPC dal database"""
        return chat_db.delete_npc(npc_id)

# Istanza globale del gestore NPC
npc_manager = NPCManager()

def query_ollama(user_input: str, npc_id: str = "aedryan", user_id: str = "default_user", include_history: bool = True) -> str:
    """Query Ollama con un NPC specifico e storico della conversazione"""
    npc = npc_manager.get_npc(npc_id)
    if not npc:
        return f"NPC {npc_id} non trovato."
    
    # Ottieni o crea la conversazione
    conversation_id = chat_db.get_or_create_conversation(npc_id, user_id)
    
    # Salva il messaggio dell'utente
    chat_db.add_message(conversation_id, "user", user_input)
    
    # Costruisci il prompt con il contesto storico
    base_prompt = npc['prompt']
    
    if include_history:
        # Ottieni il contesto della conversazione (ultimi 10 messaggi)
        conversation_context = chat_db.get_conversation_context(conversation_id, max_messages=10)
        
        if conversation_context:
            # Aggiungi il contesto al prompt
            full_prompt = f"{base_prompt}\n\n{conversation_context}\n\nAvventuriero: {user_input}\n{npc['name']}:"
        else:
            # Prima conversazione, usa solo il prompt base
            full_prompt = f"{base_prompt}\n\nAvventuriero: {user_input}\n{npc['name']}:"
    else:
        # Conversazione senza storico
        full_prompt = f"{base_prompt}\n\nAvventuriero: {user_input}\n{npc['name']}:"
    
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": full_prompt,
            "stream": False
        })
        data = response.json()
        reply = data.get("response", f"Non ho ricevuto risposta da {npc['name']}.")
        
        # Salva la risposta dell'NPC nel database
        chat_db.add_message(conversation_id, "npc", reply)
        
        # Aggiorna l'ultimo messaggio dell'NPC
        npc_manager.update_npc_last_message(npc_id, reply)
        
        return reply
    except Exception as e:
        error_msg = f"Errore nella comunicazione con {npc['name']}: {str(e)}"
        # Salva anche gli errori nel database
        chat_db.add_message(conversation_id, "npc", error_msg)
        return error_msg

def get_chats() -> Dict:
    """Ottiene la lista delle chat per il frontend"""
    npcs = npc_manager.get_all_npcs()
    return {
        "chats": npcs,
        "total": len(npcs),
        "timestamp": datetime.now().isoformat()
    }

def get_conversation_history(npc_id: str, user_id: str = "default_user", limit: int = 50) -> List[Dict]:
    """Ottiene lo storico di una conversazione specifica"""
    conversation_id = chat_db.get_or_create_conversation(npc_id, user_id)
    return chat_db.get_conversation_history(conversation_id, limit)

def get_user_conversations(user_id: str = "default_user", limit: int = 20) -> List[Dict]:
    """Ottiene tutte le conversazioni di un utente"""
    return chat_db.get_user_conversations(user_id, limit)

def delete_conversation(npc_id: str, user_id: str = "default_user") -> bool:
    """Elimina una conversazione"""
    conversation_id = chat_db.get_or_create_conversation(npc_id, user_id)
    return chat_db.delete_conversation(conversation_id)

def get_conversation_stats(npc_id: str = None) -> Dict:
    """Ottiene statistiche sulle conversazioni"""
    return chat_db.get_conversation_stats(npc_id)

# Funzione legacy per compatibilità
def query_ollama_legacy(user_input: str) -> str:
    """Funzione legacy per compatibilità con il codice esistente"""
    return query_ollama(user_input, "aedryan")
