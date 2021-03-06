#sc1341
from tkinter import Button, Label, Tk, PhotoImage, Menu
from image import image as cookieimage
import time
import pickle
import random
import threading
import logging
import sys
import os
from getpass import getuser


class UpgradesController:

    def __init__(self, data):
        if data != '':
            self.score = int(data["score"])
            self.auto_click_upgrade = int(data["auto_click_upgrade"])
            self.cookies_per_click_upgrade = int(data["cookies_per_click_upgrade"])
            self.random_bonus_upgrade = int(data["random_bonus_upgrade"])
        else:
            self.score = 0
            self.auto_click_upgrade = 0
            # SOme upgrades have to be 1 by default to have a cost...
            self.cookies_per_click_upgrade = 1
            self.random_bonus_upgrade = 0


class CookieClickerMainGUI:

    def __init__(self, data=''):
        self.root = Tk()
        #Backround color variable
        self.background_color = "white"
        self.upgrade_controller = UpgradesController(data)
        self.root.geometry("700x700")
        self.root.title("Cookie Clicker")
        self.root.config(bg=self.background_color)
        self.photo = PhotoImage(data=cookieimage)
        logging.basicConfig(filename="GUIlogs.log", level=logging.INFO)
        #Closing protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # Inits the score for the game, will change if .dat file exists
        self.score = self.upgrade_controller.score
        self.auto_click_upgrade = self.upgrade_controller.auto_click_upgrade
        self.cookies_per_click_upgrade = self.upgrade_controller.cookies_per_click_upgrade
        self.random_bonus_upgrade = self.upgrade_controller.random_bonus_upgrade
        self.thread_list = []

        # inital GUI components
        self.label = Label(self.root, text="Welcome to Cookie Clicker", font=("Helvetica", 16))
        self.version_label = Label(self.root, text="version 1.0", font=("Helvetica", 10))
        self.cookie_button = Button(self.root, text="click me!", command=self.cookie_clicked, image=self.photo)
        self.upgrades_button = Button(self.root, text="Upgrades", command=self.upgrades_GUI_menu, font=("Helvetica", 10))
        self.save_button = Button(self.root, text="Save data", command=self.export_data, font=("Helvetica", 10))
        self.score_label = Label(self.root, text=str(self.score), font=("Helvetica", 30))
        # self.cookie_debt_label = Label(self.root,text="You are in cookie debt",font=("Helvetica", 20))
        self.dark_mode_button = Button(self.root, text="Dark mode", command=self.dark_mode, font=("Helvetica", 10))
        self.light_mode_button = Button(self.root, text="Light mode", command=self.light_mode, font=("Helvetica", 10))
        self.color_menu_buttton = Button(self.root, text="Color Menu", command=self.choose_color_window, font=("Helvetica", 10))

        # pack the widgets inside the screen
        self.score_label.pack()
        self.label.pack()
        self.version_label.pack()
        self.cookie_button.pack()
        self.upgrades_button.pack()
        self.save_button.pack()
        self.dark_mode_button.pack()
        self.color_menu_buttton.pack()
        logging.info("Screen initialized")
        # Exit protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # main loop
        self.root.mainloop()
        logging.info("Main window loaded successfully...")

    # ----------------------- EXPORT DATA --------------------------------------------

    def export_data(self):
        '''Exports the data into a dictionary into the dat file that was created from the cookie_clicker.py file'''

        export_data = {"score": self.score, "auto_click_upgrade": self.upgrade_controller.auto_click_upgrade,
                       "cookies_per_click_upgrade": self.upgrade_controller.cookies_per_click_upgrade,
                       "random_bonus_upgrade": self.upgrade_controller.random_bonus_upgrade}

        with open('cookie.dat', 'wb') as f:
            pickle.dump(export_data, f)
        f.close()
        logging.info("Exported data to dat")

    # ----------------------- Dark mode/light mode --------------------------------------------

    def dark_mode(self):
        self.dark_mode_button.pack_forget()
        self.light_mode_button.pack()
        self.root.config(bg="black")
        # self.photo.config(bg="black")
        self.score_label.config(fg="white", bg="black")
        self.label.config(fg="white", bg="black")
        self.version_label.config(fg="white", bg="black")
        self.save_button.config(fg="white", bg="black")
        self.upgrades_button.config(fg="white", bg="black")
        self.light_mode_button.config(fg="white", bg="black")
        logging.info("Dark mode on")

    def light_mode(self):
        self.dark_mode_button.pack()
        self.light_mode_button.pack_forget()
        self.root.config(bg="white")
        self.score_label.config(fg="black", bg="white")
        self.save_button.config(fg="black", bg="white")
        self.upgrades_button.config(fg="black", bg="white")
        self.label.config(fg="black", bg="white")
        self.version_label.config(fg="black", bg="white")
        logging.info("Light mode on")

    # ----------------------- MAIN COOKIE CLICKED --------------------------------------------

    def cookie_clicked(self):
        '''Adds to the score when the cookie button is clicked, it then updates the label and prints out the results'''
        self.score += self.upgrade_controller.cookies_per_click_upgrade
        self.score_label.config(text=str(self.score))
        print("Button clicked: the score is: " + str(self.score))

    # ----------------------- MENU WINDOW --------------------------------------------

    def upgrades_GUI_menu(self):
        """This creates a pop-up window to modify your upgrades, it is easy to add more buttons/upgrades from here"""
        # Creates our root window
        self.root2 = Tk()
        self.root2.geometry("500x300")
        self.root2.title("Upgrades Menu")

        # Prices of the upgrades, this saves space in the "text" part of the button creation

        # Really, these varibles need to be in __init__ concider moving these if we want to progressivly increase the
        # cost of the cookies
        auto_click_price = "Buy Auto-click: $" + str(100 * self.upgrade_controller.auto_click_upgrade)
        cookies_per_click_price = "Buy more cookies per click: $" + str(
            20 * self.upgrade_controller.cookies_per_click_upgrade)
        random_bonus_price = "Buy Random Bonus: $" + str(10000)

        # Buttons

        self.auto_click_button = Button(self.root2, text=auto_click_price, command=self.auto_click)

        self.cookies_per_click_button = Button(self.root2, text=cookies_per_click_price,
                                               command=self.cookies_per_click)

        self.random_bonus_button = Button(self.root2, text=random_bonus_price, command=self.random_bonus)
        # Pack the buttons
        self.cookies_per_click_button.pack()
        self.auto_click_button.pack()
        self.random_bonus_button.pack()
        self.root2.mainloop()

    def change_backround_GUI(self):
        pass

    # ----------------------- UPGRADE FUNCTIONS --------------------------------------------

    def cookies_per_click(self):
        '''The number of cookies per click'''
        self.score -= 20 * self.upgrade_controller.cookies_per_click_upgrade + 20
        self.upgrade_controller.cookies_per_click_upgrade += 1
        self.score_label.config(text=str(self.score))

    def auto_click(self):
        '''Sets the autoclick to run, it subtracts the score by 100 times the number of upgrades that the auto_click
        has, it then sets the updatecontroller.auto_click_upgrade += 1'''

        self.score -= 100 * self.upgrade_controller.auto_click_upgrade
        self.upgrade_controller.auto_click_upgrade += 1
        self.score_label.config(text=str(self.score))
        t1 = threading.Thread(target=self.auto_click_thread_run)
        self.thread_list.append(t1)
        t1.start()
        try:
            self.auto_click_button.pack_forget()
        except:
            pass
        logging.info("Auto Click Upgrade Purchased by the user")

    def random_bonus(self):
        '''Random bonus of 10,000 cookies, it can only be purchased once, it costs 10,000 cookies,
         this function is called when the button is pressed,
        however it does not actaully do the logic of the random cookie,
        but rather starts a thread so we can use time.sleep without python crashing'''
        self.score -= 10000
        self.upgrade_controller.random_bonus_upgrade += 1
        self.score_label.config(text=str(self.score))
        random_thread = threading.Thread(target=self.random_bonus_thread_run)
        self.thread_list.append(random_thread)
        random_thread.start()
        try:
            self.random_bonus_button.pack_forget()
        except:
            pass
        logging.info("Random bonus upgrade Pressed and the thread has been successfully started")

    # ----------------------- THREADED FUNCTIONS --------------------------------------------

    def auto_click_thread_run(self):
        while True:
            time.sleep(1)
            self.score += 1
            self.score_label.config(text=str(self.score))

    def random_bonus_thread_run(self):
        '''This is the target of the random_bonus_buttton command
        that starts the chance of getting 10,000 bonus cookies every second'''
        while True:
            time.sleep(1)
            if 10 == random.randint(1, 100):
                self.score += 10000
                print("Here are 10000 random cookies... yay!")

    # -------------------------------- Exit function ----------------
    def on_closing(self):
        '''On the exit, the threads get killed
        https://christopherdavis.me/blog/threading-basics.html'''
        for thread in self.thread_list:
            thread.join()
        sys.exit()

    # ------------------ Color window ------------------------------
    def choose_color_window(self):
        """Choose a color for the backround, this automatically disables dark mode by default"""
        self.root3 = Tk()
        self.root3.geometry("400x400")
        self.root3.title("Customize Color")
        #Randomnote self.root.config(bg=colorhere)
        #Backround color vairbale is self.background_color = "white"
        #Widgets
        self.blue_button = Button(self.root3, text="Blue Background", command=self.blue_background).pack()
        self.orange_button = Button(self.root3, text="Orange Background", command=self.orange_background).pack()
        #Mainloop
        self.root3.mainloop()

    #------------------------color functions -----------------------------------

    def blue_background(self):
        """Sets the main background to blue and also changes the font color if needed"""
        self.root.config(bg="blue")
        self.score_label.config(fg="black", bg="blue")
        self.save_button.config(fg="black", bg="blue")
        self.upgrades_button.config(fg="black", bg="blue")
        self.label.config(fg="black", bg="blue")
        self.version_label.config(fg="black", bg="blue")
        self.light_mode_button.config(fg="black", bg="blue")
        self.color_menu_buttton.config(fg="black", bg="blue")
        self.dark_mode_button.config(fg="black", bg="blue")

    def orange_background(self):
        """Sets the main background to orange and also changes the font color if needed"""
        self.root.config(bg="orange")
        self.score_label.config(fg="black", bg="orange")
        self.save_button.config(fg="black", bg="orange")
        self.upgrades_button.config(fg="black", bg="orange")
        self.label.config(fg="black", bg="orange")
        self.version_label.config(fg="black", bg="orange")
        self.light_mode_button.config(fg="black", bg="orange")
        self.color_menu_buttton.config(fg="black", bg="orange")
        self.dark_mode_button.config(fg="black", bg="orange")
