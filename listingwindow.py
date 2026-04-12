#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 8 16:41:49 2025

@author: ethanjames
"""
import tkinter as tk
import scraping

# colour palette
BG_COLOR = "#1e1e2f"
FG_COLOR = "#ffffff"
ACCENT = "#4CAF50"
DANGER = "#e74c3c"
ENTRY_BG = "#2c2c3e"

pages= []
curr_page = -1

root = tk.Tk(screenName="Employment List",baseName="Employment List",className="Employment List")
root.title("Employment List")
root.configure(bg='white')
root.geometry('450x700+920+50')

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

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

def on_enter(e):
    e.widget.config(fg="#0b57d0")

def on_leave(e):
    e.widget.config(fg="#1a73e8")

btn_style = {
    "font": ("Segoe UI", 10),
    "bg": "#1a73e8",
    "fg": "white",
    "activebackground": "#0b57d0",
    "relief": "flat",
    "padx": 10,
    "pady": 5
}

class Page(tk.Frame):
    
    def __init__(self,parent,job_titles,links,page_number):

        super().__init__(parent)
        self.page_number = page_number
        label = tk.Label(self,text="Listings",font=("Arial",24))
        label.pack(pady=10)
        page_number = tk.Label(self,text="Page Number " + str(page_number+1),fg="black",cursor="hand2")
        page_number.pack(pady=10)
        curr_link = 0
        
        for title in job_titles:
            
            card = tk.Frame(self, bg="#f5f5f5", bd=1, relief="solid")
            card.pack(fill="x", padx=10, pady=5)

            link = tk.Label(card, text=title, fg="#1a73e8", cursor="hand2",bg="#f5f5f5", font=("Segoe UI", 11))
            link.pack(anchor="center", padx=10, pady=5)

            if "LISTINGS FOR" not in title:
                card.bind("<Enter>", on_enter)
                card.bind("<Leave>", on_leave)
                card.bind("<Button-1>", lambda event, url=links[curr_link]: scraping.open_link(url, title))

                link.bind("<Enter>", on_enter)
                link.bind("<Leave>", on_leave)
                link.bind("<Button-1>", lambda event, url=links[curr_link]: scraping.open_link(url, title))

            curr_link += 1
            
        previous_page_button = tk.Button(self,text="<- Previous", **btn_style, command=lambda: render_page(False,curr_page))
        previous_page_button.pack(pady=10)
        next_page_button = tk.Button(self,text="Next ->", **btn_style, command=lambda: render_page(True,curr_page))
        next_page_button.pack(pady=10)
        
    
def generate_pages(job_titles,links):

    global pages, curr_page, root

    opportunity_counter = 0
    page_number = 0
    
    while opportunity_counter < len(job_titles):
        
        titles_for_curr_page = []
        links_for_curr_page = []
        
        for j in range(0,5):
            
            if opportunity_counter < len(job_titles):
                    
                titles_for_curr_page.append(job_titles[opportunity_counter])
                links_for_curr_page.append(links[opportunity_counter])

                opportunity_counter += 1
    
        new_page = Page(scrollable_frame,titles_for_curr_page,links_for_curr_page,page_number)
        new_page.grid(row=0,column=0,sticky="nsew")
        pages.append(new_page)
        page_number += 1
        
    render_page(True,curr_page)
    
def render_page(next_page,page_number):
    
    global curr_page, pages
    if next_page and curr_page < len(pages) - 1:
        curr_page += 1
        pages[curr_page].tkraise()
    elif curr_page > 0:
        curr_page -= 1
        pages[curr_page].tkraise()
        
    
    
    
    
    
    
    
    
    
    