from gtts import gTTS

text = "Is this your pen?"
tts = gTTS(text=text, lang='en')
tts.save("audio1.mp3")
