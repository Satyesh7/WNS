# Advanced Story Generator

An enterprise-level web application designed to generate creative short stories based on user-provided topics and parameters. The application features a decoupled architecture, robust safety guardrails, and advanced user controls for creativity and length, making it a powerful and responsible AI tool.

## Features

-   **Dynamic Story Generation**: Users can input any topic to generate a unique story.
-   **Advanced User Controls**:
    -   **Creativity Slider (Temperature)**: Adjust the randomness and creativity of the story.
    -   **Length Slider (Max Tokens)**: Control the maximum length of the generated story.
-   **AI-Powered**: Utilizes Google's Gemini Pro model via LangChain for high-quality, coherent narrative generation.
-   **Content Safety Guardrails**: A configurable moderation service blocks prompts on sensitive or inappropriate topics before they are sent to the AI model.
-   **Decoupled Architecture**: A clean separation of concerns between the Python/Flask backend API and the vanilla HTML/CSS/JavaScript frontend.
-   **Robust Validation & Error Handling**: The backend validates all user inputs and parameters, providing clear, specific feedback for invalid requests.

## Tech Stack & Architecture

-   **Backend**:
    -   **Language**: Python 3.9+
    -   **Framework**: Flask
    -   **AI Orchestration**: LangChain
    -   **AI Model**: Google Generative AI (Gemini Pro)
    -   **Dependencies**: See `backend/requirements.txt`

-   **Frontend**:
    -   **Structure**: HTML5
    -   **Styling**: CSS3
    -   **Logic**: Vanilla JavaScript (ES6)

## Project Structure

story-generator-advanced/
├── backend/
│ ├── app/
│ │ ├── init.py
│ │ ├── main.py
│ │ ├── services/
│ │ │ ├── story_service.py
│ │ │ └── safety_service.py
│ │ └── config/
│ │ └── banned_keywords.py
│ └── requirements.txt
├── frontend/
│ ├── index.html
│ ├── static/
│ │ ├── css/style.css
│ │ └── js/script.js
└── README.md

## Prerequisites

-   **Python** (version 3.9 or higher)
-   **pip** (Python's package installer)
-   A **Google Gemini API Key**. Obtain one from [Google AI Studio](https://aistudio.google.com/app/apikey).

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd story-generator-advanced/backend
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    On Windows (PowerShell):
    ```powershell
    .\venv\Scripts\activate
    ```
    Your terminal prompt should now be prefixed with `(venv)`.

4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 2. Frontend Setup

The frontend consists of static files and requires no special installation. It can be served using the **Live Server** extension in Visual Studio Code.

## Running the Application

The application requires two separate processes to be running simultaneously.

### Step 1: Run the Backend Server

1.  Open a terminal and navigate to the `story-generator-advanced/backend` directory.
2.  Activate the virtual environment: `.\venv\Scripts\activate`.
3.  **Set your Gemini API Key** in the terminal session.
    On Windows (PowerShell):
    ```powershell
    $env:GEMINI_API_KEY="your_actual_gemini_api_key"
    ```
4.  **Start the Flask server:**
    ```bash
    python -m app.main
    ```
    The backend API is now running and listening on `http://localhost:5000`.

### Step 2: Run the Frontend Server

1.  Open the `story-generator-advanced` project folder in Visual Studio Code.
2.  Ensure you have the **Live Server** extension installed.
3.  In the VS Code file explorer, right-click on `frontend/index.html`.
4.  Select **"Open with Live Server"**.

Your web browser will open, and you can now use the Advanced Story Generator.

## API Endpoint Details

-   **Endpoint**: `/api/generate-story`
-   **Method**: `POST`
-   **Request Body** (JSON):
    ```json
    {
      "topic": "a dragon who loves to knit",
      "temperature": 0.8,
      "max_tokens": 250
    }
    ```
-   **Success Response** (`200 OK`):
    ```json
    {
      "story": "In a cavern lined not with gold but with yarn, lived Ignis, a dragon whose fiery passion was not for treasure, but for knitting..."
    }
    ```
-   **Error Responses** (`400 Bad Request`):
    -   If the topic is missing:
        ```json
        { "error": "Please provide a topic for the story." }
        ```
    -   If a parameter is invalid (e.g., temperature is 2.0):
        ```json
        { "error": "Temperature must be between 0.1 and 1.0." }
        ```
    -   If the topic is blocked by the safety guardrails:
        ```json
        { "error": "Stories on this topic are not permitted." }
        ```

## Configuration

### Safety Guardrails

The content moderation system can be easily configured by editing the keyword list in:
`backend/app/config/banned_keywords.py`

### API Parameter Limits

To prevent abuse and manage costs, the operational limits for temperature and token count are defined as constants at the top of the main API file. These can be adjusted by an administrator:
`backend/app/main.py`
```python
MIN_TEMP, MAX_TEMP = 0.1, 1.0
MIN_TOKENS, MAX_TOKENS = 50, 500