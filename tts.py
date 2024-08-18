from gtts import gTTS

text = "Is this your pencil?"
tts = gTTS(text=text, lang='en')
tts.save("audio1.wav")
