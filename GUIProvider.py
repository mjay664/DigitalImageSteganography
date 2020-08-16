import tkMessageBox
from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk
import ImageSteganography as IS

text_message = 'Choose an image...'
file_name_2 = ''

about_text = ''' * Copyright (C) 2018 Himanshu Verma
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
 *
 Thanks For Using It'''


def hide_window():
    global file_name_2

    def hide_message():
        global file_name_2

        if len(file_name_2) > 0:
            if len(key_area.get()) > 0:
                if len(message_area.get("1.0","end-1c")) > 0:
                    password = key_area.get()
                    try:
                        password = int(password)
                        stag_obj = IS.StagManager(file_name_2)
                        im = stag_obj.hide_message(password, message_area.get("1.0","end-1c"))
                        x = asksaveasfilename(initialdir="/", title="Save file", filetypes=(("files", "*.jpg"), ("png files", "*.png")), defaultextension='.jpg')
                        im.save(x, "PNG")
                    except ValueError:
                        tkMessageBox.showerror('Alert', 'Key must be a number')
                    key_area.delete(0, 'end')
                    message_area.delete('1.0', 'end')
                else:
                    tkMessageBox.showerror('Alert', 'Message can not be empty')
            else:
                tkMessageBox.showerror('Alert', 'Please Enter a key first')
        else:
            tkMessageBox.showerror('Alert', 'Please select an image first')

    def do_fun():
        hide_window_var.destroy()
        root.deiconify()

    def do_job():
        global file_name_2
        file_name = askopenfilename(initialdir="/", title="Select file", filetypes=(("files", "*.jpg"), ("png files", "*.png")))
        file_name_2 = file_name
        if len(file_name) > 15:
            file_name = file_name[len(file_name)-15:len(file_name)]
            file_name = '...' + file_name
        if len(file_name) == 0:
            file_name = text_message
            file_name_2 = ''
        T.config(text=file_name)
        if len(file_name_2) > 0:
            try:
                im = Image.open(file_name_2)
                size = im.size
                if size[0] < 520 or size[1] < 520:
                    tkMessageBox.showerror('Error', 'Error in image size\nImage must be 520x520 or greater')
                    file_name = text_message
                    T.config(text=file_name)
                    file_name_2 = ''
                else:
                    if size[0] > 1080:
                        tkMessageBox.showinfo('Image Resolution', 'Image Resolution is very high\nQuality will be lost in output image')
                    photo = ImageTk.PhotoImage(im.resize((189, 209)))
                    image_label.config(image=photo)
                    image_label.image = photo
            except:
                tkMessageBox.showerror('Alert', 'Selected file was not a supported image file.\nTry again...!!!')
                file_name_2 = ''

    root.withdraw()
    hide_window_var = Toplevel(root)
    hide_window_var.resizable(width=False, height=False)
    hide_window_var.title('Hide Message')
    hide_window_var.geometry('400x300+400+200')
    T = Label(hide_window_var, justify=LEFT, text=text_message, padx=1, width=20)
    T.place(x=0, y=10)
    key_mess = Label(hide_window_var, text='Key:')
    key_mess.place(x=5, y=60)
    key_area = Entry(hide_window_var, show='*', width=20)
    key_area.place(x=5, y=80)
    message = Label(hide_window_var, text='Message:')
    message.place(x=5, y=110)
    button_location = Button(hide_window_var, text='Browse...', command=do_job, anchor='sw')
    button_location.place(x=130, y=10)
    message_area = Text(hide_window_var, width=20, height=10)
    message_area.place(x=5, y=130)

    im = Image.open('label_1_icon.png')
    photo = ImageTk.PhotoImage(im)

    image_label = Label(hide_window_var, image=photo, width=190, height=210)
    image_label.place(x=200, y=80)

    final_button = Button(hide_window_var, text='Hide Message', width=26, height=3, command=hide_message)
    final_button.place(x=200, y=10)
    hide_window_var.protocol('WM_DELETE_WINDOW', do_fun)
    hide_window_var.mainloop()


