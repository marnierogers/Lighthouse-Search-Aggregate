from sys import exit as abort
from urllib.request import urlopen
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar
from re import *
from webbrowser import open as urldisplay
from sqlite3 import *


#----- Helper FFunction----------------------------------------------#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'downloaded_document',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             incognito = False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        if incognito:
            # Pretend to be a web browser instead of
            # a Python script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                               'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                               'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246')
            print("Warning - Request does not reveal client's true identity.")
            print("          This is both unreliable and unethical!")
            print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " + \
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#------- Create window, import image + put into grid -----
#Create root window, set size to screen
root_window = Tk()
screen_width = root_window.winfo_screenwidth()
screen_height = root_window.winfo_screenheight()


#Define root window title
root_window.title("Lighthouse Search: Find what you're looking for!")

#Change background colour
root_window['bg'] = 'white'

#Set default font
default_font = ('Arial Rounded MT Bold', 16)
small_default_font = ('Arial Rounded MT Italic', 14)

#------- Import logo and display -----------------------

#Import an image to display in window
lighthouse_logo = PhotoImage(file = 'lighthouse_logo_white_rectangle.png')

#Add image to the root window as a label widget
logo_label = Label(root_window, image = lighthouse_logo, borderwidth = 0)
logo_label.grid(row = 1, column = 1, columnspan = 10, padx = 5)

#------- Add spacer between widgets --------------------

spacer0 = Label(root_window, text = '', bg = 'white')
spacer0.grid(row = 2, column = 1)

#------- Create text box -------------------------------

textbox = Message(root_window, font = default_font,
                  text = "Searching for what you need is as easy as 1, 2, 3 with Lighthouse!",
                  bg = "white", width = 440, justify = CENTER, fg = "black")
textbox.grid(row = 3, column = 5, columnspan = 5)


#------- Add spacer between widgets --------------------

spacer1 = Label(root_window, text = '', bg = 'white')
spacer1.grid(row = 5, column = 1)

#------- Create frame for category window --------------

categoryframe = LabelFrame(root_window, font = default_font, text = "1. Select Category", width = 350,
                           height = 200, bd = 4, bg = 'white', relief = 'ridge', fg = "orange")
categoryframe.grid(row = 6, column = 5, padx = 20)
categoryframe.grid_propagate(False)

#------- Create radio buttons, put into category window -

# Create radio button widgets within the frame to control the
# label's colour
first_cat_button = Radiobutton(categoryframe, text = 'Used cars at Autotrader', font = default_font,
                               bg = 'white', activeforeground = "orange", value = 1)
second_cat_button = Radiobutton(categoryframe, text = 'Home Decor at Gumtree', font = default_font,
                                bg = 'white', activeforeground = "orange", value = 2)
third_cat_button = Radiobutton(categoryframe, text = 'Home Appliances at eBay' , font = default_font,
                               bg = 'white', activeforeground = "orange", value = 3)

# Put the three radio buttons into the frame
first_cat_button.grid(row = 6, column = 5, sticky = W, pady = 8)
second_cat_button.grid(row = 7, column = 5, sticky = W, pady = 8)
third_cat_button.grid(row = 8, column = 5, sticky = W, pady = 8)

#------- Create frame for item window ---------------------

itemframe = LabelFrame(root_window, font = default_font, text = "2. Select Item", width = 180,
                       height = 200, pady = 5, padx = 5, bd = 4, bg = 'white', relief = 'ridge', fg = "orange")
itemframe.grid(row = 6, column = 6, padx = 20)
itemframe.grid_propagate(False)

#------- Create push buttons, put into item window --------

# Create radio button widgets within the frame to control the
# label's colour
first_item_button = Checkbutton(itemframe, text = 'Latest', font = default_font, width = 10, height = 1,
                           pady = 2, padx = 2, bg = 'white', activeforeground = "orange", indicatoron = False)
second_item_button = Checkbutton(itemframe, text = 'Second', font = default_font, width = 10, height = 1,
                            pady = 2, padx = 2, bg = 'white', activeforeground = "orange", indicatoron = False)
third_item_button = Checkbutton(itemframe, text = 'Third' , font = default_font, width = 10, height = 1,
                           pady = 2, padx = 2, bg = 'white', activeforeground = "orange", indicatoron = False)

# Put the three radio buttons into the frame (each on
# a separate grid row and sticking to the West border)
first_item_button.grid(row = 6, column = 6, padx = 2, pady = 2)
second_item_button.grid(row = 7, column = 6, padx = 2, pady = 2)
third_item_button.grid(row = 8, column = 6, padx = 2, pady = 2)

#------- Add spacer between widgets -----------------------

spacer2 = Label(root_window, text = '', bg = 'white')
spacer2.grid(row = 7, column = 1)

#------- Create frame for options window ------------------

