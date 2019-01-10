from tkinter import *
from image import image as cookieimage
import time

class UpgradesController:

    def __init__(self, data): 
        if data != '':
            self.score = int(data["score"])
            self.auto_click_upgrade = int(data["auto_click_upgrade"])
            self.cookies_per_click_upgrade = int(data["cookies_per_click_upgrade"])
        else:        
            self.auto_click_upgrade = 0
            #All upgrades have to be 1 by default, tis is due to the logic of the game using the upgrade number to determine the cost
            self.cookies_per_click_upgrade = 1


class CookieClickerMainGUI:

    def __init__(self, root, data=''):
        self.upgrade_controller = UpgradesController(data)
        root.geometry("700x700")
        root.title("Cookie Clicker")
        self.photo = PhotoImage(data=cookieimage)
        
        #Inits the score for the game, will change if .dat file exists
        self.score = 0
        self.data = data
        self.score = self.check_import_data(self.data)
        self.label = Label(root,text="Welcome to Cookie Clicker",font=("Helvetica", 16))
        self.cookie_button = Button(root,text="click me!", command=self.cookie_clicked, image=self.photo)
        self.upgrades_button = Button(root,text="Upgrades",command=self.upgrades_GUI_menu)
        self.score_label = Label(root,text=str(self.score),font=("Helvetica", 20))

        #pack the widgets inside the screen
        self.score_label.pack()
        self.label.pack()
        self.cookie_button.pack()
        self.upgrades_button.pack()
        
        
    def export_data(self):
        '''Exports the data into a dictionary into the dat file that was created from the cookie_clicker.py file
        The format of the export_data is as follows... Score, auto_click_upgrade, cookies_per_click_upgrade'''
        
        export_data = {"score":self.score,"auto_click_upgrade":self.upgrade_controller.auto_click_upgrade,
        "cookies_per_click_upgrade":self.upgrade_controller.cookies_per_click_upgrade}
        
        with open('cookie.dat','wb') as f:
            f.write(export_data)
        f.close()

    def cookie_clicked(self):
        '''Adds to the score when the cookie button is clicked, it then updates the label... the defualt it 
        the label updates ever 200 milliseconds, do not change this!'''
        self.score += self.upgrade_controller.cookies_per_click_upgrade
        self.score_label.config(text=str(self.score))
        print("Button clicked: the score is: " + str(self.score))

    def upgrades_GUI_menu(self):
        '''This creates a pop-up window to modify your upgrades, it is easy to add more buttons/upgrades from here'''
        self.root2 = Tk()
        self.root2.geometry("500x300")
        self.root2.title("Upgrades Menu")
        self.auto_click_button = Button(self.root2, text="Buy Auto-click", command=self.auto_click)
        self.cookies_per_click_button = Button(self.root2, text="Buy more cookies per click",command=self.cookies_per_click)
        self.cookies_per_click_button.pack()
        self.auto_click_button.pack()
        self.root2.mainloop()

    def cookies_per_click(self):
        '''The number of cookies per click'''
        self.score -= 20 * self.upgrade_controller.cookies_per_click_upgrade
        self.upgrade_controller.cookies_per_click_upgrade += 1
        self.score_label.config(text=str(self.score))

    def auto_click(self):
        '''Sets the autoclick to run, it subtracts the score by 100 times the number of upgrades that the auto_click 
        has, it then sets the updatecontroller.auto_click_upgrade += 1'''
        self.score -= 100 * self.upgrade_controller.auto_click_upgrade
        self.upgrade_controller.auto_click_upgrade += 1
        self.score_label.config(text=str(self.score))
        #Possibly open a thread here?
        '''
        while True:
            #THis is a known issue that causes the program to freeze than crash, concider time.time?
            time1 = time.time()
            if (sum(time1) + 1) == time.time():    
                self.score += 1 '''


'''
Added mac and windows feature so the file check works
Updated docs
Removed import_data form the GUI class, it is messy and dumb to do it that way, the data must be parsed before even entering the object
Removed calloing the export function from the cookie_clicked function because it slows down the program noticlbly to call revusive function in tkinter
Do not need line 10 in cookie_clicker
Do not need sys module at the moment in cookie_clicker or the GUI

Problems:
    the dat file is not creating WTF is happening there?
    

'''
