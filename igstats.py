from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os

def abrir_chrome(time=2):
    sleep(time)
    #Abrrimos explorador
    browser = webdriver.Chrome()
    browser.get('https://www.instagram.com/')

    #aceptamos cookies
    aceptar_cookies = browser.find_element_by_xpath('/html/body/div[3]/div/div/button[1]')
    aceptar_cookies.click()
    return browser
"""
def ig_login(driver, time=2):
    
    sleep(time)
    load_dotenv()    
    usuario = os.getenv("usuario")
    contrasena = os.getenv("contrasena")

    #driver.find_element_by_xpath("//*[@id="loginForm"]/div/div[1]/div/label/input").send_keys(usuario)
    driver.find_element_by_xpath("//*[@id="loginForm"]/div/div[2]/div/label/input").send_keys(contrasena)
    driver.find_element_by_xpath("//*[@id="loginForm"]/div/div[3]/button/div").click()
"""
def instagram_login(driver, time = 5):
    """
    Login to Instagram using username and password.
    """
    

    load_dotenv()    
    usuario = os.getenv("usuario")
    contrasena = os.getenv("contrasena")
    sleep(time)
    driver.find_element_by_xpath("/html/body/div[3]/div/div/button[1]").click()

    sleep(time)
    usr = driver.find_element_by_name("username")
    usr.send_keys(usuario)
    password = driver.find_element_by_name("password")
    password.send_keys(contrasena)
    password.send_keys(Keys.RETURN)
    return driver


def search_target(driver,target, time=5):
    sleep(time)
    # Get the search box
    searchbox = driver.find_element_by_xpath("//input[@placeholder='Busca']")
    searchbox.clear()

    # Search by tag
    searchbox.send_keys(target)
    sleep(time)
    searchbox.send_keys(Keys.ENTER)
    sleep(time)
    searchbox.send_keys(Keys.ENTER)
    sleep(time)
    searchbox.clear()
    return driver


def scroll_down(driver, time = 2):
    sleep(time)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return driver

def go_target(driver, target, time = 2):
    sleep(time)
    #Abrrimos explorador
    driver.get('https://www.instagram.com/' + target + '/')
    return driver

def get_images(driver):
    images = driver.find_elements_by_class_name('href')

    images = [{"image":image.get_attribute('src'),"url":image.find_element_by_class_name("coreSpriteRightPaginationArrow")} for image in images]
    images = images[1:-2] #slicing-off first photo, IG logo and Profile picture
    return images

def get_posts(driver, target):
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    body = soup.find('body')
    enlaces= [link.get("href") for link in body.find_all('a')]
    posts = list(filter(lambda x: x[0:3]=='/p/',enlaces))
    return ['https://www.instagram.com/' + target + link for link in posts]

def get_likes(driver, time = 2):
    sleep(time)
    driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div[2]/a").click()
    sleep(time)
    
    users=[]

    while True:
        elements = driver.find_elements_by_xpath("//*[@id]/div/span/a")

        for element in elements:
            if element.get_attribute('title') not in users:
                users.append(element.get_attribute('title'))

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return users