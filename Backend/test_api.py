#!/usr/bin/env python3
"""
Test script per verificare il funzionamento del sistema NPC
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testando health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check OK - NPC caricati: {data['npcs_loaded']}")
            return True
        else:
            print(f"❌ Health check fallito: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Errore health check: {e}")
        return False

def test_get_chats():
    """Test endpoint per ottenere le chat"""
    print("🔍 Testando get chats...")
    try:
        response = requests.get(f"{BASE_URL}/api/chats")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Get chats OK - {data['total']} chat trovate")
            for chat in data['chats'][:3]:  # Mostra solo i primi 3
                print(f"   - {chat['name']} ({chat['id']})")
            return True
        else:
            print(f"❌ Get chats fallito: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Errore get chats: {e}")
        return False

def test_talk_to_npc(npc_id="aedryan"):
    """Test conversazione con un NPC"""
    print(f"🔍 Testando conversazione con {npc_id}...")
    try:
        message = "Ciao! Come stai oggi?"
        response = requests.post(f"{BASE_URL}/api/{npc_id}", 
                               json={"message": message})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Conversazione OK")
            print(f"   Messaggio: {message}")
            print(f"   Risposta: {data['reply'][:100]}...")
            return True
        else:
            print(f"❌ Conversazione fallita: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Errore conversazione: {e}")
        return False

def test_get_npc(npc_id="aedryan"):
    """Test ottenere dati di un NPC specifico"""
    print(f"🔍 Testando get NPC {npc_id}...")
    try:
        response = requests.get(f"{BASE_URL}/api/npc/{npc_id}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Get NPC OK - {data['name']} ({data['status']})")
            return True
        else:
            print(f"❌ Get NPC fallito: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Errore get NPC: {e}")
        return False

def test_stats():
    """Test endpoint statistiche"""
    print("🔍 Testando statistiche...")
    try:
        response = requests.get(f"{BASE_URL}/api/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Stats OK")
            print(f"   - NPC totali: {data['total_npcs']}")
            print(f"   - Online: {data['online_npcs']}")
            print(f"   - Offline: {data['offline_npcs']}")
            print(f"   - Messaggi non letti: {data['total_unread']}")
            return True
        else:
            print(f"❌ Stats fallito: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Errore stats: {e}")
        return False

def test_reload_npcs():
    """Test ricaricamento NPC"""
    print("🔍 Testando reload NPC...")
    try:
        response = requests.post(f"{BASE_URL}/api/reload-npcs")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Reload NPC OK - {data['count']} NPC ricaricati")
            return True
        else:
            print(f"❌ Reload NPC fallito: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Errore reload NPC: {e}")
        return False

def main():
    """Esegue tutti i test"""
    print("🚀 Avvio test del sistema NPC...")
    print("=" * 50)
    
    tests = [
        test_health_check,
        test_get_chats,
        test_get_npc,
        test_talk_to_npc,
        test_stats,
        test_reload_npcs
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test fallito con eccezione: {e}")
        print()
        time.sleep(0.5)  # Pausa tra i test
    
    print("=" * 50)
    print(f"📊 Risultati: {passed}/{total} test superati")
    
    if passed == total:
        print("🎉 Tutti i test sono stati superati!")
        return True
    else:
        print("⚠️  Alcuni test sono falliti. Controlla il server.")
        return False

if __name__ == "__main__":
    main() 