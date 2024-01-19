import os  # Os.system() Automatically runs the command
import webbrowser
import smtplib
import pywhatkit
import pyautogui
import pyjokes
import wikipedia
import datetime
import pyttsx3 as pyt
import speech_recognition as sr
import openai
from config import apikey
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

engine = pyt.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

window = Tk()  # basically, program starts from here!!
window.title("Eva's Music Player")
window.geometry("500x300")

pygame.mixer.init()  # initialize pygame music mixer to allow us to play audio
# todo: create a menu bar or nav bar where we add some songs
menubar = Menu(window)
window.config(menu=menubar)  # set the window to a menu bar


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want too quit?"):
        window.destroy()


songs = []
current_song = ""
paused = False


def load_music():
    global current_song
    window.directory = filedialog.askdirectory()

    for song in os.listdir(window.directory):
        name, ext = os.path.splitext(song)
        if ext == '.mp3':
            songs.append(song)

    for song in songs:
        songs_list.insert("end", song)

    songs_list.selection_set(0)
    current_song = songs[songs_list.curselection()[0]]


def play_music():
    global current_song, paused

    if not paused:
        pygame.mixer.music.load(os.path.join(window.directory, current_song))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.pause()
        paused = False


def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True


def next_music():
    global current_song, paused

    try:
        songs_list.selection_clear(0, END)
        songs_list.selection_set(songs.index(current_song)+1)
        current_song = songs[songs_list.curselection()[0]]
        play_music()
    except Exception as ex:
        print(ex)
        pass


def prev_music():
    global current_song, paused

    try:
        songs_list.selection_clear(0, END)
        songs_list.selection_set(songs.index(current_song)-1)
        current_song = songs[songs_list.curselection()[0]]
        play_music()

    except Exception as ex:
        print(ex)
        pass


MyPlaylist = Menu(menubar, tearoff=False)
MyPlaylist.add_command(label="Browse Music", command=load_music)
menubar.add_cascade(label='MyPlaylist', menu=MyPlaylist)

# todo: black box is of list of all songs
songs_list = Listbox(window,  bg="black", fg="white", width=100, height=15)
songs_list.pack()  # adds it onto window

play = PhotoImage(file='icons/start.png')
pause = PhotoImage(file='icons/pause.png')
stop = PhotoImage(file='icons/stop.png')
Next = PhotoImage(file='icons/next.png')
previous = PhotoImage(file='icons/previous.png')

# todo: create a frame a container too put widgets in it ,like a div or section
control_frame = Frame(window)
control_frame.pack()

play_btn = Button(control_frame, image=play, borderwidth=0, command=play_music)
pause_btn = Button(control_frame, image=pause, borderwidth=0, command=pause_music)
next_btn = Button(control_frame, image=Next, borderwidth=0, command=next_music)
previous_btn = Button(control_frame, image=previous, borderwidth=0, command=prev_music)


# Todo: too display on screen we can use grid in place of pack- all on the same line diff column

play_btn.grid(row=0, column=1, padx=7, pady=10)
pause_btn.grid(row=0, column=2, padx=7, pady=10)
next_btn.grid(row=0, column=3, padx=7, pady=10)
previous_btn.grid(row=0, column=0, padx=7, pady=10)

window.protocol("WM_DELETE_WINDOW", on_closing)

# window.mainloop()  # just runs our program


def sendEmail(too, cont):
    server = smtplib.SMTP('smntp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password-here')
    server.sendmail('youremail@gmail.com', too, cont)
    server.close()


def wishme():
    global hour
    hour = int(datetime.datetime.now().hour)
    if (hour >= 0) and hour < 12:
        speak("Hello Sir, Good Morning!")
    elif (hour >= 12) and hour < 18:
        speak("Hello Sir, Good Afternoon!")
    else:
        speak("Hello Sir, Good Evening!")

    speak("I am Eva Your A.I , Please tell me How May I Help You")


chatStr = ""


