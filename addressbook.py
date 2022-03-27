# @Author: Marcel Maluta
# @Date:   2022-02-28T15:48:07+01:00
# @Email:  marcelmaluta@gmail.com
# @Last modified by:   Marcel Maluta
# @Last modified time: 2022-03-27T19:13:58+02:00

## @package adressbook
#  Erstellt und verwaltet ein Adressbuch, in dem es mehrere Einträge gibt

import wx
import json
from data_handler import AddressBook

## Baut einen statisches wx Textobjekt
#  @param parent wx.Object Zugehörigkeit des wx Panelobjekt
#  @param sizer wx.Sizer Der wx Sizer in dem das Objekt eingefügt werden soll
#  @param label string Der Text der angezeigt werden soll
def staticTextBuilder(parent, sizer, label):
    st = wx.StaticText(parent, label=label)
    sizer.Add(st, 0, wx.ALL | wx.ALIGN_RIGHT, 10)
    return st

## Baut ein wx TextCtrl-Objekt in dem Benutzereingaben getätigt werden können
#  @param parent Zugehörigkeit des wx Panelobjekt
#  @param sizer Der wx Sizer in dem das Objekt eingefügt werdem soll
#  @param label Der Text der standartmäßig angezeigt werden soll
def textctrlBuilder(parent, sizer, label = ""):
    tc = wx.TextCtrl(parent, -1, size = (250, -1), value = label)
    sizer.Add(tc, 0, wx.ALL, 5)
    return tc

## Baut ein wx Button-Objekt das angeklickt werden kann
#  @param parent Zugehörigkeit des wx Panelobjekt
#  @param sizer Der wx Sizer in dem das Objekt eingefügt werden soll
#  @param label Der Text der in dem Button angezeigt werden soll
#  @param func Die Funktion die der Button auslöst
def btnBuilder(parent, sizer, label, func):
    btn = wx.Button(parent, label = label)
    btn.Bind(wx.EVT_BUTTON, func)
    sizer.Add(btn, 0, wx.ALL | wx.ALIGN_CENTER)
    return btn

## Erstellt ein Panelobjekt
class AddPanel(wx.Panel):
    ## Der Konstruktor
    #  @param parent Das vorherige Objekt
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Verwendet eine Tabelle als Vorlage
        main_sizer = wx.FlexGridSizer(8, 2, 3, 5)

        staticTextBuilder(self, main_sizer, "Vorname:")
        self.textctrl_firstname = textctrlBuilder(self, main_sizer)
        staticTextBuilder(self, main_sizer, "Nachname:")
        self.textctrl_lastname = textctrlBuilder(self, main_sizer)
        staticTextBuilder(self, main_sizer, "Telefonnummer:")
        self.textctrl_phone = textctrlBuilder(self, main_sizer)
        staticTextBuilder(self, main_sizer, "E-Mail:")
        self.textctrl_email = textctrlBuilder(self, main_sizer)
        staticTextBuilder(self, main_sizer, "Straße:")
        self.textctrl_street = textctrlBuilder(self, main_sizer)
        staticTextBuilder(self, main_sizer, "Stadt:")
        self.textctrl_city = textctrlBuilder(self, main_sizer)
        staticTextBuilder(self, main_sizer, "Postleitzahl:")
        self.textctrl_zip = textctrlBuilder(self, main_sizer)


        btnBuilder(self, main_sizer, "Hinzufügen", self.onAccept)
        btnBuilder(self, main_sizer, "Abbrechen", self.onDiscard)

        self.SetSizer(main_sizer)

    ## Methode die von dem Knopfdruck "Hinzufügen" aufgerufen wird
    #  @param event Das Eventobjekt
    def onAccept(self, event):
        firstname = self.textctrl_firstname.GetValue()
        lastname = self.textctrl_lastname.GetValue()
        phone = self.textctrl_phone.GetValue()
        email = self.textctrl_email.GetValue()
        street = self.textctrl_street.GetValue()
        city = self.textctrl_city.GetValue()
        zip = self.textctrl_zip.GetValue()

        if(firstname == "" and lastname == "" and phone == "" and email == "" and street == "" and city == "" and zip == ""):
            dialog = wx.MessageDialog(self, "Es wurden keine Daten angegeben!", style=wx.OK)
            dialog.ShowModal()
        else:
            entry = {
                "firstname": firstname,
                "lastname": lastname,
                "phone": phone,
                "email": email,
                "street": street,
                "city": city,
                "zip": zip
            }

            address = AddressBook("data.json")
            address.addEntry(entry)
            self.parent.Destroy()
            self.parent.main_panel.update_list()

    ## Methode die von dem Knopfdruck "Abbrechen" aufgerufen wird
    #  @param event Das Eventobjekt
    def onDiscard(self, event):
        self.parent.Destroy()

