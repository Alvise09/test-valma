from flask import Flask, request, jsonify
from langchain_experimental.agents import create_csv_agent
from langchain_openai import ChatOpenAI  # Import aggiornato
from flask_cors import CORS  # Import flask_cors per gestire richieste cross-origin
import os

app = Flask(__name__)
CORS(app)  # Permetti richieste cross-origin

# Leggi la chiave API da una variabile d'ambiente
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

try:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)  # Carica il modello aggiornato
    agent = create_csv_agent(llm, 'dataset.csv', verbose=True, allow_dangerous_code=True)
except Exception as e:
    print(f"Errore nell'inizializzazione dell'agente: {e}")

@app.route('/get_response', methods=['POST', 'OPTIONS'])
def get_response():
    if request.method == 'OPTIONS':
        # Gestione delle richieste preflight
        return jsonify({}), 200

    user_message = request.json.get('message')
    print(f"[DEBUG] Messaggio ricevuto: {user_message}")

    if not user_message:
        print("[DEBUG] Messaggio vuoto ricevuto.")
        return jsonify({"response": "Per favore fai una domanda valida."})

    try:
        print("[DEBUG] Invio della richiesta all'agente...")
        response = agent.run(user_message)
        print(f"[DEBUG] Risposta dall'agente: {response}")
        return jsonify({"response": response})
    except Exception as e:
        print(f"[ERROR] Eccezione nella risposta dell'agente: {e}")
        return jsonify({"response": "Errore nel processare la richiesta."})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
