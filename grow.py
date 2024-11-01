import requests
import asyncio
import json
import sys
from colorama import init, Fore, Style
import os
from datetime import datetime

# Initialize colorama
init(autoreset=True)

# Define colors for printing
red = Fore.LIGHTRED_EX
blue = Fore.LIGHTBLUE_EX
green = Fore.LIGHTGREEN_EX
yellow = Fore.LIGHTYELLOW_EX
black = Fore.LIGHTBLACK_EX
white = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL
magenta = Fore.LIGHTMAGENTA_EX

async def get_token(refresh_token):
    url = "https://securetoken.googleapis.com/v1/token?key=AIzaSyDipzN0VRfTPnMGhQ5PSzO27Cxm3DohJGY"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    response = requests.post(url, data=payload)
    token_data = response.json()
    access_token = token_data.get('access_token')
    return access_token

async def Commit(access_token):
    url = "https://hanafuda-backend-app-520478841386.us-central1.run.app/graphql"
    payload = {
        "operationName": "commitGrowAction",
        "query": """
            mutation commitGrowAction {
                commitGrowAction
            }
        """
    }
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    return result

async def initiate(access_token):
    url = "https://hanafuda-backend-app-520478841386.us-central1.run.app/graphql"
    payload = {
        "operationName": "issueGrowAction",
        "query": """
            mutation issueGrowAction {
                issueGrowAction
            }
        """
    }
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    return result

def load_accounts(file_path):
    """Load the list of accounts from a file and return it as a list."""
    try:
        with open(file_path, 'r') as f:
            refresh_token = [line.strip() for line in f if line.strip()]
        return refresh_token
    except FileNotFoundError:
        print(f"{red}Error: File '{file_path}' not found.{reset}")
        sys.exit(1)

def print_message(message, message_type='info'):
    timestamp = datetime.now().strftime("%H:%M:%S")
    if message_type == 'success':
        formatted_message = f"[ {timestamp} ] {Fore.GREEN}{Style.BRIGHT}{message}{Style.RESET_ALL}"
    elif message_type == 'error':
        formatted_message = f"[ {timestamp} ] {Fore.RED}{Style.BRIGHT}{message}{Style.RESET_ALL}"
    else:
        formatted_message = f"[ {timestamp} ] {Fore.CYAN}{message}{Style.RESET_ALL}"
    print(formatted_message)

async def main():
    file_path = 'token.txt'
    refresh_tokens = load_accounts(file_path)
    if not refresh_tokens:
        print(f"{red}No accounts found in the file.{reset}")
        sys.exit(1)

    os.system('cls' if os.name == 'nt' else 'clear')
    
    banner = f"""
    {magenta}┓┏┏┓┳┓┏┓┏┓┳┳┳┓┏┓  {white}HanaFuda Auto Grow
    {magenta}┣┫┣┫┃┃┣┫┣ ┃┃┃┃┣┫  {green}Author : {white}MortyID
    {magenta}┛┗┛┗┛┗┛┗┻ ┗┛┻┛┛┗  {white}Github : {green}https://github.com/MortyID
    """
    print(banner)

    for i in range(10000):
        for token in refresh_tokens:
            try:
                access_token = await get_token(token)
                initiategrow = await initiate(access_token)

                if 'data' in initiategrow and 'issueGrowAction' in initiategrow['data']:
                    points = initiategrow['data']['issueGrowAction']
                    print_message(f'Grow Successfully earned Points: {points}', "success")

                    grow_commit = await Commit(access_token)
                    if 'data' in grow_commit and 'commitGrowAction' in grow_commit['data']:
                        print_message('Commit Successfully', "success")
                    else:
                        print_message('Commit Grow Action did not return valid data.', "error")
                else:
                    print_message('Initiate Grow Action did not return valid data.', "error")

            except ValueError as e:

                print_message(f"Value error occurred: {e}", "error")
            except KeyError as e:

                print_message(f"Key error occurred: {e}", "error")
            except Exception as e:

                print_message(f"An unexpected error occurred: {e}", "error")

if __name__ == "__main__":
    asyncio.run(main())
