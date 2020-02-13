# -------------------------------------------------------------------------------
# Name:        ArchiComm
# Purpose:
#
# Author:      Thomas
#
# Created:     11/01/2020
# Copyright:   (c) Thomas 2020
# Licence:     <priver>
# -------------------------------------------------------------------------------
# tuto http://sebsauvage.net/python/gui/index_fr.html#import
# tuto http://apprendre-python.com/page-tkinter-interface-graphique-python-tutoriel
# http://sebsauvage.net/python/snyppets/index.html#tkinter_cxfreeze

# -*- coding: utf-8 -*-
#!/usr/bin/env python


try:
    # for Python2
    from Tkinter import *  ## notice capitalized T in Tkinter
except ImportError:
    # for Python3
    from tkinter import *  ## notice lowercase 't' in tkinter here

import tkinter as tk
from tkinter import simpledialog as sdg
import datetime

flag_list = []
list_pseudo = []
Pseudo_ok = False

# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):
    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)

        # reference to the master widget, which is the tk window
        self.master = master

        # with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    # Creation of init_window
    def init_window(self):
        self.pack(
            fill=BOTH, expand=1
        )  # allowing the widget to take the full space of the root window

        menu = Menu(self.master)  # creating a menu instance
        self.master.config(menu=menu)
        file = Menu(menu, tearoff=0)
        file.add_command(
            label="Connect",
            background="lightgray",
            activebackground="green",
            command=self.connect_action,
        )
        file.add_command(
            label="Exit",
            background="lightgray",
            activebackground="red",
            command=self.close_application,
        )  # adds a command to the menu option, calling it exit, and the command it runs on event is Exit
        menu.add_cascade(label="File", menu=file)  # added "file" to our menu
        edit = Menu(menu, tearoff=0)  # create the file object)
        edit.add_command(
            label="Undo"
        )  # adds a command to the menu option, calling it exit, and the command it runs on event is Exit
        menu.add_cascade(label="Edit", menu=edit)  # added "file" to our menu

        self.affichage1Page()

    def affichage1Page(self):
        self.frame = Frame(
            self,
            width=self.winfo_screenwidth(),
            height=self.winfo_screenheight(),
        )
        self.entryVariable = (
            tk.StringVar()
        )  # création d'un widget pour entrer du texte
        self.entry = tk.Entry(
            self, textvariable=self.entryVariable
        )  # contenu du widget est stocker dans la variable  "self.entryVariable"
        self.entry.grid(
            column=0, row=0, sticky="EW"
        )  # placement du widget dans la grille et reste coller au bord west
        self.entry.bind(
            "<Return>", self.OnPressEnter
        )  # récupère ce qu'il y a décrit dans le widget lors de l'appuis sur le bouton
        self.entryVariable.set("not usable at the moment")

        button = tk.Button(
            self,
            text="Send",  # création d'un bouton, attaché à son parent, et avec du texte
            command=self.OnButtonClick,
        )  # active la détection d'appuis sur le bouton
        button.grid(column=1, row=0)  # placement du bouton sur la grille

        global textvar  # affiche de la zone de reception
        textvar = WritableStringVar(self)

        wwindow, hwindow, xwindow, ywindow = dimention(self)
        label = tk.Label(self, textvariable=textvar, height=20)
        print("Reception area", file=textvar)
        label.grid(
            column=0, row=1, columnspan=1, sticky="NS"
        )  # placement du label

        w = Label(self, text="Connecté:")
        w.grid(column=2, row=0)

        scrollbarclient = Scrollbar(self)
        scrollbarclient.grid(column=1, row=1, sticky="NE")
        self.listbox = Listbox(self)
        self.listbox.grid(column=2, row=1, rowspan=2, sticky="NE")

        # attach listbox to scrollbar
        self.listbox.config(yscrollcommand=scrollbarclient.set)
        scrollbarclient.config(command=self.listbox.yview)

        # permet de redimentioner en manuel la taille de la fenetre
        self.grid_columnconfigure(0, weight=1)

        # Le champ texte sera automatiquement re-sélectionné
        self.entry.focus_set()
        # après que l'utilisateur ait pressé ENTREE
        # Il pourra ainsi taper immédiatement un nouveau texte dans le champ (en remplaçant le texte existant).
        self.entry.selection_range(0, tk.END)

    def OnButtonClick(self,):
        # nouvelle méthode pour faire une/des action(s) quand il y a un appuis sur le bouton qui est détecté
        print(
            "At:",
            datetime.datetime.now(),
            "Clicked button !" + " writing text:",
            self.entryVariable.get(),
        )  # Log comme quoi qqun à appuyé sur le bouton
        self.entry.focus_set()  # Le champ texte sera automatiquement re-sélectionné
        # après que l'utilisateur ait pressé ENTREE
        self.entry.selection_range(0, tk.END)
        gestion_sending(self)

    def OnPressEnter(self, uselessVar):
        # nouvelle méthode pour faire une/des action(s) quand la touche Entre est appuyée lorsque
        # la sélection est sur le widget entry
        print(
            "At:",
            datetime.datetime.now(),
            "Clicked button !" + " writing text:",
            self.entryVariable.get(),
        )  # Log comme quoi qqun à appuyé sur la touche Entre
        # Le champ texte sera automatiquement re-sélectionné après que l'utilisateur ait pressé ENTREE
        self.entry.focus_set()
        self.entry.selection_range(0, tk.END)
        gestion_sending(self)

    def connect_action(self):
        print("Try connection at {}".format(datetime.datetime.now()))
        dialog_conn(self, title="Choice a server")

    def MAJRcvMsg(self, data):
        self.labelVariable.set(data)

    def close_application(self):
        print("At:", datetime.datetime.now(), "Menu, Exit")
        if tk.messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            print(
                "Fermeture de la fenetre: {} à {}".format(
                    self.master.title(), datetime.datetime.now()
                )
            )  # log indique la fermeture de la fenetre
            self.master.quit()
        else:
            print(
                "At:",
                datetime.datetime.now(),
                "Tentative de fermeture de la fenetre: ",
                self.master.title(),
            )


