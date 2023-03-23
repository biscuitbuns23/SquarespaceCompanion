###TEST EVERYTHING HERE: comment out the modules that will affect debug
import createProducts as cp
import json
import keys as k
import pandas
import tkinter as tk
import customtkinter as ctk
import requests
import time
import menu as m



### CURRENTLY WORKING ON RETREIVING PAGE ID FOR USE IN PRODUCT CREATION
### gets a list of pages and their id's, as well as some other random info that is included.
#   returns name and id of specified page number only. This function is only intended to be
#   called by the function 'pagesList'.
def getPagesList(x):
    getStorePagesURL = 'https://api.squarespace.com/1.0/commerce/store_pages'
    getStorePagesHeaders = {'Authorization': 'Bearer ' + k.apiKey,
                            'User-Agent': 'APIAPP1.0'}
    r = requests.get(getStorePagesURL, headers=getStorePagesHeaders)
    # data is the dictionary returned by the request.
    data = r.json()
    # storePages is the 2nd key in dictionary, its value is a list of dictionaries.
    storePages = data['storePages']
    # pageOne accesses the first element of the list, which is a dictionary of the
    # first page's info. If there are multiple store pages then this is a good
    # place to start a for loop to iterate through them.
    pageOne = storePages[x]
    # pageOne has all the info we need for now. pageID and pageName are accessing
    # the specific keys and values needed for our current use.
    pageID = pageOne['id']
    pageName = pageOne['title']
    pageInfo = {pageName: pageID}
    return pageInfo


### getNumOfPages returns the number of pages. It can be called by itself if the user
#   wants the number of pages, and is also called by pagesList to be used for the range
#   of pages to be iterated over.
def getNumOfPages():
    getStorePagesURL = 'https://api.squarespace.com/1.0/commerce/store_pages'
    getStorePagesHeaders = {'Authorization': 'Bearer ' + k.apiKey,
                            'User-Agent': 'APIAPP1.0'}
    r = requests.get(getStorePagesURL, headers=getStorePagesHeaders)
    # data is the dictionary returned by the request.
    data = r.json()
    # storePages is the 2nd key in dictionary, its value is a list of dictionaries.
    storePages = data['storePages']
    numOfPages = len(storePages)
    return numOfPages


### pagesList shows a list of all pages and their id's. Calls getNumOfPages and
#   getPagesList in order to iterate over all pages.
def pagesList():
    PagesNo = getNumOfPages()
    # erases any previously saved data from 'pages.txt' file
    open('pages.txt', 'w').close()
    # iterates over pages and writes them to file
    for i in range(0, PagesNo):
        page = getPagesList(i)
        file1 = open('pages.txt', 'w')
        
        file1.write(str(page))

pagesList()

###CURRENTLY WORKING ON UI USING CUSTOMTKINTER
#window
# window = ctk.CTk()
# window.title('Squarespace Companion')
# window.geometry('600x400')

# #widgets
# label = ctk.CTkLabel(window, text = 'a ctk label',
#                         fg_color = 'red',
#                         text_color = 'white',
#                         corner_radius = 10)
# label.pack()

# button = ctk.CTkButton(window,
#                         text = 'a ctk button',
#                         fg_color = '#FF0',
#                         text_color = 'red',
#                         hover_color = '#AA0',
#                         command = lambda: ctk.set_appearance_mode('dark'))
# button.pack()

# #run
# window.mainloop()



### Command line menu loop
# print('Welcome to Squarespace Companion!\n'
#       '\n'
#       'If you have not already, please configure your settings\n'
#       'under the settings option in the main menu.')
# time.sleep(3)

# #Start the menu loop
# while True:
#     print('Main menu \n')
#     print('c - Create Products \n'
#           's - Settings \n'
#           'x - Exit \n')
#     selection = input('Select an option. \n')

#     if selection == 'c':
#         getPages()
#         print('\n')

#     elif selection == 's':
#         m.settingsMenu()

#     elif selection == 'x':
#         break

#     elif selection != ['c', 's', 'x']:
#         print('not a valid selection'
#               '\n')



### Working on a version of import excel that imports .numbers files
# from numbers_parser import Document
# doc = Document('/Users/jonathan/Downloads/DRESS INVENTORY.numbers')
# sheets = doc.sheets()
# tables = sheets[0].tables()
# rows = tables[0].rows()

# newDict = dict(doc)

# print(type(newDict))




{'pagination': {'nextPageUrl': None,
                'nextPageCursor': None,
                'hasNextPage': False},
'storePages': [{'id': '641a906c3f58246e8a8fe285',
                'title': 'All products',
                'isEnabled': True,
                'urlSlug': 'all-products'}]}