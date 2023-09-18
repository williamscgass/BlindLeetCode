from bs4 import BeautifulSoup
from selenium import webdriver
import time
import click
import random
import os
import json
import multiprocessing as mp

# retrieves all problems from link by getting all HTML <a> tags
# and keeping ones with "leetcode.com/problems/" in the href
def getAllProblemsFromRootLink(link):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Optional: Run headless (without a browser window)
    driver = webdriver.Chrome(options=options)
    # Replace with the URL of the page you want to scrape
    driver.get(link)

    time.sleep(5)
    # Wait for the page to load for 5 seconds (adjust timeout as needed)
    #wait = WebDriverWait(driver, 10)
    #wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    page = driver.page_source
    driver.quit()

    # all links for <a> tags
    soup = BeautifulSoup(page, 'html.parser')
    allLinks = soup.find_all('a')

    problems = ["https://leetcode.com" + str(link.get('href')).replace("/editorial", "/description") for link in allLinks if "/problems/" in str(link.get('href'))]
    return problems

@click.group()
def blind():
    pass

@click.command()
@click.argument('--seed', default=random.randint(0, 100000))
@click.argument('--constructor', default=os.path.join(os.getcwd(), '.default.json'))
@click.argument('--name', default='blind')
def init(__seed, __constructor, __name):
    print(__seed)
    # reads in links from constructor file and gets all problems from each link
    if not os.path.isfile(__constructor):
        raise Exception("Constructor file not found")
    
    constructor = {}
    with open(__constructor, 'r') as f:
        constructor = json.load(f)

    # use async multiprocessing to get all problems from each link
    allProblemLinks = []
    def appendToLinksCallback(links):
        allProblemLinks.extend(links[0])


    click.echo("Retrieving problems from webpages... (estimated 10s of waiting)")
    with mp.Pool(processes=mp.cpu_count()) as pool:
        pool.map_async(getAllProblemsFromRootLink, constructor['links'], callback=appendToLinksCallback)
        pool.close()
        pool.join()

    # make sure allProblems have a unique /problems/<problem-name>/...
    uniqueProblems = []
    seenProblems = set()
    def filterUniqueProblems(problem):
        splitBySlash = problem.split('/')
        if len(splitBySlash) < 5 or splitBySlash[4] in seenProblems:
            return
        
        seenProblems.add(splitBySlash[4])
        uniqueProblems.append(problem)

    for problem in allProblemLinks:
        #print(problem)
        filterUniqueProblems(problem)

    state = {}
    state["seed"] = __seed
    state["unfinishedProblems"] = uniqueProblems # only uniques
    state["finishedProblems"] = []

    # creates <name>.json file to store progress of problems, as well as the seed
    with open(__name + ".json", 'w') as f:
        json.dump(state, f)
    
blind.add_command(init)

@click.command()
@click.argument('--name', default='blind')
def next(__name):
    # reads in state from <name>.json file
    if not os.path.isfile(__name + ".json"):
        raise Exception("State file not found")
    
    state = {}
    with open(__name + ".json", 'r') as f:
        state = json.load(f)

    # randomizes the order of problems
    random.seed(state["seed"])
    problem = random.choice(state["unfinishedProblems"])
    state["unfinishedProblems"].remove(problem)
    state["finishedProblems"].append(problem)

    # updates the state file
    with open(__name + ".json", 'w') as f:
        json.dump(state, f)

    click.echo("LcBlind's selection is: " + problem)

blind.add_command(next)

if __name__ == '__main__':
# Create an instance of the Chrome WebDriver
    blind()