import tls_client
from colorama import Fore
import threading
from faker import Faker
import random
import requests
session = requests.session()
fake = Faker()

def generateStreamableCreds():
    return ''.join(str(fake.last_name()) + '@gmail.com' + ':' + str(fake.last_name()) + str(random.randint(0, 9999))) # credentials generator script

class Creation:
    def __init__(self, creds: str):
        self.email, self.password = creds.split(':')
        self.headers = {
            'authority': 'ajax.streamable.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://streamable.com',
            'pragma': 'no-cache',
            'referer': 'https://streamable.com/',
            'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        }

    def createAccount(self):
        data = {
            'username': self.email,
            'password': self.password,
            'email': self.email,
            'verification_redirect': 'https://streamable.com?alert=verified',
        }
        response = session.post('https://ajax.streamable.com/users', headers=self.headers, json=data)
        if response.status_code == 200:
            print(f"{Fore.GREEN}[ + ] Created account! credentials: {self.email}:{self.password}{Fore.RESET}")
            with open("accounts.txt", "a") as f:
    f.write(f"{self.email}:{self.password}\n")
        else:
            print(f"{Fore.RED}[-] Unable to create account! credentials: {self.email}:{self.password}, Error: {response.text}, Errno: {response.status_code}")

def runner():
    Creation(generateStreamableCreds()).createAccount()

def run_in_thread(num_threads):
    while True:
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=runner)
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()

num_threads = 5
run_in_thread(num_threads)
