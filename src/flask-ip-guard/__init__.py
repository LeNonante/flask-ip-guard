import json
import os
from flask import request, abort, current_app

class IPGuard:
    def __init__(self, app=None):
        self.whitelist = []
        self.blacklist = []
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialise l'extension avec l'application Flask."""
        # Configuration par défaut
        app.config.setdefault('IP_GUARD_MODE', 'WHITELIST') # Ou 'BLACKLIST'
        app.config.setdefault('IP_GUARD_FILE', 'ip_list.json') # Chemin du fichier JSON
        
        # On charge les listes au démarrage
        self._load_lists(app)

        # On enregistre la fonction qui s'exécutera avant chaque requête
        app.before_request(self._check_ip)

    def _load_lists(self, app):
        """Charge les IPs depuis le fichier JSON (Adapté de services/config.py)"""
        filename = app.config['IP_GUARD_FILE']
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # On sépare directement les listes actives pour optimiser
                # Dans votre code original, vous filtrez 'active' == True
                self.whitelist = [i['ip'] for i in data.get('whitelist', []) if i.get('active', True)]
                self.blacklist = [i['ip'] for i in data.get('blacklist', []) if i.get('active', True)]
        except FileNotFoundError:
            # Si le fichier n'existe pas, on laisse les listes vides (ou on le crée)
            pass
        except Exception as e:
            if app.debug:
                print(f"Erreur chargement IPGuard: {e}")

    def _check_ip(self):
        """Vérifie l'IP (Adapté de api/routes.py)"""
        mode = current_app.config['IP_GUARD_MODE']
        client_ip = request.remote_addr

        # Logique extraite de api/routes.py
        if mode == 'BLACKLIST':
            if client_ip in self.blacklist:
                abort(403, description="IP Forbidden (Blacklisted)")
                
        elif mode == 'WHITELIST':
            # En whitelist, on bloque tout ce qui n'est pas dans la liste
            if client_ip not in self.whitelist:
                abort(403, description="IP Forbidden (Not Whitelisted)")

    def reload(self):
        """Fonction utilitaire pour recharger la configuration sans redémarrer Flask"""
        self._load_lists(current_app)