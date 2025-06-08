from bs4 import BeautifulSoup
import requests

class ImageScrape:
    def __init__(self, websites):
        self.websites = websites
        
        
        for website in self.websites:
            self.scrape(website)
            

    def scrape(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        img_Tags = soup.find_all("img")
       
        for img in img_Tags:
        