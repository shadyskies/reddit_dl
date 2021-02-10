#!/usr/bin/env python3

import selenium
# import bs4
import os
import hashlib
from PIL import Image
from selenium import webdriver
import requests
import io

# class="_1oQyIsiPHYt6nx7VOmd1sz _1RYN-7H8gYctjOQeL8p2Q7 scrollerItem _3Qkp11fjcAw9I9wtLo8frE _1qftyZQ2bhqP62lbPjoGAh _2IWrSJK7OQ27rTgV_N2Zu4 Post t3_l04ex8 "
# _1oQyIsiPHYt6nx7VOmd1sz _1RYN-7H8gYctjOQeL8p2Q7 scrollerItem _3Qkp11fjcAw9I9wtLo8frE _1qftyZQ2bhqP62lbPjoGAh _1LmKpEAguLZV4jQMgQSFVL  Post t3_lgit1o 

def get_post_links(wd:webdriver, max_links, query):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    url = "https://www.reddit.com/r/" + query + "/top/?t=week"
    wd.get(url)
    count = 0
    while count < max_links:
        scroll_to_end(wd)
        posts_a = wd.find_elements_by_css_selector("a.SQnoC3ObvgnGjWt90zD9Z._2INHSNB8V5eaWp4P0rY_mE")
        count = len(posts_a)
    return posts_a
    # wd.quit()

def get_media_url(posts_a)
    media_url = []
    for a in posts_a:
        wd.get(a)
        gif_url = wd.find_elements_by_css_selector("iframe")
        img_url = wd.find_elements_by_css_selector("image._2_tDEnGMLxpM6uOa2kaDB3.ImageBox-image.media-element._1XWObl-3b9tPy64oaG6fax")
        download_images(img_url)

def download_video(links, folder_path):


def download_images(links, folder_path, url='gifs')
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        folder_path = os.path.join(folder_path, query)
        if os.path.exists(folder_path):
            file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        else:
            os.mkdir(folder_path)
            file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


wd = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver')
get_post_links(wd, 10, 'gifs')
