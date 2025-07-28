# 🤝 Contribuire a NPC Bot

Grazie per il tuo interesse a contribuire a NPC Bot! Questo documento ti guiderà attraverso il processo di contribuzione.

## 📋 Indice

- [Come Contribuire](#come-contribuire)
- [Setup Sviluppo](#setup-sviluppo)
- [Linee Guida Codice](#linee-guida-codice)
- [Processo di Pull Request](#processo-di-pull-request)
- [Segnalazione Bug](#segnalazione-bug)
- [Richiesta Funzionalità](#richiesta-funzionalità)
- [Domande](#domande)

## 🚀 Come Contribuire

Ci sono molti modi per contribuire al progetto:

### 🐛 Segnalazione Bug
- Usa il template per le issue
- Fornisci dettagli riproducibili
- Includi log e screenshot se necessario

### 💡 Richiesta Funzionalità
- Descrivi la funzionalità richiesta
- Spiega il caso d'uso
- Proponi una soluzione se possibile

### 🔧 Contributi di Codice
- Fix bug
- Aggiungi nuove funzionalità
- Migliora la documentazione
- Ottimizza le performance

### 📚 Documentazione
- Migliora il README
- Aggiungi esempi di utilizzo
- Traduci la documentazione

## 🛠️ Setup Sviluppo

### Prerequisiti
- Python 3.8+
- Node.js 16+
- Git
- Ollama (per test locali)

### 1. Fork e Clone
```bash
# Fork la repository su GitHub
# Poi clona il tuo fork
git clone https://github.com/tuousername/Npc_Bot.git
cd Npc_Bot
```

### 2. Setup Backend
```bash
cd Backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 3. Setup Frontend
```bash
cd FrontEnd
npm install
```

### 4. Setup Database
```bash
cd Backend
python test_db.py  # Inizializza il database
```

### 5. Avvia per Sviluppo
```bash
# Terminale 1: Backend
cd Backend
python api_server.py

# Terminale 2: Frontend
cd FrontEnd
npm run dev

# Terminale 3: Ollama (se necessario)
ollama serve
```

## 📝 Linee Guida Codice

### Python (Backend)

#### Stile Codice
- Segui [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Usa type hints quando possibile
- Mantieni funzioni sotto 50 righe
- Usa docstring per funzioni pubbliche

#### Esempio
```python
from typing import Dict, List, Optional

def get_npc_by_id(npc_id: str) -> Optional[Dict]:
    """
    Ottiene un NPC specifico per ID dal database.
    
    Args:
        npc_id: ID dell'NPC da cercare
        
    Returns:
        Dizionario con i dati dell'NPC o None se non trovato
    """
    # Implementazione...
```

#### Test
- Aggiungi test per nuove funzionalità
- Mantieni coverage > 80%
- Usa pytest per i test

```bash
cd Backend
python -m pytest test_*.py -v
```

### JavaScript/React (Frontend)

#### Stile Codice
- Usa ESLint e Prettier
- Segui le convenzioni React
- Usa hooks quando possibile
- Mantieni componenti piccoli e focalizzati

#### Esempio
```jsx
import React, { useState, useEffect } from 'react';

const ChatApp = ({ selectedChat, onChatSelect }) => {
  const [messages, setMessages] = useState([]);
  
  useEffect(() => {
    // Logica...
  }, [selectedChat]);
  
  return (
    <div className="chat-app">
      {/* JSX */}
    </div>
  );
};

export default ChatApp;
```

### Commit Messages

Usa il formato [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: aggiungi gestione NPC via CLI
fix: risolvi problema connessione database
docs: aggiorna README con nuove istruzioni
test: aggiungi test per import NPC
refactor: ristruttura gestione conversazioni
```

### Branch Naming

```
feature/npc-cli-manager
fix/database-connection
docs/update-readme
test/add-npc-tests
```

## 🔄 Processo di Pull Request

### 1. Crea un Branch
```bash
git checkout -b feature/tua-funzionalita
```

### 2. Sviluppa
- Scrivi il codice
- Aggiungi test
- Aggiorna documentazione
- Testa localmente

### 3. Commit
```bash
git add .
git commit -m "feat: descrizione della funzionalità"
```

### 4. Push
```bash
git push origin feature/tua-funzionalita
```

### 5. Pull Request
- Vai su GitHub
- Crea una Pull Request
- Usa il template fornito
- Descrivi le modifiche

### Template Pull Request

```markdown
## 📝 Descrizione
Breve descrizione delle modifiche

## 🔧 Tipo di Modifica
- [ ] Bug fix
- [ ] Nuova funzionalità
- [ ] Miglioramento documentazione
- [ ] Refactoring
- [ ] Test

## 🧪 Test
- [ ] Test locali passati
- [ ] Test automatici aggiunti
- [ ] Documentazione aggiornata

## 📸 Screenshot (se applicabile)

## ✅ Checklist
- [ ] Codice segue le linee guida
- [ ] Test aggiunti/aggiornati
- [ ] Documentazione aggiornata
- [ ] Commit messages seguono le convenzioni
```

## 🐛 Segnalazione Bug

### Template Issue

```markdown
## 🐛 Descrizione Bug
Descrizione chiara e concisa del bug

## 🔄 Passi per Riprodurre
1. Vai a '...'
2. Clicca su '...'
3. Scorri fino a '...'
4. Vedi errore

## ✅ Comportamento Atteso
Cosa dovrebbe succedere

## 📸 Screenshot
Se applicabile, aggiungi screenshot

## 💻 Ambiente
- OS: [es. Windows 10]
- Browser: [es. Chrome 90]
- Versione: [es. 1.0.0]

## 📋 Informazioni Aggiuntive
Qualsiasi altra informazione rilevante
```

## 💡 Richiesta Funzionalità

### Template Feature Request

```markdown
## 💡 Descrizione
Descrizione chiara della funzionalità richiesta

## 🎯 Problema
Il problema che questa funzionalità risolverebbe

## 💭 Soluzione Proposta
Descrizione della soluzione desiderata

## 🔄 Alternative Considerate
Altre soluzioni considerate

## 📋 Informazioni Aggiuntive
Screenshot, mockup, esempi di utilizzo
```

## 📚 Documentazione

### Struttura
```
docs/
├── api/           # Documentazione API
├── deployment/    # Guide deployment
├── development/   # Guide sviluppo
└── user/          # Guide utente
```

### Linee Guida
- Usa Markdown
- Includi esempi di codice
- Mantieni aggiornata
- Usa immagini quando utile

## 🧪 Testing

### Backend Tests
```bash
cd Backend
python test_api.py
python test_conversation_history.py
python test_db.py
```

### Frontend Tests
```bash
cd FrontEnd
npm test
npm run build
```

### Integration Tests
```bash
# Test completo del sistema
python -m pytest tests/integration/ -v
```

## 🔒 Sicurezza

### Segnalazione Vulnerabilità
- **NON** aprire issue pubbliche per vulnerabilità
- Invia email a: security@npcbot.com
- Descrivi la vulnerabilità in dettaglio
- Fornisci proof of concept se possibile

## 🏷️ Release

### Versioning
Seguiamo [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- Es: `1.2.3`

### Changelog
- Mantieni `CHANGELOG.md` aggiornato
- Usa sezioni: Added, Changed, Deprecated, Removed, Fixed, Security

## 🤝 Codice di Condotta

### Comportamento Atteso
- Rispetto reciproco
- Collaborazione costruttiva
- Feedback positivo
- Inclusività

### Comportamento Non Accettabile
- Linguaggio offensivo
- Trolling o commenti offensivi
- Harassment personale
- Spam o contenuto non pertinente

## 📞 Domande?

- **Issues**: [GitHub Issues](https://github.com/tuousername/Npc_Bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tuousername/Npc_Bot/discussions)
- **Email**: dev@npcbot.com

## 🙏 Ringraziamenti

Grazie a tutti i contributori che rendono NPC Bot migliore ogni giorno! 🎉

---

**Nota**: Questo documento è un work in progress. Se hai suggerimenti per migliorarlo, apri una Pull Request! 