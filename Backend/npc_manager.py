#!/usr/bin/env python3
"""
Gestore NPC - Interfaccia per gestire gli NPC nel database
"""

import sys
import os
from database import chat_db
from shared import npc_manager

def print_header():
    """Stampa l'intestazione del programma"""
    print("=" * 60)
    print("🤖 GESTORE NPC - Database Management")
    print("=" * 60)

def print_menu():
    """Stampa il menu principale"""
    print("\n📋 MENU PRINCIPALE:")
    print("1. 📝 Aggiungi nuovo NPC")
    print("2. 👁️  Visualizza tutti gli NPC")
    print("3. 🔍 Cerca NPC per ID")
    print("4. ✏️  Modifica NPC")
    print("5. 🗑️  Elimina NPC")
    print("6. 📊 Statistiche")
    print("7. ❌ Esci")
    print("-" * 40)

def get_user_input(prompt: str, required: bool = True) -> str:
    """Ottiene input dall'utente con validazione"""
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("❌ Campo obbligatorio!")

def add_npc():
    """Aggiunge un nuovo NPC"""
    print("\n📝 AGGIUNGI NUOVO NPC")
    print("-" * 30)
    
    # Raccogli i dati dell'NPC
    npc_id = get_user_input("ID NPC (es. merlin): ")
    
    # Verifica se l'NPC esiste già
    existing_npc = npc_manager.get_npc(npc_id)
    if existing_npc:
        print(f"❌ NPC con ID '{npc_id}' esiste già!")
        return
    
    name = get_user_input("Nome (es. Merlin il Mago): ")
    avatar = get_user_input("Avatar (emoji, es. 🔮): ")
    description = get_user_input("Descrizione: ")
    status = get_user_input("Status (online/offline) [default: online]: ") or "online"
    
    print("\n📝 PROMPT DELL'NPC:")
    print("Inserisci il prompt che definisce la personalità dell'NPC.")
    print("Esempio: 'Tu sei Merlin, un mago potente e saggio...'")
    print("Premi Ctrl+D (Linux/Mac) o Ctrl+Z (Windows) quando hai finito:")
    
    prompt_lines = []
    try:
        while True:
            line = input()
            prompt_lines.append(line)
    except (EOFError, KeyboardInterrupt):
        pass
    
    prompt = "\n".join(prompt_lines)
    
    if not prompt.strip():
        print("❌ Il prompt non può essere vuoto!")
        return
    
    # Crea l'NPC
    npc_data = {
        "id": npc_id,
        "name": name,
        "avatar": avatar,
        "description": description,
        "status": status,
        "prompt": prompt
    }
    
    success = npc_manager.add_npc(npc_data)
    if success:
        print(f"✅ NPC '{name}' aggiunto con successo!")
    else:
        print("❌ Errore nell'aggiunta dell'NPC!")

def list_npcs():
    """Visualizza tutti gli NPC"""
    print("\n👁️  TUTTI GLI NPC")
    print("-" * 30)
    
    npcs = npc_manager.get_all_npcs()
    if not npcs:
        print("📭 Nessun NPC trovato nel database.")
        return
    
    for i, npc in enumerate(npcs, 1):
        print(f"\n{i}. {npc['avatar']} {npc['name']} ({npc['id']})")
        print(f"   📝 {npc['description']}")
        print(f"   🟢 Status: {npc['status']}")
        print(f"   💬 Ultimo messaggio: {npc['lastMessage'][:50]}..." if npc['lastMessage'] else "   💬 Nessun messaggio")
        print(f"   📅 Creato: {npc['created_at']}")

def search_npc():
    """Cerca un NPC per ID"""
    print("\n🔍 CERCA NPC")
    print("-" * 20)
    
    npc_id = get_user_input("Inserisci l'ID dell'NPC: ")
    npc = npc_manager.get_npc(npc_id)
    
    if not npc:
        print(f"❌ NPC con ID '{npc_id}' non trovato!")
        return
    
    print(f"\n✅ NPC TROVATO:")
    print(f"   🆔 ID: {npc['id']}")
    print(f"   👤 Nome: {npc['avatar']} {npc['name']}")
    print(f"   📝 Descrizione: {npc['description']}")
    print(f"   🟢 Status: {npc['status']}")
    print(f"   💬 Ultimo messaggio: {npc['lastMessage']}")
    print(f"   📅 Creato: {npc['created_at']}")
    print(f"   📅 Aggiornato: {npc['updated_at']}")
    print(f"\n📝 PROMPT:")
    print("-" * 40)
    print(npc['prompt'])

