from flask import Flask, render_template, request, redirect
import speech_recognition as sr

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
                                while True:
                                    audio = recognizer.listen(source)
                                    transcript = recognizer.recognize_google(audio)
                                    if transcript:
                                        print("you said: {}".format(transcript))
                                        
                                    break
                                print("I have done it sir")
                            else:
                                print("you said: {}".format(transcript))
                                print("I have done it sir")

                    except:
                        print("...")

    return render_template('index.html',transcript = transcript, isLive = True)


if __name__ == "__main__":
    app.run(debug=True, threaded =True)