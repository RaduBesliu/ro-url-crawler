import lxml.html as lh
from bs4 import BeautifulSoup
import requests
import concurrent.futures
import time
import re
import os
import sys

# Clears console based on the OS
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

# Default settings for the script
fileName = "all_links.txt"
maxDepth = 4
startUrl = "http://hotnews.ro"
timeoutSec = 2
keepLinks = False
debugMode = False
messageFreq = 100
parseLibrary = "lxml"

# Global settings used in the script
currentDepth = 1
linkCounter = 0
regexHref = re.compile(r"^(?:https{0,1}\:\/\/(?:[a-zA-Z0-9\-]*\.)*?)ro.\S*")
links = [startUrl]
visitedLinks = {}

# Function to parse links using lxml
# It takes the content from a page, makes it a string and gets all the hrefs from <a> tags
# If the regex matches the link and the link hasn't been already visited, add it to the dictionary
def get_all_links_from_url_lxml(currentUrl):
  try:
    allRoLinks = []
    allLinksHref = lh.fromstring(requests.get(currentUrl, timeout=timeoutSec).content).xpath("//a/@href")
    for linkHref in allLinksHref:
      if linkHref not in visitedLinks and regexHref.match(linkHref):
        allRoLinks.append(linkHref)
        visitedLinks[linkHref] = True
    return allRoLinks
  except:
    return []

# Function to parse links using beautifulsoup4 + lxml parsing
# It makes file-like object to be parsed, all links that match the regex are put into a list
# If the link is not visited, add it to the dictionary
def get_all_links_from_url_bs4_lxml_parse(currentUrl):
  try:
    allRoLinks = []
    parsedWebsite = BeautifulSoup(requests.get(currentUrl, timeout=timeoutSec).content, "lxml", from_encoding="iso-8859-1")
    allLinkTags = parsedWebsite.find_all("a", {"href": regexHref})
    for link in allLinkTags:
      linkHref = link.get("href")
      if linkHref not in visitedLinks:
        allRoLinks.append(linkHref)
        visitedLinks[linkHref] = True
    return allRoLinks
  except:
    return []

# Function that displays current menu options
def show_menu_options():
  print("============ Web Crawler v1.0 ==============")
  print("1. Start script with current settings.")
  print("2. Change settings.")
  print("3. Exit.")
  if debugMode:
    print("WARNING : Debug mode is active. Link counter and depth will be printed every single time a link is found.")

# Function that allows the user to change script-specific settings
# It includes verification for all inputs 
def change_script_settings():
  global startUrl
  global maxDepth
  global timeoutSec
  global keepLinks
  global fileName
  global debugMode
  global messageFreq
  global parseLibrary
  exitMenu = False
  clearConsole()
  print(f"INFO: lxml -> ~37% FASTER | ~11% LESS LINKS (stats compared to bs4_lxml-parse on 350k links)")
  print("Current settings:")
  print(f"  1. Start URL: {startUrl}")
  print(f"  2. Max Depth: {maxDepth}")
  print(f"  3. Timeout (seconds): {timeoutSec}")
  print(f"  4. Keep links: {keepLinks}")
  print(f"  5. Output file: {fileName}")
  print(f"  6. Debug mode: {debugMode}")
  print(f"  7. Message frequency: {messageFreq}")
  print(f"  8. Parse library: {parseLibrary}")

  userInput = 0
  while userInput < 1 or userInput > 8:
    userInput = input('Choose option to change (1-8) or type anything else to quit: ')
    try:
      userInput = int(userInput)
      if userInput < 1 or userInput > 8:
        raise ValueError("")
    except:
      exitMenu = True
      break

  clearConsole()
  if userInput == 1:
    print("Link format: http(s)://(subdomain.)domain.ro")
    userInput = ""
    while not re.search(r"^(?:https{0,1}\:\/\/(?:[a-zA-Z0-9\-]*\.)*?)ro.\S*", userInput):
      userInput = input("New link: ")
      if userInput[-1] != '/':
        userInput = userInput + '/'

    startUrl = userInput

  elif userInput == 2:
    userInput = -1
    while userInput < 1:
      userInput = input("New max depth: ")
      try:
        userInput = int(userInput)
        if userInput < 1:
          clearConsole()
          continue
        else:
          break
      except:
        userInput = -1
        clearConsole()

    maxDepth = userInput

  elif userInput == 3:
    userInput = -1
    while userInput < 1:
      userInput = input("New timeout (seconds): ")
      try:
        userInput = int(userInput)
        if userInput < 1:
          clearConsole()
          continue
        else:
          break
      except:
        userInput = -1
        clearConsole()

    timeoutSec = int(userInput)

  elif userInput == 4:
    if keepLinks:
      keepLinks = False
    else:
      keepLinks = True

  elif userInput == 5:
    try:
      fileName = input("New file name: ")
      open(fileName, "w", encoding="utf-8")
      os.remove(fileName)
    except:
      fileName = "all_links.txt"

  elif userInput == 6:
    if debugMode:
      debugMode = False
    else:
      debugMode = True

  elif userInput == 7:
    userInput = -1
    while userInput < 1:
      userInput = input("New message frequency: ")
      try:
        userInput = int(userInput)
        if userInput < 1:
          clearConsole()
          continue
        else:
          break
      except:
        userInput = -1
        clearConsole()

    messageFreq = userInput

  elif userInput == 8:
    userInput = ""
    while userInput != "bs4_lxml-parse" and userInput != "lxml":
      userInput = input("New parsing library (bs4_lxml-parse | lxml): ")

    parseLibrary = userInput

  if exitMenu:
    initialize_menu()
  else:
    change_script_settings()

