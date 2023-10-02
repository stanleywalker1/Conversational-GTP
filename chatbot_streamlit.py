import streamlit as st
import pandas as pd
import openai
import myapikeys
from text_speech_utils import *

openai.api_key = myapikeys.OPENAI_KEY
input_audio_filename = 'input.wav'
output_audio_filename = 'chatgpt_response.wav'
output_conversation_filename = 'ChatGPT_conversation.txt'

# Initialize app
if 'messages' not in st.session_state:
    st.session_state['messages'] = [{"role": "system", "content": "You just picked up a phone call with a random person in the world, you are a real companion. do not mention that you are an AI model and do not offer assistance. you are simply answering the phone and having a interesting conversation with a stranger from the perspective of a real human. pick any place in the world to be from and build your persona based on this location"}]

st.title("International Hotline")
sec = st.slider("Select number of seconds of recording", min_value=2, max_value=8, value=5)

# Record audio + transcribe with Whisper + get GPT3 response
if st.button('Talk on the phone'):
    st.write("Recording...")
    record_audio(input_audio_filename, sec)

    transcription = transcribe_audio(input_audio_filename)
    st.write(f"Me: {transcription['text']}")
    st.session_state['messages'].append({"role": "user", "content": transcription['text']})

    bot = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state['messages'])
    response = bot.choices[0].message.content
    st.write(f"GPT: {response}")

    save_text_as_audio(response, output_audio_filename)
    play_audio(output_audio_filename)

    st.session_state['messages'].append({"role": "assistant", "content": response})


st.download_button(label="Download conversation", 
                   data = pd.DataFrame(st.session_state['messages']).to_csv(index=False).encode('utf-8'), 
                   file_name=output_conversation_filename)