optionframe = LabelFrame(root_window, font = default_font, text = "3. Save selection?", width = 350,
                         height = 80,bd = 4, bg = 'white', relief = 'ridge', fg = "orange")
optionframe.grid(row = 8, column = 5)
optionframe.grid_propagate(False)


#------- Create checkbutton, put into options window -----

# Create check button widgets within the frame
first_option_checkbutton = Checkbutton(optionframe, text = 'Yes please!', font = default_font,
                                       width = 15, height = 1, pady = 2, bg = 'white', activeforeground = "orange")

# Put the check button into options window
first_option_checkbutton.grid(row = 7, column = 4,  sticky = W)


#------- Create frame for CTA window -----------------------

CTAbuttonframe = LabelFrame(root_window, font = default_font, width = 180, height = 50,
                            pady = 5, padx = 5, bd = 0, bg = 'white')
CTAbuttonframe.grid(row = 8, column = 6)
CTAbuttonframe.grid_propagate(False)


#------- Create push button, put into CTA window ------------

# Create push button widgets within the frame
CTA_button = Button(CTAbuttonframe, text = "Let's Go!", font = default_font, width = 10,
                    height = 1, bg = 'orange', activeforeground = "white", relief = 'groove')

# Put the push button into options window
CTA_button.grid(row = 8, column = 6)


#------- Add spacer between widgets -------------------------
spacer3 = Label(root_window, text = '', bg = 'white')
spacer3.grid(row = 9, column = 1)


#------- Create Here's what we found message -----------------

textbox_result = Message(root_window, font = default_font, text = "Here's what we found!",
                         bg = "white", width = 440, justify = CENTER, fg = "black")
textbox_result.grid(row = 10, column = 5, columnspan = 5)


#------- Add spacer between widgets -------------------------
spacer4 = Label(root_window, text = '', bg = 'white')
spacer4.grid(row = 11, column = 1)


#------- Create frame for selection window ------------------

selectionframe = LabelFrame(root_window, font = default_font, width = 600, height = 250,
                            pady = 5, padx = 5, bd = 4, bg = 'orange')
selectionframe.grid(row = 12, column = 2, columnspan = 10, padx = 20, pady = 10)
selectionframe.grid_propagate(False)


#------- Add place holder image to window ------------------

placeholder_image = PhotoImage(file = 'placeholder.png')
placeholder_label = Label(selectionframe, image = placeholder_image, borderwidth = 0,
                          pady = 50)
placeholder_label.grid(row = 12, column = 3, columnspan = 2, padx = 5)


#------- Create description text box -----------------------


description_box = Text(selectionframe, font = default_font, width = 30, height = 3,
                       wrap = WORD, borderwidth = 3, relief = 'sunken',
                       padx = 20, pady = 20, fg = 'grey')
description_box.grid(row = 12, column = 5, columnspan = 3)
description_box.insert(END, 'Item description appears here')
description_box.config(state = 'disabled')


#------- Create source text box ----------------------------

source_box = Text(selectionframe, font = small_default_font, width = 30, height = 1,
                       wrap = WORD, borderwidth = 3, relief = 'sunken', fg = 'grey')
source_box.grid(row = 19, column = 3, columnspan = 3)
source_box.insert(END, 'Source: Lorem ipsum dolor sit amet')
source_box.config(state = 'disabled')


#------- Create URL text box ------------------------------

URL_box = Text(selectionframe, font = small_default_font, width = 30, height = 1,
                       wrap = WORD, borderwidth = 3, relief = 'sunken', fg = 'grey')
URL_box.grid(row = 20, column = 3, columnspan = 3)
URL_box.insert(END, 'URL: Lorem ipsum dolor sit amet')
URL_box.config(state = 'disabled')


#------- Create price message ----------------------------

item_price = Message(selectionframe, font = default_font, text = "Price: $",
                  bg = "orange", width = 100, fg = "black")
item_price.grid(row = 17, column = 6, rowspan = 2)
item_price.grid_propagate(False)

#------- Create price text box ----------------------------

price_box = Text(selectionframe, font = default_font, width = 5, height = 1,
                borderwidth = 0, fg = 'grey', pady = 5, padx = 10)
price_box.grid(row = 17, column = 7, columnspan = 2, rowspan = 2)
price_box.insert(END, '00.00')
price_box.config(state = 'disabled')
price_box.grid_propagate(False)


#------- Create CTA Buy Now -------------------------------

# Create push button widgets within the frame
CTA_buynow_button = Button(selectionframe, text = "Buy Now!", font = default_font, width = 10,
                           height = 1, bg = 'orange', activeforeground = "white", relief = 'groove')

# Put the push button into options window
CTA_buynow_button.grid(row = 20, column = 7)


#------- End mainloop --------------------------------------

#Call method for window / interact with user
root_window.mainloop()


