# Romanian Link Crawler

## Description
A CLI application that is highly customisable based on user preferences.<br>
The main options of this script are the starting website and the max depth that the user wishes to go.<br>
The application crawls Romanian websites, using multithreading, to write all the links found in a file. 

## Options
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

## Statistics
In the **stats.txt** file there is a comparison between the two parsers. ( CPU: i5-7400 ).<br>
In the **results** folder there are 4 text files containing links from previous crawls.

## Upcoming updates
  - Use Flask to display the content in a webpage
  - Optimize the crawler
