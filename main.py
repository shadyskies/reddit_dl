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
import time


def selector():
    url = "https://www.reddit.com/"
    global selector_val 
    global query
    popularity_ls_sub = ['top/','top/?t=week','top/?t=week', 'top/?t=year','top/?t=all']
    popularity_ls_search = ['&sort=top&t=day','&sort=top&t=week','&sort=top&t=month','&sort=top&t=year','&sort=top']
    
    max_links = int(input("Enter max posts to download: "))
    selector_val = int(input("For downloading, enter 1 for subreddit and 2 for downloading from search: "))
    if selector_val:
        query = input("Enter subreddit name: ")
        url += "r/" + query + '/'
        print(url)
    else:
        query = input("Enter search query: ")
        url += "/search/?q=" + query + '/'
    print("Select from one of the following popularity choices...")
    print("1.Hot\n2.Top")
    choice = int(input())
    
    if choice == 2:
        print("Top of ?")
        print("1.Today\n2.This week\n3.This month\n4.This year\n5.All time")
        choice1 = int(input())
        if selector_val == 1:
            url += popularity_ls_sub[choice1 - 1]
            return max_links, url
        else:
            url += popularity_ls_search[choice1 - 1]
            return max_links, url
            
    else:
        return max_links, url
        

def get_post_links(wd:webdriver, max_links, url):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print(url)
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
    count = 0 
    for a in posts_a:
        print(a)
        wd.get(a)
        time.sleep(1)
        a_urls = wd.find_elements_by_css_selector('a')
        try:
            video_url = [i.get_attribute('href') for i in a_urls if 'imgur' in i.get_attribute('href') or 'gfycat' in i.get_attribute('href') or "preview" in i.get_attribute('href') or "redgifs" in i.get_attribute('href')]
            # print(video_url)
            video_url = [i for i in video_url if '.png' not in i and '.jpg' not in i]
        except:
            pass
        try:
            img_url = [i.get_attribute('href') for i in a_urls if '.jpg' in i.get_attribute('href') or '.png' in i.get_attribute('href')]
        except:
            pass
    
        try:
            print(f"video:{video_url}")
            print(f"img:{img_url}")
            if len(img_url) == 0:
                img_url = [i.get_attribute('href') for i in img_url if 'imgur' in i.get_attribute('href')]
                if len(img_url) == 0 and len(video_url) == 0:
                    continue
                img_url[0] = img_url[0] + '.jpeg'
        except:
            pass
    
        try:
            download_video(url=video_url[0], folder_path='videos/', query=query, count=count)
            count += 1
        except:
            # print('video couldnt be downloaded')
            pass
        try:
            download_images(url=img_url[0], folder_path='pics/', query=query, count=count)
            count += 1
        except:
            # print("Image could not be downloaded")
            continue


def download_video(url, folder_path, query, count):
    print(url)
    fname = url.split('/')[-1]
    folder_path = os.path.join(folder_path, query)
    if os.path.exists(folder_path):
        file_path = os.path.join(folder_path, fname)
    else:
        os.mkdir(folder_path)
        file_path = os.path.join(folder_path, fname)

    if 'gfycat' in url:
        print("Debug STATEMENT")
        wd.get(url)
        time.sleep(2)
        print(f"URL: {wd.getCurrentUrl()}")
        try:
            opener = urllib.request.URLopener()
            opener.addheader('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
            filename, headers = opener.retrieve(wd.getCurrentUrl(), file_path)
            print(f"{count}::SUCCESS - saved {url} - as {file_path}")
            return
        except:
            pass
        tmp = wd.find_elements_by_css_selector('video')
        url = tmp[0].get_attribute('poster')
        url = url[:-4] + '.mp4'
        print(url)
        
    if '.jpg' in url:
        return
    if '.gifv' in url:
        fname = fname[:-1] + '.mp4'
        url = url[:url.index(".gifv")] + ".mp4"
    if 'redgifs' in url:
        wd.get(url)
        tmp = wd.find_element_by_css_selector('video')
        url = tmp.get_attribute('poster')
        url = url[:-11] + '.mp4'
        print(url)
    try:
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
        filename, headers = opener.retrieve(url, file_path)
        print(f"{count}::SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

    

def download_images(folder_path, url, query, count):
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
        print(f"{count}::SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")



if __name__ == '__main__':
    if not os.path.exists('pics'):
        os.mkdir('pics')
    if not os.path.exists('videos'):
        os.mkdir('videos/')
    wd = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver')
    try:
        max_links, url = selector()
        posts_a = get_post_links(wd, max_links=max_links, url=url)
        get_media_url(posts_a, query)
        if os.path.exists('pics/' + query):
            print(f"Downloaded {len(os.listdir('pics/' + query))} pics")
        if os.path.exists('videos/' + query):
            print(f"Downloaded {len(os.listdir('videos/' + query))} videos")
        wd.quit()
    
    except Exception as e:
        print(e)
        wd.quit()