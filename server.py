import asyncio
import websockets
import json

# Dictionnaire pour garder une trace des clients connectés
connected_clients = set()

# Fonction WebSocket pour gérer les connexions
async def handle_connection(websocket, path):
    print("Client connecté")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print("Message reçu (inutile ici) :", message)
    except:
        print("Client déconnecté")
    finally:
        connected_clients.remove(websocket)

# Fonction pour envoyer les résultats
async def send_result(url, is_safe):
    message = json.dumps({"url": url, "safe": is_safe})
    for client in connected_clients:
        await client.send(message)

# Simuler une prédiction après réception d'une URL
async def process_url(url):
    print(f"Traitement de l'URL : {url}")
    # Simulation d'une prédiction
    await asyncio.sleep(3)  # Simuler un délai
    is_safe = ".com" in url  # Exemple de logique (ajustez selon le modèle)
    await send_result(url, is_safe)

# API Flask pour recevoir les URLs (POST)
from flask import Flask, request
from flask_cors import CORS  # Importer le module CORS

app = Flask(__name__)
CORS(app)  # Activer CORS pour toutes les routes

@app.route('/receive-url', methods=['POST'])
def receive_url():
    data = request.form
    url = data.get('url', '')
    print(f"URL reçue : {url}")
    asyncio.run(process_url(url))  # Appeler le traitement en arrière-plan
    return "URL reçue", 200

# Lancer le serveur WebSocket et Flask ensemble
from threading import Thread

def run_flask():
    app.run(host='0.0.0.0', port=5000)

def run_websocket():
    start_server = websockets.serve(handle_connection, "0.0.0.0", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    Thread(target=run_flask).start()
    run_websocket()
