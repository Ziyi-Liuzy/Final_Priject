from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from keyword_extraction import extract_keywords
from music_generator.generate import generate_midi
from text_emotion import predict_emotion
from text_emotion import load_pretrained_model, load_tokenizer

app = Flask(__name__)

MIDI_FOLDER = 'static/midi'
os.makedirs(MIDI_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = MIDI_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    text = data.get('text', '')

    # Extract keywords
    keywords = extract_keywords(text)

    # Predict the emotion
    # Loading the model and tokenizer
    model = load_pretrained_model()
    tokenizer = load_tokenizer()

    emotion = predict_emotion(text, model, tokenizer)

    # Generate MIDI File
    midi_filename = generate_midi(keywords, emotion, file_name="output")
    midi_path = os.path.join(app.config['UPLOAD_FOLDER'], midi_filename)

    # Check the file path
    if not os.path.exists(midi_path):
        return jsonify({'error': 'MIDI file not found'}), 500

    response = {
        'keywords': keywords,
        'emotion': emotion,
        'midi_path': midi_filename
    }
    return jsonify(response)

@app.route('/static/midi/<filename>')
def download_midi(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
