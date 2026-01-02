# flask-ip-guard

Une extension Flask simple et légère pour restreindre l'accès à votre application via une Whitelist ou une Blacklist d'adresses IP.

## Installation

```bash
pip install flask-ip-guard
```

## Utilisation

Créez un fichier `security.json` à la racine de votre projet Flask :
```JSON
{
    "whitelist": [
        {"ip": "127.0.0.1", "active": true, "description": "Localhost"}
    ],
    "blacklist": []
}
```

Puis, dans votre application Flask (app.py) :
```Python
from flask import Flask
from flask_ip_guard import IPGuard

app = Flask(__name__)

# Configuration
app.config['IP_GUARD_MODE'] = 'WHITELIST' # ou 'BLACKLIST'
app.config['IP_GUARD_FILE'] = 'security.json'

# Initialisation
ip_guard = IPGuard(app)

@app.route('/')
def index():
    return "Accès autorisé !"
```