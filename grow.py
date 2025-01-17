import requests
import asyncio
import json
import sys
from colorama import init, Fore, Style
import os
from datetime import datetime
import time

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

async def getdata(access_token):
    url = "https://hanafuda-backend-app-520478841386.us-central1.run.app/graphql"
    payload = {
    'query': 'query GetGardenForCurrentUser {\n  getGardenForCurrentUser {\n    id\n    inviteCode\n    gardenDepositCount\n    gardenStatus {\n      id\n      growActionCount\n      gardenRewardActionCount\n    }\n    gardenMilestoneRewardInfo {\n      id\n      gardenDepositCountWhenLastCalculated\n      lastAcquiredAt\n      createdAt\n    }\n    gardenMembers {\n      id\n      sub\n      name\n      iconPath\n      depositCount\n    }\n  }\n}',
    'operationName': 'GetGardenForCurrentUser',
    }
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    return result

async def getname(access_token):
    url = "https://hanafuda-backend-app-520478841386.us-central1.run.app/graphql"
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
    json_data = {
    'query': 'query GetCurrentMinimizedUser {\n  currentMinimizedUser {\n    id\n    sub\n    name\n    iconPath\n  }\n}',
    'operationName': 'GetCurrentMinimizedUser',
    }
    response = requests.post(
    'https://hanafuda-backend-app-520478841386.us-central1.run.app/graphql',
    headers=headers,
    json=json_data,
    )
    response = response.json()
    response = response['data']['currentMinimizedUser']['name']
    return response

async def initiate(access_token):
    url = "https://hanafuda-backend-app-520478841386.us-central1.run.app/graphql"
    
    # The payload should be a dictionary, not a string
    grow_action_query = {
              "query": """
                  mutation executeGrowAction {
                      executeGrowAction(withAll: true) {
                          totalValue
                          multiplyRate
                      }
                      executeSnsShare(actionType: GROW, snsType: X) {
                          bonus
                      }
                  }
              """,
              "operationName": "executeGrowAction"
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
    response = requests.post(url, headers=headers, json=grow_action_query)
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
    elif message_type == 'warning':
        formatted_message = f"[ {timestamp} ] {Fore.YELLOW}{Style.BRIGHT}{message}{Style.RESET_ALL}"
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
                result_data  = await getdata(access_token)
                getnames     = await getname(access_token)
                print(f"{magenta}=========== {getnames} ===========")
                
                totalgrow    = result_data['data']['getGardenForCurrentUser']['gardenStatus']['growActionCount']
                if totalgrow > 0:
                    for i in range(totalgrow):
                        initiategrow = await initiate(access_token)

                        if 'data' in initiategrow and 'executeGrowAction' in initiategrow['data']:
                            points = initiategrow['data']['executeGrowAction']['totalValue']
                            print_message(f'Grow Successfully earned Points: {points}', "success")
                        else:
                            print_message('Initiate Grow Action did not return valid data.', "error")
                else:
                    print_message(f'Grow Action Count Empty.', "warning")
                    
            except ValueError as e:
                pass
            except KeyError as e:
                pass
            except Exception as e:
                pass
        print_message(f'Delay 20 Minutes For Looping.', "warning")
        time.sleep(20 * 60)
                

if __name__ == "__main__":
    asyncio.run(main())
