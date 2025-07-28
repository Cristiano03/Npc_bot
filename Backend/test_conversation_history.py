#!/usr/bin/env python3
"""
Test script per verificare il funzionamento dello storico delle conversazioni
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_conversation_history():
    """Test completo dello storico delle conversazioni"""
    print("🧪 Test dello storico delle conversazioni")
    print("=" * 50)
    
    # Test 1: Verifica che il server sia attivo
    print("\n1. Test connessione server...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ Server attivo")
        else:
            print("❌ Server non risponde correttamente")
            return False
    except Exception as e:
        print(f"❌ Errore di connessione: {e}")
        return False
    
    # Test 2: Ottieni la lista delle chat
    print("\n2. Test ottenimento chat...")
    try:
        response = requests.get(f"{BASE_URL}/api/chats")
        if response.status_code == 200:
            chats = response.json()
            print(f"✅ Trovate {len(chats.get('chats', []))} chat")
            npc_id = chats['chats'][0]['id'] if chats['chats'] else 'aedryan'
        else:
            print("❌ Errore nel recupero delle chat")
            return False
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False
    
    # Test 3: Invia alcuni messaggi di test
    print(f"\n3. Test invio messaggi a {npc_id}...")
    test_messages = [
        "Ciao! Come stai?",
        "Mi puoi raccontare qualcosa di te?",
        "Qual è la tua storia?",
        "Grazie per avermi parlato di te!"
    ]
    
    for i, message in enumerate(test_messages, 1):
        try:
            print(f"   Invio messaggio {i}: '{message}'")
            response = requests.post(f"{BASE_URL}/api/{npc_id}", json={
                "message": message,
                "user_id": "test_user",
                "include_history": True
            })
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Risposta ricevuta: {data['reply'][:50]}...")
            else:
                print(f"   ❌ Errore nella risposta: {response.status_code}")
                return False
                
            time.sleep(1)  # Pausa tra i messaggi
            
        except Exception as e:
            print(f"   ❌ Errore nell'invio: {e}")
            return False
    
    # Test 4: Verifica lo storico della conversazione
    print(f"\n4. Test recupero storico conversazione...")
    try:
        response = requests.get(f"{BASE_URL}/api/conversation/{npc_id}/history?user_id=test_user&limit=10")
        if response.status_code == 200:
            data = response.json()
            history = data.get('history', [])
            print(f"✅ Storico recuperato: {len(history)} messaggi")
            
            # Mostra i primi 3 messaggi
            for i, msg in enumerate(history[:3]):
                sender = "👤 Utente" if msg['sender'] == 'user' else "🤖 NPC"
                print(f"   {sender}: {msg['content'][:50]}...")
                
        else:
            print(f"❌ Errore nel recupero dello storico: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False
    
    # Test 5: Verifica le conversazioni dell'utente
    print(f"\n5. Test conversazioni utente...")
    try:
        response = requests.get(f"{BASE_URL}/api/user/test_user/conversations")
        if response.status_code == 200:
            data = response.json()
            conversations = data.get('conversations', [])
            print(f"✅ Trovate {len(conversations)} conversazioni per l'utente")
            
            for conv in conversations:
                print(f"   📝 {conv['npc_id']}: {conv['message_count']} messaggi")
                
        else:
            print(f"❌ Errore nel recupero delle conversazioni: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False
    
    # Test 6: Verifica statistiche
    print(f"\n6. Test statistiche...")
    try:
        response = requests.get(f"{BASE_URL}/api/conversations/stats")
        if response.status_code == 200:
            data = response.json()
            stats = data.get('stats', {})
            print(f"✅ Statistiche: {stats['total_conversations']} conversazioni totali")
            print(f"   📊 {stats['total_messages']} messaggi totali")
            print(f"   📈 Media: {stats['avg_messages']:.1f} messaggi per conversazione")
        else:
            print(f"❌ Errore nelle statistiche: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False
    
    # Test 7: Test conversazione senza storico
    print(f"\n7. Test conversazione senza storico...")
    try:
        response = requests.post(f"{BASE_URL}/api/{npc_id}", json={
            "message": "Questo è un test senza storico",
            "user_id": "test_user_no_history",
            "include_history": False
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Risposta senza storico: {data['reply'][:50]}...")
        else:
            print(f"❌ Errore: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Tutti i test completati con successo!")
    print("✅ Il sistema di storico delle conversazioni funziona correttamente")
    
    return True

def test_database_operations():
    """Test delle operazioni del database"""
    print("\n🔧 Test operazioni database...")
    print("=" * 30)
    
    try:
        from database import chat_db
        
        # Test creazione conversazione
        conv_id = chat_db.get_or_create_conversation("test_npc", "test_user")
        print(f"✅ Conversazione creata: ID {conv_id}")
        
        # Test aggiunta messaggi
        msg_id1 = chat_db.add_message(conv_id, "user", "Messaggio di test utente")
        msg_id2 = chat_db.add_message(conv_id, "npc", "Risposta di test NPC")
        print(f"✅ Messaggi aggiunti: {msg_id1}, {msg_id2}")
        
        # Test recupero storico
        history = chat_db.get_conversation_history(conv_id, limit=10)
        print(f"✅ Storico recuperato: {len(history)} messaggi")
        
        # Test contesto conversazione
        context = chat_db.get_conversation_context(conv_id, max_messages=5)
        print(f"✅ Contesto generato: {len(context)} caratteri")
        
        # Test statistiche
        stats = chat_db.get_conversation_stats("test_npc")
        print(f"✅ Statistiche: {stats}")
        
        # Pulizia
        chat_db.delete_conversation(conv_id)
        print("✅ Conversazione di test eliminata")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore nei test database: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Avvio test sistema storico conversazioni")
    print("Assicurati che il server sia in esecuzione su http://localhost:8000")
    print("e che Ollama sia attivo su http://localhost:11434")
    print()
    
    # Test database
    db_success = test_database_operations()
    
    # Test API
    api_success = test_conversation_history()
    
    if db_success and api_success:
        print("\n🎉 TUTTI I TEST SUPERATI!")
        print("Il sistema di storico delle conversazioni è pronto per l'uso.")
    else:
        print("\n❌ ALCUNI TEST FALLITI")
        print("Controlla i log per identificare i problemi.") 