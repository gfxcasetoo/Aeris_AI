# from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import keyboard
import asyncio
import requests
import os
import platform


os_type = platform.system()


env_vers = dotenv_values(".env")
GroqAPIKey = env_vers.get("GroqAPIKey")


classes = ["zCubwf", "hgkElc", "LTKOO sY7ric", "ZOLCW", "gsrt vk_bk FzvwSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
           "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe", "VQF4g",
             "qv3wpe", "kno-rdesc", "SPZz6b"]

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"


client = Groq(api_key=GroqAPIKey)

professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask."
]


messages = []


SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc"}]


def GoogleSecrch(topic):
    search(topic)
    return True


def Content(topic):
    def OpenNotepad(file):
        if os_type == "Windows":
            subprocess.Popen(["notepad", file])
        elif os_type == "Darwin":
            subprocess.Popen(["open", "-a", "TextEdit", file])
        else:
            subprocess.Popen(["nano", file])

    def ContentWriteAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer
    
    topic = topic.replace("content ", "").strip()

    data_dir = "Data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    file_path = os.path.join(data_dir, f"{topic.lower().replace(' ', '_')}.txt")

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(ContentWriteAI(topic))
    except Exception as e:
        print(f"Error writing file: {e}")
        return False

    OpenNotepad(file_path)
    return True

def YouTubeSearch(topic):
    url4Search = f"https://www.youtube.com/results?search_query={topic}"
    webbrowser.open(url4Search)
    return True

def PlayYouTube(query):
    print(f"Playing {query} on YouTube...")  # Print when playing a video
    playonyt(query)
    return True

def OpenApp(app, sess=requests.session()):
    try:
        print(f"Trying to open {app} on {os_type}...")  

        if os_type == "Windows":
            # Try opening using 'start'
            result = subprocess.run(f'start {app}', shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Successfully opened {app} using 'start'.")
                return True
            
            # Try finding the app with 'where'
            result = subprocess.run(["where", app], capture_output=True, text=True, shell=True)
            if result.stdout:
                subprocess.run(["start", "", app], shell=True)
                print(f"Successfully opened {app} using 'where' command.")
                return True
            
            # Try Windows Store Apps
            store_check = subprocess.run(["powershell", "-Command", f"Get-AppxPackage -Name *{app}*"],
                                         capture_output=True, text=True, shell=True)
            if store_check.stdout:
                subprocess.run(["explorer", f"shell:AppsFolder\\{app}.exe"], shell=True)
                print(f"Successfully opened {app} from Windows Store.")
                return True

        elif os_type == "Darwin":  # macOS
            result = subprocess.run(["osascript", "-e", f'tell application \"{app}\" to activate'],
                                    capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Successfully opened {app} on macOS.")
                return True

        else:  # Linux
            result = subprocess.run(["which", app], capture_output=True, text=True)
            if result.stdout.strip():
                subprocess.run([app])
                print(f"Successfully opened {app} on Linux.")
                return True

    except Exception as e:
        print(f"Error opening {app}: {e}")

    print(f"Could not find {app}, searching online...")
    webopen(f"https://www.google.com/search?q={app}")
    return False


def CloseApp(app):
    print(f"Closing {app}...")  # Print when closing an app
    try:
        if os_type == "Windows":
            subprocess.run(["taskkill", "/F", "/IM", f"{app}.exe"], shell=True)
        else:
            subprocess.run(["pkill", "-f", app])
        return True
    except Exception as e:
        print(f"Error closing {app}: {e}")
        return False


def System(command):
    print(f"Executing system command: {command}...")  # Print for system actions

    def mute():
        if os_type == "Windows":
            keyboard.press_and_release("volume mute")
        else:
            subprocess.run(["osascript", "-e", 'set volume output muted true'])

    def unmute():
        if os_type == "Windows":
            keyboard.press_and_release("volume mute")
        else:
            subprocess.run(["osascript", "-e", 'set volume output muted false'])

    def volume_up():
        if os_type == "Windows":
            keyboard.press_and_release("volume up")
        else:
            subprocess.run(["osascript", "-e", 'set volume output volume ((output volume of (get volume settings)) + 10)'])

    def volume_down():
        if os_type == "Windows":
            keyboard.press_and_release("volume down")
        else:
            subprocess.run(["osascript", "-e", 'set volume output volume ((output volume of (get volume settings)) - 10)'])

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    return True



async def TransletAndExecute(commands: list[str]):
    funcs = []

    for command in commands:
        if command.startswith("open"):
            if "open it" in command:
                pass
            if "open file" in command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)
        elif command.startswith("general"):
            pass

        elif command.startswith("realtime"):
            pass

        elif command.startswith("close"):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)

        elif command.startswith("play"):
            fun = asyncio.to_thread(PlayYouTube, command.removeprefix("play "))
            funcs.append(fun)

        elif command.startswith("content"):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)

        elif command.startswith("google search"):
            fun = asyncio.to_thread(GoogleSecrch, command.removeprefix("google search "))
            funcs.append(fun)

        elif command.startswith("youtube search"):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)

        elif command.startswith("system"):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)

        elif command in ["mute", "unmute", "volume up", "volume down"]:
            fun = asyncio.to_thread(System, command)
            funcs.append(fun)


        else:
            print(f"No Function Found, for {command}")
    
    return await asyncio.gather(*funcs)

    # for result in results:
    #     if isinstance(result, str):
    #         yield result
    #     else:
    #         yield result

async def Automation(commands: list[str]):
    await TransletAndExecute(commands)
    return True 

if __name__ == "__main__":
    asyncio.run(Automation(["content song for me"]))