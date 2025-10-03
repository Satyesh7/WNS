document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const generateBtn = document.getElementById('generate-btn');
    const topicInput = document.getElementById('topic-input');
    const storyDisplay = document.getElementById('story-display');
    
    // Sliders and their value displays
    const tempSlider = document.getElementById('temp-slider');
    const tempValue = document.getElementById('temp-value');
    const tokensSlider = document.getElementById('tokens-slider');
    const tokensValue = document.getElementById('tokens-value');

    // Update display values when sliders are moved
    tempSlider.addEventListener('input', () => tempValue.textContent = tempSlider.value);
    tokensSlider.addEventListener('input', () => tokensValue.textContent = tokensSlider.value);

    const generateStory = async () => {
        const topic = topicInput.value;
        if (!topic.trim()) {
            storyDisplay.innerHTML = `<p style="color: red;">Please enter a topic!</p>`;
            return;
        }

        generateBtn.disabled = true;
        storyDisplay.innerHTML = '<p>The storyteller is thinking...</p>';

        const payload = {
            topic: topic,
            temperature: parseFloat(tempSlider.value),
            max_tokens: parseInt(tokensSlider.value)
        };

        try {
            const response = await fetch('http://localhost:5000/api/generate-story', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            const data = await response.json();

            if (!response.ok) {
                storyDisplay.innerHTML = `<p style="color: red;">${data.error || 'An unknown error occurred.'}</p>`;
            } else {
                // Replace newlines with <br> tags for proper HTML rendering
                const formattedStory = data.story.replace(/\n/g, '<br>');
                storyDisplay.innerHTML = `<p>${formattedStory}</p>`;
            }

        } catch (error) {
            console.error('Error fetching story:', error);
            storyDisplay.innerHTML = '<p style="color: red;">The connection to the storyteller was lost. Please try again!</p>';
        } finally {
            generateBtn.disabled = false;
        }
    };

    generateBtn.addEventListener('click', generateStory);
    topicInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') generateStory();
    });
});