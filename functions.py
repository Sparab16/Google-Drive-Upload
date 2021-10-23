import os
from tkinter import messagebox, filedialog

import gdrive

file_selected = []


def fill_textarea(file_selected, textarea):
    """
    Function is responsible for populating the text area content
    @param file_selected: Array of files to upload
    @param textarea: Textarea object
    """
    # Delete the content of textarea if there are any
    textarea['state'] = 'normal'
    textarea.delete('1.0', 'end')
    # Inserting the files selected into the text area
    file_counter = len(file_selected)
    for file in file_selected:
        textarea.insert('1.0', 'File : ' + str(file_counter) + ' = ' + file + '\n')
        file_counter -= 1
    textarea['state'] = 'disabled'


def select_folder(textarea):
    """
    Function is responsible for showing popup box for selecting the folders to upload
    @param textarea: Object of textarea
    """
    folder_selected = filedialog.askdirectory(title='Select folder to upload', initialdir='/')
    if folder_selected:
        global file_selected
        file_selected = []
        for sub_dirs, dirs, files in os.walk(folder_selected):
            for file in files:
                if not '\\' in sub_dirs:  # Condition to not include the hidden files
                    file_selected.append(sub_dirs + '/' + file)
        fill_textarea(file_selected, textarea)
    else:
        messagebox.showerror(title='No folder is selected', message='Please select a folder to upload')


def select_file(textarea):
    """
    Function is responsible for showing popup box for selecting the files to upload
    @param textarea: Object of textarea
    """
    global file_selected
    file_selected = []
    file_selected = filedialog.askopenfilenames(title='Select files to upload', initialdir='/')
    if file_selected:
        fill_textarea(file_selected, textarea)
    else:
        messagebox.showerror(title='No files are selected', message='Please select atleast one file to upload')


def upload(foldername_entry, textarea, root):
    """
    Function is responsible for calling gdrive modules
    @param foldername_entry: Foldername Entry Object
    @param textarea: Textarea Object
    @param root: Window Object
    """
    # Condition to check whether the foldername exists
    if foldername_entry.get():
        global file_selected
        # Condition to check if there are any files to upload
        if file_selected:
            service = gdrive.authentication()
            folder_id = gdrive.create_folder(service, foldername_entry.get())
            is_upload_successfull = gdrive.upload(service, folder_id, file_selected, textarea, root)
            # if upload successfull
            if is_upload_successfull:
                messagebox.showinfo(title='Upload Successful',
                                    message='All the files are uploaded to Google Drive')
                # Clear the textarea content
                fill_textarea([], textarea)
                # Clear the folder name content
                foldername_entry.delete(0, 'end')
            else:
                messagebox.showerror(title='Upload Unsuccessfull', message='Files are not uploaded to Google Drive')
        else:
            messagebox.showerror(title='No files to upload', message='Please select files or folder to upload')
    else:
        messagebox.showerror(title='Folder name is empty or invalid', message='Please enter the folder name')
