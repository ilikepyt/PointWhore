import os, time, praw, yaml, emoji, random, pyimgur, requests, traceback, webbrowser, downsyndrome

with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)
    domains = config["domains"]
    imgur_id = config["imgur_id"]
    client_id = config["client_id"]
    client_secret = config["client_secret"]
    user_agent = config["user_agent"]
    subs = config["subs"]

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

def unemoji(string):
    return str(emoji.demojize(string))

def upload(file, title):
    try:
        with open('tokens.txt') as f:
            access_token, refresh_token = f.read().strip().split()
        im = pyimgur.Imgur(imgur_id, access_token=access_token, refresh_token=refresh_token)
    except FileNotFoundError:
        im = pyimgur.Imgur(imgur_id)
        webbrowser.open(im.authorization_url('pin'))
        pin = input('Gimme the pin: ')
        access_token, refresh_token = im.exchange_pin(pin)
        with open('tokens.txt', 'w') as f:
            f.write(f'{access_token} {refresh_token}')
        img = im.upload_image(file)
        img.submit_to_gallery(title=title)

def pick_sub(sub_list):
    subreddit = reddit.subreddit(random.choice(sub_list))
    return subreddit

while True:
    try:
        sr = pick_sub(sub_list=subs)
        print('Random Subreddit Is:',sr)
        submissions = list(sr.top('all', limit=1000))
        submission = random.choice(submissions)
        if submission.domain in domains and '.gifv' not in submission.url:
            with open('ids.txt') as db:
                if submission.id not in db.read():
                    print('Imgur/Reddit Domain!')
                    file = submission.url.replace('https://i.imgur.com/','').replace('https://i.redd.it/','')
                    downsyndrome.download(url=submission.url, file_name=file)
                    print('Downloaded Image')
                    upload(file=file, title=unemoji(submission.title))
                    print('Uploaded To Gallery')
                    with open('ids.txt', 'a') as dbfile:
                        dbfile.write(submission.id + '\n')
                    os.remove(file)
                    print('Deleted File')
                    time.sleep(300)
                elif submission.id in db.read():
                    print('Already acted on submission :(')
        else:
            print('Submission Not Actionable :(')
            time.sleep(60)
    except Exception:
        print(traceback.format_exc())
        time.sleep(60)
    except KeyboardInterrupt:
        print('Shutting Down :(')
        quit()
