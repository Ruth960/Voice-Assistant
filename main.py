import pyttsx3
import speech_recognition as sr
import  datetime
import wikipedia
import webbrowser
import os
import smtplib     
#import pyautogui
import pyautogui
from PIL import Image, ImageTk
import tkinter as tk
import cv2

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id)
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!Hope you had a good sleep, ")

    elif hour>=12 and hour<18:
        speak("Good Afternoon! Hope you are having a good day, ")

    else:
        speak("Good Evening! Hope you had a good day,")

    speak("How can I help  you today?")

def takeCommand():


    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f'User said: {query}\n')

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query

def play_music(action=None, current_track_index=0):
    
    music_dir = 'https://wynk.in/u/e4Lp1FqAy'  #Change the path to you music folder
    music_files = [f for f in (music_dir)]
    #music_files = [f for f in os.listdir(music_dir)]

    if len(music_files) == 0:
        speak("No music found.")
        return

    speak("Playing music.")
    selected_music = os.path.join(music_dir, music_files[current_track_index]) 
    if action == 'next':
        current_track_index = (current_track_index + 1) % len(music_files)
    elif action == 'previous':
        current_track_index = (current_track_index - 1) % len(music_files)
    
    


    try:
        os.system(f'start {selected_music}')  
    except Exception as e:
        print("Error playing music:", str(e))
        speak("Sorry, I couldn't play music at the moment.")
def pause_music():
    try:
        pyautogui.press('playpause') 
        speak("Music paused.")
    except Exception as e:
        print("Error pausing music:", str(e))
        speak("Sorry, I couldn't pause the music at the moment.")

# Function to resume music
def resume_music():
    try:
        pyautogui.press('playpause') 
        speak("Resuming music.")
    except Exception as e:
        print("Error resuming music:", str(e))
        speak("Sorry, I couldn't resume the music at the moment.")

def camera():
    cap = cv2.VideoCapture(0)  
    image_count = 0  # counting the images taken
    root = tk.Tk()
    root.title("Camera")

    def save_image():
        nonlocal image_count
        ret, frame = cap.read()
        image_count += 1
        img_name = f"img_{image_count}.png" 
        cv2.imwrite(img_name, frame)  # Save the captured frame as an image

    def video_stream():
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=img)
        label.config(image=img)
        label.img = img
        label.after(10, video_stream)

    label = tk.Label(root)
    label.pack()

    # Button to capture and save an image
    capture_button = tk.Button(root, text="camera", command=save_image)
    capture_button.pack()

    video_stream()
    root.mainloop()

    # closecamera when done
    cap.release()


if __name__ == "_main_":
    wishMe()
    while True:
    # if 1:

        query = takeCommand().lower()

        if 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open file manager' in query:
            webbrowser.open("www.filemanager.com")

        elif 'open google' in query:
            webbrowser.open("google.com")   

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'increase volume' in query:
            pyautogui.press("volumeup")

        elif 'reduce volume' in query:
            pyautogui.press("volumedown")
        
        elif 'mute audio' in query or 'mute' in query:
            pyautogui.press("volumemute")
            
        elif 'unmute audio ' in query or 'unmute' in query:
            pyautogui.press("volumeunmute")
        elif 'play music'in query:
            play_music()
        elif 'stop music' in query:
            pause_music()

        elif 'continue playing' in query or 'play again' in query:
            resume_music()
        elif 'next song' in query:
          play_music(action='next')  
        elif 'play previous song' in query:
          play_music(action='previous') 
        elif 'open camera' in query:
            speak("opening camera.")
            camera() 
            speak("camera closed")
