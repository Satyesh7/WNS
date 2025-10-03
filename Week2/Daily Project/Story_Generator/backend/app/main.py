import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from app.services.story_service import generate_story
from app.services.safety_service import is_prompt_safe

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app) 

# --- Constants for Enterprise-Level Control ---
MIN_TEMP, MAX_TEMP = 0.1, 1.0
MIN_TOKENS, MAX_TOKENS = 50, 500
DEFAULT_TEMP, DEFAULT_TOKENS = 0.7, 150

@app.route('/api/generate-story', methods=['POST'])
def handle_generate_story():
    data = request.get_json()

    # --- Robust Input Validation ---
    if not data:
        return jsonify({"error": "Invalid request body."}), 400

    topic = data.get('topic', '').strip()
    if not topic:
        return jsonify({"error": "Please provide a topic for the story."}), 400

    # --- Guardrail Check ---
    if not is_prompt_safe(topic):
        logger.warning(f"Blocked unsafe prompt attempt for topic: '{topic}'")
        return jsonify({"error": "Stories on this topic are not permitted."}), 400

    # --- Parameter Validation with Defaults ---
    try:
        temp = float(data.get('temperature', DEFAULT_TEMP))
        tokens = int(data.get('max_tokens', DEFAULT_TOKENS))
    except (ValueError, TypeError):
        return jsonify({"error": "Temperature and max_tokens must be valid numbers."}), 400

    # Enforce enterprise limits
    if not (MIN_TEMP <= temp <= MAX_TEMP):
        return jsonify({"error": f"Temperature must be between {MIN_TEMP} and {MAX_TEMP}."}), 400
    if not (MIN_TOKENS <= tokens <= MAX_TOKENS):
        return jsonify({"error": f"Max tokens must be between {MIN_TOKENS} and {MAX_TOKENS}."}), 400

    logger.info(f"Request: topic='{topic}', temp={temp}, tokens={tokens}")

    # --- Main Logic ---
    try:
        story = generate_story(topic=topic, temperature=temp, max_tokens=tokens)
        if story:
            return jsonify({"story": story})
        else:
            return jsonify({"error": "Failed to generate story"}), 500
    except Exception as e:
        logger.error(f"An internal server error occurred: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)