import streamlit as st
import torch
import numpy as np
from diffusers import AudioLDM2Pipeline, DPMSolverMultistepScheduler
import pyaudio
import scipy
import os.path
import librosa
import matplotlib.pyplot as plt

# Front-end layout
st.header("AI Musician", divider=False)
st.subheader("Give Me A Song Description", divider=False)

left, right = st.columns([3, 1], vertical_alignment="bottom")
prompt = left.text_input("Song description")
song_len = right.number_input("Song length (in seconds)")

# Prepare model pipeline
if "pipeline" not in st.session_state:
    model = "cvssp/audioldm2-music"
    pipe = AudioLDM2Pipeline.from_pretrained(model, torch_dtype=torch.float16)
    pipe.to("cuda")
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    st.session_state["pipeline"] = pipe

# Generate music
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=16000, output=True)
if prompt and song_len:
    with st.spinner("Generating, please wait... 🎶"):
        audios = st.session_state["pipeline"](
            prompt, 
            num_inference_steps=200,
            audio_length_in_s=int(song_len)
        ).audios
        for audio in audios:
            stream.write(audio.astype(np.float32))
            scipy.io.wavfile.write(prompt+"_output.wav", rate=16000, data=audio)


# Generate spectrogram
if(os.path.isfile(prompt+"_output.wav")):
    st.subheader("Generated Result", divider=False)

    y, sr = librosa.load(prompt+"_output.wav")
    D = np.abs(librosa.stft(y))**2
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)

    fig, ax = plt.subplots()
    S_dB = librosa.power_to_db(S, ref=np.max)
    img = librosa.display.specshow(S_dB, x_axis='time',
                            y_axis='mel', sr=sr,
                            fmax=8000, ax=ax)
    fig.colorbar(img, ax=ax, format='%+2.0f dB')
    ax.set(title='Mel-frequency spectrogram')

    fig.savefig(prompt+"_output.png")

    # Front-end layout
    st.image(prompt+"_output.png", caption=prompt)
    st.audio(prompt+"_output.wav")