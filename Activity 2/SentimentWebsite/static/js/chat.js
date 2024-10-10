const chatBox = document.getElementById('chat-box');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const timerDiv = document.getElementById('timer');
const secondsSpan = document.getElementById('seconds');
const loadingDiv = document.getElementById('loading');

let timer; // Variable to hold the timer
let seconds = 0; // Time elapsed in seconds

sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

async function sendMessage() {
    const userMessage = messageInput.value.trim();
    console.log("User message:", userMessage);  // Log the user message
    if (userMessage === "") {
        console.log("No message entered.");  // Log if no message is entered
        return;
    }

    // Display user message
    appendMessage(userMessage, 'user');
    messageInput.value = "";

    // Start the timer
    startLoading();
    startTimer();

    // Disable send button
    sendButton.disabled = true;

    try {
        // Send message to the server
        console.log("Sending message to server...");  // Log before sending the message
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        });

        if (!response.ok) {
            console.error('Network response was not ok:', response.statusText);  // Log any errors in response
            throw new Error('Network response was not ok: ' + response.statusText);
        }

        // Stop the timer
        stopLoading();
        clearInterval(timer);
        timerDiv.style.display = 'none'; // Hide the timer when done
        sendButton.disabled = false;

        const data = await response.json();
        console.log("Bot response received:", data.response);  // Log the bot's response

        const botMessage = data.response;

        // Display bot response
        appendMessage(botMessage, 'bot');
    } catch (error) {
        stopLoading();
        clearInterval(timer);
        appendMessage("Oops! Something went wrong. Please try again.", 'bot');
        sendButton.disabled = false; // Enable send button
    }
}

function startLoading() {
    loadingDiv.style.display = 'block'; // Show loading message
}

function stopLoading() {
    loadingDiv.style.display = 'none'; // Hide loading message
}

function startTimer() {
    let seconds = 0;
    timerDiv.style.display = 'block'; // Show the timer
    secondsSpan.textContent = seconds;

    timer = setInterval(() => {
        seconds++;
        secondsSpan.textContent = seconds; // Update the displayed seconds
    }, 1000);
}

function appendMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;  // Scroll to the bottom
}