## Erstellt ein Fensterobjekt
class AddFrame(wx.Frame):
    ## Der Konstruktor
    #  @param parent Das vorherige Objekt
    def __init__(self, parent):
        super().__init__(parent=parent, title="Eintrag hinzufügen", size=wx.Size(400, 350))
        self.panel = AddPanel(self)
        self.main_panel = parent
        self.SetIcon(wx.Icon("agenda.png"))
        self.Show()

## Erstellt eine Panelobjekt
class EditPanel(wx.Panel):
    ## Der Konstruktor
    #  @param parent Das vorherige Objekt
    #  @param entry Der Eintrag der ausgewählt wurde
    def __init__(self, parent, entry):
        super().__init__(parent)
        self.parent = parent
        main_sizer = wx.FlexGridSizer(8, 2, 3, 5)

        staticTextBuilder(self, main_sizer, "Vorname:")
        self.textctrl_firstname = textctrlBuilder(self, main_sizer, entry["firstname"])
        staticTextBuilder(self, main_sizer, "Nachname:")
        self.textctrl_lastname = textctrlBuilder(self, main_sizer, entry["lastname"])
        staticTextBuilder(self, main_sizer, "Telefonnummer:")
        self.textctrl_phone = textctrlBuilder(self, main_sizer, entry["phone"])
        staticTextBuilder(self, main_sizer, "E-Mail:")
        self.textctrl_email = textctrlBuilder(self, main_sizer, entry["email"])
        staticTextBuilder(self, main_sizer, "Straße:")
        self.textctrl_street = textctrlBuilder(self, main_sizer, entry["street"])
        staticTextBuilder(self, main_sizer, "Stadt:")
        self.textctrl_city = textctrlBuilder(self, main_sizer, entry["city"])
        staticTextBuilder(self, main_sizer, "Postleitzahl:")
        self.textctrl_zip = textctrlBuilder(self, main_sizer, entry["zip"])

        btnBuilder(self, main_sizer, "Aktualisieren", self.onAccept)
        btnBuilder(self, main_sizer, "Abbrechen", self.onDiscard)

        self.SetSizer(main_sizer)

    ## Die Methode die von dem Knopfdruck "Aktualisieren" aufgerufen wird
    #  @param event Das Eventobjekt
    def onAccept(self, event):
        firstname = self.textctrl_firstname.GetValue()
        lastname = self.textctrl_lastname.GetValue()
        phone = self.textctrl_phone.GetValue()
        email = self.textctrl_email.GetValue()
        street = self.textctrl_street.GetValue()
        city = self.textctrl_city.GetValue()
        zip = self.textctrl_zip.GetValue()
        if(firstname == "" and lastname == "" and phone == "" and email == "" and street == "" and city == "" and zip == ""):
            dialog = wx.MessageDialog(self, "Es wurden keine Daten angegeben!", style=wx.OK)
            dialog.ShowModal()
        else:
            focus = self.parent.main_panel.list_ctrl.GetFocusedItem()
            self.parent.main_panel.list[focus]["firstname"] = firstname
            self.parent.main_panel.list[focus]["lastname"] = lastname
            self.parent.main_panel.list[focus]["phone"] = phone
            self.parent.main_panel.list[focus]["email"] = email
            self.parent.main_panel.list[focus]["street"] = street
            self.parent.main_panel.list[focus]["city"] = city
            self.parent.main_panel.list[focus]["zip"] = zip
            address = AddressBook("data.json")
            address.saveList(self.parent.main_panel.list)
            self.parent.main_panel.update_list()
            self.parent.Destroy()

    ## Die Methode die von dem Knopfdruck "Abbrechen" aufgerufen wird
    #  @param event Das Eventobjekt
    def onDiscard(self, event):
        self.parent.Destroy()

