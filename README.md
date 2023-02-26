# Anime Recommendation System: Project Overview 
* Created scrapers by using Jikan (時間) REST API to scrap anime and user information from myanimelist[DOT]net.
* Scraped 2333 anime TV productions between 2010-2022 from myanimelist using python and the created scraper.
* Scraped 86269 individual users' data.

TODO:
* data cleaning
* EDA
* model build

## Code and Resources Used 
**Python Version:** 3.9  
**Packages:** pandas(1.4.4)  
**Jikan API:** https://jikan.moe/  
**Scraper Github:** https://github.com/ildeniz/Anime_Recommendation_System/blob/master/mal_scraper.py 

## Web Scraping
The scrapers used to scrape 2333 anime TV productions between 2010-2022 from myanimelist[DOT]net, and 86269 individual users' scores & watch status info.

I had to get creative to collect user data since Jikan API no longer supports scraping anime list of individual users. Instead of scraping data directly from user data, I utilised each anime's "user updates" section. This section goes up to a maximum of 100 pages, and each page is consistent with 75 individual users. Due to time constraints issues, I preferred to scrap data from the first 5 pages. During scraping, I realised that sometimes users appear on multiple pages; I dealt with this problem in the source and implemented a section to remove duplicates while scraping.

For each anime, we got the following information:
*	Anime title
*	Anime MAL ID
*	Rating *(Animes w/o a user rating are excluded.)*
*	Number of users who rated the anime
*	Number of members of the anime 
*	Number of members favourited the anime
*	Genre 
*	Premiered year
*	Premiered season  

For each user, we got the following information:
* User name
* Score assigned by the user to a given anime
* User's watch status of the anime
* The id number of the anime

## Data Cleaning

## EDA

## Model Building 

## Model performance

## Productionization 




