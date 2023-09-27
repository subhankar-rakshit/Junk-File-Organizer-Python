'''Junk File Organizer in Python using Tkinter Library.
Developed by Subhankar Rakshit
~PySeek~'''

import os
import shutil
from tkinter import *
from threading import *
from PIL import ImageTk, Image
from tkinter import messagebox, filedialog


file_types={
   'Documents' : ('.pdf','.doc','.xls','txt','.csv','.xml','.zip', '.docx', '.DOCX', '.odt'),
   'Pictures' : ('.jpg','.jpeg','.png','.JPG', '.webp'),
   'Videos' : ('.mp4','.mkv','.3gp','.flv','.mpeg'),
   'Music' : ('.mp3','.wav','.m4a','.webm'),
   'Programs' : ('.py','.cpp','.c','.sh','.js'),
   'Apps' : ('.exe','.apk'),
}

class File_Organizer:
    def __init__(self, root):
        # Setting the Tkinter main window
        self.window = root
        self.window.geometry("720x500")
        self.window.title('File Organizer - PySeek')
        self.window.resizable(width = False, height = False)
        self.window.configure(bg='gray90')

        self.selected_dir = ''
        self.browsed = False

        # Frame 1: For the Logo
        self.frame_1 = Frame(self.window,bg='gray90',\
        width=280, height=70)
        self.frame_1.pack()
        self.frame_1.place(x=20, y=20)

        self.display_logo()

        # About Button
        About_Btn = Button(self.window, text="About", \
        font=("Kokila", 10, 'bold'), bg="dodger blue", \
        fg="white", width=5, command=self.about_window)
        About_Btn.place(x=600, y=20)

        # Exit Button
        Exit_Btn = Button(self.window, text="Exit", \
        font=("Kokila", 10, 'bold'), bg="dodger blue", \
        fg="white", width=5, command=self.exit_window)
        Exit_Btn.place(x=600, y=60)

        # Frame 2: For the Main Page Widgets
        self.frame_2 = Frame(self.window, bg="white",\
        width=720,height=480)
        self.frame_2.place(x=0, y=110)

        self.main_page()

    # Function to display the File Organizer Logo
    def display_logo(self):
        image = Image.open('Images/logo.png')
        resized_image = image.resize((280, 70))
        self.logo = ImageTk.PhotoImage(resized_image)
        label = Label(self.frame_1, bg='gray90',image=self.logo)
        label.pack()

    def main_page(self):
        Heading_Label = Label(self.frame_2, \
        text="Please Select the Folder", \
        font=("Kokila", 20, 'bold'), bg='white')
        Heading_Label.place(x=160, y=20)

        Folder_Button = Button(self.frame_2, text="Select Folder", \
        font=("Kokila", 10, 'bold'), bg="gold", width=10, \
        command=self.select_directory)
        Folder_Button.place(x=130, y=80)

        self.Folder_Entry = Entry(self.frame_2, \
        font=("Helvetica", 12), width=32)
        self.Folder_Entry.place(x=256, y=85)

        Status = Label(self.frame_2, text="Status: ", \
        font=("Kokila", 12, 'bold'), bg='white')
        Status.place(x=180, y=130)

        # Status Label:
        self.Status_Label = Label(self.frame_2, text="Not Started Yet", \
        font=("Kokila", 12), bg="white", fg="red")
        self.Status_Label.place(x=256, y=130)

        Start_Button = Button(self.frame_2, text="Start", \
        font=("Kokila", 13, 'bold'), bg="dodger blue", fg="white", \
        width=8, command=self._threading)
        Start_Button.place(x=280, y=180)

    # Function to get the target directory location
    def select_directory(self):
        self.selected_dir = filedialog.askdirectory(title = \
        "Select a location")
        self.Folder_Entry.insert(0, self.selected_dir)

        self.selected_dir = str(self.selected_dir)

        # Checking if the folder path is exists or not
        if os.path.exists(self.selected_dir):
            self.browsed = True

    def _threading(self):
        self.x = Thread(target=self.organizer, daemon=True)
        self.x.start()
    
    def organizer(self):
        # If no directory is chosen
        if not self.browsed:
            messagebox.showwarning('No folders are choosen', \
            'Please Select a Folder First')
            return
        try:
            # Showing the current status of the operation
            self.Status_Label.config(text='Processing...')

            self.Current_Path = self.selected_dir

            if os.path.exists(self.Current_Path):
            # self.Folder_List1: stores all the folders that 
            # are already presented in the selected directory
                self.Folder_List1 = []
                # self.Folder_List2: stores newly created folders
                self.Folder_List2 = []
                self.flag = False

                for folder, extensions in file_types.items():
                    self.folder_name = folder
                    self.folder_path = os.path.join(self.Current_Path, self.folder_name)

                    # Change the directory to the current 
                    # folder path that we've selected
                    os.chdir(self.Current_Path)

                    # If the folder is already present in that directory
                    if os.path.exists(self.folder_name):
                        self.Folder_List1.append(self.folder_name)
                    # If the folder is not present in that directory,
                    # then create a new folder
                    else:
                        self.Folder_List2.append(self.folder_name)
                        os.mkdir(self.folder_path)
                    
                    # Calling the 'file_finder' function to
                    # find a specific type of file (or extension)
                    # and change their old path to new path.
                    for item in self.file_finder(self.Current_Path, extensions):
                        self.Old_File_Path = os.path.join(self.Current_Path,item)
                        self.New_File_Path = os.path.join(self.folder_path,item)

                        # Moving each file to their new location
                        shutil.move(self.Old_File_Path, self.New_File_Path)
                        self.flag = True
            else:
                messagebox.showerror('Error!','Please Enter a Valid Path!')

            # Checking if the files are separated or not
            # If `flag` is True: It means the program discovered
            # matching files and they have been organized.
            if self.flag:
                self.Status_Label.config(text='Done!')
                messagebox.showinfo('Done!', 'Operation Successful!')
                self.reset()
            # If `flag` is False: It means the program didn't find
            # any matching files there; only empty folders are created.
            if not self.flag:
                self.Status_Label.config(text='Complete!')
                messagebox.showinfo('Done!', \
                'Folders have been created\nNo Files were there to move')
                self.reset()
        # If any error occurs
        except Exception as es:
            messagebox.showerror("Error!",f"Error due to {str(es)}")

    # Function to find a specific file-type
    def file_finder(self, folder_path, file_extensions):
        self.files = []
        for file in os.listdir(folder_path):
            for extension in file_extensions:
                if file.endswith(extension):
                    self.files.append(file)
        return self.files

    def reset(self):
        self.Status_Label.config(text='Not Started Yet')
        self.Folder_Entry.delete(0, END)
        self.selected_dir = ''

    def about_window(self):
        messagebox.showinfo("File Organizer",\
        "Developed by Subhankar Rakshit\n~PySeek")
    
    def exit_window(self):
        self.window.destroy()

# The main function
if __name__ == "__main__":
    root = Tk()
    obj = File_Organizer(root)
    root.mainloop()
