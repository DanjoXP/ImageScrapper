import tkinter as tk
import tkinter.messagebox

class Window:
    
    website = []
    
    def __init__(self,title,x,y):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{x}x{y}")
        
        self.listBox = tk.Listbox(self.root, width=140,height=15)
        self.listBox.pack(anchor="nw",pady=0,padx=10)
        
        self.entryLabel = tk.Label(self.root, text="Enter Website To Scrape:")
        self.entryLabel.pack(anchor="nw",padx=10)
        
        self.entry = tk.Entry(self.root,width=100)
        self.entry.pack(anchor="nw",padx=10,pady=0)
        
        self.frame = tk.Frame(self.root,width=25,height=25)
        self.frame.pack(anchor="w",pady=10)
        
        self.addWebsiteButton = tk.Button(self.frame,text="Add Website",width=15,command=self.addWebsite)
        self.addWebsiteButton.pack(side=tkinter.LEFT,padx=10)
    
        self.clearWebsitesButton = tk.Button(self.frame,text="Clear Websites", width=15,command=self.clearWebsites)
        self.clearWebsitesButton.pack(side=tkinter.LEFT,padx=10)
        
        self.removeWebsiteButton = tkinter.Button(self.frame,text="Remove Website", width=15,command=self.removeWebsite)
        self.removeWebsiteButton.pack(side=tkinter.LEFT,padx=10)
       
        self.scraperButton = tk.Button(self.frame,text="Scrape Websites", width=15,command=self.scrapeWebsite)
        self.scraperButton.pack(side=tkinter.LEFT,padx=10)
        self.root.mainloop()
    
    def addWebsite(self):
        text = self.entry.get().strip()
        if not text:
           self.displayWarning("Unable To Peform Action", "You Cannot Leave Entry Box Empty!")
           return 
            
        self.listBox.insert(tk.END,self.entry.get())
        self.entry.delete(0,tk.END)
        self.website.append(text)
            
    def removeWebsite(self):
        selected = self.listBox.curselection()
        
        if not selected:
            self.displayWarning("Unable To Peform Action", "You Must Select Atleast 1 Website To Remove!")
            return
        
        for i in reversed(selected):
            self.website.remove(self.listBox.get(i))
            self.listBox.delete(i)
        
        print(self.website)
    
    def clearWebsites(self):
        self.listBox.delete(0,tkinter.END)
        self.website.clear()
        print(f"Websites : {self.website}")
        
    def displayWarning(self, error, message):
       tk.messagebox.showwarning(error,message)
       
    def scrapeWebsite(self):
        if(self.listBox.size() == 0):
            self.displayWarning("Unable To Perform Action", "No Websites Entered To Scrape!")
            return
        ## Scraper Logic Still To Implment
        ## Scraper will be on in seperate file Scraper.py
        