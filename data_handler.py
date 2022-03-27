# @Author: Marcel Maluta
# @Date:   2022-03-08T15:53:24+01:00
# @Email:  marcelmaluta@gmail.com
# @Last modified by:   Marcel Maluta
# @Last modified time: 2022-03-09T19:27:57+01:00

## @package data_handler
#  Ein Hilfspaket in dem zusätzliche Klassen und Funktionen bereitgestellt werden

import json

## Eine Knotenpunkt eines Binärbaums
class Node():
    ## Der Konstruktor
    #  @param data Der Wert der in dem Knotenpunkt gespeichert werden soll
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

## Binärbaum in dem Dictionaries gespeichert werden
class EntryTree():
    ## Der Konstruktor
    def __init__(self):
        self.root = None

    ## Fügt einen neuen Knotenpunkt geordnet ein
    #  @param data Der Wert der in dem Knotenpunkt gespeichert werden soll
    def add(self, data):
        if self.root == None:
            self.root = Node(data)
        else:
            self._add(data, self.root)

    ## Fügt einen neuen Knotenpunkt geordnet ein
    #  @param data Der Wert der in dem Knotenpunkt gespeichert werden soll
    #  @param node Der momentane Knoten der ausgewählt wurde
    def _add(self, data, node):
        if data["firstname"] < node.data["firstname"]:
            if node.left is not None:
                self._add(data, node.left)
            else:
                node.left = Node(data)
        else:
            if node.right is not None:
                self._add(data, node.right)
            else:
                node.right = Node(data)

    ## Gibt eine geordnete Liste zurück
    #  @param node Der ausgewählte Knoten
    #  @param list Die Liste in der die Daten gespeichert werden sollen
    def getList(self, node, list):
        if node.left is not None:
            self.getList(node.left, list)
        list.append(node.data)
        if node.right is not None:
            self.getList(node.right, list)

## Hilfsobjekt um eine .json Datei zu verwalten
class AddressBook():
    ## Der Konstruktor
    #  @param path Der Dateipfad zu der .json Datei
    def __init__(self, path):
        self.path = path

    ## Fügt einen neuen Eintrag in die .json Datei ein
    #  @param entry Das Dictionary das neu eingefügt werden soll
    def addEntry(self, entry):
        list = self.loadList()
        list.append(entry)

        # Liste in einen Binärbaum eintragen
        tree = EntryTree()
        for e in list:
            tree.add(e)

        # Neue geordnete Liste erstellen
        ordered_list = []
        tree.getList(tree.root, ordered_list)
        self.saveList(ordered_list)

    ## Ladet die .json Datei und gibt eine Liste zurück
    def loadList(self):
        f = open(self.path, "r")
        list = json.load(f)
        return list

    ## Schreibt im JSON Format in eine Datei
    #  @param list Die Liste die abgespeichert werden soll
    def saveList(self, list):
        f = open(self.path, "w")
        json.dump(list, f, indent=4)
        f.close()
