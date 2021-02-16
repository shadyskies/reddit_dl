#!/usr/bin/env python3

from bs4 import BeautifulSoup
import os
import hashlib
from PIL import Image
import requests
import io
import urllib.request
import time


HEADERS = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


def get_post_links(max_links, query, selector_val):
    posts_a = []
    if selector_val:
        url = "https://www.reddit.com/search/?q=" + query + "&sort=top"
    else:
        url = "https://www.reddit.com/r/" + query + "/top/?t=week"
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content,'html.parser')
    count = 0
    
    while count < max_links:
        posts_a += soup.find_all('a',{'class':["SQnoC3ObvgnGjWt90zD9Z","_2INHSNB8V5eaWp4P0rY_mE"]})
        count = len(posts_a)

    posts_a = ["https://reddit.com" + i['href'] for i in posts_a]
    posts_a = posts_a[:max_links]
    print(posts_a)
    return posts_a


def get_media_url(posts_a, query):
    count = 0 
    for a in posts_a:
        a_urls = []
        print(a)
        page = requests.get(a, headers=HEADERS)
        soup = BeautifulSoup(page.content,'html.parser')
        temp = soup.find('a',{"class":['_13svhQIUZqD9PVzFcLwOKT', 'styled-outbound-link']})
        if temp != None:
            a_urls.append(temp['href'])
        else:
            a_urls1 = soup.find_all('div',{'class':"_3Oa0THmZ3f5iZXAQ0hBJ0k"})
            media_urls = str(a_urls1[0])
            a_urls.append(media_urls[media_urls.index('href')+5:media_urls.index('rel')])
        # try:
        #     video_url = [i['href'] for i in a_urls if 'imgur' in i['href'] or 'gfycat' in i['href'] or "preview" in i['href']]
        # except:
        #     pass
        # try:
        #     img_url = [i['href'] for i in a_urls if '.jpg' in i['href'] or '.png' in i['href']]
        # except:
        #     pass
        
        # try:
        #     print(f"video:{video_url}")
        #     print(f"img:{img_url}")
        #     if len(img_url) == 0:
        #         img_url = [i['href'] for i in img_url if 'imgur' in i['href']]
        #         if len(img_url) == 0 and len(video_url) == 0:
        #             continue
        #         img_url[0] = img_url[0] + '.jpeg'
        # except:
        #     pass
        try:
            count += 1
            download_images(url=a_urls[0], folder_path='pics/', query=query, count=count)
        except Exception as e:
            print(f'no images in img_url')
            pass
        try:
            count += 1
            download_video(url=a_urls[0], folder_path='videos/', query=query, count=count)
        except Exception as e:
            print(f'no videos in video_url')
            pass


def download_video(url, folder_path, query, count):
    fname = url.split('/')[-1]
    if '.jpg' in url:
        return
    if '.gifv' in url:
        fname = fname[:-1] + '.mp4'
        url = url[:url.index(".gifv")] + ".mp4"
    elif 'gfycat' in url:
        wd.get(url)
        tmp = wd.find_elements_by_css_selector('video')
        url = tmp[0].get_attribute('poster')
        url = url[:-4] + '.mp4'
        print(url)
    folder_path = os.path.join(folder_path, query)
    if os.path.exists(folder_path):
        file_path = os.path.join(folder_path, fname)
    else:
        os.mkdir(folder_path)
        file_path = os.path.join(folder_path, fname)
    try:
        urllib.request.urlretrieve(url, file_path)
        print(f"{count}::SUCCESS(video) - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

def download_images(folder_path, url, query, count):
    print("url: ",str(url))
    url = url[1:]
    url = url[:-1]
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
    try:
        print("##############################################################################")
        print("Enter 0 to download from subreddit")
        print("Enter 1 to download from search")
        selector_val = int(input())
        query = input("Enter query to download: ")
        max_links = int(input("Enter number of links: "))
        posts_a = get_post_links(max_links, query,selector_val)
        get_media_url(posts_a, query)
        print(f"Downloaded {len(os.listdir('pics/'+query))} files")
    
    except Exception as e:
        print(e)