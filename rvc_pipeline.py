import pyttsx3
import sounddevice as sd
import soundfile as sf
from flask import Flask, request, jsonify
from rvc_infer import rvc_convert

def text_to_wav(text, filename, voice_index=0, ):
    engine = pyttsx3.init(driverName='sapi5')
    
    voices = engine.getProperty('voices')
    if voice_index >= len(voices):
        print(f"Invalid voice index. Choose between 0 and {len(voices) - 1}. Using default voice.")
    else:
        engine.setProperty('voice', voices[voice_index].id)
    
    engine.setProperty('rate', 150)
    engine.save_to_file(text, filename)
    engine.runAndWait()

def play_audio(filename):
    data, samplerate = sf.read(filename)
    sd.play(data, samplerate)
    sd.wait()

def tts(message):
    engine = pyttsx3.init(driverName='sapi5')
    voices = engine.getProperty('voices')
    print("Available voices:")
    for index, voice in enumerate(voices):
        print(f"{index}: {voice.name}")

    voice_index = 1
    text = message
    audio_file_name = "out.wav"
    
    text_to_wav(text, 
                audio_file_name, 
                voice_index)
    
    return audio_file_name

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def api_call():
    file = request.get_json()['file']
    pitch = request.get_json()['key']
    model = request.get_json()['model']

    print(f"audio file path: {file}")
    # play_audio(audio_file_name)
    rvc_convert(model_path=model,
                f0_up_key=pitch,
                input_path=file)

    return jsonify({"status": "done"})

if __name__ == '__main__':
    app.run()
