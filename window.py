import tkinter as tk
import scraping
import logging

logging.basicConfig(level=logging.INFO)

# colour palette
BG_COLOR = "#1e1e2f"
FG_COLOR = "#ffffff"
ACCENT = "#4CAF50"
DANGER = "#e74c3c"
ENTRY_BG = "#2c2c3e"

# window

root = tk.Tk(screenName="IOF",baseName="iof",className="IOF",useTk=1)
root.configure(bg=BG_COLOR)
root.title('Employment Finder')

# scroll wheel
container = tk.Frame(root)
container.pack(fill="both", expand=True)

canvas = tk.Canvas(container, bg=BG_COLOR, highlightthickness=0)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


# dimensions
root.geometry("500x700+600+50")

# variables for links
curr_link_row = 4

# entry lists
entry_lists = []
keyword = ""


def confirm_keyword(entry):

    global keyword
    keyword = entry.get()
    
# event listeners
def add_link(confirm_button):

   global curr_link_row
   new_label = tk.Label(scrollable_frame,text="New Company")
   new_label.grid(row=curr_link_row,column=2,pady=20)
   
   new_entry = tk.Entry(scrollable_frame)
   new_entry.grid(row=curr_link_row,column=3,pady=20)
   entry_lists.append(new_entry)
   
   delete_button = tk.Button(scrollable_frame,text='Remove',command=lambda: destroy_link(new_label,new_entry,delete_button),bg=DANGER)
   delete_button.grid(row=curr_link_row,column=4,pady=20)
   curr_link_row += 1
   
   confirm_button.grid_forget()
   confirm_button.grid(row=curr_link_row+1,column=3,pady=20)   
   
def destroy_link(label,entry,button):
    
    label.destroy()
    entry_lists.remove(entry)
    entry.destroy()
    button.destroy()
    
        
# GUI elements
title = tk.Label(scrollable_frame, text='Welcome To Employment Finder!',
        bg=BG_COLOR, fg=FG_COLOR, font=("Arial",16,"bold"))
title.grid(row=0,column=3,pady=20)

add_keyword_label = tk.Label(scrollable_frame,text='Enter Keyword').grid(row=2,column=2)
add_keyword_entry = tk.Entry(scrollable_frame,bg=ENTRY_BG)
add_keyword_entry.grid(row=2,column=3,padx=10,pady=5)

add_keyword_submit = tk.Button(scrollable_frame,text='Submit',command=lambda: confirm_keyword(add_keyword_entry),bg="green").grid(row=2,column=4)

confirm_links_button = tk.Button(scrollable_frame,text='Confirm Companies',command=lambda: scraping.search_links(entry_lists,keyword),bg="green")

add_link_button = tk.Button(scrollable_frame,text='Add Company',width=25,command=lambda: add_link(confirm_links_button),pady=15)
add_link_button.grid(row=3,column=3)

confirm_links_button.grid(row=curr_link_row+1,column=3,pady=20)
curr_link_row += 1

root.mainloop()