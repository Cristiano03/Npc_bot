#!/usr/bin/env python3
"""
Script per importare NPC da file JSON nel database
"""

import json
import sys
import os
from database import chat_db
from shared import npc_manager

def import_npcs_from_json(json_file: str):
    """Importa NPC da un file JSON nel database"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        npcs = data.get('npcs', [])
        if not npcs:
            print("❌ Nessun NPC trovato nel file JSON!")
            return
        
        print(f"📁 Importando {len(npcs)} NPC da {json_file}...")
        
        imported = 0
        skipped = 0
        errors = 0
        
        for npc in npcs:
            try:
                # Verifica se l'NPC esiste già
                existing = npc_manager.get_npc(npc['id'])
                if existing:
                    print(f"⚠️  NPC '{npc['name']}' ({npc['id']}) già esistente, saltato.")
                    skipped += 1
                    continue
                
                # Prepara i dati per il database
                npc_data = {
                    "id": npc['id'],
                    "name": npc['name'],
                    "avatar": npc['avatar'],
                    "description": npc['description'],
                    "status": npc.get('status', 'online'),
                    "prompt": npc['prompt']
                }
                
                # Aggiungi l'NPC al database
                success = npc_manager.add_npc(npc_data)
                if success:
                    print(f"✅ Importato: {npc['avatar']} {npc['name']} ({npc['id']})")
                    imported += 1
                else:
                    print(f"❌ Errore nell'importazione di {npc['name']} ({npc['id']})")
                    errors += 1
                    
            except Exception as e:
                print(f"❌ Errore nell'importazione di {npc.get('name', 'Unknown')}: {str(e)}")
                errors += 1
        
        print(f"\n📊 RISULTATO IMPORT:")
        print(f"   ✅ Importati: {imported}")
        print(f"   ⚠️  Saltati: {skipped}")
        print(f"   ❌ Errori: {errors}")
        
    except FileNotFoundError:
        print(f"❌ File {json_file} non trovato!")
    except json.JSONDecodeError as e:
        print(f"❌ Errore nel parsing del JSON: {str(e)}")
    except Exception as e:
        print(f"❌ Errore generico: {str(e)}")

def export_npcs_to_json(json_file: str):
    """Esporta tutti gli NPC dal database a un file JSON"""
    try:
        npcs = npc_manager.get_all_npcs()
        if not npcs:
            print("❌ Nessun NPC trovato nel database!")
            return
        
        # Prepara i dati per l'export
        export_data = {"npcs": []}
        for npc in npcs:
            export_npc = {
                "id": npc['id'],
                "name": npc['name'],
                "avatar": npc['avatar'],
                "description": npc['description'],
                "status": npc['status'],
                "prompt": npc['prompt'],
                "lastMessage": npc['lastMessage'],
                "lastMessageTime": npc['lastMessageTime'],
                "unread": npc['unread']
            }
            export_data["npcs"].append(export_npc)
        
        # Salva nel file JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Esportati {len(npcs)} NPC in {json_file}")
        
    except Exception as e:
        print(f"❌ Errore nell'esportazione: {str(e)}")

def main():
    """Funzione principale"""
    print("=" * 60)
    print("📁 GESTORE IMPORT/EXPORT NPC")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python import_npcs.py import <file.json>  # Importa NPC da JSON")
        print("  python import_npcs.py export <file.json>  # Esporta NPC a JSON")
        print("  python import_npcs.py backup              # Backup automatico")
        return
    
    command = sys.argv[1].lower()
    
    if command == "import":
        if len(sys.argv) < 3:
            print("❌ Specifica il file JSON da importare!")
            return
        json_file = sys.argv[2]
        import_npcs_from_json(json_file)
        
    elif command == "export":
        if len(sys.argv) < 3:
            print("❌ Specifica il file JSON di destinazione!")
            return
        json_file = sys.argv[2]
        export_npcs_to_json(json_file)
        
    elif command == "backup":
        # Backup automatico con timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"npcs_backup_{timestamp}.json"
        export_npcs_to_json(backup_file)
        
    else:
        print(f"❌ Comando '{command}' non riconosciuto!")
        print("Comandi disponibili: import, export, backup")

if __name__ == "__main__":
    main() 