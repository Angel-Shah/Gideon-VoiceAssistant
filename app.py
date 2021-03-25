from flask import Flask, render_template, request, redirect
import speech_recognition as sr
import pyttsx3

app = Flask(__name__)


@app.route("/", methods =["GET","POST"])
def index():
    transcript = ""
    if request.method == "POST":
        print("RECEIVED FORM DATA!!!!!!!!")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename =="":
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)

            transcript = recognizer.recognize_google(data,key=None)
            print(transcript)
  
    return render_template('index.html',transcript = transcript, isLive = False)

@app.route('/lol')
def liveSpeech():
    transcript =""

    recognizer = sr.Recognizer()
    talker = pyttsx3.init()
    talker.setProperty('rate',150)
    voices = talker.getProperty('voices')
    talker.setProperty('voice', voices[2].id)
   
    # for voice in voices:
    #     talker.setProperty('voice', voice.id)
    #     talker.say('Gideon is at your service sir')
    #     talker.say('What would you like')
    #     talker.say('The quick brown fox jumped over the lazy dog.')
    # talker.runAndWait()

    talker.say('Gideon is at your service sir')
    talker.say('What would you like')
    talker.runAndWait()


    with sr.Microphone() as source:
                print("Say something")

                while True:
                    audio = recognizer.listen(source)
                    try:
                        transcript = recognizer.recognize_google(audio)
                        firstWord = transcript.split(' ', 1)[0]
                        print("first word of your sentece was: {}".format(firstWord))
                        if firstWord == "Gideon":
                            if (len(transcript) == 6):
                                print("Yes sir? What would you like?")
                                talker.say("Yes sir? What would you like?")
                                talker.runAndWait()
                                while True:
                                    audio = recognizer.listen(source)
                                    transcript = recognizer.recognize_google(audio)
                                    if transcript:
                                        if(transcript == "shut down"):
                                            talker.say("shutting down now, until next time sir ...")
                                            talker.runAndWait()
                                            
                                            return redirect(url_for('index'))

                                        else:
                                            print("you said: {}".format(transcript))
                                            talker.say("you said: {}".format(transcript))
                                            talker.say("I have done it sir")
                                            talker.runAndWait()
                                        
                                    break
                                print("I have done it sir")
                            else:
                                mastersCommand = transcript[7:]
                                print("you said: {}".format(mastersCommand))
                                print("I have done it sir")
                                talker.say("you said: {}".format(mastersCommand))
                                talker.say("I have done it sir")
                                talker.runAndWait()

                    except:
                        print("...")

    return render_template('index.html',transcript = transcript, isLive = True)


if __name__ == "__main__":
    app.run(debug=True, threaded =True)