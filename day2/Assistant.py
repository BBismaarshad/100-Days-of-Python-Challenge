import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib

# Initialize Text-to-Speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set the voice (male/female)

def speak(audio):
    """Convert text to speech"""
    engine.say(audio)  # Convert the given audio string to speech
    engine.runAndWait()  # Wait until speech is finished

def wishMe():
    """Greet the user based on time"""
    hour = int(datetime.datetime.now().hour)  # Get the current hour
    if hour < 12:
        speak("Good Morning!")  # Greet user in the morning
    elif hour < 18:
        speak("Good Afternoon!")  # Greet user in the afternoon
    else:
        speak("Good Evening!")  # Greet user in the evening
    speak("I am Bisma. How can I assist you?")  # Introduce the assistant

def takeCommand():
    """Take voice input from user and return text"""
    r = sr.Recognizer()  # Initialize the recognizer
    with sr.Microphone() as source:  # Use the microphone as the audio source
        print("Listening...")
        r.pause_threshold = 1  # Set the pause threshold between words
        audio = r.listen(source)  # Listen to the audio input
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')  # Recognize the speech using Google's API
        print(f"User said: {query}\n")  # Print the recognized query
    except:
        print("Please say that again...")  # Handle if speech is not recognized
        return "None"  # Return None if there was an error in recognition
    return query.lower()  # Return the query in lowercase

def sendEmail(to, content):
    """Send email using SMTP"""
    try:
        # Set up the SMTP server and login
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Start the TLS encryption for security
        server.login('youremail@gmail.com', 'your-password')  # Log into the email account
        server.sendmail('youremail@gmail.com', to, content)  # Send the email
        server.close()  # Close the connection to the SMTP server
        speak("Email has been sent!")  # Confirm that the email was sent
    except:
        speak("Sorry, I couldn't send the email.")  # Error handling if email fails to send

def takeNotes():
    """Take notes from the user and save them"""
    speak("What should I write?")  # Ask the user what to note
    note = takeCommand()  # Take voice input for the note
    with open("notes.txt", "a") as file:  # Open the file in append mode
        file.write(note + "\n")  # Write the note to the file
    speak("Note saved.")  # Confirm that the note was saved

def readNotes():
    """Read saved notes"""
    try:
        with open("notes.txt", "r") as file:  # Open the notes file in read mode
            notes = file.read()  # Read the contents of the file
            speak("Your notes are as follows")  # Notify the user
            speak(notes)  # Read the notes aloud
    except FileNotFoundError:
        speak("No notes found.")  # Handle case where the file does not exist

if __name__ == "__main__":
    wishMe()  # Greet the user
    while True:
        query = takeCommand()  # Continuously listen for commands
        
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')  # Inform user that search is starting
            query = query.replace("wikipedia", "")  # Remove the word 'wikipedia' from the query
            results = wikipedia.summary(query, sentences=2)  # Search Wikipedia for the query
            speak("According to Wikipedia")  # Introduce the Wikipedia result
            speak(results)  # Read out the Wikipedia summary
        
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")  # Open YouTube in the browser
        
        elif 'open google' in query:
            webbrowser.open("google.com")  # Open Google in the browser
        
        elif 'play music' in query:
            music_dir = 'D:\\Music'  # Define the directory where music is stored
            songs = os.listdir(music_dir)  # List all songs in the directory
            os.startfile(os.path.join(music_dir, songs[0]))  # Play the first song in the list
        
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")  # Get the current time
            speak(f"The time is {strTime}")  # Read the time aloud
        
        elif 'email to' in query:
            try:
                speak("What should I say?")  # Ask the user for the email content
                content = takeCommand()  # Take the email content from the user
                to = "recipient@example.com"  # Specify the recipient email address
                sendEmail(to, content)  # Send the email
            except:
                speak("Unable to send email")  # Handle errors in email sending
        
        elif 'take notes' in query:
            takeNotes()  # Call the function to take notes
        
        elif 'read notes' in query:
            readNotes()  # Call the function to read notes
        
        elif 'exit' in query or 'stop' in query:
            speak("Goodbye!")  # Say goodbye when the program stops
            break  # Exit the loop and stop the program