def edit_npc():
    """Modifica un NPC esistente"""
    print("\n✏️  MODIFICA NPC")
    print("-" * 25)
    
    npc_id = get_user_input("Inserisci l'ID dell'NPC da modificare: ")
    npc = npc_manager.get_npc(npc_id)
    
    if not npc:
        print(f"❌ NPC con ID '{npc_id}' non trovato!")
        return
    
    print(f"\n📝 Modificando NPC: {npc['name']}")
    print("Lascia vuoto per mantenere il valore attuale.")
    
    name = get_user_input(f"Nome [{npc['name']}]: ", required=False) or npc['name']
    avatar = get_user_input(f"Avatar [{npc['avatar']}]: ", required=False) or npc['avatar']
    description = get_user_input(f"Descrizione [{npc['description']}]: ", required=False) or npc['description']
    status = get_user_input(f"Status [{npc['status']}]: ", required=False) or npc['status']
    
    print(f"\n📝 PROMPT ATTUALI:")
    print("-" * 40)
    print(npc['prompt'])
    print("-" * 40)
    
    change_prompt = get_user_input("Vuoi modificare il prompt? (s/n): ", required=False).lower()
    
    if change_prompt in ['s', 'si', 'y', 'yes']:
        print("Inserisci il nuovo prompt. Premi Ctrl+D (Linux/Mac) o Ctrl+Z (Windows) quando hai finito:")
        prompt_lines = []
        try:
            while True:
                line = input()
                prompt_lines.append(line)
        except (EOFError, KeyboardInterrupt):
            pass
        
        prompt = "\n".join(prompt_lines)
        if not prompt.strip():
            print("❌ Il prompt non può essere vuoto! Mantenuto quello attuale.")
            prompt = npc['prompt']
    else:
        prompt = npc['prompt']
    
    # Aggiorna l'NPC
    npc_data = {
        "id": npc_id,
        "name": name,
        "avatar": avatar,
        "description": description,
        "status": status,
        "prompt": prompt
    }
    
    success = npc_manager.update_npc(npc_id, npc_data)
    if success:
        print(f"✅ NPC '{name}' aggiornato con successo!")
    else:
        print("❌ Errore nell'aggiornamento dell'NPC!")

def delete_npc():
    """Elimina un NPC"""
    print("\n🗑️  ELIMINA NPC")
    print("-" * 20)
    
    npc_id = get_user_input("Inserisci l'ID dell'NPC da eliminare: ")
    npc = npc_manager.get_npc(npc_id)
    
    if not npc:
        print(f"❌ NPC con ID '{npc_id}' non trovato!")
        return
    
    print(f"\n⚠️  STAI PER ELIMINARE:")
    print(f"   👤 {npc['avatar']} {npc['name']} ({npc['id']})")
    print(f"   📝 {npc['description']}")
    
    confirm = get_user_input("Sei sicuro? Questa azione eliminerà anche tutte le conversazioni! (s/n): ").lower()
    
    if confirm in ['s', 'si', 'y', 'yes']:
        success = npc_manager.delete_npc(npc_id)
        if success:
            print(f"✅ NPC '{npc['name']}' eliminato con successo!")
        else:
            print("❌ Errore nell'eliminazione dell'NPC!")
    else:
        print("❌ Operazione annullata.")

def show_stats():
    """Mostra le statistiche"""
    print("\n📊 STATISTICHE")
    print("-" * 20)
    
    npcs = npc_manager.get_all_npcs()
    online_count = sum(1 for npc in npcs if npc.get("status") == "online")
    total_unread = sum(npc.get("unread", 0) for npc in npcs)
    
    # Statistiche conversazioni
    conv_stats = chat_db.get_conversation_stats()
    
    print(f"🤖 NPC Totali: {len(npcs)}")
    print(f"🟢 Online: {online_count}")
    print(f"🔴 Offline: {len(npcs) - online_count}")
    print(f"📬 Messaggi non letti: {total_unread}")
    print(f"\n💬 CONVERSAZIONI:")
    print(f"   📊 Totali: {conv_stats['total_conversations']}")
    print(f"   💭 Messaggi totali: {conv_stats['total_messages']}")
    print(f"   📈 Media messaggi per conversazione: {conv_stats['avg_messages']:.1f}")

def main():
    """Funzione principale"""
    print_header()
    
    while True:
        print_menu()
        choice = get_user_input("Scelta: ")
        
        if choice == "1":
            add_npc()
        elif choice == "2":
            list_npcs()
        elif choice == "3":
            search_npc()
        elif choice == "4":
            edit_npc()
        elif choice == "5":
            delete_npc()
        elif choice == "6":
            show_stats()
        elif choice == "7":
            print("\n👋 Arrivederci!")
            break
        else:
            print("❌ Scelta non valida!")
        
        input("\nPremi INVIO per continuare...")

if __name__ == "__main__":
    main() 