import os
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
import time
class ImageScrape:
    def __init__(self, websites,gui):
        self.websites = websites
        self.save_folder = "Images"
        self.gui = gui
        self.visited = set()
        
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)
        for website in self.websites:
            self.scrape(website,1)
            
    def scrape(self,url,depth):
        url = url.rstrip("/")
        if url in self.visited or depth < 0:
            return 
        
        print(f"Scraping Url: {url}")
        self.visited.add(url)
        
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print("Failed to fetch page", url,"-", e)
            return
        
        img_Tags = soup.find_all("img")
       
        for i,img in enumerate(img_Tags):
            try:
                img_url = img.get("src")
                
                if not img_url:
                    continue
            
                img_url = urljoin(url,img_url)
                data = requests.get(img_url, timeout=5).content
                ext = os.path.splitext(img_url)[1].split("?")[0]
                
                if not ext:
                    ext = ".jpg"
                domain = urlparse(url).netloc.replace(".", "-")
                
                file_name = f"{domain}_image_{i}{ext}"
                self.save_Image(file_name,data)
                time.sleep(1)
            
            except Exception as e:
                print(f"Error Downloading Image {file_name} ",e)
                
        if depth > 0:
            for tag in soup.find_all("a", href=True):
                link = urljoin(url, tag['href'])
                if not link.startswith("http"):
                    continue
                if urlparse(link).netloc == urlparse(url).netloc:
                    self.scrape(link, depth = depth - 1)
    
    def save_Image(self,file_name,data):
        full_path = os.path.join(self.save_folder, file_name)
        with open(full_path, "wb") as f:
            f.write(data)
        self.gui.root.after(0, self.gui.add_image, data)
        print("Image Saved")
            