import streamlit as st
from PIL import Image
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
import cv2
import colorsys
from collections import Counter

# Helper function to map hues to musical notes
def hue_to_note(hue):
    scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    index = int(hue * 12) % 7  # Scale over one octave with 7 notes
    return scale[index]

# Extract dominant colors and generate a melody
def extract_dominant_colors(image, num_colors):
    image = image.resize((100, 100))
    pixels = list(image.getdata())
    colors = Counter(pixels)
    most_common = colors.most_common(num_colors)

    # Assuming each 'color' in 'most_common' is directly the RGB tuple
    notes = [hue_to_note(colorsys.rgb_to_hsv(color[0]/255., color[1]/255., color[2]/255.)[0]) for color, _ in most_common]
    return notes

# Synthesize audio from notes
def synthesize_audio(notes):
    note_frequencies = {'C': 261.63, 'D': 293.66, 'E': 329.63, 'F': 349.23, 'G': 392.00, 'A': 440.00, 'B': 493.88}
    melody = AudioSegment.silent(duration=0)
    for note in notes:
        generator = Sine(note_frequencies[note])
        note_segment = generator.to_audio_segment(duration=200)  # Each note lasts 500 ms
        melody += note_segment
    return melody

# Streamlit user interface
st.title('Image to Music Converter')
uploaded_file = st.file_uploader("Upload an image and convert it into music.", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    st.write("Generating music based on the dominant colors in the image...")
    num_colors = st.slider("Number of colours to extract", 0, 100, 5)
    notes = extract_dominant_colors(image, num_colors)
    audio = synthesize_audio(notes)
    
    # Save and display the audio
    audio_path = './generated_music.wav'
    audio.export(audio_path, format='wav')
    st.audio(audio_path, format='audio/wav')