#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 22:27:13 2020

@author: Eric

To get Instagram data from the given profiles: 
    - 365 x
    - Iacho x
    - Santo Placardx
    - Nico Tatuero / Tatuero Estudio x
    - Lucky Lion x
    
Todo: 
    - Create functions; one for info and then for posts 
    - return lists and dicts
    - append posts dict to info dict. 
"""
#importing necesary libraries

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time 
import pandas as pd 
import json
import os 


#changing the option to have headless browser & disabling GPU
options = Options()
options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument('--no-sandbox') # # Bypass OS security model
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")

#defining our driver 
driver = webdriver.Chrome(options=options)

#date today
date_time = time.strftime("%d%m%Y")

#list of usernames to scrape
user_names = ['iacho','365kioscosargentinos',
              'santoplacard','luckylion.oficial',
              'nico_tatuero','tatueroestudio']

#list to store dictionary with user info 
user_info = []
#list to store JSON dump so we don't call twice 
post_data_list = []
#cleaned posts data list 
posts_list = []
#base_path
base_path = '/Users/Eric/Documents/Python/Projects/IG_scraper/Profiles/' 


def get_profile_info():
    for user in user_names:
        #target url for each profile 
        URL = f'https://www.instagram.com/{user}/?__a=1'
        #getting the URL
        driver.get(URL)
        #reading URL
        soup = BeautifulSoup(driver.page_source,'lxml').get_text()
        #loading into JSON
        json_data = json.loads(soup)        
        #user information
        user_name = json_data['graphql']['user']['username']
        followers = json_data['graphql']['user']['edge_followed_by']['count']
        following = json_data['graphql']['user']['edge_follow']['count']
        hist_dest = json_data['graphql']['user']['highlight_reel_count']
        num_posts = json_data['graphql']['user']['edge_owner_to_timeline_media']['count']
        profile_pic = json_data['graphql']['user']['profile_pic_url_hd']
        #saving user info to dictionary 
        profile_info_dict = {
                        'User':user_name,
                        'Followers':followers,
                        'Following':following,
                        'Hist. Dest':hist_dest,
                        'Number of Posts':num_posts,
                        'Profile Pic ':profile_pic
                        }
        #adding dictionary to list 
        user_info.append(profile_info_dict)
        #getting the posts data 
        post_data = json_data['graphql']['user']['edge_owner_to_timeline_media']['edges']
#        with open(f'{user_name}.json','w') as json_file:
#            json.dump(post_data,json_file)
        #appending it to a list so we don't have to make another call 
        post_data_list.append(post_data)
    
    driver.quit()
    
    return user_info,post_data_list,


#
#def clean_post_data():
#    i = 0
#    for data in post_data_list:
#        target = data[i]['node']
#        pic_url = target['display_url']
#        capt = target['edge_media_to_caption']['edges'][0]['node']['text']
#        comments = target['edge_media_to_comment']['count']
#        likes = target['edge_liked_by']['count']
#        
#        posts_dict = {
#                    'Post Number':i+1,
#                    'Caption':capt,
#                    'Number of Comments':comments,
#                    'Number of Like':likes,
#                    'Post URL':pic_url
#                    }
#        posts_list.append(posts_dict)
#        i += 1
#        
#    return posts_list

def clean_post_data():
    
    for json_item in post_data_list: 
        for posts in json_item: 
            usrname = posts['node']['owner']['username']
            pic_url = posts['node']['display_url']
            comments = posts['node']['edge_media_to_comment']['count']
            caption = posts['node']['edge_media_to_caption']['edges']
            if len(caption) == 1:
                caption = caption[0]['node']['text']
            likes = posts['node']['edge_liked_by']['count']
            posts_dict = {
                        'UserName': usrname,
                        'Number of Comments':comments,
                        'Number of Like':likes,
                        'Caption':caption,
                        'Post URL':pic_url
                        }
            posts_list.append(posts_dict)
    
    return posts_list

def create_folders(): 
    for user in user_names:
        folder = base_path + user
        if not os.path.exists(folder):
            os.mkdir(folder)

def save_userinfo():
    
    for user in user_info: 
        name = user['User'].split(" ")
        name_join = ''.join(name)
        path_to_save = base_path + name_join + "/" + name_join+"_userinfo_" + date_time + ".csv"
        df = pd.DataFrame(user,index=[0])
        df.to_csv(path_to_save,encoding='utf-8-sig')
        
def save_postinfo():
    posts_list_chunk = [posts_list[i:i+12] for i in range(0, len(posts_list), 12)]
    for posts in posts_list_chunk: 
        name = posts[0]['UserName']
        save_path= base_path + name + '/' + name + '_postinfo_' + date_time + '.csv'
        df1 = pd.DataFrame.from_dict(posts)
        df1 = df1.drop(['UserName'],axis=1)
        df1.to_csv(save_path,encoding='utf-8-sig')

def run_all():
    
    get_profile_info()
    clean_post_data()
    create_folders()
#    save_userinfo()
    save_postinfo()


run_all()


#downloading the profile picture 
#save_img = Image.open(requests.get(profile_pic,stream = True).raw).save('profilepic.jpg')
#


#df = pd.DataFrame(posts_list)
#df.to_csv('test_iacho.csv',encoding='utf-8-sig')
