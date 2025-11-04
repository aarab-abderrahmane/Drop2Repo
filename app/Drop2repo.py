import subprocess
from customtkinter import *
import customtkinter as ctk
from tkinter import filedialog, messagebox
import sqlite3
import webbrowser
import sys
import tkinter as tk
import re
from PIL import Image
import platform
import threading
import time
import traceback  
from CTkMessagebox import CTkMessagebox
from tkinter import ttk
from CTkPDFViewer import CTkPDFViewer
from CTkToolTip import CTkToolTip


class SplashScreen:
    def __init__(self, app, on_complete_callback):
        self.app = app
        self.on_complete = on_complete_callback
        self.db_file = os.path.join(os.path.dirname(__file__), "app_settings.db")
        self.running = True
        
        self.app.resizable(False,False)
        self.app.geometry('935x525')


        self.center_window()
        
        self.app.iconbitmap(Registration.resource_path("send_icon.ico"))

        self.accepted = self.load_acceptance_status()
        
        if self.accepted:
            self.on_complete()
            return
            
        self.setup_ui()

    def center_window(self):

        self.app.update_idletasks()
        width = self.app.winfo_width()
        height = self.app.winfo_height()
        x = (self.app.winfo_screenwidth() // 2) - (width // 2)
        y = (self.app.winfo_screenheight() // 2) - (height // 2)
        self.app.geometry(f"+{x}+{y}")

    def setup_ui(self):

        self.frame = ctk.CTkFrame(self.app, fg_color="#1B1B19")
        self.frame.pack(fill="both", expand=True)

        self.sentences = [
            {
                "text": "⚫ No personal data is collected",
                "bg_color": "#ff2cfa",
                "text_color": "#000000"
            },

            {
                "text": "⚫ You are responsible for all changes you push",
                "bg_color": "#ff6c52",
                "text_color": "#0005fd"
            },
            
            {
                "text": "⚫ The application is free to use",
                "bg_color": "#07381f",
                "text_color": "#ff84fa"
            },
                        {
                "text": "⚫ This application is for personal use only",
                "bg_color": "#2c024a",
                "text_color": "#2df482"
            }
        ]


        self.current_sentence = 0
        self.typed_text = ""
        self.typing_speed = 30
        self.sentence_delay = 2000

        self.typing_label = ctk.CTkLabel(
            self.frame,
            text="",
            font=("Arial", 24, "bold"),
            text_color="#ffffff",
            wraplength=600,
            justify="center"
        )
        self.typing_label.pack(pady=80, padx=20, expand=True)


        self.bottom_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.bottom_frame.pack(side="bottom", pady=20)

        self.terms_frame = ctk.CTkFrame(self.bottom_frame,fg_color='transparent')
        self.terms_frame.pack(pady=10)

        self.terms_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            self.terms_frame,
            text="I agree to the ",
            variable=self.terms_var,
            text_color="white",
            border_color="white",
            checkbox_width=20,
            checkbox_height=20,
            font=("Arial", 12,'bold'),
            command=self.toggle_start_button
        ).pack(side="left")

        self.terms_link= ctk.CTkLabel(self.terms_frame,text="terms of use" ,cursor="hand2",font=('Arial',12,'underline'),text_color="#006ca5")
        self.terms_link.pack(side="left")
        self.terms_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/aarab-abderrahmane/python/releases/tag/6")) 

        self.start_btn = ctk.CTkButton(
            self.bottom_frame,
            text="Start Use",
            command=self.on_accept,
            state="disabled",
            border_color="black",
            border_width=2,
            corner_radius=30,
            text_color="yellow",
            hover_color="black",
            fg_color="transparent",
            text_color_disabled="black",
            height=40,
            width=100,
            hover=True,
            font=("Arial", 14, "bold")
        )
        self.start_btn.pack(pady=10)

        self.start_typing_effect()

    def start_typing_effect(self):

        self.running=True
        self.type_next_character()


    def type_next_character(self):

        if not self.running:
            return
            
        if len(self.typed_text) < len(self.sentences[self.current_sentence]["text"]):
            self.typed_text += self.sentences[self.current_sentence]["text"][len(self.typed_text)]
            try:
                self.frame.configure(fg_color=self.sentences[self.current_sentence]["bg_color"])
                self.typing_label.configure(
                    text=self.typed_text,
                    text_color=self.sentences[self.current_sentence]["text_color"]
                )
                
                self.app.update_idletasks()
                self.app.after(self.typing_speed, self.type_next_character)
            except Exception as e:
                print(f"Error in typing effect: {e}")
                self.running = False
        else:
            self.app.after(self.sentence_delay, self.next_sentence)

    def next_sentence(self):

        if not self.running:
            return
            
        self.typed_text = ""
        self.current_sentence = (self.current_sentence + 1) % len(self.sentences)
        self.type_next_character()

    def toggle_start_button(self):

        if hasattr(self, 'start_btn'):
            if self.terms_var.get():
                self.start_btn.configure(
                    state="normal",
                    fg_color="transparent",
                    text_color="yellow",
                    border_color='yellow'
                )
            else:
                self.start_btn.configure(
                    state="disabled",
                    fg_color="transparent",
                    text_color="black",
                    border_color='black',
                )



    def load_acceptance_status(self):

        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.execute("""CREATE TABLE IF NOT EXISTS 
                             app_settings (setting TEXT PRIMARY KEY, value TEXT)""")
                result = conn.execute("SELECT value FROM app_settings WHERE setting='terms_accepted'").fetchone()
                return result and result[0] == "1"
        except:
            return False

    def save_acceptance_status(self, accepted):

        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.execute("INSERT OR REPLACE INTO app_settings VALUES (?, ?)", 
                           ("terms_accepted", "1" if accepted else "0"))
        except Exception as e:
            print(f"Error saving acceptance: {e}")

    def on_accept(self):

        if self.terms_var.get():
            self.running = False
            self.save_acceptance_status(True)
            
            self.frame.pack_forget()
            self.frame.destroy()
            
            self.app.update_idletasks()
            
            self.app.after(100, self._complete_transition)

    def _complete_transition(self):

        self.app.resizable(False, False)
        self.on_complete()


class Registration:
    def __init__(self, app, switch_to_push):
        self.app = app
        self.switch_to_push = switch_to_push

        self.is_git_installed = self.check_git_installed()
        if not self.is_git_installed:
            messagebox.showerror("Git Not Installed", "Git is not installed on your system. Please install Git to proceed.")
            sys.exit(0)
            return
        

        self.frame = ctk.CTkFrame(self.app,fg_color="#000000")

        self.frame.pack(fill="both", expand=True)
        


        
        self.app.title('Drop2Repo')
        self.app.iconbitmap(self.resource_path("send_icon.ico")) 
        self.app.geometry('925x525')
        self.app.resizable(False,False)


        if self.check_git_authenticated():
            self.switch_to_push(self)
            return


        self.image = Image.open(self.resource_path("image_start.jpg"))
        self.photo = CTkImage(self.image, size=(350, 500))
        self.image_label = CTkLabel(self.frame, image=self.photo, text="")
        self.image_label.place(x=20, y=10)

        
        self.image = Image.open(self.resource_path("mouse.jpg"))
        self.photo = CTkImage(self.image, size=(150, 150))
        self.image_label = CTkLabel(self.frame, image=self.photo, text="")
        self.image_label.place(x=750, y=370)

        self.image = Image.open(self.resource_path("crown.jpg"))
        self.photo = CTkImage(self.image, size=(200, 180))
        self.image_label = CTkLabel(self.frame, image=self.photo, text="")
        self.image_label.place(x=400, y=90)

        self.image = Image.open(self.resource_path("lamp.jpg"))
        self.photo = CTkImage(self.image, size=(120, 120))
        self.image_label = CTkLabel(self.frame, image=self.photo, text="")
        self.image_label.place(x=835, y=-30)



        self.email_label = ctk.CTkLabel(self.frame, text="Registration",font=('Consolas',20,'bold'),text_color="#ffb2e6")
        self.email_label.place(x=585,y=80)

        
        self.image = Image.open(self.resource_path("send.png"))
        self.photo = CTkImage(self.image, size=(40, 40))
        self.image_label = CTkLabel(self.frame, image=self.photo, text="")
        self.image_label.place(x=720, y=70)


        self.email_entry = ctk.CTkEntry(self.frame, placeholder_text="  Enter your email",height=50,width=310,text_color="white",font=('Consolas',15,'bold'),fg_color="#131212",border_color="white",corner_radius=8)
        self.email_entry.place(x=520,y=150)

        self.username_entry = ctk.CTkEntry(self.frame, placeholder_text="  Enter your username",height=50,width=310,text_color="white",font=('Consolas',15,'bold'),fg_color="#131212",border_color="white",corner_radius=8)
        self.username_entry.place(x=520,y=230)

        self.save_button = ctk.CTkButton(self.frame, text="Login",width=310,height=40,corner_radius=15,font=('Consolas',15,'bold'), command=self.save_credentials,border_width=3,border_spacing=15,border_color="#ffb2e6",fg_color="#941b85",text_color="white",hover_color="#444444")
        self.save_button.place(x=520,y=330)

    
        
    def check_git_installed(self):
        try:
            is_windows = platform.system() == "Windows"

            subprocess.run(
                ['git', '--version'],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if is_windows else 0
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
        

    def check_git_authenticated(self):
        try:
            is_windows = platform.system() == "Windows"

            user_email = subprocess.check_output(
                ['git', 'config', '--global', 'user.email'],
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if is_windows else 0
            ).strip()
            user_name = subprocess.check_output(
                ['git', 'config', '--global', 'user.name'],
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if is_windows else 0
            ).strip()
            if user_email and user_name:
                return True
            return False
        except subprocess.CalledProcessError:
            return False
        

    @staticmethod
    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    


    def save_credentials(self):
        email = self.email_entry.get().strip()
        username = self.username_entry.get().strip()

        if not self.is_valid_email(email):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        if not username:
            messagebox.showerror("Error", "Please enter a valid username.")
            return

        is_windows = platform.system() == "Windows"

        subprocess.run(
            ['git', 'config', '--global', 'user.email', email],
            creationflags=subprocess.CREATE_NO_WINDOW if is_windows else 0
        )
        subprocess.run(
            ['git', 'config', '--global', 'user.name', username],
            creationflags=subprocess.CREATE_NO_WINDOW if is_windows else 0
        )

        messagebox.showinfo("Success", "Git credentials saved successfully!")
        self.switch_to_push(self)


    def is_valid_email(self, email):
        regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        
        if re.match(regex, email):
            return True
        else:
            return False


class GitPushPage:
    def __init__(self, app):
        self.app = app
        self.file_checkboxes = {}
        self.select_all_var = ctk.BooleanVar()
        self.switch_var = ctk.BooleanVar(value=False)
        self.bypass_gpg_var = ctk.BooleanVar(value=False)
        self.staged_files_buttons = {}
        self.has_changes = False
        self.app.resizable(False,False)
        self.app.geometry('925x525')
        


        self.connect = sqlite3.connect('modifs.db')
        self.cursor = self.connect.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS modifs (
        path TEXT,
        switch_name TEXT,
        state_boolean BOOLEAN,
        id INTEGER PRIMARY KEY
        )''')
        self.connect.commit()



        self.home_frame = ctk.CTkFrame(app,fg_color="#131212")
        self.home_frame.pack(side='left', fill="both", expand=True)

        self.paned_window = tk.PanedWindow(self.home_frame, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, bg="#131212",sashwidth=2)
        self.paned_window.pack(fill="both", expand=True)

        self.frame_left = ctk.CTkFrame(self.paned_window,width=450, corner_radius=0,border_width=0,fg_color="#131212")
        self.paned_window.add(self.frame_left)


        self.frame_right = ctk.CTkFrame(self.paned_window,width=450, corner_radius=0,border_width=0,fg_color="#131212")
        self.paned_window.add(self.frame_right)

        self.frame_input_path = ctk.CTkFrame(self.frame_left,width=800,height=30,fg_color="transparent")

        self.frame_buttons = ctk.CTkFrame(self.frame_left,width=800,height=30,corner_radius=15,border_width=1,border_color='#211f1f' , fg_color="#0A0909")

        self.frame_inside_buttons_0 = ctk.CTkFrame(self.frame_buttons,fg_color="transparent",corner_radius=15)
        self.frame_inside_buttons_1 = ctk.CTkFrame(self.frame_buttons,fg_color="transparent",corner_radius=15,width=310)
        self.frame_inside_buttons_2 = ctk.CTkFrame(self.frame_buttons,fg_color="transparent",corner_radius=15,width=310)


        self.home_frame.update()
        self.paned_window.sash_place(0, 450, 0) 

        
        self.combo_box = CTkComboBox(
            self.frame_left,
            values=["Get Premium", "Documentation", "Help","Logout","last version",'version : 8.0.1'],
            command=self.on_combobox_select,
            width=120,
            height=30,
            font=('Consolas', 12, 'bold'),
            dropdown_font=('Consolas', 12,'bold'),
            corner_radius=8,
            fg_color="black",
            button_color="#6411ad",
            border_color="#6411ad",
            button_hover_color="#444444",
            dropdown_hover_color="#a50044",
            text_color="white",
            justify="left",
            dropdown_fg_color="#333333",
            dropdown_text_color="#d7d7d9"
        )

        

        self.combo_box.set(" M E N U ")
        self.combo_box.place(x=10,y=10)


        self.brand_frame= ctk.CTkFrame(self.frame_right,fg_color='transparent')

        self.name = ctk.CTkLabel(self.brand_frame, text="@aarab-abderrahmane", text_color="white",font=('Consolas',12,'bold'))
        self.name.pack(pady=0)
        self.name.configure(cursor="hand2")
        self.name.bind("<Button-1>", lambda event : self.open_link("1",event))


        self.emty_space = ctk.CTkLabel(self.frame_left,text="")
        self.emty_space.pack(pady=35)

        self.folder_entry = ctk.CTkEntry(self.frame_input_path, height=45,width=310,font=('Comic Sans MS',15,'bold'), placeholder_text="folder path",border_color="#211f1f",border_width=3,text_color="#ffbe29",corner_radius=8,fg_color="#0A0909")
        self.folder_entry.pack(side="left",padx=10)
        self.frame_input_path.pack(pady=10)
        self.folder_entry.bind('<Return>', self.process_folder_path)  


        self.image_history = Image.open(Registration.resource_path("history.png"))
        self.photo_history = CTkImage(self.image_history, size=(30, 30))

        self.history_label = ctk.CTkLabel(self.frame_input_path, image=self.photo_history, text="",fg_color='transparent',cursor="hand2")
        self.history_label.bind("<Button-1>", self.open_path_history)
        self.history_label.pack(side="right")


        self.image_folder = Image.open(Registration.resource_path("file-explorer.png"))
        self.photo_folder = CTkImage(self.image_folder, size=(37, 30))


        self.folder_label = ctk.CTkLabel(self.frame_inside_buttons_1, image=self.photo_folder, text="",fg_color='transparent',cursor="hand2")

        self.folder_label.bind("<Button-1>", self.select_folder)


        self.frame_buttons.pack(pady=10)

        
        self.commit_entry = ctk.CTkEntry(self.frame_inside_buttons_0,height=30,width=310,font=('Consolas',17,'bold'), placeholder_text="your commit",border_width=0,corner_radius=15,fg_color='transparent',border_color="gray")
        self.commit_entry.pack(pady=5)

        self.push_button = ctk.CTkButton(self.frame_left, text="Push to GitHub", command=self.push_to_github, fg_color="#081F0C",hover_color="#115029",height=40,text_color="#00ff62", corner_radius=0,font=('Consolas', 14,'bold'))
        self.push_button.pack(anchor="s",fill="x", side="bottom")



        self.frame_top=ctk.CTkFrame(self.frame_right,height=100,fg_color='black',corner_radius=0 , border_width=1)
        self.frame_top.pack(side="top",fill="x")

        self.select_all_checkbox = ctk.CTkCheckBox(self.frame_top, text="Select All",font=('Consolas',15,'bold'),text_color="#e0aaff",fg_color="#0aa023",hover_color="#0A0909",checkbox_width=25,checkbox_height=25,corner_radius=8,border_width=2, variable=self.select_all_var, command=self.toggle_select_all)
        self.select_all_checkbox.pack(padx=10,pady=10,side="left")

        
        self.image_refresh = Image.open(Registration.resource_path("refresh-page-option.png"))
        self.photo_refresh = CTkImage(self.image_refresh, size=(25, 25))
        

        self.refresh_button = ctk.CTkButton(
        self.frame_top,
        text="",
        width=50, 
        height=35, 
        fg_color="black", 
        border_color="gray",
        border_width=2,
        corner_radius=8,
        image=self.photo_refresh,
        command=self.update_git_status,
        hover_color="#252422"
        )

        self.refresh_button.pack(padx=10,pady=15,side="right")


        self.file_list_frame = ctk.CTkScrollableFrame(self.frame_right, width=400, height=400,fg_color='transparent')
        self.file_list_frame.pack(fill='x',expand=True)


        self.image_setting = Image.open(Registration.resource_path("setting-2.png"))
        self.photo_setting = CTkImage(self.image_setting, size=(45, 45))

        self.setting_label = ctk.CTkLabel(self.frame_inside_buttons_1, image=self.photo_setting, text="",fg_color='transparent',cursor="hand2")

        self.setting_label.bind("<Button-1>", self.open_settings)



        self.image_adnaced_settings = Image.open(Registration.resource_path("tools.png"))
        self.photo_adnaced_settings = CTkImage(self.image_adnaced_settings, size=(15, 15))

        self.advanced_settings = ctk.CTkButton(
            self.frame_left,
            image=self.photo_adnaced_settings,
            text="Other tools",
            hover_color="#2b2b2b",
            command=self.open_additional_page,
            fg_color='transparent',
            corner_radius=8,
            font=('Consolas', 14,'bold', 'underline'),

        )
        self.advanced_settings.pack(pady=0)



        self.progress_bar = ctk.CTkProgressBar(
            self.frame_left, 
            width=310, 
            height=8, 
            fg_color="#2b2b2b",
            corner_radius=5,
            border_color="green",
            border_width=1,
            mode="indeterminate")
        
        self.image_pull = Image.open(Registration.resource_path("cloud.png"))
        self.photo_pull = CTkImage(self.image_pull, size=(35, 35))



        self.pull_button = ctk.CTkButton(
            self.frame_inside_buttons_1,
            image=self.photo_pull,
            text="",
            command=self.pull_from_github,
            fg_color="#0A0909",
            corner_radius=15,
            font=('Consolas',12,'bold'),
            width=30,
            height=20,
            hover_color="#0A0909",
            bg_color="transparent",
            border_width=0,
            state="disabled"
        )



        self.image_delete = Image.open(Registration.resource_path("trash.png"))
        self.photo_delete = CTkImage(self.image_delete, size=(15, 15))

        self.delete_last_commit_button = ctk.CTkButton(
            self.frame_inside_buttons_2,
            text="del",
            image=self.photo_delete,
            command=self.delete_last_commit,
            hover_color="#211f1f",
            fg_color="black",
            corner_radius=15,
            width=90,
            height=40,
            text_color="#65F7FF",
            border_color="#211f1f",
            border_width=2,
            font=('Consolas', 14, 'bold')
        )
        self.delete_last_commit_button.pack(side='left')


        self.image_edit = Image.open(Registration.resource_path("edit.png"))
        self.photo_edit = CTkImage(self.image_edit, size=(17, 17))

        self.edit_last_commit_button = ctk.CTkButton(
            self.frame_inside_buttons_2,
            text="Edit",
            image=self.photo_edit,
            command=self.edit_last_commit,
            hover_color="#211f1f",
            fg_color="black",
            corner_radius=15,
            width=90,
            height=40,
            text_color="#f84e68",
            border_color="#211f1f",
            border_width=2,
            font=('Consolas', 14, 'bold')
        )
        self.edit_last_commit_button.pack(pady=5,padx=4, side='left')


        self.image_commit = Image.open(Registration.resource_path("time.png"))
        self.photo_commit = CTkImage(self.image_commit, size=(20, 20))

        self.commit_button = ctk.CTkButton(
            self.frame_inside_buttons_2,
            text="commit",
            image=self.photo_commit,
            command=self.commit_changes,
            hover_color="#211f1f",
            fg_color="black",
            border_color="#211f1f",
            border_width=2,
            corner_radius=15,
            text_color="#a0f759",
            font=('Consolas', 14, 'bold'),
            height=40,
            width=50,
        )
        self.commit_button.pack(side="left")

        self.frame_inside_buttons_0.pack(padx=10,pady=10)
        self.frame_inside_buttons_1.pack(padx=10,pady=5,fill="x", expand=True )
        self.line_label = ctk.CTkFrame(
            self.frame_buttons,
            width=300,
            height=2,
            corner_radius=100,
            fg_color="#211f1f",
        )


        self.folder_label.pack(side="left",padx=4)
        self.setting_label.pack(side="right",padx=0,pady=3)

        self.pull_button.pack(padx=0,side='right')







        self.brand_frame.pack(side='bottom',fill="x")


        self.remote_check_active = True
        self.start_remote_check()

        
        self.progress_bar.configure(progress_color="green")

        self.progress_bar.set(0.5)
        self.progress_bar.pack(pady=10)
        self.progress_bar.pack_forget() 
                
        self.commit_entry.bind('<Return>',lambda event : self.push_to_github())
    
        self.reload_data()




        self.load_switch_states()

        switch_state = self.switch_var.get()
        if switch_state is not None:
            self.switch_var.set(switch_state)
        else:
            self.switch_var.set("False")


    def update_switches_based_on_path(self, folder_path):
        try:
            conn = sqlite3.connect('modifs.db')
            cursor = conn.cursor()
            cursor.execute("SELECT state_boolean FROM modifs WHERE path = ?", (folder_path,))
            result = cursor.fetchone()
            
            if result:
                state = result[0]
                self.switch_var.set(state)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            if 'conn' in locals():
                conn.close()


    def open_path_history(self,event):

        self.home_frame.pack_forget()
        PathHistoryPage(self.app, self)


    def update_refresh_button_color(self):
        if self.has_changes:
            self.refresh_button.configure(fg_color="#123601",border_color="#1ef801", hover_color="#000000",border_width=2)

        else:
            self.refresh_button.configure(fg_color="black", hover_color="#3e224b",border_width=2,border_color="gray")

    def commit_changes(self):
        self.commit_button.configure(state="disabled")
        
        self.progress_bar.pack(pady=10)
        self.progress_bar.start()
        
        threading.Thread(
            target=self._execute_commit_operation,
            daemon=True
        ).start()


    def _execute_commit_operation(self):
        try:
            repo_path = self.folder_entry.get().strip()
            commit_message = self.commit_entry.get().strip()

            if not repo_path:
                self.app.after(0, messagebox.showerror, "Error", "Please select a project folder first.")
                return

            if not commit_message:
                self.app.after(0, messagebox.showerror, "Error", "Please enter a commit message.")
                return

            selected_files = [f for f, (var, _, is_staged) in self.file_checkboxes.items() 
                            if not is_staged and var.get()]

            if not selected_files:
                self.app.after(0, messagebox.showerror, "Error", "Please select at least one file to commit.")
                return

            is_windows = platform.system() == "Windows"
            creation_flags = subprocess.CREATE_NO_WINDOW if is_windows else 0

            add_result = subprocess.run(
                ["git", "-C", repo_path, "add"] + selected_files,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=creation_flags
            )

            if add_result.returncode != 0:
                raise Exception(f"Failed to add files:\n{add_result.stderr}")

            commit_cmd = ["git", "-C", repo_path, "commit", "-m", commit_message]
            if self.bypass_gpg_var.get():
                commit_cmd.append("--no-gpg-sign")

            commit_result = subprocess.run(
                commit_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=creation_flags
            )

            if commit_result.returncode == 0:
                self.app.after(0, messagebox.showinfo, "Success", "Changes committed successfully!")
                self.app.after(0, self.update_git_status)
                
                if self.switch_var.get():
                    self.app.after(0, self.commit_entry.delete, 0, 'end')
                    self.app.after(0, self.commit_entry.insert, 0, commit_message)
            else:
                raise Exception(f"Failed to commit:\n{commit_result.stderr}")

        except Exception as e:
            self.app.after(0, messagebox.showerror, "Error", f"An error occurred:\n{str(e)}")
            print(traceback.format_exc())
        finally:
            self.app.after(0, self.progress_bar.stop)
            self.app.after(0, self.progress_bar.pack_forget)
            self.app.after(0, lambda: self.commit_button.configure(state="normal"))
            

    def edit_last_commit(self):
        repo_path = self.folder_entry.get().strip()
        new_message = self.commit_entry.get().strip()
        
        if not repo_path:
            messagebox.showerror("Error", "Please select a project folder first.")
            return
            
        if not new_message:
            messagebox.showerror("Error", "Please enter a commit message first.")
            return
        
        try:
            is_windows = platform.system() == "Windows"
            creation_flags = subprocess.CREATE_NO_WINDOW if is_windows else 0
            
            result = subprocess.run(
                ["git", "-C", repo_path, "log", "-1", "--pretty=%B"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=creation_flags
            )
            
            if result.returncode != 0:
                messagebox.showerror("Error", f"Failed to get last commit:\n{result.stderr}")
                return
                
            last_message = result.stdout.strip()
            
            if new_message == last_message:
                messagebox.showwarning("Warning", "The new message is identical to the last commit message.")
                return
                
            confirm = messagebox.askyesno(
                "Confirm Edit",
                f"Are you sure you want to change the last commit message?\n\n"
                f"Old message: {last_message}\n"
                f"New message: {new_message}",
                icon='question'
            )
            
            if not confirm:
                return
                
            amend_result = subprocess.run(
                ["git", "-C", repo_path, "commit", "--amend", "-m", new_message],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=creation_flags
            )
            
            if amend_result.returncode == 0:
                messagebox.showinfo("Success", "Last commit message updated successfully!")
                
                if self.switch_var.get():
                    self.commit_entry.delete(0, 'end')
                    self.commit_entry.insert(0, new_message)
            else:
                messagebox.showerror("Error", f"Failed to edit last commit:\n{amend_result.stderr}")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")


    def update_settings_from_db(self):

        self.load_switch_states()
        
        switch_state = self.switch_var.get()
        if switch_state is not None:
            self.switch_var.set(switch_state)
        else:
            self.switch_var.set(False)
        
        self.cursor.execute("SELECT state_boolean FROM modifs WHERE path = ? AND switch_name = 'show_delete_button'", 
                        (self.folder_entry.get().strip(),))
        result = self.cursor.fetchone()
        if result:
            state = bool(result[0])
            if state:
                self.line_label.pack(pady=5,fill="x")
                self.frame_inside_buttons_2.pack(pady=5,fill="x", expand=True ,side="left")
            else:
                self.frame_inside_buttons_2.pack_forget()
                self.line_label.pack_forget()


    def delete_last_commit(self):
        repo_path = self.folder_entry.get().strip()
        if not repo_path:
            messagebox.showerror("Error", "Please select a project folder first.")
            return

        try:
            is_windows = platform.system() == "Windows"
            creation_flags = subprocess.CREATE_NO_WINDOW if is_windows else 0

            check_push = subprocess.run(
                ["git", "-C", repo_path, "log", "origin/main..main"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=creation_flags
            )

            if check_push.returncode != 0:
                messagebox.showerror("Error", f"Failed to check commit status:\n{check_push.stderr}")
                return

            if not check_push.stdout.strip():
                messagebox.showwarning(
                    "Cannot Delete",
                    "The last commit has already been pushed to GitHub.\n"
                    "You cannot delete pushed commits for safety reasons.",
                    icon='warning'
                )
                return

            confirm = messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete the last local commit?\n"
                "This action cannot be undone!",
                icon='question'
            )
            if not confirm:
                return

            result = subprocess.run(
                ["git", "-C", repo_path, "reset", "--hard", "HEAD~1"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=creation_flags
            )

            if result.returncode == 0:
                messagebox.showinfo("Success", "Last unpushed commit deleted successfully!")
                self.update_git_status()
            else:
                messagebox.showerror("Error", f"Failed to delete last commit:\n{result.stderr}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}") 


    def process_folder_path(self, event=None):

        folder_path = self.folder_entry.get().strip()
        
        if not folder_path:
            messagebox.showerror("Error", "Please enter a folder path")
            return
        
        if not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Folder path does not exist")
            return
        
        if not self.is_git_repository(folder_path):
            messagebox.showerror("Error", "The selected folder is not a Git repository")
            return

        self.progress_bar.pack(pady=10)
        self.progress_bar.start()
        self.folder_entry.configure(state="disabled")

        try:
            self.cursor.execute('INSERT INTO modifs (path, state_boolean) VALUES (?, ?)', 
                                (folder_path, False))
            self.connect.commit()
        except sqlite3.IntegrityError:
            pass
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to save path: {str(e)}")
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            self.folder_entry.configure(state="normal")
            return

        threading.Thread(
            target=self.update_database_and_status,
            args=(folder_path, 'modifs.db'),
            daemon=True
        ).start()


    def update_database_and_status(self, folder_path, db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            try:
                cursor.execute('INSERT INTO modifs (path, state_boolean) VALUES (?, ?)', 
                            (folder_path, True))
            except sqlite3.IntegrityError:
                cursor.execute('UPDATE modifs SET state_boolean = ? WHERE path = ?', 
                            (True, folder_path))
            
            cursor.execute('UPDATE modifs SET state_boolean = ? WHERE path != ?', 
                        (False, folder_path))
            
            conn.commit()
        except sqlite3.Error as e:
            self.app.after(0, lambda: messagebox.showerror("Database Error", f"Failed to update path: {str(e)}"))
        finally:
            if 'conn' in locals():
                conn.close()
            self.app.after(0, self.hide_loading_indicator)

    def update_ui_after_success(self, folder_path):

        self.folder_entry.delete(0, 'end')
        self.folder_entry.insert(0, folder_path)
        self.update_git_status()
        self.select_all_var.set(False)
        
        try:
            self.cursor.execute("DELETE FROM modifs")
            self.cursor.execute(
                'INSERT INTO modifs (path, state_boolean) VALUES (?, ?)',
                (folder_path, False)
            )
            self.connect.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Sync Error", 
                            f"Failed to sync main database:\n{str(e)}")

    def hide_loading_indicator(self):

        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.folder_entry.configure(state="normal")


    def is_git_repository(self, path):

        git_dir = os.path.join(path, '.git')
        return os.path.isdir(git_dir)
    
    def open_additional_page(self, event=None):

        self.home_frame.pack_forget()
        self.additional_page = AdditionalPage(self.app, self)



    def open_settings(self, event=None):
        self.home_frame.pack_forget()
        self.app.settings_frame = Settings(self.app, self)
        self.app.settings_frame.load_switch_state()


    def open_gmail(self):
      
        self.gmail_window = ctk.CTkToplevel(self.app,fg_color="black")
        self.gmail_window.title("Compose Email")
        self.gmail_window.geometry("500x340")
        self.gmail_window.resizable(False,False)

      
        from PIL import Image, ImageTk

        self.image = Image.open(Registration.resource_path("treasure_box_secret_prize_award_rich_coin_gold_game_icon_262449.ico"))
        self.photo = ImageTk.PhotoImage(self.image)

        self.gmail_window.iconphoto(False, self.photo)

        self.gmail_window.lift()
        self.gmail_window.attributes("-topmost", True)

        window_width = 400
        window_height = 300
        screen_width = self.gmail_window.winfo_screenwidth()
        screen_height = self.gmail_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.gmail_window.geometry(f"+{x}+{y}")




        self.subject_entry = ctk.CTkEntry(
            self.gmail_window,
            placeholder_text="Enter the subject...",
            width=360,
            height=45,
            border_width=0,
            fg_color="#ff8ae4",
            corner_radius=5,
            text_color="black",
            font=('Consolas', 14,'bold'),
            placeholder_text_color="black"
        )
        self.subject_entry.pack(padx=20,pady=25)


        self.body_label = ctk.CTkLabel(self.gmail_window, text="body :",text_color="white",fg_color="transparent", font=('Consolas', 14, 'bold'))
        self.body_label.pack(pady=0)
        
        self.body_entry = ctk.CTkTextbox(
            self.gmail_window,
            border_color="white",
            border_width=0,
            corner_radius=5,
            fg_color="#2b2b2b",
            width=360,
            height=150,
            font=('Consolas', 12)
        )
        self.body_entry.pack(pady=5)
        


        self.send_button = ctk.CTkButton(
            self.gmail_window,
            text="Send",
            command=self.compose_and_open_gmail,
            width=360,
            height=40,
            corner_radius=5,
            fg_color="black",
            border_color="#ff6642",
            hover_color="#ff6642",
            border_width=1,
            font=('Consolas', 15, 'bold')
        )
        self.send_button.pack(pady=10)

        
    def compose_and_open_gmail(self):

        subject = self.subject_entry.get().strip()
        body = self.body_entry.get("1.0", "end-1c").strip()

        if not subject or not body:
            messagebox.showerror("Error", "Please fill in both the subject and message.")
            return

        email = "abderrahmanerb.contact@gmail.com"

        gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={email}&su={subject}&body={body}"
        
        webbrowser.open(gmail_url)

        self.gmail_window.destroy()


    def on_combobox_select(self, choice):

        if choice == "Get Premium":
            self.combo_box.set(" M E N U ")
            self.open_link('2')

        elif choice == "Help":
            self.combo_box.set(" M E N U ")
            self.open_gmail()

        elif choice == "Logout":
            self.combo_box.set(" M E N U ")
            self.logout_user()  

        elif choice == "Documentation":
            self.combo_box.set(" M E N U ")
            self.open_documentation_page()
        
        elif choice =="version : 7.1.1":
            self.combo_box.set(" M E N U ")
            self.open_link("3")
        
        elif choice =="last version":
            self.combo_box.set(" M E N U ")
            self.open_link("4")

        else :    self.combo_box.set(" M E N U ")




    def logout_user(self):

        confirm = CTkMessagebox(
            title="Confirm Logout",
            message="Are you sure you want to logout?\nThis will remove your Git credentials.",
            icon="question",
            option_1="No",
            option_2="Yes"
        )
        
        if confirm.get() != "Yes":
            self.combo_box.set(" M E N U ")
            return
        
        try:
            is_windows = platform.system() == "Windows"
            creation_flags = subprocess.CREATE_NO_WINDOW if is_windows else 0
            
            subprocess.run(
                ["git", "config", "--global", "--unset", "user.name"],
                check=True,
                creationflags=creation_flags
            )
            subprocess.run(
                ["git", "config", "--global", "--unset", "user.email"],
                check=True,
                creationflags=creation_flags
            )
            
            CTkMessagebox(
                title="Success", 
                message="Logged out successfully.\nGit user name and email have been removed.",
                icon="check"
            )
            
            self.home_frame.pack_forget()
            
            Registration(self.app, self.create_git_push_page)
            
        except subprocess.CalledProcessError as e:
            CTkMessagebox(
                title="Error", 
                message=f"Failed to remove Git configurations:\n{str(e)}",
                icon="cancel"
            )
        finally:
            self.combo_box.set(" M E N U ")


    def create_git_push_page(self, registration_frame):

        registration_frame.frame.pack_forget()
        registration_frame.frame.destroy()
        GitPushPage(self.app)

    def open_documentation_page(self, event=None):
        self.home_frame.pack_forget()
        self.additional_page = DocumentaionPage(self.app, self) 


    def run_git_command(self, command, repo_path):
        is_windows = platform.system() == "Windows"

        if is_windows:
            process = subprocess.Popen(
                command,
                cwd=repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            process = subprocess.Popen(
                command,
                cwd=repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        stdout, stderr = process.communicate()
        return stdout, stderr
    

    def start_remote_check(self):
      threading.Thread(target=self.check_status_changes_loop, daemon=True).start()

    def check_status_changes_loop(self):
        while self.remote_check_active:
            self.check_remote_changes()
            self.check_local_changes()
            time.sleep(2)

    def check_local_changes(self):
        repo_path = self.folder_entry.get().strip()
        if not repo_path:
            return

        try:
            result = subprocess.run(
                ['git', '-C', repo_path, 'status', '--porcelain'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            )
            
            has_changes = bool(result.stdout.strip())
            if has_changes != self.has_changes:
                self.has_changes = has_changes
                self.app.after(0, self.update_refresh_button_color)
                
        except Exception as e:
            print(f"Error checking local changes: {e}")    

    def check_remote_changes_loop(self):
    
        while self.remote_check_active:
            self.check_remote_changes()
            time.sleep(3)

    
    def check_remote_changes(self):
        repo_path = self.folder_entry.get().strip()
        if not repo_path:
            return

        try:
            is_windows = platform.system() == "Windows"

            fetch_process = subprocess.Popen(
                ["git", "-C", repo_path, "fetch"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if is_windows else 0
            )
            fetch_process.communicate(timeout=5)

            status_process = subprocess.Popen(
                ["git", "-C", repo_path, "status", "-uno"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if is_windows else 0
            )
            stdout, _ = status_process.communicate(timeout=10)

            if "Your branch is behind" in stdout:
                self.app.after(0, self.enable_pull_button)
            else:
                self.app.after(0, self.disable_pull_button)

        except subprocess.TimeoutExpired:
            print("Git fetch/status took too long, skipping this check.")
        except Exception as e:
            print(f"Error checking remote changes: {e}")


    def enable_pull_button(self):
        self.image_pull = Image.open(Registration.resource_path("cloud_enable.png"))
        self.photo_pull = CTkImage(self.image_pull, size=(35, 35))
   
        self.pull_button.configure(state="normal",image=self.photo_pull,cursor="hand2",fg_color="#0A0909")

    def disable_pull_button(self):
        self.image_pull = Image.open(Registration.resource_path("cloud.png"))
        self.photo_pull = CTkImage(self.image_pull, size=(35, 35))


        self.pull_button.configure(state="disabled",image=self.photo_pull,fg_color="#0A0909")


    def pull_from_github(self):
        repo_path = self.folder_entry.get().strip()
        if not repo_path:
            messagebox.showerror("Error", "Please select a project folder.")
            return
        
        self.cleanup_previous_pull()

        self.progress_bar.pack(pady=10)
        self.progress_bar.start()
        self.pull_button.configure(state="disabled",fg_color="#0A0909")
        
        
        
        self.pull_output = []

        threading.Thread(target=self.run_pull_operation, args=(repo_path,), daemon=True).start()


    def show_pull_details(self):

        details_window = ctk.CTkToplevel(self.app,fg_color='black')
        details_window.title("Pull Operation Details")
        details_window.geometry("380x400")
        window_width = 380
        window_height = 400
        screen_width = details_window.winfo_screenwidth()
        screen_height = details_window.winfo_screenheight()
        position_x = int((screen_width - window_width) / 2)
        position_y = int((screen_height - window_height) / 2)
        details_window.geometry(f"+{position_x}+{position_y}")
        details_window.attributes('-topmost', True)
        details_window.focus()
        
        textbox = ctk.CTkTextbox(
            details_window,
            wrap="word",
            scrollbar_button_color="#FF0000",
            scrollbar_button_hover_color="#CC0000",
            corner_radius=15,
            fg_color="#333638" ,
            font=('Consolas', 13)
              )
        textbox.pack(fill="both", expand=True, padx=10, pady=10)
        
        for line in self.pull_output:
            textbox.insert("end", line + "\n")
            


    def run_pull_operation(self, repo_path):
        try:
            is_windows = platform.system() == "Windows"
            
            process = subprocess.Popen(
                ["git", "-C", repo_path, "pull"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if is_windows else 0
            )
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.pull_output.append(output.strip())
            
            _, stderr = process.communicate()
            
            if stderr:
                self.app.after(0, self.show_error, f"Failed to pull changes")
            else:
                self.app.after(0, self.show_info, "Changes pulled successfully!")
                self.app.after(0, self.show_success_with_details_button)
                self.app.after(0, self.update_git_status)

        except Exception as e:
            self.app.after(0, self.show_error, f"An error occurred:\n{str(e)}")
        finally:
            self.app.after(0, self.progress_bar.stop)
            self.app.after(0, self.progress_bar.pack_forget)
            self.app.after(0, lambda: self.pull_button.configure(state="normal"))


    def show_success_with_details_button(self):
            
                self.details_button = ctk.CTkButton(
                self.frame_left,
                text="Show Detailed Output",
                command=self.show_pull_details,
                fg_color="#203635",
                text_color="#20cc9c",
                border_color="#20cc9c",
                hover_color="#2b5755",
                border_width=1,
                width=150,
                height=30,
                font=('Consolas', 12)
                )
                self.details_button.pack(pady=5)


    def cleanup_previous_pull(self):

        if hasattr(self, 'details_button') and self.details_button.winfo_exists():
            self.details_button.pack_forget()
            self.details_button.destroy()
            del self.details_button
        
        if hasattr(self, 'pull_output'):
            self.pull_output.clear()
        else:
            self.pull_output = []


    def save_switch_state(self, switch_name, state):
        try:
            settings_path = "GLOBAL_SETTINGS"
            
            self.cursor.execute("SELECT * FROM modifs WHERE path = ? AND switch_name = ?", 
                            (settings_path, switch_name))
            result = self.cursor.fetchone()

            if result:
                self.cursor.execute("UPDATE modifs SET state_boolean = ? WHERE path = ? AND switch_name = ?", 
                                (state, settings_path, switch_name))
            else:
                self.cursor.execute("INSERT INTO modifs (path, switch_name, state_boolean) VALUES (?, ?, ?)", 
                                (settings_path, switch_name, state))
            self.connect.commit()
        except Exception as e:
            print(f"Error saving switch state: {e}")


    def load_switch_states(self):
        try:
            settings_path = "GLOBAL_SETTINGS"
            
            self.cursor.execute("SELECT switch_name, state_boolean FROM modifs WHERE path = ?", 
                            (settings_path,))
            results = self.cursor.fetchall()
            
            default_states = {
                "use_last_commit": False,
                "bypass_gpg": False,
                "show_delete_button": False
            }
            
            for switch_name, state in results:
                default_states[switch_name] = bool(state)
            
            self.switch_var.set(default_states["use_last_commit"])
            self.bypass_gpg_var.set(default_states["bypass_gpg"])
            
            if default_states["show_delete_button"]:
                self.line_label.pack(pady=5,fill="x")
                self.frame_inside_buttons_2.pack(pady=2)
            else:
                self.frame_inside_buttons_2.pack_forget()
                self.line_label.pack_forget()

                
        except Exception as e:
            print(f"Error loading switch states: {e}")
            self.switch_var.set(False)
            self.bypass_gpg_var.set(False)
            self.frame_inside_buttons_2.pack_forget()
            self.line_label.pack_forget()

    def toggle_last_commit(self):
        state = self.switch_var.get()
        self.save_switch_state(state)

        if state:
            threading.Thread(target=self._fetch_last_commit_message, daemon=True).start()
        else:
            self.commit_entry.delete(0, 'end')


    

    def _fetch_last_commit_message(self):
        repo_path = self.folder_entry.get().strip()
        if not repo_path:
            self.app.after(0, messagebox.showerror, "Error", "Please select a project folder.")
            return

        try:
            is_windows = platform.system() == "Windows"

            result = subprocess.run(
                ["git", "-C", repo_path, "log", "-1", "--pretty=%B"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW if is_windows else 0
            )
            last_commit_message = result.stdout.strip()

            self.app.after(0, self._update_commit_entry, last_commit_message)

        except subprocess.CalledProcessError as e:
            self.app.after(0, messagebox.showerror, "Error", f"Failed to get last commit message:\n{e.stderr}")
        except Exception as e:
            self.app.after(0, messagebox.showerror, "Error", f"An error occurred:\n{str(e)}")     


    def _update_commit_entry(self, last_commit_message):
        if last_commit_message:
            self.commit_entry.delete(0, 'end')
            self.commit_entry.insert(0, last_commit_message)

 
    def get_last_commit_message(self):
        repo_path = self.folder_entry.get().strip()
        if not repo_path:
            messagebox.showerror("Error", "Please select a project folder.")
            return None

        try:
            is_windows = platform.system() == "Windows"

            result = subprocess.run(
                ["git", "-C", repo_path, "log", "-1", "--pretty=%B"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW if is_windows else 0
            )
            return result.stdout.strip()

        except subprocess.CalledProcessError as e:
            error_message = f"Failed to get last commit message:\n{e.stderr}"
            self.app.after(0, messagebox.showerror, "Error", error_message)
            return None
        

    def open_link(self,x,event=None):
        if x=="1":
            webbrowser.open("https://abderrahmane-aarab.carrd.co/")
        elif x=="3":
            webbrowser.open("https://github.com/aarab-abderrahmane/Drop2Repo/releases/tag/7.1.1")
        elif x=="2" :
            webbrowser.open("https://abderrahmanerb.gumroad.com/l/Drop2Repo")
        elif x=="4":
            webbrowser.open("https://github.com/aarab-abderrahmane/Drop2Repo/releases")
        else: pass


    
    def toggle_select_all(self):
        state = self.select_all_var.get()
        
        for file, file_data in self.file_checkboxes.items():
            if len(file_data) == 3:
                var, checkbox, is_staged = file_data
                if not is_staged:
                    var.set(state)
                    if "❌" in checkbox.cget("text"):
                        checkbox.configure(
                            text_color="#20cdf2" if state else "#ff6b6b",
                            font=('Consolas', 13, 'bold' if state else 'normal')
                        )
                    else:
                        checkbox.configure(
                            text_color="#20cdf2" if state else "white",
                            font=('Consolas', 13, 'bold' if state else 'normal')
                        )

    def update_git_status(self):
        repo_path = self.folder_entry.get().strip()
        if not repo_path:
            return
    
        self.progress_bar.pack(pady=10)
        self.progress_bar.start()
        self.refresh_button.configure(state="disabled")

        threading.Thread(target=self._fetch_git_status, args=(repo_path,), daemon=True).start()


    def _fetch_git_status(self, repo_path):
        try:
            result = subprocess.run(
                ['git', '-C', repo_path, 'status', '--porcelain'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            )
            self.app.after(0, self._update_ui_with_files, result.stdout)
        except subprocess.CalledProcessError as e:
            self.app.after(0, messagebox.showerror, "Error", f"Failed to get Git status:\n{e.stderr}")
        finally:
            self.app.after(0, self.progress_bar.stop)
            self.app.after(0, self.progress_bar.pack_forget)
            self.app.after(0, lambda: self.refresh_button.configure(state="normal"))

    
    def _show_no_files_message(self):

        self.no_files_label = ctk.CTkLabel(
            self.file_list_frame, 
            text="",
            font=('Consolas', 13, 'bold'),
            text_color="#e0aaff"
        )
        self.no_files_label.pack(pady=50)
        
        self.empty_text = "No modified files found.."
        self.write_text_2(0)

    def _update_ui_with_files(self, git_status_output):

        self.file_checkboxes.clear()
        self.staged_files_buttons.clear()

        for widget in self.file_list_frame.winfo_children():
            widget.destroy()

        if hasattr(self, 'no_files_label'):
            self.no_files_label = None

        self.has_changes = bool(git_status_output)
        
        self.update_refresh_button_color()

        if not git_status_output:
            self._show_no_files_message()
            return

        staged_files = []
        unstaged_files = []
        staged_deleted = []

        for line in git_status_output.splitlines():
            status = line[:2]
            filename = line[3:].strip('"')
            
            if status.strip() == 'D' or status[0] == 'D':
                unstaged_files.append(('D', filename, "deleted"))
            elif status == 'D ' or status == 'AD':
                staged_deleted.append(('D', filename, "staged_deleted"))
            elif status[0] == 'A' or status == 'M ':
                staged_files.append((status, filename))
            elif status[0] == ' ' and status[1] == 'M':
                unstaged_files.append((status, filename, "modified"))
            elif status == '??':
                unstaged_files.append((status, filename, "untracked"))

        if unstaged_files:

            for status, filename, file_state in unstaged_files:
                var = ctk.BooleanVar()
                if file_state == "deleted":
                    display_text = f"❌ {filename}"
                elif file_state == "modified":
                    display_text = f"✎ {filename}"
                else:
                    display_text = f"{filename}"

                checkbox = ctk.CTkCheckBox(
                    self.file_list_frame,
                    text=display_text,
                    variable=var,
                    fg_color="#20363e",
                    hover_color='#333333',
                    border_color="#f42535",
                    font=('Consolas', 15),
                    command=lambda f=filename: self._on_file_selected(f)
                )
                if file_state == "deleted":
                    checkbox.configure(text_color="#ff6b6b", font=('Consolas', 15))
                checkbox.pack(anchor="w", padx=5, pady=5)
                checkbox.bind("<Button-3>", lambda e, f=filename: self._copy_filename_to_commit(f))
                self.file_checkboxes[filename] = (var, checkbox, False)

        if staged_files or staged_deleted:
            label = ctk.CTkLabel(self.file_list_frame, 
                                text="Staged Files:",
                                font=('Consolas', 13, 'bold'),
                                text_color="#51cf66")
            label.pack(anchor="w", pady=(15, 5), padx=10)

            for status, filename in staged_files:
                button = ctk.CTkButton(
                    self.file_list_frame,
                    text=f"✓ {filename}",
                    fg_color="transparent",
                    border_color="#51cf66",
                    border_width=1,
                    text_color="#51cf66",
                    hover_color="#203635",
                    font=('Consolas', 15, 'bold'),
                    width=200,
                    height=30,
                    anchor="center",
                    command=lambda f=filename: self._on_staged_file_clicked(f)
                )
                button.pack(anchor="w", padx=5, pady=2)
                self.staged_files_buttons[filename] = button

            for status, filename, file_state in staged_deleted:
                button = ctk.CTkButton(
                    self.file_list_frame,
                    text=f"🗑️{filename}",
                    fg_color="transparent",
                    border_color="#ff6b6b",
                    border_width=1,
                    text_color="#ff6b6b",
                    hover_color="#3a3a3a",
                    font=('Consolas', 15),
                    width=200,
                    height=30,
                    anchor="center",
                    command=lambda f=filename: self._on_staged_file_clicked(f)
                )
                button.pack(anchor="w", padx=5, pady=2)
                self.staged_files_buttons[filename] = button

        self._display_unpushed_commits()


    def _display_unpushed_commits(self):

        unpushed_commits = []
        try:
            repo_path = self.folder_entry.get().strip()
            if repo_path:
                result = subprocess.run(
                    ['git', '-C', repo_path, 'log', '--pretty=format:%h|%s', 'origin/main..main'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
                )
                if result.returncode == 0 and result.stdout.strip():
                    unpushed_commits = [line.split('|', 1) for line in result.stdout.splitlines()]
        except:
            pass

        if unpushed_commits:
            self.unpushed_commits_shown = True
            label = ctk.CTkLabel(self.file_list_frame, 
                                text="Unpushed Commits:",
                                font=('Consolas', 13, 'bold'),
                                text_color="#ff922b")
            label.pack(anchor="w", pady=(15, 5), padx=10)

            for commit_hash, commit_message in unpushed_commits:
                btn = ctk.CTkButton(
                    self.file_list_frame,
                    text=f"{commit_hash}: {commit_message[:50]}{'...' if len(commit_message) > 50 else ''}",
                    fg_color="transparent",
                    border_color="#ff922b",
                    border_width=1,
                    text_color="#ff922b",
                    hover_color="#3a3a3a",
                    font=('Consolas', 15),
                    height=30,
                    anchor="w",
                    command=lambda ch=commit_hash: self._show_commit_details(ch)
                )
                btn.pack(fill="x", padx=5, pady=2)
        else:
            self.unpushed_commits_shown = False



    def _show_commit_details(self, commit_hash):

        repo_path = self.folder_entry.get().strip()
        if not repo_path:
            return

        try:
            result = subprocess.run(
                ['git', '-C', repo_path, 'show', '--stat', commit_hash],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            )
            
            if result.returncode == 0:
                details_window = ctk.CTkToplevel(self.app)
                details_window.title(f"Commit Details: {commit_hash}")
                
                window_width = 400
                window_height = 200
                screen_width = self.app.winfo_screenwidth()
                screen_height = self.app.winfo_screenheight()
                
                x = (screen_width - window_width) // 2
                y = (screen_height - window_height) // 2
                
                details_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
                
                details_window.lift()
                details_window.attributes('-topmost', True)
                details_window.focus_force()
                
                textbox = ctk.CTkTextbox(details_window, wrap="none")
                textbox.pack(fill="both", expand=True, padx=10, pady=10)
                
                textbox.insert("end", result.stdout)
                textbox.configure(state="disabled")
                
                close_btn = ctk.CTkButton(
                    details_window,
                    text="Close",
                    command=details_window.destroy,
                    fg_color="#ff6b6b",
                    hover_color="#ff5252"
                )
                close_btn.pack(pady=10)
                
                details_window.protocol("WM_DELETE_WINDOW", details_window.destroy)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show commit details:\n{str(e)}")

    def _display_unstaged_files(self, files):

        if not files:
            return


        for status, filename in files:
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(
                self.file_list_frame,
                text=filename,
                variable=var,
                fg_color="#20363e",
                hover_color='#333333',
                border_color="#f42535",
                font=('Consolas', 13),
                command=lambda f=filename: self._on_file_selected(f)
            )
            checkbox.pack(anchor="w", padx=5, pady=5)
            checkbox.bind("<Button-3>", lambda e, f=filename: self._copy_filename_to_commit(f))
            self.file_checkboxes[filename] = (var, checkbox, False)

    def _copy_filename_to_commit(self, filename):

        file_name_only = os.path.basename(filename)
        
        self.commit_entry.delete(0, 'end')
        
        self.commit_entry.insert(0, file_name_only)

    def _display_staged_files(self, files):

        if not files:
            return

        label = ctk.CTkLabel(self.file_list_frame, 
                            text="Staged Files:",
                            font=('Consolas', 13, 'bold'),
                            text_color="#51cf66")
        label.pack(anchor="w", pady=(15, 5), padx=10)

        for status, filename in files:
            button = ctk.CTkButton(
                self.file_list_frame,
                text=f"♻ {filename}",
                fg_color="transparent",
                border_color="#51cf66",
                border_width=1,
                text_color="#51cf66",
                hover_color="#203635",
                font=('Consolas', 12, 'bold'),
                width=200,
                height=30,
                anchor="center",
                command=lambda f=filename: self._on_staged_file_clicked(f)
            )
            button.pack(anchor="w", padx=5, pady=2)
            self.staged_files_buttons[filename] = button

    def _on_staged_file_clicked(self, filename):

        self._unstage_file(filename)

    def _unstage_file(self, filename):

        repo_path = self.folder_entry.get().strip()
        if not repo_path:
            return

        try:
            subprocess.run(
                ["git", "-C", repo_path, "reset", "--", filename],
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            )
            self.update_git_status()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to unstage file:\n{e.stderr}")



    def _on_file_selected(self, filename):

        if filename in self.file_checkboxes:
            var, checkbox, is_staged = self.file_checkboxes[filename]
            if var.get():
                if "❌" in checkbox.cget("text"):
                    checkbox.configure(text_color="#20cdf2", font=('Consolas', 15, 'bold'))
                else:
                    checkbox.configure(text_color="#20cdf2", font=('Consolas', 15, 'bold'))
            else:
                if "❌" in checkbox.cget("text"):
                    checkbox.configure(text_color="#ff6b6b", font=('Consolas', 15))
                else:
                    checkbox.configure(text_color="white", font=('Consolas', 15))



    def write_text_2(self, index):

        if index < len(self.empty_text):
            current_text = self.empty_text[:index + 1]
            self.no_files_label.configure(text=current_text)
            self.app.after(70, self.write_text_2, index + 1)

    def _add_files_to_ui(self, files):
        for file in files:
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(
                self.file_list_frame,
                text=file,
                variable=var,
                fg_color="green",
                border_color="#c1121f",
                corner_radius=6,
                border_width=1,
                hover_color="#c1121f",
                font=('Consolas', 12),
                checkbox_height=22,
                checkbox_width=22,
                command=lambda f=file: self.update_checkbox_style(f)
            )
            checkbox.pack(anchor="w", pady=5)
            self.file_checkboxes[file] = (var, checkbox)

            checkbox.bind("<Button-3>", lambda event, f=file: self.insert_filename_to_commit(f))

    def insert_filename_to_commit(self, filename):

        file_name_only = os.path.basename(filename)
        current_text = self.commit_entry.get()
        self.commit_entry.delete(0, 'end')
        self.commit_entry.insert(0, f"{file_name_only}")


    def update_checkbox_style(self, file):
        if file in self.file_checkboxes:
            var, checkbox, is_staged = self.file_checkboxes[file]
            if var.get():
                checkbox.configure(text_color="green", font=('Consolas', 12, 'bold'))
            else:
                checkbox.configure(text_color="white", font=('Consolas', 12))


    def reload_data(self):
        self.cursor.execute("SELECT path FROM modifs WHERE path != 'GLOBAL_SETTINGS'")
        mdf = self.cursor.fetchall()
        
        if mdf:
            self.folder_entry.delete(0, 'end')
            self.folder_entry.insert(0, mdf[0][0])
            
            self.load_switch_states()
            
            if self.switch_var.get():
                threading.Thread(target=self._fetch_last_commit_message, daemon=True).start()
            
            self.update_git_status()

        


    def select_folder(self,event=None):
        folder = filedialog.askdirectory()
        if folder:
            try:
                git_dir = os.path.join(folder, '.git')
                if not os.path.isdir(git_dir):
                    messagebox.showerror("Error", "The selected folder is not a Git repository.")
                    return

                current_switch_states = {
                    "use_last_commit": self.switch_var.get(),
                    "bypass_gpg": self.bypass_gpg_var.get(),
                    "show_delete_button": self.frame_inside_buttons_2.winfo_ismapped() if hasattr(self, 'frame_inside_buttons_2') else False
                }

                self.folder_entry.delete(0, 'end')
                self.folder_entry.insert(0, str(folder))

                for widget in self.file_list_frame.winfo_children():
                    widget.destroy()
                self.file_checkboxes = {}

                self.pull_button.configure(state="disabled", fg_color="#333333", border_color='black')
                self.select_all_var.set(False)

                try:
                    self.cursor.execute('INSERT OR IGNORE INTO modifs (path, state_boolean) VALUES (?, ?)', 
                                        (folder, False))
                    self.connect.commit()
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"Failed to save path: {str(e)}")

                self.switch_var.set(current_switch_states["use_last_commit"])
                self.bypass_gpg_var.set(current_switch_states["bypass_gpg"])

                if current_switch_states["show_delete_button"]:
                    self.frame_inside_buttons_2.pack(pady=2)
                else:
                    self.frame_inside_buttons_2.pack_forget()

                self.update_git_status()

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while selecting the folder: {str(e)}")

                
    def run_command_without_window(command):
        is_windows = platform.system() == "Windows"

        if is_windows:
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        return result
    

    def push_to_github(self):
        repo_path = self.folder_entry.get().strip()
        commit_message = self.commit_entry.get().strip()

        if not repo_path:
            messagebox.showerror("Error", "Please select the project first.")
            return

        if not commit_message:
            messagebox.showerror("Error", "please enter a commit message.")
            return

        staged_files = list(self.staged_files_buttons.keys())
        selected_unstaged = [f for f,(v,_,s) in self.file_checkboxes.items() if not s and v.get()]
        
        if not staged_files and not selected_unstaged:
            messagebox.showerror("Error", "There are no specific files to sumbit.")
            return

        self.progress_bar.pack(pady=10)
        self.progress_bar.start()
        self.push_button.configure(state="disabled")

        threading.Thread(
            target=self._execute_git_operations,
            args=(repo_path, commit_message, staged_files, selected_unstaged),
            daemon=True
        ).start()


    def show_error(self, message):

        messagebox.showerror("Error", message)

    def show_info(self, message):

        messagebox.showinfo("Success", message)



    def _execute_git_operations(self, repo_path, commit_message, staged_files, selected_unstaged):
        try:
            is_windows = platform.system() == "Windows"
            
            if staged_files:
                pass
                
            if selected_unstaged:
                result = subprocess.run(
                    ["git", "-C", repo_path, "add"] + selected_unstaged,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if is_windows else 0
                )
                if result.returncode != 0:
                    raise Exception(f"Failed to add files:\n{result.stderr}")

            commit_cmd = ["git", "-C", repo_path, "commit", "-m", commit_message]
            if self.bypass_gpg_var.get():
                commit_cmd.append("--no-gpg-sign")

            commit_result = subprocess.run(
                commit_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if is_windows else 0
            )
            
            if commit_result.returncode != 0:
                raise Exception(f"Failed to commit:\n{commit_result.stderr}")

            push_result = subprocess.run(
                ["git", "-C", repo_path, "push"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if is_windows else 0
            )
            
            if push_result.returncode != 0:
                error_msg = push_result.stderr or push_result.stdout or "Unknown push error."
                raise Exception(f"Failed to push:\n{error_msg}")

            self.app.after(0, self.show_info, "Changes successfully sumbmitted to GitHub!")
            self.app.after(0, self.update_git_status)

        except Exception as e:
            self.app.after(0, self.show_error, f"An error occurred:\n{str(e)}")
        finally:
            self.app.after(0, self.progress_bar.stop)
            self.app.after(0, self.progress_bar.pack_forget)
            self.app.after(0, lambda: self.push_button.configure(state="normal"))
            
    def is_file_deleted_in_git(self, repo_path, filename):

        result = subprocess.run(
            ["git", "-C", repo_path, "ls-files", "--deleted"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
        )
        return filename in result.stdout.splitlines()



class Settings:
    def __init__(self, app, git_push_frame):
        self.app = app
        self.git_push_frame = git_push_frame

        self.settings_frame = ctk.CTkFrame(self.app,fg_color="#131212")
        self.settings_frame.pack(fill="both", expand=True)


        self.emty_space  = ctk.CTkLabel(self.settings_frame,text="")
        self.emty_space.grid(row=0,column=0,padx=140)
        self.label = ctk.CTkLabel(self.settings_frame, text="Settings Page :", font=('Consolas', 25, 'bold'))
        self.label.place(x=360,y=59)


        self.empty_label = ctk.CTkLabel(self.settings_frame, text="")
        self.empty_label.grid(column=1,row=1,pady=40)

        

        self.switch_var = ctk.BooleanVar(value=False)
        self.switch = ctk.CTkSwitch(
            self.settings_frame,
            text="  Get Last Commit",
            variable=self.switch_var,
            fg_color="#938daa",
            corner_radius=10,
            progress_color="green",
            border_width=0,
            font=('Consolas', 14),
            width=10,
            command=self.toggle_last_commit
        )
        self.switch.grid(row=2,column=1,sticky="nsew",padx=40,pady=20)



        self.use_last_commit_label = ctk.CTkLabel(
            self.settings_frame,
            text="?",
            font=('Consolas', 15, 'bold','underline'),
            text_color="yellow",
            cursor="hand2"
        )
        self.use_last_commit_label.grid(row=2,column=2,sticky="nsew",padx=15)
        self.use_last_commit_label.bind("<Button-1>", lambda event : self.show_setting_details("1",event))



        self.bypass_gpg_var = ctk.BooleanVar(value=False)
        self.bypass_gpg_switch = ctk.CTkSwitch(
            self.settings_frame,
            text="  Bypass GPG when pushing",
            variable=self.bypass_gpg_var,
            fg_color="#938daa",
            progress_color="green",
            border_width=0, 
            font=('Consolas', 14),
            width=10,
            command=lambda: self.toggle_switch("bypass_gpg", self.bypass_gpg_var )
        )
        self.bypass_gpg_switch.grid(row=3,column=1,sticky="nsew", padx=40)


        self.use_last_commit_label = ctk.CTkLabel(
            self.settings_frame,
            text="?",
            font=('Consolas', 15, 'bold','underline'),
            text_color="yellow",
            cursor="hand2"
        )
        self.use_last_commit_label.grid(row=3,column=2,sticky="nsew",padx=15)
        self.use_last_commit_label.bind("<Button-1>", lambda event : self.show_setting_details("2",event))



        self.show_delete_button_var = ctk.BooleanVar(value=False)
        self.show_delete_button_switch = ctk.CTkSwitch(
            self.settings_frame,
            text="  Show advanced buttons",
            variable=self.show_delete_button_var,
            fg_color="#938daa",
            progress_color="green",
            border_width=0, 
            font=('Consolas', 14),
            command=self.toggle_delete_button_visibility
        )
        self.show_delete_button_switch.grid(row=4, column=1, sticky="nsew", pady=20,padx=40)


        self.show_delete_button_label = ctk.CTkLabel(
            self.settings_frame,
            text="?",
            font=('Consolas', 15, 'bold', 'underline'),
            text_color="yellow",
            cursor="hand2"
        )
        self.show_delete_button_label.grid(row=4, column=2, sticky="nsew", padx=15)
        self.show_delete_button_label.bind("<Button-1>", lambda e: self.show_setting_details("3", e))


        self.image_back = Image.open(Registration.resource_path("back-button.png"))
        self.photo_back = CTkImage(self.image_back, size=(20, 20))

        self.back_button = ctk.CTkButton(
            self.settings_frame,
            image=self.photo_back,
            text="",
            command=self.go_back_to_home,
            width=60,
            height=35,
            corner_radius=8,
            border_width=2,
            fg_color="#380f0f",
            hover_color="black",
            border_color="#fc0909",
            text_color="white",
            font=('Consolas', 15, 'bold')
        )
        self.back_button.place(x=10,y=10)


            
        self.load_switch_state()


    def show_ctk_messagebox(self,title, message, icon):
        CTkMessagebox(title=title, message=message, icon=icon)

    def show_setting_details(self,x,event=None) : 
        if x == "1":
            self.app.after(0, lambda: self.show_ctk_messagebox(
            "Setting Details",
            "When this option is enabled, the commit message field will be automatically filled with the last commit message used.\n\n"
            "This is useful if you want to reuse the same commit message frequently.",
            "info"
              ))
            
        elif x == "2":
            self.app.after(0, lambda: self.show_ctk_messagebox(
            "Settings Details",
            "Enabling this option allows you to bypass GPG signing for your Git commits.\n\n"
            "This means you can commit changes without requiring GPG verification.",
            "info"
        ))

        elif x == "3":
            CTkMessagebox(
                title="Setting Details",
                message="When enabled, this will show the other buttons button in the main interface.\n\n",
                icon="info"
            )

    
    def load_switch_state(self):
        try:
            settings_path = "GLOBAL_SETTINGS"
            
            self.git_push_frame.cursor.execute("SELECT switch_name, state_boolean FROM modifs WHERE path = ?", 
                                            (settings_path,))
            results = self.git_push_frame.cursor.fetchall()
            
            default_states = {
                "use_last_commit": False,
                "bypass_gpg": False,
                "show_delete_button": False
            }
            
            for switch_name, state in results:
                default_states[switch_name] = bool(state)
            
            self.switch_var.set(default_states["use_last_commit"])
            self.bypass_gpg_var.set(default_states["bypass_gpg"])
            self.show_delete_button_var.set(default_states["show_delete_button"])
            
            self.toggle_delete_button_visibility()
            
        except Exception as e:
            print(f"Error loading switch states: {e}")
            self.switch_var.set(False)
            self.bypass_gpg_var.set(False)
            self.show_delete_button_var.set(False)

    def toggle_switch(self, switch_name, switch_var):
        state = switch_var.get()
        self.git_push_frame.save_switch_state(switch_name, state)


    def toggle_delete_button_visibility(self):
        state = self.show_delete_button_var.get()
        self.git_push_frame.save_switch_state("show_delete_button", state)
        
        if state:
            self.git_push_frame.line_label.pack(pady=5,fill="x")
            self.git_push_frame.frame_inside_buttons_2.pack(pady=2)
            
        else:
            self.git_push_frame.line_label.pack_forget()
            self.git_push_frame.frame_inside_buttons_2.pack_forget()


    def toggle_last_commit(self):
        state = self.switch_var.get()
        self.git_push_frame.save_switch_state("use_last_commit", state)

        if state:
            threading.Thread(target=self.git_push_frame._fetch_last_commit_message, daemon=True).start()
        else:
            self.git_push_frame.commit_entry.delete(0, 'end')

    
    def go_back_to_home(self):
        self.git_push_frame.save_switch_state("use_last_commit", self.switch_var.get())
        self.git_push_frame.save_switch_state("bypass_gpg", self.bypass_gpg_var.get())
        self.git_push_frame.save_switch_state("show_delete_button", self.show_delete_button_var.get())
        
        self.settings_frame.pack_forget()
        self.git_push_frame.home_frame.pack(fill="both", expand=True)
        
        self.git_push_frame.load_switch_states()


class AdditionalPage:
    def __init__(self, app, git_push_frame):
        self.app = app
        self.git_push_frame = git_push_frame

        self.frame = ctk.CTkFrame(self.app,fg_color="#131212")
        self.frame.pack(fill="both", expand=True)

        self.label = ctk.CTkLabel(self.frame, text="", font=('Consolas', 20, 'bold'))
        self.label.pack(pady=30)

        self.buttons_frame = ctk.CTkFrame(self.frame,fg_color="transparent")
        self.buttons_frame.pack(pady=20)

        self.create_button_with_image("chemistry.png", "Laboratory","1", self.button1_clicked)
        self.create_button_with_image("create.png", "Git Clone","2", self.button2_clicked)
        self.create_button_with_image("security.png", "Stopped..","3", self.button3_clicked)

        self.image_back = Image.open(Registration.resource_path("back-button.png"))
        self.photo_back = CTkImage(self.image_back, size=(20, 20))

        self.back_button = ctk.CTkButton(
            self.frame,
            image=self.photo_back,
            text="",
            command=self.go_back_to_home,
            width=60,
            height=35,
            corner_radius=8,
            border_width=2,
            fg_color="#380f0f",
            hover_color="black",
            border_color="#fc0909",
            text_color="white",
            font=('Consolas', 15, 'bold')
        )
        self.back_button.place(x=10,y=10)


    def create_button_with_image(self, image_path, text,x, command):
        image = Image.open(Registration.resource_path(image_path))
        photo = CTkImage(image, size=(160, 160))

        self.button = ctk.CTkButton(
                self.buttons_frame,
                text=text,
                image=photo,
                compound="top",
                command=command,
                hover_color="black",
                width=230,
                height=300,
                text_color="#ffe4c7",
                border_color="#211f1f",
                fg_color="black",
                corner_radius=8,
                border_width=3,
                font=('Consolas', 14, 'bold'),

            )


        self.button.pack(side="left", padx=10, pady=30)

        self.button.image = photo

    def button1_clicked(self):
        self.open_commits_page()

    def button2_clicked(self):
        self.open_git_clone_page()

    def button3_clicked(self):
        print("Button 3 clicked")

    def go_back_to_home(self):
        
        self.frame.pack_forget()
        self.git_push_frame.home_frame.pack(fill="both", expand=True)  


    def open_commits_page(self):

        self.frame.pack_forget()
        self.commits_page = CommitsPage(self.app, self.git_push_frame) 

    def open_git_clone_page(self):

            self.frame.pack_forget()
            self.git_clone_page = GitClonePage(self.app, self)


class DocumentaionPage:
    def __init__(self, app, git_push_frame):
        self.app = app
        self.git_push_frame = git_push_frame

        self.frame = ctk.CTkFrame(self.app, fg_color="#2b2b2b")
        self.frame.pack(fill="both", expand=True)

        self.pdf_frame = ctk.CTkFrame(self.frame, fg_color="#1e1e1e")
        self.pdf_frame.pack(fill="both", expand=True)

        pdf_path = Registration.resource_path("documentatiob.pdf")
        self.pdf_viewer = CTkPDFViewer(master=self.pdf_frame, file=pdf_path,page_width=600)
        self.pdf_viewer.pack(expand=True, fill="both")

        self.image_back = Image.open(Registration.resource_path("back-button.png"))
        self.photo_back = CTkImage(self.image_back, size=(20, 20))

 
        self.back_button = ctk.CTkButton(
            self.frame,
            image=self.photo_back,
            text="",
            command=self.go_back_to_home,
            width=60,
            height=35,
            corner_radius=8,
            border_width=2,
            fg_color="#380f0f",
            hover_color="black",
            border_color="#fc0909",
            text_color="white",
            font=('Consolas', 15, 'bold')
        )
        self.back_button.place(x=10,y=10)

    def go_back_to_home(self):

        self.frame.pack_forget()
        self.git_push_frame.home_frame.pack(fill="both", expand=True)
        if hasattr(self.git_push_frame, 'combo_box'):
          self.git_push_frame.combo_box.set(" M E N U ")


class CommitsPage:
    def __init__(self, app, git_push_frame):
        self.app = app
        self.app.resizable(True,True)

        self.git_push_frame = git_push_frame

        self.frame = ctk.CTkFrame(self.app,fg_color="#131212")
        self.frame.pack(fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.frame, text="Commits History", font=('Consolas', 20, 'bold','underline'))
        self.title_label.pack(pady=10)

        self.search_filter_frame = ctk.CTkFrame(self.frame,fg_color='transparent')
        self.search_filter_frame.pack( padx=10, pady=10)

        self.search_entry = ctk.CTkEntry(self.search_filter_frame, placeholder_text="Search commits...", font=('Consolas', 15, 'bold'),fg_color="#1b1b1f",corner_radius=8,border_color='white',border_width=1, width=250,height=35)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.filter_commits)

        self.sort_options = [
        "Newest to Oldest", 
        "Oldest to Newest", 
        "Longest Message First", 
        "Shortest Message First"
        ]
        self.sort_combobox = ctk.CTkComboBox(
            self.search_filter_frame,
            values=self.sort_options,
            command=self.sort_commits,
            width=140,
            height=35,
            fg_color="#393429",
            dropdown_fg_color="#1e1e1e",
            dropdown_text_color="white",
            text_color="white",
            border_width=2,
            border_color="#f77f00",
            corner_radius=8,
            font=('Consolas', 14),
            dropdown_font=('Consolas', 13),
            button_color="#f77f00",
            dropdown_hover_color="#f77f00",
            button_hover_color="darkgray"
        )
        self.sort_combobox.pack(side="left", padx=5)
        self.sort_combobox.set("Newest to Oldest")
        self.sort_combobox.set('FILTER')


        self.image_back = Image.open(Registration.resource_path("arrows.png"))
        self.photo_back = CTkImage(self.image_back, size=(20, 20))

        self.back_button = ctk.CTkButton(
            self.frame,
            image=self.photo_back,
            text="",
            command=self.go_back_to_home,
            width=60,
            height=35,
            corner_radius=8,
            border_width=2,
            fg_color="#380f0f",
            hover_color="black",
            border_color="#fc0909",
            text_color="white",
            font=('Consolas', 15, 'bold')
        )
        self.back_button.place(x=10,y=10)




        self.image_info = Image.open(Registration.resource_path("question-mark.png"))
        self.photo_info = CTkImage(self.image_info, size=(25, 25))

        self.label_info = ctk.CTkLabel(self.frame, image=self.photo_info, text="",fg_color='transparent',cursor="hand2")
        self.label_info.place(x=80,y=12)

        self.label_info.bind("<Button-1>", lambda event: self.show_usage_instructions(event))


        self.table_frame = ctk.CTkFrame(self.frame)
        self.table_frame.pack(fill="both", expand=True)

        self.columns = ["Commit Hash", "Author", "Date", "Message", "Status"]
        self.tree = ttk.Treeview(self.table_frame, columns=self.columns, show="headings", selectmode="browse")
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Consolas", 11, "bold"))
        style.configure("Treeview", font=('Consolas', 9), background="#131212",fieldbackground="#131212", foreground="white", rowheight=35)
        style.map("Treeview",
          background=[('selected', '#a50044')])
        
        self.tree.tag_configure('oddrow', background='#393429')
        
        self.tree.pack(fill="both", expand=True)

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=160, anchor="center", stretch=True)

        


        self.loading_label = ctk.CTkLabel(self.tree, text="Loading commits...", font=('Consolas', 16,'bold'), text_color="#00ff00",fg_color="#131212")
        self.loading_label.place(relx=0.5, rely=0.5, anchor="center") 

        threading.Thread(target=self.load_commits_data, daemon=True).start()

        self.tree.bind("<Double-1>", self.handle_commit_deletion)

        self.tree.bind("<Button-3>", self.revert_to_commit)


    def sort_commits(self, choice):

        try:
            if hasattr(self, 'empty_label') and self.empty_label.winfo_exists():
                self.empty_label.destroy()


            if choice == "Newest to Oldest":
                sorted_data = sorted(self.commits_data, 
                                key=lambda x: self.parse_git_date(x[2]), 
                                reverse=True)
            elif choice == "Oldest to Newest":
                sorted_data = sorted(self.commits_data, 
                                key=lambda x: self.parse_git_date(x[2]))
            elif choice == "Longest Message First":
                sorted_data = self.sort_commits_by_message_length(reverse=True)
            elif choice == "Shortest Message First":
                sorted_data = self.sort_commits_by_message_length(reverse=False)
            else:
                sorted_data = self.commits_data

            self.populate_table(sorted_data)
        
        except Exception as e:
            print(f"Error sorting commits: {e}")
            self.show_ctk_messagebox("Error", f"Failed to sort commits: {str(e)}", "cancel")

    def parse_git_date(self, git_date_str):

        from datetime import datetime
        try:
            date_part = ' '.join(git_date_str.split()[:5])
            return datetime.strptime(date_part, '%a %b %d %H:%M:%S %Y')
        except:
            return git_date_str
        

    def sort_commits_by_message_length(self, reverse=False):

        if not self.commits_data:
            return []

        sorted_data = sorted(self.commits_data, key=lambda x: len(x[3]), reverse=reverse)
        return sorted_data

    def show_usage_instructions(self, event=None):

        instructions = (
        "How to use the table:\n\n"
        "1. Search: Type in the search field to filter commits based on text.\n"
        "2. Sort:\n"
        "   - Newest to Oldest: Sort commits by date (newest first).\n"
        "   - Oldest to Newest: Sort commits by date (oldest first).\n"
        "   - Longest Message First: Sort commits by message length (longest first).\n"
        "   - Shortest Message First: Sort commits by message length (shortest first).\n"
        "3. Delete: Double-click on an unpushed commit to delete it.\n"
        "4. Revert to a specific version: Right-click on a commit to revert to its state.\n"
        "5. Protection: Pushed commits are protected and cannot be deleted.\n\n"
        "Note: Make sure to select a valid Git repository before performing any actions."
        )
        self.show_ctk_messagebox_2("Usage Instructions", instructions, "info")
        
    def load_commits_data(self):

        self.commits_data = self.get_commits_data()
        self.app.after(0, self.populate_table, self.commits_data)
        self.app.after(0, self.loading_label.place_forget)

    def handle_commit_deletion(self, event):

        item = self.tree.identify_row(event.y)
        commit_hash = self.tree.item(item, "values")[0]
        status = self.tree.item(item, "values")[4]

        if status == "Unpushed":
            confirm = CTkMessagebox(title="Confirm Delete", message=f"Are you sure you want to delete commit {commit_hash}?", 
                                    icon="question", option_1="Yes", option_2="No")
            if confirm.get() == "Yes":
                self.delete_commit(commit_hash)
        else:
            self.show_ctk_messagebox("Error", "This commit has been pushed to GitHub. Cannot delete.", "cancel")


    def revert_to_commit(self, event):

        item = self.tree.identify_row(event.y)
        commit_hash = self.tree.item(item, "values")[0]

        confirm = CTkMessagebox(title="Confirm Revert", message=f"Are you sure you want to revert to commit {commit_hash}?", 
                                icon="question", option_1="Yes", option_2="No")
        if confirm.get() == "Yes":
            self.checkout_commit(commit_hash)


    def show_ctk_messagebox_2(self, title, message, icon):
        self.app.after(0, lambda: CTkMessagebox(title=title, message=message, icon=icon,justify="center",height=200,width=600))
    
    def show_ctk_messagebox(self, title, message, icon):
        self.app.after(0, lambda: CTkMessagebox(title=title, message=message, icon=icon,justify="center"))
    

    def checkout_commit(self, commit_hash):

        repo_path = self.git_push_frame.folder_entry.get().strip()
        if not repo_path:
            self.show_ctk_messagebox("Error", "Please select a Git repository first.", "cancel")
            return

        try:
            is_windows = platform.system() == "Windows"
            creation_flags = subprocess.CREATE_NO_WINDOW if is_windows else 0

            subprocess.run(
                ["git", "-C", repo_path, "checkout", commit_hash],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=creation_flags
            )

            self.git_push_frame.update_git_status()

            self.show_ctk_messagebox("Success", f"Reverted to commit {commit_hash} successfully.", "check")

        except subprocess.CalledProcessError as e:
            self.show_ctk_messagebox("Error", f"Failed to revert to commit:\n{e.stderr}", "cancel")


    def delete_commit(self, commit_hash):

        repo_path = self.git_push_frame.folder_entry.get().strip()
        if not repo_path:
            self.show_ctk_messagebox("Error", "Please select a Git repository first.", "cancel")
            return

        try:
            is_windows = platform.system() == "Windows"
            creation_flags = subprocess.CREATE_NO_WINDOW if is_windows else 0

            subprocess.run(
                ["git", "-C", repo_path, "branch", "backup-branch"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=creation_flags
            )

            subprocess.run(
                ["git", "-C", repo_path, "reset", "--hard", f"{commit_hash}^"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=creation_flags
            )

            self.commits_data = self.get_commits_data()
            self.populate_table(self.commits_data)

            self.show_ctk_messagebox("Success", f"Commit {commit_hash} deleted successfully.", "check")

        except subprocess.CalledProcessError as e:
            self.show_ctk_messagebox("Error", f"Failed to delete commit:\n{e.stderr}", "cancel")


    def is_commit_pushed(self, commit_hash):

        repo_path = self.git_push_frame.folder_entry.get().strip()
        if not repo_path:
            return False

        try:
            is_windows = platform.system() == "Windows"
            creation_flags = subprocess.CREATE_NO_WINDOW if is_windows else 0

            result = subprocess.run(
                ["git", "-C", repo_path, "log", "--branches", "--not", "--remotes"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
                creationflags=creation_flags
            )
            return commit_hash not in result.stdout
        except subprocess.CalledProcessError:
            return False


    def sort_commits_by_date(self, choice):

        if choice == "Newest to Oldest":
            sorted_data = sorted(self.commits_data, key=lambda x: x[2], reverse=True)
        else:
            sorted_data = sorted(self.commits_data, key=lambda x: x[2])

        self.populate_table(sorted_data)


    def get_commits_data(self):

        repo_path = self.git_push_frame.folder_entry.get().strip()
        if not repo_path:
            self.show_ctk_messagebox("Error", "Please select a Git repository first.", "cancel")
            return []

        try:
            is_windows = platform.system() == "Windows"
            creation_flags = subprocess.CREATE_NO_WINDOW if is_windows else 0

            result = subprocess.run(
                ["git", "-C", repo_path, "log", "--pretty=format:%h|%an|%ad|%s"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
                creationflags=creation_flags
            )
            commits = result.stdout.splitlines()

            commits_data = []
            for commit in commits:
                commit_hash, author, date, message = commit.split("|", 3)
                status = "Pushed" if self.is_commit_pushed(commit_hash) else "Unpushed"
                commits_data.append([commit_hash, author, date, message, status])

            return commits_data

        except subprocess.CalledProcessError as e:
            self.show_ctk_messagebox("Error", f"Failed to fetch commits:\n{e.stderr}", "cancel")
            return []
        

    def populate_table(self, data):

        for row in self.tree.get_children():
            self.tree.delete(row)

        if not data:
                self.tree.insert("", "end", values=("", "", "", "", ""))
                self.empty_label = ctk.CTkLabel(self.tree, text="", font=('Consolas', 16,'bold'), text_color="red",fg_color='#131212')
                self.empty_label.place(relx=0.5, rely=0.5, anchor="center")
                self.emty_text = "No data available"
                self.write_text(0)
        else:
            for i, commit in enumerate(data):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tree.insert("", "end", values=commit, tags=(tag,))


    def write_text(self, index):

        if index < len(self.emty_text):
            current_text = self.emty_text[:index + 1]
            self.empty_label.configure(text=current_text)
            self.app.after(160, self.write_text, index + 1)


    def filter_commits(self, event=None):

        if hasattr(self, 'empty_label') and self.empty_label.winfo_exists():
          self.empty_label.destroy() 

        search_text = self.search_entry.get().strip().lower()
        filtered_data = [commit for commit in self.commits_data if search_text in " ".join(commit).lower()]
        self.populate_table(filtered_data)

    def go_back_to_home(self):

        self.frame.pack_forget()
        self.git_push_frame.home_frame.pack(fill="both", expand=True)


class GitClonePage:
    def __init__(self, app, additional_page):
        self.app = app
        self.additional_page = additional_page

        self.frame = ctk.CTkFrame(self.app,fg_color="#131212")
        self.frame.pack(fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.frame, text="Git Clone", font=('Consolas', 20, 'bold', 'underline'))
        self.title_label.pack(pady=30)

        self.input_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.input_frame.pack(pady=10)

        self.url_label = ctk.CTkLabel(self.input_frame, text="Repository URL:", font=('Consolas', 14, 'bold'))
        self.url_label.pack(anchor="w", padx=20)
        self.url_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="https://github.com/username/repository.git",
            height=45,
            width=400,
            font=('Consolas', 14),
            fg_color="#dc7af5",
            text_color="black",
            border_width=3,
            placeholder_text_color="black",
            border_color="#8035bd",
            corner_radius=8
        )
        self.url_entry.pack(pady=5, padx=20)

        self.path_label = ctk.CTkLabel(self.input_frame, text="Destination Path:", font=('Consolas', 14, 'bold'))
        self.path_label.pack(anchor="w", padx=20)

        self.path_frame = ctk.CTkFrame(self.input_frame, width=400, fg_color="transparent", corner_radius=8, border_width=2, border_color="#8035bd")
        self.path_frame.pack(fill="x", padx=20)

        self.path_entry = ctk.CTkEntry(
            self.path_frame,
            placeholder_text="Select a folder to save the repository",
            height=45,
            width=337,
            border_width=0,
            font=('Consolas', 14),
            fg_color="#131212",
            text_color="#ffbe29",
            corner_radius=8
        )
        self.path_entry.pack(side="left", padx=5, pady=3)

        self.image_folder = Image.open(Registration.resource_path("file-explorer.png"))
        self.photo_folder = CTkImage(self.image_folder, size=(25, 25))
        self.browse_button = ctk.CTkButton(
            self.path_frame,
            text="",
            image=self.photo_folder,
            width=50,
            height=37,
            command=self.select_folder,
            fg_color="#131212",
            hover_color="#8035bd",
            border_width=0,
            corner_radius=5
        )
        self.browse_button.pack(side="left", pady=3, fill='y')

        self.clone_button = ctk.CTkButton(
            self.frame,
            text="Clone Repository",
            command=self.clone_repository,
            fg_color="#255c25",
            hover_color="green",
            corner_radius=8,
            font=('Consolas', 14, 'bold'),
            width=200,
            height=40
        )
        self.clone_button.pack(pady=20)

        self.progress_bar = ctk.CTkProgressBar(
            self.frame,
            width=310,
            height=10,
            fg_color="#2b2b2b",
            corner_radius=4,
            border_color="#00d87c",
            border_width=1,
            progress_color="#04d97f",
            mode="indeterminate"
        )
        self.progress_bar.pack(pady=10)
        self.progress_bar.pack_forget()



        self.image_back = Image.open(Registration.resource_path("arrows.png"))
        self.photo_back = CTkImage(self.image_back, size=(20, 20))
        self.back_button = ctk.CTkButton(
            self.frame,
            image=self.photo_back,
            text="",
            command=self.go_back,
            width=60,
            height=35,
            corner_radius=8,
            border_width=2,
            fg_color="#380f0f",
            hover_color="black",
            border_color="#fc0909",
            text_color="white",
            font=('Consolas', 15, 'bold')
        )
        self.back_button.place(x=10, y=10)

    def select_folder(self):

        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, 'end')
            self.path_entry.insert(0, folder)

    def get_repo_name_from_url(self, repo_url):

        repo_url = repo_url.strip()
        repo_name = repo_url.split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        return repo_name

    def clone_repository(self):

        repo_url = self.url_entry.get().strip()
        destination_path = self.path_entry.get().strip()

        if not repo_url:
            messagebox.showerror("Error", "Please enter a repository URL.")
            return
        if not destination_path:
            messagebox.showerror("Error", "Please select a destination path.")
            return
        if not repo_url.startswith("https://") and not repo_url.startswith("git@"):
            messagebox.showerror("Error", "Please enter a valid repository URL (e.g., https://github.com/username/repository.git).")
            return

        repo_name = self.get_repo_name_from_url(repo_url)
        if not repo_name:
            messagebox.showerror("Error", "Could not determine repository name from URL.")
            return

        response = messagebox.askyesno(
            "Confirmation",
            f"Do you want to clone the repository into a folder named '{repo_name}'?\n"
            f"If you choose 'No', the repository contents will be cloned directly into:\n{destination_path}"
        )

        final_destination = destination_path
        if response:
            final_destination = os.path.join(destination_path, repo_name)
            if os.path.exists(final_destination):
                messagebox.showerror(
                    "Error",
                    f"A folder named '{repo_name}' already exists at '{destination_path}'.\n"
                    "Please choose a different path or rename the existing folder."
                )
                return
        else:
            if os.path.exists(destination_path) and os.listdir(destination_path):
                messagebox.showerror(
                    "Error",
                    f"The destination path '{destination_path}' is not empty.\n"
                    "Please choose an empty folder to clone the repository directly."
                )
                return

        self.clone_button.configure(state="disabled")
        self.progress_bar.pack(pady=10)
        self.progress_bar.start()

        threading.Thread(
            target=self._execute_clone_operation,
            args=(repo_url, final_destination),
            daemon=True
        ).start()

    def _execute_clone_operation(self, repo_url, destination_path):

        try:
            is_windows = platform.system() == "Windows"
            creation_flags = subprocess.CREATE_NO_WINDOW if is_windows else 0

            result = subprocess.run(
                ["git", "clone", repo_url, destination_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=creation_flags
            )

            if result.returncode == 0:
                self.app.after(0, messagebox.showinfo, "Success", f"Repository cloned successfully to {destination_path}!")
                self.app.after(0, lambda: self.additional_page.git_push_frame.folder_entry.delete(0, 'end'))
                self.app.after(0, lambda: self.additional_page.git_push_frame.folder_entry.insert(0, destination_path))
                self.app.after(0, self.update_git_push_database, destination_path)
                self.app.after(0, self.additional_page.git_push_frame.update_git_status)
            else:
                error_msg = result.stderr or result.stdout or "Unknown error during cloning."
                raise Exception(error_msg)

        except Exception as e:
            self.app.after(0, messagebox.showerror, "Error", f"Failed to clone repository:\n{str(e)}")
        finally:
            self.app.after(0, self.progress_bar.stop)
            self.app.after(0, self.progress_bar.pack_forget)
            self.app.after(0, lambda: self.clone_button.configure(state="normal"))

    def update_git_push_database(self, destination_path):

        try:
            self.additional_page.git_push_frame.cursor.execute(
                "DELETE FROM modifs WHERE path != 'GLOBAL_SETTINGS'"
            )
            self.additional_page.git_push_frame.cursor.execute(
                'INSERT INTO modifs (path, state_boolean) VALUES (?, ?)',
                (destination_path, False)
            )
            self.additional_page.git_push_frame.connect.commit()
        except sqlite3.Error as e:
            self.app.after(0, messagebox.showerror, "Database Error", f"Failed to update database:\n{str(e)}")

    def go_back(self):

        self.frame.pack_forget()
        self.additional_page.git_push_frame.home_frame.pack(fill="both", expand=True)


class PathHistoryPage:
    def __init__(self, app, git_push_frame):
        self.app = app
        self.git_push_frame = git_push_frame
        self.frame = ctk.CTkFrame(app,fg_color="#131212")
        self.frame.pack(fill="both", expand=True)


        self.buttons_frame = ctk.CTkFrame(self.frame,fg_color="transparent",width=400,height=40)
        
        self.title_label = ctk.CTkLabel(self.frame, text="Select Saved Path", font=('Consolas', 20, 'bold'))
        self.title_label.pack(pady=30)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self.frame, width=600, height=200,fg_color="transparent")
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.path_vars = []
        self.load_saved_paths()
        
        self.confirm_button = ctk.CTkButton(
                                            self.buttons_frame,
                                            height=40,
                                            corner_radius=8,
                                            border_width=0,
                                            text_color="#00ff0d",
                                            font=('Consolas', 15, 'bold'),
                                            text="Select Path",
                                            command=self.confirm_selection, 
                                            fg_color="#0b3d0b",
                                            hover_color="green",
                                            width=200)
        
        self.confirm_button.pack(side="left",padx=10)
        
        self.back_button = ctk.CTkButton(
                                        self.buttons_frame, 
                                        text="Back", 
                                        command=self.go_back,
                                        height=40,
                                        corner_radius=8,
                                        border_width=2,
                                        fg_color="#380f0f",
                                        hover_color="black",
                                        border_color="#fc0909",
                                        text_color="white",
                                        font=('Consolas', 15, 'bold'),
                                        width=100)
        
 
        
        self.back_button.pack(side="right")

        self.buttons_frame.pack(pady=20)

    def load_saved_paths(self):

        try:
            self.git_push_frame.cursor.execute("SELECT DISTINCT path FROM modifs WHERE path != 'GLOBAL_SETTINGS'")
            results = self.git_push_frame.cursor.fetchall()
            
            for i, (path,) in enumerate(results):
                var = ctk.BooleanVar()
                checkbox = ctk.CTkCheckBox(self.scroll_frame, text=path, variable=var, 
                                            onvalue=True, offvalue=False, fg_color="green",corner_radius=8,border_width=2,hover_color="black",font=('Consolas', 18))
                checkbox.pack(pady=5, anchor="w")
                self.path_vars.append((var, path))
                
            if not results:
                ctk.CTkLabel(self.scroll_frame, text="No saved paths found.", font=('Consolas', 14, 'italic')).pack(pady=20)
                
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Failed to load paths: {str(e)}", icon="cancel")

    def confirm_selection(self):
        selected_paths = [path for var, path in self.path_vars if var.get()]
        if not selected_paths:
            CTkMessagebox(title="No Selection", message="Please select a path.", icon="cancel")
            return

        selected_path = selected_paths[0]
        
        self.git_push_frame.folder_entry.delete(0, 'end')
        self.git_push_frame.folder_entry.insert(0, selected_path)

        self.git_push_frame.update_git_status()

        self.frame.pack_forget()
        self.git_push_frame.home_frame.pack(fill="both", expand=True)

    def go_back(self):

        self.frame.pack_forget()
        self.git_push_frame.home_frame.pack(fill="both", expand=True)





def main():
    app = ctk.CTk()

    window_width = 925
    window_height = 525
    app.geometry(f"{window_width}x{window_height}")

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    app.geometry(f"+{x}+{y}")

    def on_closing():
        if hasattr(app, 'git_push_frame'):
            app.git_push_frame.save_switch_state("use_last_commit", app.git_push_frame.switch_var.get())
            app.git_push_frame.save_switch_state("bypass_gpg", app.git_push_frame.bypass_gpg_var.get())
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)  

    def start_main_app():
        def switch_to_push(registration_frame):
            registration_frame.frame.pack_forget()
            registration_frame.frame.destroy()
            app.git_push_frame = GitPushPage(app)

        registration_frame = Registration(app, switch_to_push)
  
    splash_screen = SplashScreen(app, start_main_app)
    app.mainloop()

if __name__ == "__main__":
    main()