def unhide_window():
    global  file_name_2

    def unhide_message():
        global file_name_2

        if len(file_name_2) > 0:
            if len(key_area.get()) > 0:
                password = key_area.get()
                try:
                    password = int(password)
                    stag_obj = IS.StagManager(file_name_2)
                    s = stag_obj.show_message(password)
                    tkMessageBox.showinfo('Success', 'Your Message Retrieved Successfully...!!!')
                    message_area.configure(state=NORMAL)
                    message_area.delete('1.0', 'end')
                    message_area.insert('1.0', s)
                    message_area.configure(state=DISABLED)
                except ValueError:
                    tkMessageBox.showerror('Alert', 'Key must be a number')
                key_area.delete(0, 'end')
            else:
                tkMessageBox.showerror('Alert', 'Please Enter a key first')
        else:
            tkMessageBox.showerror('Alert', 'Please select an image first')

    def do_fun():
        unhide_window_var.destroy()
        root.deiconify()

    def do_job():
        global file_name_2
        file_name = askopenfilename(initialdir="/", title="Select file",
                                    filetypes=(("files", "*.jpg"), ("png files", "*.png")))
        file_name_2 = file_name
        if len(file_name) > 15:
            file_name = file_name[len(file_name) - 15:len(file_name)]
            file_name = '...' + file_name
        if len(file_name) == 0:
            file_name = text_message
            file_name_2 = ''
        T.config(text=file_name)
        if len(file_name_2) > 0:
            try:
                im = Image.open(file_name_2)
                photo = ImageTk.PhotoImage(im.resize((189, 209)))
                image_label.config(image=photo)
                image_label.image = photo
            except:
                tkMessageBox.showerror('Alert', 'Selected file was not a supported image file.\nTry again...!!!')
                file_name_2 = ''

    root.withdraw()
    unhide_window_var = Toplevel(root)
    unhide_window_var.resizable(width=False, height=False)
    unhide_window_var.title('Show Message')
    unhide_window_var.geometry('400x300+400+200')

    T = Label(unhide_window_var, justify=LEFT, text=text_message, padx=1, width=20)
    T.place(x=0, y=10)
    key_mess = Label(unhide_window_var, text='Key:')
    key_mess.place(x=5, y=60)
    key_area = Entry(unhide_window_var, show='*', width=20)
    key_area.place(x=5, y=80)
    message = Label(unhide_window_var, text='Message:')
    message.place(x=5, y=110)
    button_location = Button(unhide_window_var, text='Browse...', command=do_job, anchor='sw')
    button_location.place(x=130, y=10)
    message_area = Text(unhide_window_var, state=DISABLED, width=20, height=10)
    message_area.place(x=5, y=130)

    im = Image.open('label_1_icon.png')
    photo = ImageTk.PhotoImage(im)

    image_label = Label(unhide_window_var, image=photo, width=190, height=210)
    image_label.place(x=200, y=80)

    final_button = Button(unhide_window_var, text='Show Message', width=26, height=3, command=unhide_message)
    final_button.place(x=200, y=10)


    unhide_window_var.protocol('WM_DELETE_WINDOW', do_fun)
    unhide_window_var.mainloop()


def about():
    def do_fun():
        about_window.destroy()
        root.deiconify()

    root.withdraw()
    about_window = Toplevel(root)
    about_window.resizable(width=False, height=False)
    about_window.title('About')
    about_window.geometry('400x300+400+200')
    about_label = Label(about_window, text=about_text, padx=5, pady=10, justify=CENTER)
    about_label.place(x=0, y=0)
    about_window.protocol('WM_DELETE_WINDOW', do_fun)
    about_window.mainloop()


root = Tk()
root.title('Image Steganography')
root.geometry('400x300+400+200')

im = Image.open('label_aa.png')
photo = ImageTk.PhotoImage(im.resize((400, 300)))

label_1 = Label(root, image=photo)
label_1.image = photo
label_1.place(x=0,y=0)
root.resizable(width=False, height=False)
menu = Menu(root)
root.config(menu=menu)
file_menu = Menu(menu, tearoff=False)
menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Hide', command=hide_window)
file_menu.add_separator()
file_menu.add_command(label='Unhide', command=unhide_window)
help_menu = Menu(menu, tearoff=False)
menu.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='About...', command=about)

root.mainloop()

