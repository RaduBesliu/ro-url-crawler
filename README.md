# Romanian Link Crawler

## Description
A CLI application that is highly customisable based on user preferences.<br>
The main options of this script are the starting website and the max depth that the user wishes to go.<br>
The application crawls Romanian websites, using multithreading, to write all the links found in a file.

### All options
  - Start URL
  - Max depth
  - Timeout
  - Keep links
    - If the option is set to true, all the links found will be written in a file
  - Output file
  - Debug Mode
    - Prints the current depth and link counter every time a new link is found
  - Message frequency
    - How frequently information about the script will be printed
  - Parse library
    - Choose between lxml and BeautifulSoup using lxml parser

## Technologies
  - Python
    - BeautifulSoup
    - lxml
    - ThreadPoolExecutor