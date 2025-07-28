# 🚀 Guida al Deployment

Questa guida ti aiuterà a deployare NPC Bot in produzione.

## 🌐 Opzioni di Deployment

### 1. **VPS (Virtual Private Server)**

#### Prerequisiti
- VPS con Ubuntu 20.04+ o Debian 11+
- 2GB RAM minimo (4GB raccomandato)
- 20GB spazio disco
- Accesso SSH

#### Setup VPS
```bash
# Aggiorna sistema
sudo apt update && sudo apt upgrade -y

# Installa dipendenze
sudo apt install -y python3 python3-pip python3-venv nodejs npm nginx git

# Installa Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Clona repository
git clone https://github.com/tuousername/Npc_Bot.git
cd Npc_Bot
```

#### Configurazione Backend
```bash
cd Backend

# Crea ambiente virtuale
python3 -m venv venv
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt

# Configura variabili ambiente
cat > .env << EOF
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=openhermes
DEBUG=False
HOST=0.0.0.0
PORT=8000
EOF

# Inizializza database
python test_db.py
```

#### Configurazione Frontend
```bash
cd FrontEnd

# Installa dipendenze
npm install

# Build per produzione
npm run build

# Configura nginx
sudo tee /etc/nginx/sites-available/npc-bot << EOF
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /path/to/Npc_Bot/FrontEnd/dist;
        try_files \$uri \$uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Abilita sito
sudo ln -s /etc/nginx/sites-available/npc-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Systemd Services
```bash
# Backend service
sudo tee /etc/systemd/system/npc-bot-backend.service << EOF
[Unit]
Description=NPC Bot Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/Npc_Bot/Backend
Environment=PATH=/path/to/Npc_Bot/Backend/venv/bin
ExecStart=/path/to/Npc_Bot/Backend/venv/bin/python api_server.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Ollama service
sudo tee /etc/systemd/system/ollama.service << EOF
[Unit]
Description=Ollama LLM Server
After=network.target

[Service]
Type=simple
User=ollama
ExecStart=/usr/local/bin/ollama serve
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Avvia servizi
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl enable npc-bot-backend
sudo systemctl start ollama
sudo systemctl start npc-bot-backend
```

### 2. **Docker Deployment**

#### Dockerfile Backend
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY Backend/requirements.txt .
RUN pip install -r requirements.txt

COPY Backend/ .

EXPOSE 8000

CMD ["python", "api_server.py"]
```

#### Dockerfile Frontend
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY FrontEnd/package*.json ./
RUN npm ci

COPY FrontEnd/ .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
```

#### Docker Compose
```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped

  backend:
    build:
      context: .
      dockerfile: Backend/Dockerfile
    container_name: npc-bot-backend
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_URL=http://ollama:11434/api/generate
      - OLLAMA_MODEL=openhermes
    depends_on:
      - ollama
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: FrontEnd/Dockerfile
    container_name: npc-bot-frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  ollama_data:
```

#### Deploy con Docker
```bash
# Build e avvia
docker-compose up -d

# Verifica status
docker-compose ps

# Log
docker-compose logs -f
```

### 3. **Cloudflare Tunnel (Raccomandato)**

#### Setup Cloudflare
1. Crea account su [Cloudflare](https://cloudflare.com)
2. Installa `cloudflared`:
   ```bash
   # Linux
   curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared
   chmod +x cloudflared
   sudo mv cloudflared /usr/local/bin/

   # Windows
   # Scarica da https://github.com/cloudflare/cloudflared/releases
   ```

#### Configurazione Tunnel
```bash
# Login
cloudflared tunnel login

# Crea tunnel
cloudflared tunnel create npc-bot

# Configura DNS
cloudflared tunnel route dns npc-bot your-domain.com

# Configura tunnel
cat > ~/.cloudflared/config.yml << EOF
tunnel: [TUNNEL-ID]
credentials-file: ~/.cloudflared/[TUNNEL-ID].json

ingress:
  - hostname: your-domain.com
    service: http://localhost:8000
  - hostname: www.your-domain.com
    service: http://localhost:8000
  - service: http_status:404
EOF

# Avvia tunnel
cloudflared tunnel run npc-bot
```

#### Systemd Service per Tunnel
```bash
sudo tee /etc/systemd/system/cloudflared.service << EOF
[Unit]
Description=Cloudflare Tunnel
After=network.target

[Service]
Type=simple
User=cloudflared
ExecStart=/usr/local/bin/cloudflared tunnel run npc-bot
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable cloudflared
sudo systemctl start cloudflared
```

## 🔧 Configurazione SSL

### Let's Encrypt (VPS)
```bash
# Installa Certbot
sudo apt install certbot python3-certbot-nginx

# Ottieni certificato
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Aggiungi: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Cloudflare (Automatico)
- Abilita "Always Use HTTPS" in Cloudflare
- SSL/TLS mode: "Full (strict)"

## 📊 Monitoraggio

### Logs
```bash
# Backend logs
sudo journalctl -u npc-bot-backend -f

# Ollama logs
sudo journalctl -u ollama -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Health Checks
```bash
# API health
curl https://your-domain.com/api/health

# Ollama status
curl http://localhost:11434/api/tags
```

### Backup Database
```bash
# Backup automatico
sudo tee /etc/cron.daily/npc-bot-backup << EOF
#!/bin/bash
cp /path/to/Npc_Bot/Backend/chat_history.db /backup/npc-bot-\$(date +%Y%m%d).db
find /backup -name "npc-bot-*.db" -mtime +7 -delete
EOF

chmod +x /etc/cron.daily/npc-bot-backup
```

## 🔒 Sicurezza

### Firewall
```bash
# UFW
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### Rate Limiting
```bash
# Nginx rate limiting
sudo tee /etc/nginx/conf.d/rate-limit.conf << EOF
limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;

location /api/ {
    limit_req zone=api burst=20 nodelay;
    proxy_pass http://localhost:8000;
}
EOF
```

### Environment Variables
```bash
# Produzione
export DEBUG=False
export OLLAMA_URL=http://localhost:11434/api/generate
export OLLAMA_MODEL=openhermes
export HOST=0.0.0.0
export PORT=8000
```

## 🚨 Troubleshooting

### Problemi Comuni

#### Ollama non risponde
```bash
# Verifica servizio
sudo systemctl status ollama

# Riavvia
sudo systemctl restart ollama

# Verifica modello
ollama list
ollama pull openhermes
```

#### Database corrotto
```bash
# Backup e ripristino
cp chat_history.db chat_history.db.backup
python import_npcs.py backup
rm chat_history.db
python api_server.py
```

#### Frontend non si connette
```bash
# Verifica CORS
# Controlla console browser
# Verifica URL API nel frontend
```

## 📞 Supporto

- **Issues**: [GitHub Issues](https://github.com/tuousername/Npc_Bot/issues)
- **Documentazione**: [Wiki](https://github.com/tuousername/Npc_Bot/wiki)
- **Community**: [Discussions](https://github.com/tuousername/Npc_Bot/discussions)

---

**Nota**: Questa guida è un work in progress. Aggiornamenti regolari per nuove funzionalità e best practices. 