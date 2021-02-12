#!/usr/bin/env python3

import selenium
# import bs4
import os
import hashlib
from PIL import Image
from selenium import webdriver
import requests
import io
import urllib.request

# class="_1oQyIsiPHYt6nx7VOmd1sz _1RYN-7H8gYctjOQeL8p2Q7 scrollerItem _3Qkp11fjcAw9I9wtLo8frE _1qftyZQ2bhqP62lbPjoGAh _2IWrSJK7OQ27rTgV_N2Zu4 Post t3_l04ex8 "
# _1oQyIsiPHYt6nx7VOmd1sz _1RYN-7H8gYctjOQeL8p2Q7 scrollerItem _3Qkp11fjcAw9I9wtLo8frE _1qftyZQ2bhqP62lbPjoGAh _1LmKpEAguLZV4jQMgQSFVL  Post t3_lgit1o 

def get_post_links(wd:webdriver, max_links, query, selector_val):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    if selector_val:
        url = "https://www.reddit.com/search/?q=" + query + "&sort=top"
    else:
        url = "https://www.reddit.com/r/" + query + "/top/?t=week"
    wd.get(url)
    count = 0
    while count < max_links:
        scroll_to_end(wd)
        posts_a = wd.find_elements_by_css_selector("a.SQnoC3ObvgnGjWt90zD9Z._2INHSNB8V5eaWp4P0rY_mE")
        count = len(posts_a)
    posts_a = [i.get_attribute('href') for i in posts_a]
    posts_a = posts_a[:max_links]
    # print(posts_a)
    return posts_a


def get_media_url(posts_a, query):
    media_url = []
    for a in posts_a:
        print(a)
        wd.get(a)
        try:
            gif_url = wd.find_elements_by_css_selector("a")
        except:
            pass
        media_url = [i.get_attribute('href') for i in gif_url if 'imgur' in i.get_attribute('href') or 'gfycat' in i.get_attribute('href')]
        # img_url = wd.find_elements_by_css_selector("a")
        # media_url = [i.get_attribute('href') for i in img_url if '.jpg' in i.get_attribute('href') or '.png' in i.get_attribute('href')]
        if len(media_url) == 0:
        #     media_url = [i.get_attribute('href') for i in img_url if 'imgur' in i.get_attribute('href')]
        #     if len(media_url) == 0:
                continue
        #     media_url[0] = media_url[0] + '.jpeg'
        print(media_url)
        # download_images(url=media_url[0], folder_path='pics/', query=query)
        download_video(url=media_url[0], folder_path='videos/', query=query)

def download_video(url, folder_path, query):
    fname = url.split('/')[-1]
    if '.gifv' in url:
        fname = fname[:-1] + '.mp4'
        url = url[:url.index(".gifv")] + ".mp4"
    if 
    folder_path = os.path.join(folder_path, query)
    if os.path.exists(folder_path):
        file_path = os.path.join(folder_path, fname)
    else:
        os.mkdir(folder_path)
        file_path = os.path.join(folder_path, fname)
    try:
        urllib.request.urlretrieve(url, file_path)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


def download_images(folder_path, url, query):
    # print(url)
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



if __name__ == '__main__':
    if not os.path.exists('pics'):
        os.mkdir('pics')
    if not os.path.exists('videos'):
        os.mkdir('videos/')
    wd = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver')
    print("##########################")
    print("Enter 0 to download from subreddit")
    print("Enter 1 to download from search")
    selector_val = int(input())
    query = input("Enter query to download: ")
    max_links = int(input("Enter number of links: "))
    posts_a = get_post_links(wd,max_links, query,selector_val)
    get_media_url(posts_a, query)
    print(f"Downloaded {len(os.listdir('videos/'+query))} files")
    wd.quit()