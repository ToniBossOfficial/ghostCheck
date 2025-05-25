from time import sleep,time
import threading
import tkinter
import tkinter.messagebox
import customtkinter
import os
import json
from bs4 import BeautifulSoup

import logging
logging.basicConfig(level=10)
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.support.wait import WebDriverWait
import undetected_chromedriver as uc

import random
# import undetected_chromedriver
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.window_dimensions = [1100,580]
        self.window_minSize = [800,400]

        self.following = False
        self.followers = False


        # configure window
        self.title("GhostCheck - a ToniBoss program")
        self.geometry(f"{self.window_dimensions[0]}x{self.window_dimensions[1]}")
        self.minsize(self.window_minSize[0],self.window_minSize[1])

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0,), weight=1)
        self.grid_rowconfigure((1, 2, 3, 4,), weight=0)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0) # Left sidebar frame
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="GhostCheck", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_login_button = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.run_in_thread(self.login))
        self.sidebar_login_button.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_unfollow_button = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.run_in_thread(self.unfollow_button_event))
        self.sidebar_unfollow_button.grid(row=2, column=0, padx=20, pady=10)
        # self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        # self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

       

        # create scrollable frame Followers
        self.scrollable_frame_followers = customtkinter.CTkScrollableFrame(self, label_text="Followers")
        self.scrollable_frame_followers.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame_followers.grid_columnconfigure(0, weight=1)
        
        #self.scrollable_frame_switches = []
        # for i in range(100):
        #     switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
        #     switch.grid(row=i, column=0, padx=10, pady=(0, 20))
        #     self.scrollable_frame_switches.append(switch)

        self.followers_upload_button = customtkinter.CTkButton(self, command=lambda: self.run_in_thread(self.browse_files, "Followers")) # Upload data button
        self.followers_upload_button.grid(row=2, column=1, padx=20, pady=10)

        # create scrollable frame
        self.scrollable_frame_following = customtkinter.CTkScrollableFrame(self, label_text="Users You Follow")
        self.scrollable_frame_following.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame_following.grid_columnconfigure(0, weight=1)

        self.following_upload_button = customtkinter.CTkButton(self, command=lambda: self.run_in_thread(self.browse_files, "Following")) # Upload data button
        self.following_upload_button.grid(row=2, column=2, padx=20, pady=10)



        

        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkScrollableFrame(self, label_text="Unfollow List")
        self.checkbox_slider_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        # self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        # self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        # self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        # self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        # self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        # self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")
        self.no_follow_back_button = customtkinter.CTkButton(self, command=lambda: self.run_in_thread(self.who_doesnt_follow_back)) # Button that on click shoud compare the lists and see who doesnt follow you back
        self.no_follow_back_button.grid(row=1, column=3, padx=20, pady=10)

        self.not_following_button = customtkinter.CTkButton(self, command=lambda: self.run_in_thread(self.who_we_dont_follow_back)) # Button for people we dont follow back
        self.not_following_button.grid(row=2, column=3, padx=20, pady=10)

        self.everyone_button = customtkinter.CTkButton(self, command=lambda: self.run_in_thread(self.everyone_once)) # Get everyone button
        self.everyone_button.grid(row=3, column=3, padx=20, pady=10)

        # set default values
        self.sidebar_login_button.configure(text="Login To Instagram")
        self.sidebar_unfollow_button.configure(state="disabled", text="Unfollow")
        self.followers_upload_button.configure(text="Upload Followers Data")
        self.following_upload_button.configure(text="Upload Following Data")
        self.no_follow_back_button.configure(state="disabled", text="Who doesn't Follow you Back")
        self.not_following_button.configure(state="disabled", text="Who you don't Follow Back")
        self.everyone_button.configure(state="disabled", text="Everyone")
        
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.settings_path = dir_path + '/settings.json'
        

        settings_exist = os.path.isfile(self.settings_path)

        if settings_exist:
            with open(self.settings_path, 'r') as file:
                data = json.load(file)
            
            self.appearance_mode_optionemenu.set(data['appearance'])
            self.scaling_optionemenu.set(data['scaling'])

            customtkinter.set_appearance_mode(data['appearance'])
            new_scaling_float = int(data['scaling'].replace("%", "")) / 100
            customtkinter.set_widget_scaling(new_scaling_float)
            
        else:
            self.appearance_mode_optionemenu.set("System")
            self.scaling_optionemenu.set("100%")

            settings = {'appearance':'System', 'scaling': '100%'}

            with open(self.settings_path,'w') as file:
                json.dump(settings, file, indent=4)

            
    
    def run_in_thread(self, target_func, *args):
        threading.Thread(target=target_func, args=args, daemon=True).start()

    def login(self):
        # self.driver = undetected_chromedriver.Chrome(headless=True,use_subprocess=False)
        self.driver = uc.Chrome()
        self.driver.get("https://www.instagram.com/")

        self.after(0, lambda: self.sidebar_unfollow_button.configure(state="normal"))

    def unfollow_button_event(self):
        
        # if not hasattr(self, 'driver'):
        #     tkinter.messagebox.showerror("Error", "You must log in first!")
        #     return
        
        checkboxes = self.checkbox_slider_frame.winfo_children()
        print(checkboxes)
        for checkbox in checkboxes:
            if isinstance(checkbox, customtkinter.CTkCheckBox) and checkbox.get() == 1:
                username = checkbox.cget("text").split(" : ", 1)[-1]

                # Perform unfollow logic for this username
                print(f"Would unfollow: {username}")
                self.unfollow_user(username)
                    
                    
                # --- Add your Selenium code here ---
                # Example: self.unfollow_user(username)
    def unfollow_user(self, username):
        driver = self.driver
        driver.get(f"https://www.instagram.com/{username}/")
        sleep(round(random.uniform(1.5,3),2))

        try:
            # Find the unfollow button using nested div strategy
            unfollow_button = driver.find_element(
                "xpath",
                "//button[.//div[normalize-space(text())='Ακολουθείτε']]"
            )
            unfollow_button.click()
            sleep(0.5)

            # Confirm unfollow
            confirm_button = driver.find_element(
            "xpath",
            "//div[@role='button'][.//span[text()='Να μην ακολουθώ']]"
            )
            confirm_button.click()
            sleep(0.7)

            print(f"Unfollowed {username}")

        except Exception as e:
            try:
                    # Find the unfollow button using nested div strategy
                unfollow_button = driver.find_element(
                    "xpath",
                    "//button[.//div[normalize-space(text())='Following']]"
                )
                unfollow_button.click()
                sleep(0.5)

                # Confirm unfollow
                confirm_button = driver.find_element(
                "xpath",
                "//div[@role='button'][.//span[text()='Unfollow']]"
                )
                confirm_button.click()
                sleep(0.6)
                print(f"Unfollowed {username}")
            except Exception as e:
                print(e)

        



    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

        with open(self.settings_path, 'r') as file:
            data = json.load(file)

        new_data = {'appearance': new_appearance_mode, 'scaling':data['scaling']}

        with open(self.settings_path,'w') as file:
            json.dump(new_data, file, indent=4)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

        with open(self.settings_path, 'r') as file:
            data = json.load(file)
            
        new_data = {'appearance': data['appearance'], 'scaling':new_scaling}

        with open(self.settings_path,'w') as file:
            json.dump(new_data, file, indent=4)

   
    def add_items_to_frame(self, frame , items, checkbox=False):
        if frame.winfo_children():
            for widget in frame.winfo_children():
                widget.destroy()  # deleting widget
        id_row = 0
        for i in items:
            if not checkbox:
                label = customtkinter.CTkLabel(master=frame, text=f"{id_row+1} : {i}")
                label.grid(row=id_row, column=0, padx=10, pady=(0, 20))
                id_row += 1
            else:
                checkbox_widget = customtkinter.CTkCheckBox(master=frame, text=f"{id_row+1} : {i}")
                checkbox_widget.grid(row=id_row, column=0, padx=10, pady=(0, 20))
                checkbox_widget.select()
                
                id_row += 1
    
    def who_doesnt_follow_back(self):
        difference = [item for item in self.following_list if item not in self.followers_list]
        self.after(0, lambda: self.add_items_to_frame(self.checkbox_slider_frame, difference, True))
    
    def who_we_dont_follow_back(self):
        difference = [item for item in self.followers_list if item not in self.following_list]
        self.after(0, lambda: self.add_items_to_frame(self.checkbox_slider_frame, difference, True))

    def everyone_once(self):
        combined = list(set(self.followers_list + self.following_list))
        self.after(0, lambda: self.add_items_to_frame(self.checkbox_slider_frame, combined, True))


    def browse_files(self, next):
        def task():
            error = False
            start_here_filepath = customtkinter.filedialog.askopenfilename()

            try:
                start_here_filepath = start_here_filepath.replace("start_here.html", "")
            except Exception as errorMSG:
                print(errorMSG)
                error = True

            if not error:
                try:
                    if next == "Following":
                        self.following = True
                        end_file = "connections/followers_and_following/following.html"
                        frame = self.scrollable_frame_following
                    elif next == "Followers":
                        self.followers = True
                        end_file = "connections/followers_and_following/followers_1.html"
                        frame = self.scrollable_frame_followers

                    filepath = start_here_filepath + end_file
                    with open(filepath, "r", encoding='utf-8') as file:
                        html_content = file.read()

                    soup = BeautifulSoup(html_content, 'html.parser')
                    link_texts = [a.get_text(strip=True) for a in soup.find_all('a')]

                    if next == "Following":
                        self.following_list = link_texts
                    elif next == "Followers":
                        self.followers_list = link_texts

                    self.after(0, lambda: self.add_items_to_frame(frame, link_texts))

                    if self.followers and self.following:
                        self.after(0, lambda: [
                            self.no_follow_back_button.configure(state="normal"),
                            self.not_following_button.configure(state="normal"),
                            self.everyone_button.configure(state="normal"),
                        ])

                except Exception as errorMSG:
                    print(errorMSG)

        self.run_in_thread(task)

        
        





if __name__ == "__main__":
    app = App()
    app.mainloop()