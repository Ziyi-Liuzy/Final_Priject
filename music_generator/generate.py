
from midiutil import MIDIFile
import random
import os

def generate_midi(keywords, emotion, file_name="output", output_dir='static/midi'):
    maintonic = 60  # middle C
    tonic = maintonic
    track = 0
    channel = 0
    
    # Set music parameters and instruments according to mood
    if emotion == "joy":
        tempo = random.randint(120, 160)
        volume = 90 
        key_offset = 0  # Major
        instrument = 76  # Pan Flute
        chord_type = "consonant"  # Harmony Chords
        tonic = 60  # Middle C
    elif emotion == "anger":
        tempo = random.randint(110, 130)
        volume = 110
        key_offset = -5  # Minor
        instrument = 48  # Timpani
        chord_type = "dissonant"  # Dissonant Chords
        tonic = 55  # Lower the pitch
    elif emotion == "sadness":
        tempo = random.randint(60, 80)
        volume = 60
        key_offset = -3  # Minor
        instrument = 43  # Cello (大提琴)
        chord_type = "dissonant"
        tonic = 50  # Lower pitch
    elif emotion == "fear":
        tempo = random.randint(100, 130)
        volume = 70
        key_offset = -4  # Minor
        instrument = 79  # Whistle（哨）
        chord_type = "dissonant"
        tonic = 48  # Lower pitch
    else:  # neutral
        tempo = random.randint(90, 110)
        volume = 70
        key_offset = 0  # Unclear major or minor key
        instrument = 16  # 	Dulcimer
        chord_type = "consonant"
        tonic = 60  # Middle C

    # Initializing MIDI
    beats_per_measure = random.randint(3, 7)
    # Initial time
    time = beats_per_measure + 1 
    # Create a MIDI file with two tracks (instrument and drums)
    MyMIDI = MIDIFile(2)
    MyMIDI.addTempo(track, 0, tempo)
    # Set the instrument timbre
    MyMIDI.addProgramChange(track, channel, 0, instrument) 

    # Define note mapping (keywords)
    char_assoc = {
        "a": -7, "b": -14, "c": 21, "d": 4, "e": 0, "f": -9, "g": -8, "h": 16, "i": -5, "j": 15, 
        "k": 24, "l": 5, "m": 17, "n": -3, "o": -12, "p": -17, "q": 11, "r": 7, "s": 12, "t": 10, 
        "u": -3, "v": 8, "w": 9, "x": 13, "y": 6, "z": 18
    }

    # Set a basic rhythm pattern
    basic_rhythm = [0.5, 0.5, 0.5, 1] 

    # Generate notes based on keywords
    time = 0
    rhythm_index = 0

# Iterate through each keyword to create musical notes
    for word in keywords:
        for char in word:
            if char.lower() in char_assoc:
                pitch = tonic + char_assoc[char.lower()] + key_offset
                duration = basic_rhythm[rhythm_index % len(basic_rhythm)]
                if chord_type == "consonant":
                    # Major triad
                    MyMIDI.addNote(track, channel, pitch, time, duration, volume)
                    MyMIDI.addNote(track, channel, pitch + 4, time, duration, volume)
                    MyMIDI.addNote(track, channel, pitch + 7, time, duration, volume)
                elif chord_type == "dissonant":
                    # Minor triads
                    MyMIDI.addNote(track, channel, pitch, time, duration, volume)
                    MyMIDI.addNote(track, channel, pitch + 3, time, duration, volume)
                    MyMIDI.addNote(track, channel, pitch + 7, time, duration, volume)

                time += duration
                rhythm_index += 1

    # Generate drum track
    drum_pitch = 35 if emotion in ["joy", "anger"] else 42 if emotion == "sadness" else 48 if emotion == "fear" else 31
    drum_volume = 120 if emotion in ["joy", "anger"] else 50 if emotion == "sadness" else 90 if emotion == "fear" else 70
    MyMIDI.addProgramChange(1, 9, 0, 8)
    MyMIDI.addTrackName(1, 0, "drums")
    for i in range(1, beats_per_measure + 1):
        MyMIDI.addNote(1, 9, drum_pitch, i, 0.25, drum_volume)

    os.makedirs(output_dir, exist_ok=True)

    # Saving MIDI Files
    midi_filename = f"{file_name}_music.mid"
    midi_path = os.path.join(output_dir, midi_filename)
    with open(midi_path, "wb") as output_file:
        MyMIDI.writeFile(output_file)

    print(f"MIDI file generated: {midi_path}")
    return midi_filename 
