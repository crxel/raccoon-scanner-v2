import re
import requests
import subprocess
import threading
import fade
from colorama import Fore
from mcstatus import JavaServer
import os
import pwinput


gre = Fore.GREEN
blu = Fore.BLUE
yel = Fore.YELLOW
red = Fore.RED
w = Fore.WHITE
p = Fore.MAGENTA

os.system('cls')
print(fade.pinkred('''
 ______     ______     ______     ______     ______     ______     __   __    
/\  == \   /\  __ \   /\  ___\   /\  ___\   /\  __ \   /\  __ \   /\ "-.\ \   
\ \  __<   \ \  __ \  \ \ \____  \ \ \____  \ \ \/\ \  \ \ \/\ \  \ \ \-.  \  
 \ \_\ \_\  \ \_\ \_\  \ \_____\  \ \_____\  \ \_____\  \ \_____\  \ \_\\"\_\ 
  \/_/ /_/   \/_/\/_/   \/_____/   \/_____/   \/_____/   \/_____/   \/_/ \/_/ 
                    Raccoon Scanner | Made by crxelty
'''))

def clean():
    print(f'{yel}[*] Cleaning ips.txt')
    with open('ips.txt', 'w') as i :
        i.write(fr'''
 __         ______     ______     ______    
/\ \       /\  __ \   /\  ___\   /\  ___\   
\ \ \____  \ \ \/\ \  \ \ \__ \  \ \___  \  
 \ \_____\  \ \_____\  \ \_____\  \/\_____\ 
  \/_____/   \/_____/   \/_____/   \/_____/ 
       Raccoon Logs | Made by crxelty''')
        print(f'{gre}[+] Cleaned!')

def main():
    while True:
            url = "https://minecraft-mp.com/servers/random/"
            r = requests.get(url)
            ips = re.findall(r'<strong>(.*?)</strong></button>', r.text)
            for ip in ips:
                    try:
                        res = re.sub(r':([^:]+)$',"",ip)
                        result = subprocess.run(f'ping -n 1 {res}', capture_output=True, text=True)
                        output = result.stdout
                        pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
                        r = re.findall(pattern, output)
                        r = str(list(set(r))).replace('[', '').replace(']', '').replace('\'', '')
                        if output != f'Ping request could not find host {result} Please check the name and try again.':
                            if r != '':
                                try:
                                    server = JavaServer.lookup(r)
                                    status = server.status()
                                    # query = server.query()
                                    if status.players.online > 1:
                                        print(f'{p}[{w}+{p}] {w}Found Server! {p}IP:{w} {r} {w}| {yel}Players:{w} {status.players.online} {w}| {p}Ping:{w} {status.latency}')
                                        with open('ips.txt', 'a') as i:
                                            i.write(f'\n=============================================\nDomain: {res}\nIP: {r}\nPlayers: {status.players.online}\nPing: {status.latency}')

                                    elif status.players.online < 1:
                                        pass
                                    
                                except Exception:
                                    pass

                            elif r == '':
                                pass

                    except Exception:
                        pass

clean()
threads = []
for i in range(200):
    t = threading.Thread(target=main)
    t.start()
    threads.append(t)