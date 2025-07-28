# 📋 Changelog

Tutte le modifiche notevoli a questo progetto saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e questo progetto aderisce al [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Sistema di gestione NPC via CLI
- Import/Export NPC da JSON
- Statistiche avanzate del sistema
- Documentazione completa

### Changed
- Migrazione da JSON a database SQLite
- Ristrutturazione completa del backend
- Aggiornamento API endpoints

### Fixed
- Problemi di memoria conversazioni
- Bug nella gestione NPC
- Errori di connessione database

## [2.0.0] - 2024-01-XX

### Added
- **Database SQLite**: Gestione completa di NPC e conversazioni
- **Tabella NPC**: Storage persistente per tutti gli NPC
- **Gestione CLI**: Interfaccia a riga di comando per gestire NPC
- **Import/Export**: Script per migrazione da JSON a database
- **API Aggiornate**: Nuovi endpoint per gestione NPC
- **Statistiche Avanzate**: Monitoraggio completo del sistema
- **Documentazione**: README completo e guide dettagliate

### Changed
- **Architettura**: Migrazione completa da file JSON a database SQLite
- **NPCManager**: Riscritto per utilizzare il database
- **API Server**: Aggiornato con nuovi endpoint
- **Database Schema**: Nuova tabella `npcs` con relazioni
- **Gestione Memoria**: Sistema migliorato per conversazioni

### Removed
- **File JSON**: `npcs.json` non più necessario
- **Reload Endpoint**: `/api/reload-npcs` rimosso
- **Gestione File**: Logica di caricamento da file JSON

### Fixed
- **Memoria Conversazioni**: Risolto problema persistenza
- **Gestione Errori**: Migliorata gestione errori database
- **Performance**: Ottimizzazioni query database
- **Sicurezza**: Prepared statements per prevenire SQL injection

## [1.0.0] - 2024-01-XX

### Added
- **Sistema Base**: Chat con NPC intelligenti
- **Integrazione Ollama**: Supporto modelli LLM locali
- **Frontend React**: Interfaccia WhatsApp-style
- **API RESTful**: Endpoint completi per comunicazione
- **Gestione Conversazioni**: Sistema di memoria per chat
- **Database SQLite**: Storage per messaggi e conversazioni
- **NPC Predefiniti**: Re Aedryan, Thorin, Elara
- **Sistema di Test**: Test suite per API e funzionalità

### Features
- Chat in tempo reale con NPC
- Memoria delle conversazioni precedenti
- Interfaccia utente moderna e responsive
- API completa per integrazioni
- Sistema di autenticazione utenti
- Statistiche di utilizzo
- Gestione errori robusta

### Technical
- Backend FastAPI (Python)
- Frontend React con Vite
- Database SQLite per persistenza
- Integrazione Ollama per LLM
- CORS configurato per sviluppo
- Type hints e documentazione

---

## 📝 Note di Rilascio

### Versioning
- **MAJOR**: Cambiamenti incompatibili con versioni precedenti
- **MINOR**: Nuove funzionalità compatibili con versioni precedenti
- **PATCH**: Bug fix compatibili con versioni precedenti

### Breaking Changes
- v2.0.0: Migrazione da JSON a database SQLite
- v1.0.0: Rilascio iniziale

### Deprecation
- v2.0.0: File `npcs.json` deprecato
- v2.0.0: Endpoint `/api/reload-npcs` deprecato

### Migration Guide
Per migrare da v1.0.0 a v2.0.0:
1. Backup del file `npcs.json`
2. Aggiorna il codice per utilizzare il database
3. Usa `import_npcs.py` per migrare NPC esistenti
4. Aggiorna le chiamate API se necessario

---

## 🔗 Link Utili

- [Documentazione API](https://github.com/tuousername/Npc_Bot/wiki/API)
- [Guide Migrazione](https://github.com/tuousername/Npc_Bot/wiki/Migration)
- [Changelog Completo](https://github.com/tuousername/Npc_Bot/releases) 