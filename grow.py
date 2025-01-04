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
    payload = json.dumps({
  "query": "query GetSnsShare($actionType: SnsShareActionType!, $snsType: SnsShareSnsType!) {\\n  getSnsShare(actionType: $actionType, snsType: $snsType) {\\n    lastShareBonusAt\\n    isExistNewBonus\\n  }\\n}",
  "variables": {
    "actionType": "GROW",
    "snsType": "X"
  },
  "operationName": "GetSnsShare"
})
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    return result

async def initiate(access_token):
    url = "https://hanafuda-backend-app-520478841386.us-central1.run.app/graphql"
    
    # The payload should be a dictionary, not a string
    payload = {
      "query": "mutation ExecuteGrowAction {\n  executeGrowAction {\n    baseValue\n    leveragedValue\n    totalValue\n    multiplyRate\n  }\n}",
      "operationName": "ExecuteGrowAction"
    }
    
    headers = {
      'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
      'Accept': "application/graphql-response+json, application/json",
      'Content-Type': "application/json",
      'accept-language': "en-US,en;q=0.9",
      'authorization': f"Bearer {access_token}",
      'origin': "https://hanafuda.hana.network",
      'priority': "u=1, i",
      'referer': "https://hanafuda.hana.network/",
      'sec-ch-ua': "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
      'sec-ch-ua-mobile': "?0",
      'sec-ch-ua-platform': "\"Windows\"",
      'sec-fetch-dest': "empty",
      'sec-fetch-mode': "cors",
      'sec-fetch-site': "cross-site"
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

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

    for i in range(100000000):
        for token in refresh_tokens:
            try:
                access_token = await get_token(token)
                initiategrow = await initiate(access_token)

                if 'data' in initiategrow and 'executeGrowAction' in initiategrow['data']:
                    points = initiategrow['data']['executeGrowAction']['totalValue']
                    print_message(f'Grow Successfully earned Points: {points}', "success")
                else:
                    print_message('Initiate Grow Action did not return valid data.', "error")

            except ValueError as e:
                pass
            except KeyError as e:
                pass
            except Exception as e:
                pass
                

if __name__ == "__main__":
    asyncio.run(main())