## Erstellt eine Fensterobjekt
class EditFrame(wx.Frame):
    ## Der Konstruktor
    #  @param entry dict Der Adressbucheintrag der ausgewählt wurde
    #  @param parent Das vorherige Element
    def __init__(self, entry, parent):
        super().__init__(parent=parent, title="Eintrag hinzufügen", size=wx.Size(400, 350))
        self.panel = EditPanel(self, entry)
        self.main_panel = parent
        self.SetIcon(wx.Icon("agenda.png"))
        self.Show()

## Erstellt die grafische Oberfläche des Adressbuchs
class AdressBookPanel(wx.Panel):

    ## Der Konstruktor
    #  @param parent Das vorherige Element
    def __init__(self, parent):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Liste für die Adressbucheinträge erstellen
        self.list_ctrl = wx.ListCtrl(
            self, size=(-1, 1000),
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.list_ctrl.InsertColumn(0, "Vorname", width=100)
        self.list_ctrl.InsertColumn(1, "Nachname", width=100)
        self.list_ctrl.InsertColumn(2, "E-mail", width=200)
        self.list_ctrl.InsertColumn(3, "Telefonnummer", width=100)
        self.list_ctrl.InsertColumn(4, "Straße", width=100)
        self.list_ctrl.InsertColumn(5, "Stadt", width=100)
        self.list_ctrl.InsertColumn(6, "Postleitzahl", width=100)
        self.update_list()
        main_sizer.Add(self.list_ctrl, 0, wx.ALL , 5)

        # Rechtes Panel einfügen
        second_sizer = wx.BoxSizer(wx.VERTICAL)
        btnBuilder(self, second_sizer, "Neuer Eintrag", self.onAdd)
        btnBuilder(self, second_sizer, "Bearbeiten", self.onEdit)
        btnBuilder(self, second_sizer, "Löschen", self.onDelete)
        btnBuilder(self, second_sizer, "Aktualisieren", self.onUpdate)

        main_sizer.Add(second_sizer, 0, wx.ALL, 3)
        self.SetSizer(main_sizer)

    ## Die Methode die von dem Knopfdruck "Hinzufügen" aufgerufen wird
    #  @param event Das Eventobjekt
    def onAdd(self, event):
        frame = AddFrame(self)

    ## Die Methode die von dem Knopfdruck "Bearbeiten" aufgerufen wird
    #  @param event Das Eventobjekt
    def onEdit(self, event):
        focus = self.list_ctrl.GetFocusedItem()
        entry = self.list[focus]
        myframe = EditFrame(entry, self)

    ## Die Methode die von dem Knopfdruck "Löschen" aufgerufen wird
    #  @param event Das Eventobjekt
    def onDelete(self, event):
        dlg = wx.MessageDialog(None, "Möchten Sie den Eintrag löschen?", "Eintrag löschen?", wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            focus = self.list_ctrl.GetFocusedItem()
            self.list.pop(focus)
            address = AddressBook("data.json")
            address.saveList(self.list)
            self.update_list()

    ## Die Methode die von dem Knopfdruck "Aktualisieren" aufgerufen wird
    #  @param event Das Eventobjekt
    def onUpdate(self, event):
        self.update_list()

    ## Aktualisiert die grafische Oberfläche wenn eine Veränderung des Adressbuchs vorgenommen wurde
    #  @param self Der Objektzeiger
    def update_list(self):
        address = AddressBook("data.json")
        self.list = address.loadList()
        self.list_ctrl.DeleteAllItems()
        index = 0
        for entry in self.list:
            self.list_ctrl.InsertItem(index, entry["firstname"])
            self.list_ctrl.SetItem(index, 1, entry["lastname"])
            self.list_ctrl.SetItem(index, 2, entry["email"])
            self.list_ctrl.SetItem(index, 3, entry["phone"])
            self.list_ctrl.SetItem(index, 4, entry["street"])
            self.list_ctrl.SetItem(index, 5, entry["city"])
            self.list_ctrl.SetItem(index, 6, str(entry["zip"]))
            index += 1

## Das Fensterobjekt für das Adressbuch
class AdressBookFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Adressbuch", size=wx.Size(950, 500), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.panel = AdressBookPanel(self)
        self.SetIcon(wx.Icon("agenda.png"))
        self.Show()

if __name__ == '__main__':
    app = wx.App(False)
    frame = AdressBookFrame()
    app.MainLoop()