class WritableStringVar(tk.StringVar):
    def write(self, added_text):
        new_text = self.get() + added_text
        self.set(new_text)

    def clear(self):
        self.set("")


class dialog_conn(sdg.Dialog):
    def __init__(self, parent, title=None):
        super().__init__(parent, title=title)

    def body(self, master):
        Label(master, text="Adresse:").grid(row=0)
        Label(master, text="Port:").grid(row=1)
        # Label(master, text="Pseudo:").grid(row=2)

        self.ip1 = Entry(master, width=4)
        self.ip2 = Entry(master, width=4)
        self.ip3 = Entry(master, width=4)
        self.ip4 = Entry(master, width=4)
        self.port = Entry(master, width=4)
        # self.Pseudo = Entry(master, width=16)

        self.ip1.grid(row=0, column=1)
        self.ip2.grid(row=0, column=2)
        self.ip3.grid(row=0, column=3)
        self.ip4.grid(row=0, column=4)
        self.port.grid(row=1, column=1)
        # self.Pseudo.grid(row=2, column=1, columnspan=3)
        return self.ip1  # renvoi l'élément à focus

    def apply(self, title=None):
        try:
            Ip1 = int(self.ip1.get())
            Ip2 = int(self.ip2.get())
            Ip3 = int(self.ip3.get())
            Ip4 = int(self.ip4.get())
            if 0 >= Ip1 or Ip1 >= 255:
                print("Premier champs de IP incorrect")
                self.ip1.delete("", "end")
            else:
                IP = (
                    " ".join(
                        [
                            str(Ip1),
                            ".",
                            str(Ip2) + ".",
                            str(Ip3),
                            ".",
                            str(Ip4),
                        ]
                    )
                ).replace(" ", "")
                Port = int(self.port.get())
                # Pseudo = self.Pseudo.get()
                DataToSend.put(["Connect", IP, Port], True)
        except ValueError:
            print("ip incorrect")


def gestion_sending(self):
    global flag_list
    global list_pseudo
    global Pseudo_ok
    if flag_list:
        if Pseudo_ok == True:
            WriteMsgRcv("Me: " + self.entryVariable.get())
            DataToSend.put(["text", self.entryVariable.get(), ""], True)
        else:
            write_pseudo = self.entryVariable.get()
            if write_pseudo not in list_pseudo:
                print("PSEUDO OK")
                Pseudo_ok = True
                DataToSend.put(["Pseudo", self.entryVariable.get(), ""], True)
            else:
                Pseudo_ok = False
                print("PSEUDO NOK")


def dimention(self):
    w = self.winfo_screenwidth() / 2
    h = self.winfo_screenheight() / 2
    x = w / 2
    y = h / 2
    return w, h, x, y


def WriteMsgRcv(dataRcv):
    global textvar
    print(dataRcv, file=textvar)


def addClient(data):
    global list_pseudo
    print("Ajouter dans la liste:", data)
    list_pseudo.append(data)
    app.listbox.insert(END, data)


def set_flag_list():
    global app
    global flag_list
    flag_list = True
    app.entryVariable.set("Write your pseudo here")
    app.entry.focus_set()


def removeClient(target):
    global app
    indexTarget = app.listbox.get(0, tk.END).index(target)
    app.listbox.delete(indexTarget)


# if __name__ == "__main__":
def run_window(status):
    global DataToSend
    global app
    global flag_list
    global list_pseudo
    global Pseudo_ok
    Pseudo_ok = False
    flag_list = False
    DataToSend = status
    # root window created. Here, that would be the only window, but
    # you can later have windows within windows.
    root = Tk()
    root.title("ArchiComm")  # on name la fonction

    root.geometry("%dx%d+%d+%d" % (dimention(root)))  # dimentionne la fenetre
    app = Window(root)  # creation of an instance
    print(
        "création fenetre:", root.title(), datetime.datetime.now()
    )  # log indique la creation de la fenetre

    root.mainloop()  # mainloop

    print("App close")
    DataToSend.put("exit")
