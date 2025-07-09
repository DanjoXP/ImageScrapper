import os
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
class ImageScrape:
    def __init__(self, websites,gui):
        self.websites = websites
        self.save_folder = "Images"
        self.gui = gui
        
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

        
        for website in self.websites:
            self.scrape(website)
            

    def scrape(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        img_Tags = soup.find_all("img")
       
        for i,img in enumerate(img_Tags):
            try:
                img_url = img.get("src")
                
                if not img_url:
                    continue
            
                img_url = urljoin(url,img_url)
                data = requests.get(img_url).content
                ext = os.path.splitext(img_url)[1].split("?")[0]
                
                if not ext:
                    ext = ".jpg"
                
                file_name = f"image_{i}{ext}"
                self.save_Image(file_name,data)
            
            except requests.exceptions.RequestException:
                print("Error",img_url)   
    
    def save_Image(self,file_name,data):
        full_path = os.path.join(self.save_folder, file_name)
        with open(full_path, "wb") as f:
            f.write(data)
        self.gui.root.after(0, self.gui.add_image, data)
        print("Image Saved")
            