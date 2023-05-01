import os
import requests
import datetime
import random
import time
from bs4 import BeautifulSoup as bs

banner = '''
 ██▓███   ██▀███   ███▄    █ ▄▄▄█████▓  ██████  ▄████▄   ██▀███   ▄▄▄       ██▓███  ▓█████  ██▀███  
▓██░  ██▒▓██ ▒ ██▒ ██ ▀█   █ ▓  ██▒ ▓▒▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒▒████▄    ▓██░  ██▒▓█   ▀ ▓██ ▒ ██▒
▓██░ ██▓▒▓██ ░▄█ ▒▓██  ▀█ ██▒▒ ▓██░ ▒░░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▒██  ▀█▄  ▓██░ ██▓▒▒███   ▓██ ░▄█ ▒
▒██▄█▓▒ ▒▒██▀▀█▄  ▓██▒  ▐▌██▒░ ▓██▓ ░   ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ░██▄▄▄▄██ ▒██▄█▓▒ ▒▒▓█  ▄ ▒██▀▀█▄  
▒██▒ ░  ░░██▓ ▒██▒▒██░   ▓██░  ▒██▒ ░ ▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒ ▓█   ▓██▒▒██▒ ░  ░░▒████▒░██▓ ▒██▒
▒▓▒░ ░  ░░ ▒▓ ░▒▓░░ ▒░   ▒ ▒   ▒ ░░   ▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░▒▓▒░ ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░
░▒ ░       ░▒ ░ ▒░░ ░░   ░ ▒░    ░    ░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░  ▒   ▒▒ ░░▒ ░      ░ ░  ░  ░▒ ░ ▒░
░░         ░░   ░    ░   ░ ░   ░      ░  ░  ░  ░          ░░   ░   ░   ▒   ░░          ░     ░░   ░ 
            ░              ░                ░  ░ ░         ░           ░  ░            ░  ░   ░     
                                               ░                                                       

                                                                                       by cyb3rm4gus
'''

# function to scrape pics
def scrape_pics():

    print(banner);

    # get amount of scraped pics from user input
    amount_of_pics = int(input("Enter the number of pics to scrape: "))

    # get delay in ms from user input
    delay_in_ms = int(input("Enter the delay in milliseconds: "))

    # create a folder for the pics, use the mask "amount of pics + datetime" to name the folder
    now = datetime.datetime.now()
    folder_name = str(amount_of_pics) + "_" + now.strftime("%Y%m%d_%H%M%S")
    save_path = 'output/' + folder_name + '/'
    os.mkdir(save_path)

    # loop to scrape pics
    pics_saved = 0
    for i in range(amount_of_pics):
        # generate a random string of 6 characters
        rand_str = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))

        # request the url with the random string
        url = f"https://prnt.sc/{rand_str}"

        # Bypass cloudflare filter
        headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            print("An error occurred:", str(e))
            continue

        soup = bs(response.content, 'html.parser')

        nugget = soup.find('img', {'id': 'screenshot-image'})

        if nugget:
            img_src = nugget['src']
            print(f"Image {rand_str} found, saving...")

            try:
                img_response = requests.get(img_src, headers=headers)
            except Exception as e:
                print("An error occurred:", str(e))
                continue

            if len(img_response.content) == 503 or len(img_response.content) == 950:
                print(f"Image {rand_str} does not exist, skipping...")
                continue

            # save the image to the folder
            with open(f"{save_path}/{rand_str}.png", "wb") as f:
                f.write(img_response.content)
                pics_saved += 1
                print(f"Image {rand_str} saved successfully!")

        else:
            print(f"Image {rand_str} not found, skipping...")
            continue

        # delay before making next request
        time.sleep(delay_in_ms / 1000)


    # return how many actual pics were saved
    return pics_saved

# call the function and handle exceptions
try:
    pics_saved = scrape_pics()
    print(f"{pics_saved} pics were saved successfully!")
except Exception as e:
    print("An error occurred:", str(e))