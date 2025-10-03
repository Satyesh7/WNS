
## Prerequisites

Before you begin, ensure you have the following installed on your system:

-   **Python** (version 3.9 or higher)
-   **pip** (Python's package installer, typically comes with Python)
-   A **Google Gemini API Key**. You can obtain one from [Google AI Studio](https://aistudio.google.com/app/apikey).

## Setup and Installation

Follow these steps to set up the project on your local machine.

### 1. Clone the Repository

First, get the project files onto your machine. If you don't have a git repository, simply ensure the project folder is ready.

### 2. Backend Setup

This involves creating an isolated Python environment and installing the required libraries.

1.  **Navigate to the backend directory:**
    ```bash
    cd joke-generator/backend
    ```

2.  **Create a virtual environment:**
    This creates an isolated `venv` folder to store the project's Python dependencies.
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    On Windows (PowerShell):
    ```powershell
    .\venv\Scripts\activate
    ```
    Your terminal prompt should now be prefixed with `(venv)`.

4.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Frontend Setup

No special installation is required for the frontend. It consists of static files that can be served by any simple web server. The easiest way to run it is with the **Live Server** extension in Visual Studio Code.

## Running the Application

The application requires two separate processes to be running simultaneously: the backend API and the frontend web server.

### Step 1: Run the Backend Server

1.  Open a terminal and navigate to the `joke-generator/backend` directory.
2.  Activate the virtual environment if it's not already active: `.\venv\Scripts\activate`.
3.  **Set your Gemini API Key**. This is a critical step.
    On Windows (PowerShell), run the following command, replacing the placeholder with your actual key:
    ```powershell
    $env:GEMINI_API_KEY="your_actual_gemini_api_key"
    ```
4.  **Start the Flask server:**
    ```bash
    python -m app.main
    ```
    The backend API is now running and listening on `http://localhost:5000`.

### Step 2: Run the Frontend Server

1.  Open the `joke-generator` project in Visual Studio Code.
2.  Make sure you have the **Live Server** extension installed.
3.  In the VS Code file explorer, right-click on `frontend/index.html`.
4.  Select **"Open with Live Server"**.

Your default web browser will open to a URL like `http://127.0.0.1:5500`, and you can now use the Joke Generator!

## API Endpoint Details

The backend provides a single API endpoint for generating puns.

-   **Endpoint**: `/api/get-pun`
-   **Method**: `POST`
-   **Request Body** (JSON):
    ```json
    {
      "topic": "computers"
    }
    ```
-   **Success Response** (`200 OK`):
    ```json
    {
      "pun": "Why was the computer cold? It left its Windows open."
    }
    ```
-   **Error Responses** (`400 Bad Request`):
    -   If the topic is missing:
        ```json
        { "error": "Please provide a topic for the joke." }
        ```
    -   If the topic is blocked by the safety guardrails:
        ```json
        { "error": "Jokes on this topic are not permitted." }
        ```

## Configuration

### Safety Guardrails

The content moderation system is controlled by a simple keyword list. You can easily customize the list of forbidden topics by editing the following file:

`backend/app/config/banned_keywords.py`

Simply add or remove strings from the `FORBIDDEN_KEYWORDS` list to change the guardrail behavior. The check is case-insensitive.