from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import time


# retrieves all problems from link by getting all HTML <a> tags
# and keeping ones with "leetcode.com/problems/" in the href
def getAllProblemsFromRootLink(page):
    # all links for <a> tags
    soup = BeautifulSoup(page, 'html.parser')
    allLinks = soup.find_all('a')

    # append all links from clicking on divs
    divs = soup.find_all('div')
    for div in divs:
       pass # click on div and then extract new link after clicking
        
    for link in allLinks:
        print(link.get('href'))

    problems = [str(link.get('href')) for link in allLinks if "problems" in str(link.get('href'))]
    return problems

original_url = "https://leetcode.com/studyplan/leetcode-75/"


# result = getAllProblemsFromRootLink("https://leetcode.com/studyplan/leetcode-75/");
# print(result)

if __name__ == '__main__':
# Create an instance of the Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Optional: Run headless (without a browser window)
    driver = webdriver.Chrome(options=options)
    # Replace with the URL of the page you want to scrape
    driver.get(original_url)

    time.sleep(10)
    # Wait for the page to load for 5 seconds (adjust timeout as needed)
    #wait = WebDriverWait(driver, 10)
    #wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    getAllProblemsFromRootLink(driver.page_source)
    driver.quit()