# Main function to start the script
def start_script():
  global startUrl
  global maxDepth
  global timeoutSec
  global keepLinks
  global fileName
  global debugMode
  global currentDepth
  global links
  global linkCounter
  global parseLibrary
  timeStart = time.perf_counter()
  # Open file if the user wants to keep the links
  if keepLinks:
    file = open(fileName, "w", encoding="utf-8")
  with concurrent.futures.ThreadPoolExecutor() as executor: 
    while currentDepth <= maxDepth:
      currentDepth = str(currentDepth)
      # Call different functions depending on the users' chosen parser
      # The executor maps each of the link from the links array and calls the
      # function with it as a parameter
      if parseLibrary == "bs4_lxml-parse":
        results = executor.map(get_all_links_from_url_bs4_lxml_parse, links)
      else:
        results = executor.map(get_all_links_from_url_lxml, links)
      links = []
      linksDict = {}
      for result in results:
        for link in result:
          if link != "" and link not in linksDict:
            links.append(link)
            linksDict[link] = True

            if keepLinks:
              file.write(link + '\n')
            
            linkCounter += 1
            if debugMode:
              print(currentDepth, linkCounter)

            if not linkCounter % messageFreq:
              timePassed = time.perf_counter()
              timeP = "{:.4f}".format(timePassed - timeStart)
              speedP = "{:.4f}".format(linkCounter / (timePassed - timeStart))
              print(f"Link count: {linkCounter} | Depth: {currentDepth} | Time elapsed: {timeP} | Avg. speed: {speedP} links/second")

      print(f"Links found from start to depth {currentDepth}: {linkCounter}. Time elapsed: {round(time.perf_counter() - timeStart, 4)}.")
      currentDepth = int(currentDepth)
      currentDepth += 1
      
  executor.shutdown()
  if keepLinks:
    file.close()

  timeEnd = time.perf_counter()
  print(f"-----------------------------------------\nFinished in {round(timeEnd - timeStart, 4)} second(s).")
  print(f"Found {linkCounter} different links.")
  print(f"Average speed: {round(linkCounter / (timeEnd - timeStart), 2)} links/second")

# Function to initialize menu
def initialize_menu():
  clearConsole()
  show_menu_options()
  userInput = 0
  while userInput < 1 or userInput > 3:
    userInput = int(input("Choose option (1-3): "))
  
  clearConsole()
  if userInput == 1:
    start_script()

  elif userInput == 2:
    change_script_settings()

  else:
    sys.exit(0)

initialize_menu()