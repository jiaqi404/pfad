import streamlit as st
import torch
import numpy as np
from diffusers import AudioLDM2Pipeline, DPMSolverMultistepScheduler
import pyaudio
import scipy

if "pipeline" not in st.session_state:
    model = "cvssp/audioldm2-music"
    pipe = AudioLDM2Pipeline.from_pretrained(model, torch_dtype=torch.float16)
    pipe.to("cuda")
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    # pipe.enable_model_cpu_offload()
    st.session_state["pipeline"] = pipe

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=16000, output=True)

if prompt := st.text_input("Give me a song description"):
    with st.spinner("AI musician is creating music for you, please wait..."):
        audios = st.session_state["pipeline"](
            prompt, 
            num_inference_steps=200,
            audio_length_in_s=60
        ).audios
        for audio in audios:
            stream.write(audio.astype(np.float32))
            scipy.io.wavfile.write(prompt+"_output.wav", rate=16000, data=audio)