def chat(queri):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Mate: {queri}\nEva: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    speak(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def takeCommand():
    # it takes microphone input from the user and returns string output
    r = sr.Recognizer()

    with sr.Microphone() as source:
        # seconds of non-speaking audio before a phrase is considered complete
        audio = r.listen(source)
    try:
        print("Recognition...")
        queri = r.recognize_google(audio,
        language='en-IN')  # Performs speech recognition on ``audio_data instances`` , using the Google Speech Recognition API.
        print(f"User said:{queri}")
        return queri
    except Exception as ex:
        print(ex)
        return "Some Error Occurred. Sorry from Eva"


if __name__ == "__main__":  # main code start from here
    print("Welcome too Eva's AI")
    wishme()
    while True:
        print("Listening...")
        query = takeCommand().lower()

        # todo: Add more sites
        sites = [["youtube", "https://www.youtube.com"], ["google", "https://www.google.in"],
                 ["wikipedia", "https://www.wikipedia.com"]]
        for site in sites:

            if f"open {site[0]}" in query:
                speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        # logic for executing tasks based on query
        if 'wikipedia' in query:
            try:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According too wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                print(e)
                speak(f"Sorry sir. I am not able too search for {query}")

        elif 'email to Dipesh' in query:
            try:
                speak("what should I say?")
                content = takeCommand()
                to = "dipeshmate97@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry sir. I am not able too send this email")

        elif 'playlist' in query:

            try:
                speak("Sure Sir, You have to Select a Song to play from your Playlist")
                window.mainloop()
                takeCommand()

            except Exception as e:
                print(e)
                window.destroy()
                takeCommand()

        elif 'stop music' in query:
            speak("Music Stop Sir")
            pause_music()

        elif 'play' in query:
            query = query.replace('play', '')
            speak('playing' + query)
            pywhatkit.playonyt(query)

        elif 'open notepad' in query:
            speak("opening Notepad Application Sir...")
            notePad = "C:\\Windows\\System32\\notepad.exe"
            os.startfile(notePad)
            while True:
                notepadQuery = takeCommand().lower()
                if "paste" in notepadQuery:
                    pyautogui.hotkey('ctrl', 'v')
                    speak("Done Sir!")
                elif "save this file" in notepadQuery:
                    pyautogui.hotkey('ctrl', 's')
                    speak("Sir, Please Specify a name for this file")
                    savingNotepadQuery = takeCommand()
                    pyautogui.write(savingNotepadQuery)
                    pyautogui.press('enter')
                elif 'type' in notepadQuery:
                    speak("Please Tell me what should i write...")
                    while True:
                        writeInNotepad = takeCommand()
                        if writeInNotepad == 'exit typing':
                            writeInNotepad = takeCommand()
                            speak("Done sir")
                        else:
                            pyautogui.write(writeInNotepad)
                elif 'exit notepad' or 'close Notepad' in notepadQuery:
                    speak("quiting Notepad Sir...")
                    pyautogui.hotkey('ctrl', 'w')
                    break

        # elif 'play song' in query or 'play a song' in query:
        #     speak("yes Sir Please Wait a Moment")
        #     songs = os.listdir('C:\\Users\\D-Mate\\Documents\\pythonProject\\myVirtualAssistance\\Musics')
        #     os.startfile(os.path.join('C:\\Users\\D-Mate\\Documents\\pythonProject\\myVirtualAssistance\\Musics', songs[0]))

        elif 'pause' in query:
            pyautogui.press('space')
            speak("Done Sir")

        elif 'joke' in query:
            joke = pyjokes.get_joke()
            print(joke)
            speak(joke)

        # todo: Add the time
        elif 'the time' in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            speak(f"Sir, the time is, {hour} hour, {minute} minutes")

        elif 'open VS code'.lower() in query.lower():
            copePath = "C:\\Users\\D-Mate\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(copePath)

        elif 'thank you' in query:
            speak("Your Welcome Sir! Any Other Help I Can do For You Sir!")

        elif 'bye-bye' in query:
            speak("Bye Bye Sir!")
            exit()

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            # 'chat' in query.lower():
            print('Chatting')
            chat(query)
