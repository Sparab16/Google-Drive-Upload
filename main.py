from tkinter import *
from tkinter import ttk

import functions


def main():
    """
    Function is responsible for creating different widgets objects and then calling place_widgets method to place them on screen
    """
    # Root Container
    try:
        container = Tk()
        content = ttk.Frame(master=container, padding=(3, 3, 12, 12))

        # Create a frame to hold the textarea
        frame_textarea = ttk.Frame(master=content, borderwidth=2, width=400, height=400, padding=10, relief='ridge')
        textarea = Text(master=frame_textarea, state='disabled', padx=5, pady=5)
        foldername_label = ttk.Label(master=content, text='Folder Name')
        foldername_entry = ttk.Entry(master=content)

        # File Upload and Folder Upload Buttons
        file_upload_button = ttk.Button(master=content, text='Upload Files', width=20)
        folder_upload_button = ttk.Button(master=content, text='Upload Folder', width=20)

        # Final Upload to Google Drive Button
        upload_to_gdrive = ttk.Button(master=content, text='Upload to Google Drive', width=30)

        # Scrollbar
        scrollbar = ttk.Scrollbar(master=frame_textarea, orient='vertical', command=textarea.yview)
        textarea['yscrollcommand'] = scrollbar.set

        # Basic configuration for root container
        container.title('Google Drive Upload')

        # Binding methods to widgets
        binding_method(file_upload_button, folder_upload_button, foldername_entry, upload_to_gdrive, textarea, container)
        # Calling place_widget
        place_widget(container, content, frame_textarea, textarea, foldername_label, foldername_entry, file_upload_button,
                     folder_upload_button, upload_to_gdrive, scrollbar)

        container.mainloop()
    except Exception as e:
        raise Exception(e)


def binding_method(*widgets):
    """
    Function is responsible for binding methods on to the widgets.
    @param widgets: Objects of different widgets
    """
    try:
        file_upload_button, folder_upload_button, foldername_entry, upload_to_gdrive, textarea, container = widgets

        # File upload button binding
        file_upload_button.bind('<Button-1>', lambda event, textarea=textarea: functions.select_file(textarea))
        # Folder upload button binding
        folder_upload_button.bind('<Button-1>', lambda event, textarea=textarea: functions.select_folder(textarea))
        # Upload to Google Drive Button Binding
        upload_to_gdrive.bind('<Button-1>',
                              lambda event, foldername_entry=foldername_entry, textarea=textarea,
                                     root=container: functions.upload(
                                  foldername_entry, textarea, root))
    except Exception as e:
        raise Exception(e)


def place_widget(*widgets):
    """
    Function is responsible for placing the widgets on to the screen
    @param widgets: Objects of different widgets
    """
    try:
        container, content, frame_textarea, textarea, foldername_label, foldername_entry, file_upload_button, folder_upload_button, upload_to_gdrive, scrollbar = widgets
        # Placing the widgets on to the screen
        content.grid(column=0, row=0, sticky=(N, S, E, W))
        frame_textarea.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
        textarea.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
        foldername_label.grid(column=3, row=0, columnspan=2, sticky=(N, S, E, W), padx=5, pady=5)
        foldername_entry.grid(column=3, row=1, columnspan=2, sticky=(N, E, W), padx=5, pady=5)
        file_upload_button.grid(column=0, row=2, sticky=(N, S), padx=5, pady=5)
        folder_upload_button.grid(column=1, row=2, sticky=(N, S, W), padx=5, pady=5)
        upload_to_gdrive.grid(column=3, row=2, columnspan=2, sticky=N, padx=5, pady=5)
        scrollbar.grid(column=1, row=0, sticky=(N, S))

        # Configuration of widgets
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=3)
        content.columnconfigure(2, weight=3)
        content.columnconfigure(3, weight=1)
        content.columnconfigure(4, weight=1)
        content.rowconfigure(1, weight=1)

        frame_textarea.columnconfigure(0, weight=3)
        frame_textarea.rowconfigure(0, weight=3)
    except Exception as e:
        raise Exception(e)

if __name__ == '__main__':
    main()
