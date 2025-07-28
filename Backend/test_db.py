#!/usr/bin/env python3
"""
Test semplice per verificare il database
"""

from database import chat_db

def test_database():
    print("🧪 Test Database NPC")
    print("=" * 40)
    
    # Test inizializzazione
    print("✅ Database inizializzato")
    
    # Test recupero NPC
    npcs = chat_db.get_all_npcs()
    print(f"📊 NPC trovati: {len(npcs)}")
    
    for npc in npcs:
        print(f"   - {npc['avatar']} {npc['name']} ({npc['id']})")
        print(f"     📝 {npc['description']}")
    
    # Test ricerca NPC specifico
    aedryan = chat_db.get_npc_by_id("aedryan")
    if aedryan:
        print(f"\n✅ Re Aedryan trovato: {aedryan['name']}")
    else:
        print("\n❌ Re Aedryan non trovato!")
    
    print("\n🎉 Test completato!")

if __name__ == "__main__":
    test_database() 