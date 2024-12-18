import os
from flask import Flask, request, jsonify
from langchain_experimental.agents import create_csv_agent
from langchain_openai import ChatOpenAI  # Import aggiornato
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Abilita CORS

os.environ["OPENAI_API_KEY"] = "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"

try:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    agent = create_csv_agent(llm, 'dataset.csv', verbose=True, allow_dangerous_code=True)
except Exception as e:
    print(f"Failed to initialize agent: {e}")

@app.route('/get_response', methods=['POST', 'OPTIONS'])
def get_response():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"response": "Please ask a valid question."})

    try:
        response = agent.run(user_message)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": "Failed to process the request."})


# Usa la porta dinamica che Render imposta
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Ottieni la porta o usa 5000 di fallback
    app.run(host="0.0.0.0", port=port, debug=True)
