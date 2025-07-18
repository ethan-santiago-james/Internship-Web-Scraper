#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 8 16:41:49 2025

@author: ethanjames
"""
import tkinter as tk
import scraping

pages= []
curr_page = -1

root = tk.Tk(screenName="Employment List",baseName="Employment List",className="Employment List")
root.title("Employment List")
root.configure(bg='white')
root.geometry('435x700+920+50')

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
    
class Page(tk.Frame):
    
    def __init__(self,parent,job_titles,links,page_number):

        super().__init__(parent)
        self.page_number = page_number
        label = tk.Label(self,text="Listings",font=("Arial",24))
        label.pack(pady=10)
        page_number = tk.Label(self,text="Page Number " + str(page_number),fg="black",cursor="hand2")
        page_number.pack(pady=10)
        curr_link = 0
        
        for title in job_titles:
            
            if "LISTINGS FOR" in title:
                
                link = tk.Label(self,text=title,fg='red',cursor="hand2")
                link.pack(pady=10)
                
            else:

                link = tk.Label(self,text=title,fg="aqua",cursor="hand2")
                link.pack(pady=10)
                link.bind("<Button-1>",lambda event, url=links[curr_link]: scraping.open_link(url,title))
            curr_link += 1
            
        previous_page_button = tk.Button(self,text="Previous Page",command=lambda: render_page(False,curr_page))
        previous_page_button.pack(pady=10)
        next_page_button = tk.Button(self,text="Next Page",command=lambda: render_page(True,curr_page))
        next_page_button.pack(pady=10)
        
    
def generate_pages(job_titles,links):

    global pages, curr_page, root

    opportunity_counter = 0
    page_number = 0
    
    while opportunity_counter < len(job_titles):
        
        titles_for_curr_page = []
        links_for_curr_page = []
        
        for j in range(0,10):
            
            if opportunity_counter < len(job_titles):
                    
                titles_for_curr_page.append(job_titles[opportunity_counter])
                links_for_curr_page.append(links[opportunity_counter])

                opportunity_counter += 1
    
        new_page = Page(root,titles_for_curr_page,links_for_curr_page,page_number)
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
        
    
    
    
    
    
    
    
    
    
    