#run on ubuntu
import os
import json
import random
import time

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
import instagram_scraper as insta

#quiet but keeps Logs
#100 posts per Scraping
tag_scraper = insta.InstagramScraper(login_user='memescraperproject', login_pass='*********', destination='output/', media_types=['image'], interactive = True, quiet=False, maximum = 50, media_metadata=False, log_destination='scraper/logs/', latest=True,tag=True, filename='scraper/tags.txt')

users_scraper = insta.InstagramScraper(login_user='memescraperproject', login_pass='**********', destination='output/', media_types=['image'], interactive = True, quiet=False, maximum = 50, media_metadata=True, log_destination='scraper/logs/', latest=True,tag=False, filename='scraper/ig-users.txt')

#bash test block
with open("../cronjobs_Out.txt", 'a') as cjout:
	cjout.write("got jobs?\n")
	print("got jobs?")
exit()
#end bash test block
#this loop will scrape by tags first then users
#for medium in ('u', 't'):
for medium in ('t'):
    #assign the input file
    if medium == 'u':
        if users_scraper.login_user and users_scraper.login_pass:
            print("pre-auth")
            users_scraper.authenticate_with_login()
            print("post auth")
        if not users_scraper.authenticated:
            continue

        print("User input file:", users_scraper.filename)
        with open(users_scraper.filename, "r") as userf:
            users_scraper.usernames = userf.readlines()
        users_scraper.usernames = [x.strip() for x in users_scraper.usernames]

        users_scraper.scrape()
        users_scraper.save_cookies()
        users_scraper.logout()
    if medium == 't':
        if tag_scraper.login_user and tag_scraper.login_pass:
            print("pre-auth")
            #tag_scraper.authenticate_with_login()
            print("post auth")

        print("Tag input file:", tag_scraper.filename)

        #last off
        with open(tag_scraper.filename, "r") as tagsf:
            count = 0
            random.seed(time.time(),1)
            step = int(random.random()*30)+1
            max = 10

            while tagsf.readable() and (len(tag_scraper.usernames) <= max):
                tag = tagsf.readline()
                if count % step == 0:
                    tag_scraper.usernames.append( tag.strip())
                    print(tag, ': step count nusernames length:\n', step, count, len(tag_scraper.usernames))
                count = count + 1

        #tag_scraper.usernames = [x.strip() for x in tag_scraper.usernames]

        try:
            tag_scraper.scrape_hashtag()
        except json.decoder.JSONDecodeError as e:
            print("json error caught: ", e)
            break

        tag_scraper.save_cookies()
        tag_scraper.logout()
