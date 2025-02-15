function startRecording() {
    fetch('/microphone')
        .then(response => response.json())
        .then(data => {
            if (data.transcript) {
                document.getElementById('result').innerText = "Command: " + data.transcript;
                controlRobotHand(data.transcript);
                updateHistory(data.transcript);
            } else {
                document.getElementById('result').innerText = "Error: " + data.error;
            }
        });
}

function stopRecording() {
    // Implement stop recording functionality if needed
    document.getElementById('result').innerText = "Recording stopped.";
}

function controlRobotHand(command) {
    fetch('/control', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ command: command }),
    });
}

function updateHistory(command) {
    const history = document.getElementById('history');
    const listItem = document.createElement('li');
    listItem.innerText = command;
    history.appendChild(listItem);
}