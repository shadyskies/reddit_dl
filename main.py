#!/usr/bin/env python3

import selenium
# import bs4
import os
import hashlib
from PIL import Image
from selenium import webdriver

# class="_1oQyIsiPHYt6nx7VOmd1sz _1RYN-7H8gYctjOQeL8p2Q7 scrollerItem _3Qkp11fjcAw9I9wtLo8frE _1qftyZQ2bhqP62lbPjoGAh _2IWrSJK7OQ27rTgV_N2Zu4 Post t3_l04ex8 "
# _1oQyIsiPHYt6nx7VOmd1sz _1RYN-7H8gYctjOQeL8p2Q7 scrollerItem _3Qkp11fjcAw9I9wtLo8frE _1qftyZQ2bhqP62lbPjoGAh _1LmKpEAguLZV4jQMgQSFVL  Post t3_lgit1o 

def get_links(wd:webdriver, max_links, query):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    url = "https://www.reddit.com/r/" + query + "/top/?t=week"
    wd.get(url)
    urls = []
    count = 0
    while count < max_links:
        scroll_to_end(wd)
        posts_a = wd.find_elements_by_css_selector("a.SQnoC3ObvgnGjWt90zD9Z._2INHSNB8V5eaWp4P0rY_mE")
        count = len(posts_a)
        # print(posts_a)
        for i in posts_a:
            print(i.get_attribute('href'))

    wd.quit()


def download_video(links, folder_path)

wd = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver')
get_links(wd, 10, 'gifs')