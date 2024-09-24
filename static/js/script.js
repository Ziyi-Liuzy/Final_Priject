document.getElementById('textForm').addEventListener('submit', function(e) {
    e.preventDefault(); 
    const text = document.getElementById('textInput').value;

    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text })  // Send the user input text to the backend
    })
    .then(response => response.json())
    .then(data => {
        // Display extracted keywords
        document.getElementById('keywords').innerText = data.keywords.join(', ');

        // Display extracted emotions
        document.getElementById('emotion').innerText = data.emotion;

        // Set up MIDI file download link
        document.getElementById('midiLink').href = `/static/midi/${data.midi_path}`;

        // Setting up MIDI playback
        const midiPath = `/static/midi/${data.midi_path}`; 
        document.getElementById('playMIDI').setAttribute('onClick', `MIDIjs.play('${midiPath}');`);

        // Display results block
        document.getElementById('result').style.display = 'block';
    })
    .catch(error => console.error('Error:', error));
});
