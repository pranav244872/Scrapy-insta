import scrapy
from instacraper.settings import LOGIN_URL, LOGIN_PAYLOAD
from selenium import webdriver
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse
import time

class LoginSpiderSpider(scrapy.Spider):
    name = "login_spider"
    allowed_domains = ["www.instagram.com"]
    start_urls = ['https://www.instagram.com/accounts/login']

    def parse(self, response):
        self.driver = webdriver.Firefox()
        self.driver.get(response.url)
        print("WEBSITE IS OPENED")
        time.sleep(5)
        self.login(response)

    
    def login(self,response):
        time.sleep(5)
        username_input = self.driver.find_element("name","username")
        password_input = self.driver.find_element('name','password')
        login_button = self.driver.find_element(By.XPATH,"//button[@type='submit']")
        print("TYPING USERNAME")
        username_input.send_keys(LOGIN_PAYLOAD['username'])
        print('TYPING PASSWORD')
        password_input.send_keys(LOGIN_PAYLOAD['password'])
        login_button.click()
        time.sleep(10)
        if '<title>Instagram</title>' and 'aria-label="Home"' in self.driver.page_source:
            self.logger.info('Login Successful!')
            self.driver.get(f'https://www.instagram.com/{LOGIN_PAYLOAD["username"]}/followers')
            time.sleep(10)
            followers_url = f'https://www.instagram.com/{LOGIN_PAYLOAD["username"]}/followers'
            followers_html = self.driver.page_source
            followers_response = HtmlResponse(url = followers_url, body = followers_html, encoding = 'utf-8')
            self.followers_checker(followers_response)
        else:
            self.logger.error('Login Failed')


    def followers_checker(self,response):
        followers = response.xpath("//span[@class='_aacl _aaco _aacw _aacx _aad7 _aade']/text()").getall()
        print("FOLLOWERS = ", followers)
        self.driver.get(f'https://www.instagram.com/{LOGIN_PAYLOAD["username"]}/following')
        time.sleep(10)
        following_html=self.driver.page_source
        following_response = HtmlResponse(url=f'https://www.instagram.com/{LOGIN_PAYLOAD["username"]}/following', body = following_html, encoding = 'utf-8' )
        print('CALLING FOLLOWING CHECKER')
        self.following_checker(following_response, followers)

    def following_checker(self,response,followers):
        print("FOLLOWING CHECKER STARTED")
        following = response.xpath("//span[@class='_aacl _aaco _aacw _aacx _aad7 _aade']/text()").getall()
        print("FOLLOWING = ", following)
        req_list = []
        print('LOOP STARTED')
        for i in following:
            if i in followers:
                continue
            req_list.append(i)
        return req_list
        
