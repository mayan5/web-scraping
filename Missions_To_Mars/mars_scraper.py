from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd 

def scrape():
    mars_news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    executable_path = {"executable_path": "C:/Users/Marisabel Matta/Desktop/exp/web-scraping-challenge-main/Missions_To_Mars/chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    first = None
    #for some reason it doesn't work everytime, so it will just keep trying!
    #while first is None:
        
    browser.visit(mars_news_url)
    html = browser.html
    
    more_soup = BeautifulSoup(html, 'html.parser')

    first = more_soup.find('li', class_='slide')

    

    if first is None:
        return_this = {
            'news_title': 'Something went wrong talking to Nasa!',
            'news_summary': "For some reason when using scrape from the python file, it doesn't find any html for the page."
        }
    else:
        news_title = first.h3.text

        news_summary = first.find('div', class_='rollover_description_inner').text

        return_this = {
            "news_title": news_title,
            'news_summary': news_summary
        }

    
    perseverance_image_url = 'https://www.nasa.gov/perseverance/images'

    try:
        browser.visit(perseverance_image_url)
        image_html = browser.html
        image_soup = BeautifulSoup(image_html,'html.parser')

        images = image_soup.find('div', class_='is-gallery')
        first_img = images.find('div', class_='image')
        first_img_href = first_img.find('img')['src']

        return_this.update({'perseverance_image':'https://www.nasa.gov' + first_img_href})

    except:
        pass


    
    browser.quit()




    facts_url = 'https://space-facts.com/mars/'

    tables = pd.read_html(facts_url)
    df=tables[0]
    df=df.rename(columns={0:'',1:'Mars'})
    facts_table = df.to_html(index=False,classes='table table-striped', justify='left')

    return_this.update({"data_table": facts_table})


    hemisphere_image_urls = [
        {'title': 'Cerberus Hemisphere', 'img_url':'https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg'},
        {'title': 'Schiaparelli Hemisphere', 'img_url':'https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg'},
        {'title': 'Syrtis Major Hemisphere', 'img_url':'https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg'},
        {'title': 'Valles Marineris Hemisphere', 'img_url':'https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg'}
    ]

    return_this.update({'hemisphere_image_urls': hemisphere_image_urls})

    return return_this


