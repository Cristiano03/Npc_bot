import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os

class ChatDatabase:
    def __init__(self, db_path: str = "chat_history.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inizializza il database con le tabelle necessarie"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabella per gli NPC
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS npcs (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    avatar TEXT NOT NULL,
                    description TEXT NOT NULL,
                    status TEXT DEFAULT 'online',
                    prompt TEXT NOT NULL,
                    last_message TEXT DEFAULT '',
                    last_message_time TEXT DEFAULT '',
                    unread_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabella per le conversazioni
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    npc_id TEXT NOT NULL,
                    user_id TEXT DEFAULT 'default_user',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    title TEXT DEFAULT '',
                    message_count INTEGER DEFAULT 0,
                    FOREIGN KEY (npc_id) REFERENCES npcs (id)
                )
            ''')
            
            # Tabella per i messaggi
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    sender TEXT NOT NULL, -- 'user' o 'npc'
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id)
                )
            ''')
            
            # Tabella per le sessioni utente
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    npc_id TEXT NOT NULL,
                    conversation_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id),
                    FOREIGN KEY (npc_id) REFERENCES npcs (id)
                )
            ''')
            
            # Indici per migliorare le performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_npcs_id ON npcs(id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversations_npc ON conversations(npc_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user_npc ON user_sessions(user_id, npc_id)')
            
            conn.commit()
            
            # Inizializza gli NPC di default se la tabella è vuota
            self._init_default_npcs()
    
    def _init_default_npcs(self):
        """Inizializza gli NPC di default se la tabella è vuota"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM npcs')
            if cursor.fetchone()[0] == 0:
                default_npcs = [
                    {
                        "id": "aedryan",
                        "name": "Re Aedryan",
                        "avatar": "👑",
                        "description": "Re del regno di Virelund",
                        "status": "online",
                        "prompt": "Tu sei Re Aedryan, sovrano decadente del regno di Virelund, un regno sull'orlo della rovina.\n\nIl tuo popolo è decimato da una malattia sconosciuta chiamata \"Il Sussurro Pallido\", una piaga che prosciuga lentamente mente e corpo, lasciando solo corpi tremanti e occhi vuoti. I migliori guaritori hanno fallito. Gli dèi tacciono. I confini si sgretolano, e i nobili fuggono come topi dalla nave che affonda.\n\nTu, però, resisti.\n\nTi sei rifiutato di abbandonare il tuo trono. Pur stanco, malato, e segnato dal dolore, mantieni la tua dignità. Hai radunato mercenari, avventurieri, e studiosi da terre lontane — la tua ultima speranza. A loro affidi una missione disperata: scoprire l'origine della pestilenza e porvi fine, con ogni mezzo necessario.\n\nParla con tono regale, lento, pesato, come se ogni parola costasse fatica. Mostra tracce di amarezza, ma anche scintille di orgoglio e determinazione. A volte ti perdi nei ricordi di un regno florido. Hai il cuore spezzato, ma ancora vivi per il tuo popolo.\n\nQuando i personaggi ti parlano, rispondi come Re Aedryan. Mantieni coerenza emotiva e narrativa.\nRispondi solo come Re Aedryan. Non spiegare il tuo comportamento.",
                        "lastMessage": "Come posso aiutarti oggi?",
                        "lastMessageTime": "12:30",
                        "unread_count": 0
                    },
                    {
                        "id": "thorin",
                        "name": "Thorin",
                        "avatar": "⚔️",
                        "description": "Guerriero coraggioso",
                        "status": "online",
                        "prompt": "Tu sei Thorin, un guerriero coraggioso e fiero. Sei un combattente esperto che ha visto molte battaglie e ha sempre combattuto per la giustizia e l'onore.\n\nParla con determinazione e coraggio, mostrando la tua esperienza in battaglia e la tua saggezza guerriera.",
                        "lastMessage": "Pronto per la battaglia!",
                        "lastMessageTime": "11:45",
                        "unread_count": 2
                    },
                    {
                        "id": "elara",
                        "name": "Elara",
                        "avatar": "🏹",
                        "description": "Ranger elfica",
                        "status": "online",
                        "prompt": "Tu sei Elara, una ranger elfica che vive in armonia con la natura. Sei esperta nell'arte della caccia e della sopravvivenza nella foresta.\n\nParla con grazia e saggezza, mostrando la tua connessione con la natura e la tua esperienza come ranger.",
                        "lastMessage": "La natura mi chiama",
                        "lastMessageTime": "10:20",
                        "unread_count": 0
                    }
                ]
                
                for npc in default_npcs:
                    cursor.execute('''
                        INSERT INTO npcs (id, name, avatar, description, status, prompt, last_message, last_message_time, unread_count)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        npc['id'], npc['name'], npc['avatar'], npc['description'], 
                        npc['status'], npc['prompt'], npc['lastMessage'], 
                        npc['lastMessageTime'], npc['unread_count']
                    ))
                
                conn.commit()
    
    # Metodi per gestire gli NPC
    def get_all_npcs(self) -> List[Dict]:
        """Ottiene tutti gli NPC"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, avatar, description, status, prompt, 
                       last_message, last_message_time, unread_count, 
                       created_at, updated_at
                FROM npcs
                ORDER BY name
            ''')
            
            npcs = []
            for row in cursor.fetchall():
                npcs.append({
                    'id': row[0],
                    'name': row[1],
                    'avatar': row[2],
                    'description': row[3],
                    'status': row[4],
                    'prompt': row[5],
                    'lastMessage': row[6],
                    'lastMessageTime': row[7],
                    'unread': row[8],
                    'created_at': row[9],
                    'updated_at': row[10]
                })
            
            return npcs
    
    def get_npc_by_id(self, npc_id: str) -> Optional[Dict]:
        """Ottiene un NPC specifico per ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, avatar, description, status, prompt, 
                       last_message, last_message_time, unread_count, 
                       created_at, updated_at
                FROM npcs
                WHERE id = ?
            ''', (npc_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'name': row[1],
                    'avatar': row[2],
                    'description': row[3],
                    'status': row[4],
                    'prompt': row[5],
                    'lastMessage': row[6],
                    'lastMessageTime': row[7],
                    'unread': row[8],
                    'created_at': row[9],
                    'updated_at': row[10]
                }
            return None
    
    def create_npc(self, npc_data: Dict) -> bool:
        """Crea un nuovo NPC"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO npcs (id, name, avatar, description, status, prompt)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    npc_data['id'],
                    npc_data['name'],
                    npc_data['avatar'],
                    npc_data['description'],
                    npc_data.get('status', 'online'),
                    npc_data['prompt']
                ))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False  # ID già esistente
    
    def update_npc(self, npc_id: str, npc_data: Dict) -> bool:
        """Aggiorna un NPC esistente"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE npcs 
                SET name = ?, avatar = ?, description = ?, status = ?, 
                    prompt = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (
                npc_data['name'],
                npc_data['avatar'],
                npc_data['description'],
                npc_data.get('status', 'online'),
                npc_data['prompt'],
                npc_id
            ))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_npc(self, npc_id: str) -> bool:
        """Elimina un NPC e tutte le sue conversazioni"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Elimina le conversazioni dell'NPC
            cursor.execute('DELETE FROM conversations WHERE npc_id = ?', (npc_id,))
            
            # Elimina l'NPC
            cursor.execute('DELETE FROM npcs WHERE id = ?', (npc_id,))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def update_npc_last_message(self, npc_id: str, message: str, time: str = None):
        """Aggiorna l'ultimo messaggio di un NPC"""
        if time is None:
            time = datetime.now().strftime("%H:%M")
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE npcs 
                SET last_message = ?, last_message_time = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (message, time, npc_id))
            conn.commit()
    
    def get_or_create_conversation(self, npc_id: str, user_id: str = "default_user") -> int:
        """Ottiene o crea una conversazione per un utente con un NPC specifico"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Cerca una conversazione esistente
            cursor.execute('''
                SELECT id FROM conversations 
                WHERE npc_id = ? AND user_id = ?
                ORDER BY updated_at DESC LIMIT 1
            ''', (npc_id, user_id))
            
            result = cursor.fetchone()
            
            if result:
                conversation_id = result[0]
                # Aggiorna il timestamp di attività
                cursor.execute('''
                    UPDATE conversations 
                    SET updated_at = CURRENT_TIMESTAMP 
                    WHERE id = ?
                ''', (conversation_id,))
            else:
                # Crea una nuova conversazione
                cursor.execute('''
                    INSERT INTO conversations (npc_id, user_id, title)
                    VALUES (?, ?, ?)
                ''', (npc_id, user_id, f"Chat con {npc_id}"))
                conversation_id = cursor.lastrowid
            
            conn.commit()
            return conversation_id
    
    def add_message(self, conversation_id: int, sender: str, content: str) -> int:
        """Aggiunge un messaggio alla conversazione"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Inserisce il messaggio
            cursor.execute('''
                INSERT INTO messages (conversation_id, sender, content)
                VALUES (?, ?, ?)
            ''', (conversation_id, sender, content))
            
            message_id = cursor.lastrowid
            
            # Aggiorna il contatore dei messaggi e il timestamp della conversazione
            cursor.execute('''
                UPDATE conversations 
                SET message_count = message_count + 1, 
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (conversation_id,))
            
            conn.commit()
            return message_id
    
    def get_conversation_history(self, conversation_id: int, limit: int = 50) -> List[Dict]:
        """Ottiene lo storico di una conversazione"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT sender, content, timestamp
                FROM messages 
                WHERE conversation_id = ?
                ORDER BY timestamp ASC
                LIMIT ?
            ''', (conversation_id, limit))
            
            messages = []
            for row in cursor.fetchall():
                messages.append({
                    'sender': row[0],
                    'content': row[1],
                    'timestamp': row[2]
                })
            
            return messages
    
    def get_conversation_context(self, conversation_id: int, max_messages: int = 10) -> str:
        """Ottiene il contesto della conversazione per l'LLM"""
        messages = self.get_conversation_history(conversation_id, max_messages)
        
        if not messages:
            return ""
        
        context = "Contesto della conversazione precedente:\n\n"
        for msg in messages:
            role = "Utente" if msg['sender'] == 'user' else "NPC"
            context += f"{role}: {msg['content']}\n\n"
        
        return context
    
    def get_user_conversations(self, user_id: str = "default_user", limit: int = 20) -> List[Dict]:
        """Ottiene le conversazioni di un utente"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT c.id, c.npc_id, c.title, c.message_count, c.updated_at,
                       m.content as last_message
                FROM conversations c
                LEFT JOIN messages m ON m.id = (
                    SELECT id FROM messages 
                    WHERE conversation_id = c.id 
                    ORDER BY timestamp DESC LIMIT 1
                )
                WHERE c.user_id = ?
                ORDER BY c.updated_at DESC
                LIMIT ?
            ''', (user_id, limit))
            
            conversations = []
            for row in cursor.fetchall():
                conversations.append({
                    'id': row[0],
                    'npc_id': row[1],
                    'title': row[2],
                    'message_count': row[3],
                    'updated_at': row[4],
                    'last_message': row[5] or ""
                })
            
            return conversations
    
    def delete_conversation(self, conversation_id: int) -> bool:
        """Elimina una conversazione e tutti i suoi messaggi"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Elimina i messaggi
            cursor.execute('DELETE FROM messages WHERE conversation_id = ?', (conversation_id,))
            
            # Elimina la conversazione
            cursor.execute('DELETE FROM conversations WHERE id = ?', (conversation_id,))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def get_conversation_stats(self, npc_id: str = None) -> Dict:
        """Ottiene statistiche sulle conversazioni"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if npc_id:
                cursor.execute('''
                    SELECT COUNT(*) as total_conversations,
                           SUM(message_count) as total_messages,
                           AVG(message_count) as avg_messages
                    FROM conversations 
                    WHERE npc_id = ?
                ''', (npc_id,))
            else:
                cursor.execute('''
                    SELECT COUNT(*) as total_conversations,
                           SUM(message_count) as total_messages,
                           AVG(message_count) as avg_messages
                    FROM conversations
                ''')
            
            row = cursor.fetchone()
            return {
                'total_conversations': row[0] or 0,
                'total_messages': row[1] or 0,
                'avg_messages': row[2] or 0
            }
    
    def cleanup_old_conversations(self, days_old: int = 30) -> int:
        """Pulisce le conversazioni vecchie"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Trova le conversazioni da eliminare
            cursor.execute('''
                SELECT id FROM conversations 
                WHERE updated_at < datetime('now', '-{} days')
            '''.format(days_old))
            
            old_conversations = [row[0] for row in cursor.fetchall()]
            
            # Elimina le conversazioni e i messaggi associati
            for conv_id in old_conversations:
                self.delete_conversation(conv_id)
            
            return len(old_conversations)

# Istanza globale del database
chat_db = ChatDatabase() 