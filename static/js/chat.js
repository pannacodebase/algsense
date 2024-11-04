// Function to send a message and detect commands
function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();

    if (!message) return;

    // Display user's message in chat box
    displayUserMessage(message);

    // Determine which command is being issued
    if (isMarkerCommand(message)) {
        handleMarkerCommand(message);
    } else {
        handleChatMessage(message);
    }

    // Clear chat input
    chatInput.value = '';
}

// Function to display the user's message
function displayUserMessage(message) {
    const chatBoxBody = document.getElementById('chatBoxBody');
    const userMessage = document.createElement('p');
    userMessage.textContent = `You: ${message}`;
    chatBoxBody.appendChild(userMessage);
}

// Function to check if the message is a marker command
function isMarkerCommand(message) {
    return /\b(add|create) marker\b/i.test(message);
}

// Function to handle marker commands
function handleMarkerCommand(message) {
    // Send message to backend to generate coordinates
    fetch('/generate_marker', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        if (data.coords) {
            const coords = [data.coords[0], data.coords[1]]; // Adjust based on your return structure
            
            // Add the new marker to the map without refresh
            addMarkersToMap([{
                location: data.location || "New Marker", // Ensure 'location' is being set correctly
                latitude: coords[0],
                longitude: coords[1]
            
            }]);

            // Notify user in the chat box
            appendBotMessage(`Marker added: ${data.location || "New Marker"} at (${coords[0]}, ${coords[1]})`);
        } else {
            appendBotMessage("Could not generate coordinates.");
        }
    })
    .catch(error => console.error('Error:', error));
}

// Function to handle regular chat messages
function handleChatMessage(message) {
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        appendBotMessage(data.response);
    })
    .catch(error => console.error('Error:', error));
}

// Function to toggle the chat box visibility
function toggleChatBox() {
    const chatBox = document.getElementById("chatBox");
    if (chatBox) {
        chatBox.style.display = chatBox.style.display === "none" ? "block" : "none";
    }
}

// Ensure `sendMessage` is called when the user presses Enter in the input box
document.getElementById("chatInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});

// Function to append bot message in the chat box
function appendBotMessage(message) {
    const chatBoxBody = document.getElementById('chatBoxBody');
    const botMessage = document.createElement('p');
    botMessage.textContent = `Bot: ${message}`;
    chatBoxBody.appendChild(botMessage);
}
