# Wuzzuf Web Scrapper

#### Author: **Ziad Zakaria** 
#### Date: **1/17/2023**
#

## **What is Wuzzuf and Why I Choose it?**
WUZZUF.net is created and managed by [BasharSoft](https://basharsoft.com/), a technology firm founded in 2009 and one of very few companies in the MENA region specialized in developing Innovative Online Recruitment Solutions for top enterprises and organizations. Most job postes in Egypt is on Wuzzuf, So i saw it as a good source of data for Egypt's market. 
#

## **Why I did this Project?**
In Egypt, due to the current conomic poor situation, many people and talents began to seek a freelancing jobs even shift careers to get paid in USD instead of EGP. a distinguishable portion started exploring data science especially, data analysis. the problem it is hard to get data about salaries with respect to experience, number of open positions, companies location, etc..

So, i decided to build a web scraper for wuzzuf's website to scrape all the data about data science related roles. then in a future project i will analyze these data to get insights that might help the data roles seekers in their decision and what skills they should improve to be ready for the market    
#

## **Why Selenium?**
Wuzzuf's content is rendered using Javascript. That instance, a simple get request to the URL below would only return the viewable content. We're looking for something more.
#

## **What Actually The Script Do?**

The script presents a main function called  **scraper** what it actually does that it take the following parameters:

* **Job title** to search for ex: *Data Analyst*, or even it can be more general like *Data* which would return every job title that might be related to  the word data.  

* **No. of pages** to search in 

* **list of keywords** that you are intersted in to be in your job title to extract
#

