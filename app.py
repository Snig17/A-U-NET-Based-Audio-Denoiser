import streamlit
import os
import streamlit as st
import librosa
import librosa.display

import matplotlib
import matplotlib.pyplot as plt
import soundfile as sf
from prediction_denoise import prediction


def clean_temp():
    """
    Remove all files in specific paths
    """

    paths_to_remove = ['input/',
                       'output/']

    try:
        for path in paths_to_remove:
            for f in os.listdir(path):
                if not 'README' in f:
                    os.remove(os.path.join(path, f))
    except Exception as e:
        print(e)


if __name__ == '__main__':

    os.makedirs('input', exist_ok=True)
    os.makedirs('output', exist_ok=True)

    clean_temp()  # Clean temporal files on each upload

    # General description

    st.title("Audio denoising - Speech Enhancement")
    st.text("")

    # Upload file
    st.subheader("- Choose an audio file")
    uploaded_file = st.file_uploader("Choose an audio file", type=[
        'wav', 'mp3', 'ogg'])

    if uploaded_file is not None:  # File > 0 bytes

        file_details = {"FileName": uploaded_file.name,
                        "FileType": uploaded_file.type,
                        "FileSize": uploaded_file.size}
        st.write(file_details)

        #######################
        # UPLOADED FILE
        #######################
        if (file_details['FileType'] in ('audio/wav', 'audio/x-wav') or
            file_details['FileType'] in ('audio/mp3', 'audio/mpeg') or
                file_details['FileType'] == 'audio/ogg'):

            if file_details['FileType'] in ('audio/mp3', 'audio/mpeg'):
                with open('input/noisy_voice_long_t2.mp3', 'wb') as f:
                    f.write(uploaded_file.getbuffer())

                data, samplerate = sf.read('input/noisy_voice_long_t2.mp3')
                sf.write('input/noisy_voice_long_t2.wav', data, samplerate)

            elif file_details['FileType'] == 'audio/ogg':
                with open('input/noisy_voice_long_t2.ogg', 'wb') as f:
                    f.write(uploaded_file.getbuffer())

                data, samplerate = sf.read('input/noisy_voice_long_t2.ogg')
                sf.write('input/noisy_voice_long_t2.wav', data, samplerate)

            else:
                with open('input/noisy_voice_long_t2.wav', 'wb') as f:
                    f.write(uploaded_file.getbuffer())

            st.subheader("Input audio:")

            # INPUT
            audio_file = open('input/noisy_voice_long_t2.wav', 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/wav')

            y, sr = librosa.load('input/noisy_voice_long_t2.wav')

            # Tempo and beat
            tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
            st.write('Estimated tempo: {:.2f} beats per minute'.format(tempo))

            # Waveplot
            fig, ax = plt.subplots(nrows=1, sharex=True, sharey=True)
            fig.set_figheight(4)
            fig.set_figwidth(16)
            librosa.display.waveplot(y, sr=sr)
            ax.set(title='Input audio')
            st.pyplot(fig)

            # Denoise prediction
            prediction("weights", "model_unet", "input/", "output/",
                       ["noisy_voice_long_t2.wav"], "denoise.wav", 8000, 1.0, 8064, 8064, 255, 63)

            # OUTPUT

            st.subheader("Output audio:")

            audio_file = open('output/denoise.wav', 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/wav')
            y, sr = librosa.load('output/denoise.wav')

            # Tempo and beat
            tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
            st.write('Estimated tempo: {:.2f} beats per minute'.format(tempo))

            # Waveplot
            fig, ax = plt.subplots(nrows=1, sharex=True, sharey=True)
            fig.set_figheight(4)
            fig.set_figwidth(16)
            librosa.display.waveplot(y, sr=sr)
            ax.set(title='Output audio')
            st.pyplot(fig)

        else:
            st.error("Unsupported file type. Please upload a .wav, .mp3, or .ogg file.")