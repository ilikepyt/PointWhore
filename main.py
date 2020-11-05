import os, time, praw, random, config, pyimgur, requests, webbrowser, traceback

reddit = praw.Reddit(client_id=config.c_id,client_secret=config.c_s,user_agent=config.u_a,username=config.un,password=config.pw)

while True:
    try:
        subreddit = reddit.subreddit(random.choice(config.subs))
        print('Random subreddit is:',subreddit)
        submission = random.choice(list(subreddit.top('all', limit=None)))
        if submission.domain in ['i.redd.it', 'i.imgur.com']:
            print('Domain is in our list!')
            file_name = submission.url.replace('https://i.imgur.com/','').replace('https://i.redd.it/','')
            response = requests.get(submission.url)
            file = open(file_name, "wb")
            file.write(response.content)
            file.close()
            try:
                with open('tokens.txt') as f:
                    access_token, refresh_token = f.read().strip().split()
                im = pyimgur.Imgur(config.i_id, access_token=access_token, refresh_token=refresh_token)
            except FileNotFoundError as ex:
                im = pyimgur.Imgur(CLIENT_ID)
                auth_url = im.authorization_url('pin')
                webbrowser.open(auth_url)
                pin = input("Gimme the pin: ")
                access_token, refresh_token = im.exchange_pin(pin)
                with open('tokens.txt', 'w') as f:
                    f.write(f'{access_token} {refresh_token}')
            uploaded_image = im.upload_image(file_name, title=submission.title)
            uploaded_image.submit_to_gallery(title=submission.title)
            print('Submitted!')
            os.remove(file_name)
            print('Deleted File')
            time.sleep(300)
                        
        elif submission.domain not in ['i.redd.it', 'i.imgur.com']:
            print('domain is not in domains :(')
            time.sleep(10)
            
    except Exception: time.sleep(60)     
    except KeyboardInterrupt: quit()