import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from app.services.joke_service import generate_pun_on_topic
from app.services.safety_service import is_prompt_safe

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app) 

@app.route('/api/get-pun', methods=['POST'])
def get_pun():
    """
    API endpoint to generate a pun based on a user-provided topic,
    with safety guardrails.
    """
    data = request.get_json()

    # --- Edge Case and Input Validation ---
    if not data or 'topic' not in data or not data['topic'].strip():
        logger.warning("API call with missing or empty topic.")
        return jsonify({"error": "Please provide a topic for the joke."}), 400

    topic = data['topic']
    logger.info(f"Received request for a pun on topic: '{topic}'")

    # --- Guardrail Check ---
    if not is_prompt_safe(topic):
        logger.warning(f"Blocked unsafe prompt attempt for topic: '{topic}'")
        return jsonify({"error": "Jokes on this topic are not permitted."}), 400

    # --- Main Logic ---
    try:
        pun = generate_pun_on_topic(topic)
        if pun:
            return jsonify({"pun": pun})
        else:
            return jsonify({"error": "Failed to generate pun"}), 500
    except Exception as e:
        logger.error(f"An internal server error occurred: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)