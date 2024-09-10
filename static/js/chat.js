
function autoResize(textarea) {
    textarea.style.overflow = 'hidden';
    
    textarea.style.height = 'auto';
    
    textarea.style.height = (textarea.scrollHeight) + 'px';
}


const textarea = document.getElementById('userInput');

textarea.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

function asyncDisplayMessage(sender, message, messageDiv = null) {
    var chatBox = document.getElementById("chatBox");
    
    if (!messageDiv) {
        messageDiv = document.createElement("div");
        messageDiv.className = sender === "User" ? "user-message" : "llm-message";
        chatBox.appendChild(messageDiv);
    }
    
    var formattedMessage = message.replace(/\n/g, '<br>');

    function linkify(inputText) {
        var urlRegex = /(https?:\/\/[^\s]+)/g;
        return inputText.replace(urlRegex, function(url) {
            return '<a href="' + url + '" target="_blank" style="text-decoration: underline;">' + url + '</a>';
        });
    }

    formattedMessage = linkify(formattedMessage);

    messageDiv.innerHTML += formattedMessage;
    chatBox.scrollTop = chatBox.scrollHeight;

    return messageDiv; 
}

async function asyncSendMessage(event) {
    event.preventDefault();

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const userInput = document.getElementById('userInput').value;
    const ragMode = document.getElementById('ragMode').value;

    asyncDisplayMessage('User', userInput);

    document.getElementById('userInput').value = '';

    const formData = new FormData();
    formData.append('question', userInput);
    formData.append('rag_mode', ragMode);

    const response = await fetch('/chat/astreaming/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let messageDiv = null;

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        messageDiv = asyncDisplayMessage('LLM', chunk, messageDiv);
    }
}


function sendMessage(event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var inputField = document.getElementById("userInput");
    var message = inputField.value.trim();
    
    if (message === "") {
        return;
    }

    let formData = new FormData();
    formData.append('question', message);
    displayMessage("User", message);
    
    // Send the POST request with the CSRF token
    fetch("/send-question/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": csrftoken,
            'Accept': 'application/json',  
        }  
    }).then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            displayMessage("LLM", data.answer);
        } else {
            console.error('Error in response:', data);
        }
    })
    .catch(error => console.error('Error:', error));

    inputField.value = "";  // Clear the input field
}

function displayMessage(sender, message) {
    var chatBox = document.getElementById("chatBox");
    var messageDiv = document.createElement("div");

    var formattedMessage = message.replace(/\n/g, '<br>');

    function linkify(inputText) {
        var urlRegex = /(https?:\/\/[^\s]+)/g;
        return inputText.replace(urlRegex, function(url) {
            return '<a href="' + url + '" target="_blank" style="text-decoration: underline;">' + url + '</a>';
        });
    }

    formattedMessage = linkify(formattedMessage);

    messageDiv.innerHTML = formattedMessage;
    messageDiv.className = sender === "User" ? "user-message" : "llm-message";
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

