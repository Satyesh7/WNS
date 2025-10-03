document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const topicInput = document.getElementById('topic-input');
    const jokeDisplay = document.getElementById('joke-display');

    const fetchPun = async () => {
        const topic = topicInput.value;

        // --- Frontend Edge Case Validation ---
        if (!topic.trim()) {
            jokeDisplay.innerHTML = '<p style="color: red;">Please enter a topic!</p>';
            return;
        }

        generateBtn.disabled = true;
        jokeDisplay.innerHTML = '<p>Thinking of a good one...</p>';

        try {
            const response = await fetch('http://localhost:5000/api/get-pun', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ topic: topic }),
            });

            const data = await response.json();

            // --- Handle both successful and error responses from the API ---
            if (!response.ok) {
                // Display the specific error message from the backend (e.g., "Jokes on this topic...")
                jokeDisplay.innerHTML = `<p style="color: red;">${data.error || 'An unknown error occurred.'}</p>`;
            } else {
                jokeDisplay.innerHTML = `<p>${data.pun}</p>`;
            }

        } catch (error) {
            console.error('Error fetching pun:', error);
            jokeDisplay.innerHTML = '<p style="color: red;">Sorry, my humor module is offline. Please try again!</p>';
        } finally {
            generateBtn.disabled = false;
        }
    };

    generateBtn.addEventListener('click', fetchPun);

    // Allow pressing Enter to generate a pun
    topicInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            fetchPun();
        }
    });
});