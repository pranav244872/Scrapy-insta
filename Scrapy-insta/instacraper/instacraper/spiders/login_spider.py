import scrapy
from instacraper.settings import LOGIN_PAYLOAD
from selenium import webdriver
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse
import time
import logging

class LoginSpiderSpider(scrapy.Spider):
    name = "login_spider"
    allowed_domains = ["www.instagram.com"]
    start_urls = ['https://www.instagram.com/accounts/login']

    def parse(self, response):
        #Initializing webdriver
        self.driver = webdriver.Firefox()
        
        #Loading website into driver
        self.driver.get(response.url)
        logging.info('WEBSITE IS OPENED')
        time.sleep(5)
        self.login(response)

    
    def login(self,response):
        time.sleep(5)
        #Finding elements with username and password "name" html tag
        username_input = self.driver.find_element("name","username")
        password_input = self.driver.find_element('name','password')

        #Finding Login Button
        login_button = self.driver.find_element(By.XPATH,"//button[@type='submit']")
        
        #Typing Username
        logging.info('TYPING USERNAME')
        username_input.send_keys(LOGIN_PAYLOAD['username'])

        #Typing Password
        logging.info('TYPING PASSOWORD')
        password_input.send_keys(LOGIN_PAYLOAD['password'])

        #Click the login button
        login_button.click()
        time.sleep(10)

        #Checking if login successful or not
        if '<title>Instagram</title>' and 'aria-label="Home"' in self.driver.page_source:
            #If login successful
            logging.info("LOGIN SUCCESSFUL")

            #Going to the followers page
            self.driver.get(f'https://www.instagram.com/{LOGIN_PAYLOAD["username"]}/followers')
            logging.info("OPENED FOLLOWERS PAGE")
            time.sleep(5)

            #Starting a loop to scroll through the followers list
            #Followers list is a dynamic element where new followers are only revelead after you scroll to the bottom
            element = self.driver.find_element(By.XPATH,"//div[@class = '_aano']")
            #The number in range function is directly proportional to the number of followers.
            #Example = 100 followers = 30 scrolls
            for _ in range(30):
                self.driver.execute_script("arguments[0].scrollTop += arguments[0].offsetHeight;", element)
                logging.info("SCROLLING FOLLOWERS PAGE")
                time.sleep(2)
            
            #now that all the followers have loaded
            #Retrieving the html of the followers page
            time.sleep(5)
            followers_url = f'https://www.instagram.com/{LOGIN_PAYLOAD["username"]}/followers'
            followers_html = self.driver.page_source
            followers_response = HtmlResponse(url = followers_url, body = followers_html, encoding = 'utf-8')
            logging.info("RETRIEVED COMPLETE FOLLOWERS HTML")
            
            #After retrieving the html now calling a function which reads the html
            logging.info("CALLING FOLLOWERS CHECKER")
            self.followers_checker(followers_response)
        
        else:
            #If login fails
            logging.info("LOGIN FAILED")


    def followers_checker(self,response):
        #Reading complete followers html
        followers = response.xpath("//span[@class='_ap3a _aaco _aacw _aacx _aad7 _aade']/text()").getall()
        #Retrieving followers list
        logging.info("RETRIEVED FOLLOWERS LIST")
        logging.info(f'followers={followers}')
        #Going to the following page
        self.driver.get(f'https://www.instagram.com/{LOGIN_PAYLOAD["username"]}/following')
        logging.info("RETRIEVED FOLLOWING PAGE")
        time.sleep(5)

        #Starting a loop to scroll through the following list
        #Following list is a dynamic element where new followers are only revelead after you scroll to the bottom
        element = self.driver.find_element(By.XPATH,"//div[@class = '_aano']")
        #The number in range function is directly proportional to the number of followers.
        #Example = 100 following = 30 scrolls
        for _ in range(30):
            self.driver.execute_script("arguments[0].scrollTop += arguments[0].offsetHeight;", element)
            logging.info("SCROLLING FOLLOWING PAGE")
            time.sleep(2)

        #now that all the followers have loaded
        #Retrieving the html of the followers page
        time.sleep(5)
        following_html=self.driver.page_source
        following_response = HtmlResponse(url=f'https://www.instagram.com/{LOGIN_PAYLOAD["username"]}/following', body = following_html, encoding = 'utf-8' )
        logging.info("RETRIEVED COMPLETE FOLLOWERS HTML")
        
        #After retrieving the html now calling a function which reads the html
        logging.info("CALLING FOLLOWERS CHECKER")
        self.following_checker(following_response, followers)
        

    def following_checker(self,response,followers):
        #Reading complete following html
        following = response.xpath("//span[@class='_ap3a _aaco _aacw _aacx _aad7 _aade']/text()").getall()
        
        #Retrieving following list
        logging.info("RETRIEVED FOLLOWING LIST")
        logging.info(f'following={following}')
        '''
        self.following = following
        self.req_list(self, self.followers,self.following)

    def req_list(self, followers, following):
        req_list = []
        print('LOOP STARTED')
        for i in self.following:
            if i in self.followers:
                continue
            else:
                req_list.append(i)
                continue
        print(req_list)
'''