import speech_recognition as sr
import pyttsx3
import webbrowser
import traceback
import datetime
import pywhatkit
import smtplib

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print("leo:", text)
    engine.say(text)
    engine.runAndWait()

def send_email():
    try:
        speak("Whom should I send the email to? Please type the email address.")
        to = input("Enter recipient email: ")

        speak("What is the subject?")
        subject = input("Subject: ")

        speak("What should I say?")
        message = input("Message: ")

        # Replace with your email and password (App password if 2FA enabled)
        sender_email = "youremail@gmail.com"
        sender_password = "yourpassword"

        final_message = f"Subject: {subject}\n\n{message}"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to, final_message)
        server.quit()

        speak("Email has been sent successfully.")
    except Exception as e:
        speak("Sorry, I couldn't send the email.")
        print("Error:", e)

def processCommand(command):
    command = command.lower()
    print("Processing Command:", command)

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "search" in command:
        query = command.replace("search", "").strip()
        if query:
            speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("What should I search for?")

    elif "youtube" in command:
        query = command.replace("youtube", "").strip()
        if query:
            speak(f"Playing {query} on YouTube")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        else:
            speak("What should I play on YouTube?")

    elif "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time}")

    elif "date" in command:
        date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {date}")

    elif "send whatsapp" in command:
        try:
            number = input("Enter number (with +91 etc): ")
            speak("What is the message?")
            msg = input("Enter message: ")
            hour = datetime.datetime.now().hour
            minute = datetime.datetime.now().minute + 2
            pywhatkit.sendwhatmsg(number, msg, hour, minute)
            speak("Message scheduled successfully.")
        except Exception as e:
            speak("Sorry, I couldn't send the message.")
            print("Error:", e)

    elif "send email" in command or "email" in command:
        send_email()

    elif "exit" in command or "quit" in command or "stop" in command:
        speak("Goodbye, have a nice day!")
        exit()

    else:
        speak("Sorry, I didn't understand that.")

if __name__ == "__main__":
    speak("Initializing leo...")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word (say 'leo')...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=3)

            wake_word = recognizer.recognize_google(audio).lower()
            print("Heard:", wake_word)

            if "exit" in wake_word or "stop" in wake_word or "quit" in wake_word:
                speak("Shutting down. Goodbye!")
                break

            elif "leo" in wake_word:
                speak("Yes, I am listening.")

                with sr.Microphone() as source:
                    print("Speak your command...")
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=6)

                command = recognizer.recognize_google(audio)
                processCommand(command)

        except sr.WaitTimeoutError:
            print("Listening timed out.")
        except sr.UnknownValueError:
            print("Could not understand.")
        except sr.RequestError as e:
            print(f"API request error: {e}")
        except KeyboardInterrupt:
            speak("Shutting down manually. Goodbye!")
            break
        except Exception as e:
            print("Unexpected error:")
            traceback.print_exc()
