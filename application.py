import tkinter as tk
from tkinter.filedialog import askopenfile
import threading
import image_scrapper
from PIL import Image, ImageTk
from io import BytesIO
class Window:
    def __init__(self,title,x,y):
        self.websites = []
        self.images = []
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{x}x{y}")
        
        self.list_box = tk.Listbox(self.root, width=140,height=15)
        self.list_box.pack(anchor="n",padx=10,expand=True,fill="x")
        
        self.entry_label = tk.Label(self.root, text="Enter Website To Scrape:",anchor="n")
        self.entry_label.pack(padx=1,expand=True,fill="x")
        
        self.entry = tk.Entry(self.root,width=100)
        self.entry.pack(anchor="nw",padx=10,expand=True,fill="x")
        
        self.frame = tk.Frame(self.root,width=25,height=25)
        self.frame.pack(anchor="w",pady=10,expand=True,fill="x")
        
        self.add_website_button = tk.Button(self.frame,text="Add Website",width=15,command=self.add_website)
        self.add_website_button.pack(side=tk.LEFT,padx=10,expand=True,fill="x")
    
        self.clear_websites_button = tk.Button(self.frame,text="Clear Websites", width=15,command=self.clear_websites)
        self.clear_websites_button.pack(side=tk.LEFT,padx=10,expand=True,fill="x")
        
        self.remove_website_button = tk.Button(self.frame,text="Remove Website", width=15,command=self.remove_website)
        self.remove_website_button.pack(side=tk.LEFT,padx=10,expand=True,fill="x")
        
        self.load_websites_button = tk.Button(self.frame,text="Load Websites", width=15, command=self.load_websites)
        self.load_websites_button.pack(side=tk.LEFT,padx=10,expand=True,fill="x")
       
        self.scraper_button = tk.Button(self.frame,text="Scrape Websites", width=15,command=self.scrape_website)
        self.scraper_button.pack(side=tk.LEFT,padx=10,expand=True,fill="x")
        
        self.canvas = tk.Canvas(self.root, height=100, width=x-20, bg="#D3D3D3", highlightthickness=0)
        self.scroll_bar = tk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=self.scroll_bar.set)

        self.canvas.pack(side="bottom", fill="none", expand=False)
        self.scroll_bar.pack(side="bottom", fill="x",expand=True,)
        
    def add_website(self):
        text = self.entry.get().strip()
        if not text:
           self.display_warning("Unable To Perform Action", "Entry box cannot be empty!")
           return 
       
        if not self.is_valid_url(text):
            self.display_warning("Unable To Perform Action", "Invalid URL")
            return
            
            
        self.list_box.insert(tk.END,self.entry.get())
        self.entry.delete(0,tk.END)
        self.websites.append(text)
            
    def remove_website(self):
        selected = self.list_box.curselection()
        
        if not selected:
            self.display_warning("Unable To Perform Action", "You Must Select At Least 1 Website To Remove!")
            return
        
        for i in reversed(selected):
            self.websites.remove(self.list_box.get(i))
            self.list_box.delete(i)
    
    def clear_websites(self):
        self.list_box.delete(0,tk.END)
        self.websites.clear()

        
    def display_warning(self, error, message):
       tk.messagebox.showwarning(error,message)
       
    def scrape_website(self):
        if(self.list_box.size() == 0):
            self.display_warning("Unable To Perform Action", "No Websites Entered To Scrape!")
            return
        
        thread = threading.Thread(target=image_scrapper.ImageScrape, args=(self.websites,self))
        thread.daemon = True
        thread.start()
    
    def add_image(self,data):
        image = Image.open(BytesIO(data))
        image = image.resize((50,50))
        
        photo = ImageTk.PhotoImage(image)
        self.images.append(photo)
        label = tk.Label(self.scrollable_frame, image=photo)
        label.pack(side="left",padx=5,pady=5)
        
    def load_websites(self):
        file = askopenfile(mode='r', filetypes=[('Text files', '*.txt')])
        
        if file:
            for line in file:
                    if self.is_valid_url(line):
                        self.list_box.insert(tk.END,line.strip())
                        self.websites.append(line.strip())
        
            file.close()
            
    def is_valid_url(self,url):
        url = url.lower()
        if url.startswith("http://") or url.startswith("https://"):
                return True
        else:
            return False
        