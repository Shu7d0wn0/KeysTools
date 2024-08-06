<h1 align="center">DISCORD SERVER: https://discord.gg/H3BZEeDYuR</h1> 
<h1 align="center">Shu7d0wn Keystools</h1> 

<p>
  <h3>⭐ N'oubliez pas de définir le référentiel sur "Star" ça nous apporte beaucoup de soutien!! ⬆️</h3>
</p>

<h1>📜・Explications:</h1>

<p>
Cette procédure installe et configure un serveur API Flask sur un serveur Ubuntu, avec une base de données SQLite pour gérer des clés d'accès, puis intègre un bot Discord pour générer, lister et supprimer ces clés via des commandes Discord. Cela permet aux utilisateurs, même hors du réseau local, d'accéder aux fonctionnalités de l'outil en utilisant des clés d'accès enregistrées et validées.
</p>

<h1>⚠️ Descriptions:</h1>

<p>
    👨‍💻 -> Developpé en <strong>Python et sh</strong>.<br>
  🌍 -> Tool en <strong>Français</strong>.<br>
  💻 -> Disponible sur <strong>Linux</strong>.<br>
  🔎 -> <strong>Il n'y a pas de malware</strong>, <strong>backdoor</strong>.<br>
  📂 -> <strong>Open Source</strong> uniquement à des fins de vérification, garantissant l’absence de programmes malveillants.<br>
  🔄 -> <strong>Fréquemment mis à jour</strong>.<br>
  💰 -> <strong>Gratuit</strong> pour tout le monde.<br>
</p>

<h1>🔒・Exigences:</h1>

<h3>Ubuntu Server:</h3>

<p>
Système d'exploitation
Ubuntu 20.04 ou supérieur

<h1>Logiciels et dépendances</h1>
<h3>Mise à jour et installation des paquets essentiels</h3>

<h1>Bibliothèques Python :</h1>

```
Flask
Gunicorn
requests
discord.py
flask-limiter
```
</p>


<h1>⏳・Installation:</h1>

<p>
  
Installation et Configuration
1. Mise à jour et Installation des dépendances
  
```
sudo apt update
sudo apt install sqlite3
sudo apt install python3-pip
sudo apt install python3-venv
sudo apt install tmux
sudo apt install nginx
```
Création et configuration de la base de données (il faut mettre ligne pas ligne)
```
sqlite3 access_keys.db

CREATE TABLE keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiration_date TIMESTAMP,
    computer_id TEXT
);
```
3. Création et activation de l'environnement virtuel
```
python3 -m venv myenv
source myenv/bin/activate
```
4. Installation de Flask et autres dépendances
```
pip install flask
pip install gunicorn
pip install requests
pip install discord.py
pip install flask-limiter
```
5. Création du fichier api.py
```
nano api.py
```
Insérez le code "api.py" qui est dans Github

6. Démarrage de Flask avec Gunicorn (sorir fenetre tnux : CTRL + B  relaché puis D)
```
tmux new -s api
source myenv/bin/activate
sudo ufw allow 5001/tcp
gunicorn -w 4 -b 0.0.0.0:5001 api:app
```
7. Configuration de Nginx
```
sudo nano /etc/nginx/sites-available/myapp
```
Insérez la configuration suivante : (comande pour avoir adresse ipv6 :  curl -6 ifconfig.co)
```
server {
    listen 80;
    server_name your_ipv6_address (votre adresse ipv6 ;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
Puis, activez la configuration et redémarrez Nginx :
```
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
sudo unlink /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```
8. Démarrage de Gunicorn comme un Service
Créez le fichier de service :
```
sudo nano /etc/systemd/system/gunicorn.service
```
Ajoutez-y la configuration suivante :
```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=yourusername
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/your/project/myenv/bin/gunicorn -w 4 -b 0.0.0.0:5001 api:app

[Install]
WantedBy=multi-user.target
```
Rechargez les démons et démarrez le service :
```
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```
9. Test de l'API
Testez l'API localement et à distance :
```
curl -X POST http://127.0.0.1:5001/generate_key -H "Content-Type: application/json" -d '{"duration": 1}'
curl -X POST http://127.0.0.1:5001/validate_key -H "Content-Type: application/json" -d '{"key":"your_generated_key"}'
curl -X POST http://[your_ipv6_address]/generate_key
curl -X POST http://[your_ipv6_address]/validate_key -H "Content-Type: application/json" -d '{"key":"your_generated_key"}'
```
10. Configuration du Bot Discord
Créez et configurez bot.py :
```
nano bot.py
```
Insérez le code "bot.py" qui est dans le github :

11. Démarrage du Bot Discord
Créez une session tmux pour le bot Discord et démarrez-le :
```
tmux new -s discord_bot
source myenv/bin/activate
python3 bot.py
```
Vérifications
Vérifiez la réponse de l'API pour list_keys :
```
curl http://[your_ipv6_address]/list_keys
```

</p>

<h1>☠️・Builder:</h1>

Shu7d0wn

<h1>⚠️・Explications:</h1>

<p>
Cette procédure installe et configure un serveur API Flask sur un serveur Ubuntu, avec une base de données SQLite pour gérer des clés d'accès, puis intègre un bot Discord pour générer, lister et supprimer ces clés via des commandes Discord. Cela permet aux utilisateurs, même hors du réseau local, d'accéder aux fonctionnalités de l'outil en utilisant des clés d'accès enregistrées et validées.
</p>

<h2>🔗・Credits:</h2>

<p>
  - <a href="https://discord.gg/H3BZEeDYuR">Discord</a><br>
  - Creator: Shu7d0wn<br>
  - Version: 1.0
</p>
