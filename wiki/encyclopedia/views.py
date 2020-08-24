import re
import random

from django.shortcuts import render, redirect
from django import forms
from markdown2 import Markdown

from . import util

def error_404_view(request, exception):
    return render(request,'encyclopedia/404.html')

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search1(input):
    all_entries = util.list_entries()
    pattern = re.compile(input)
    result = []
    for i in all_entries:
        if re.fullmatch(pattern, i):
            result.append(i)
    return result

def search2(input):
    all_entries = util.list_entries()
    results = []
    for i in all_entries:
        if re.search(input, i, re.IGNORECASE):
            results.append(i)
    return results

def wiki(request, title = ''):
    if not title:
        if not request.POST:
            return index(request)
        else:
            user_input = request.POST['search']
    else:
        user_input = title
    entry = util.get_entry(user_input)
    if not entry:
        entries = search2(user_input)
        if not entries:
            return render(request, "encyclopedia/search.html", {
                    "msg" : "We are sorry, we cannot find any match with your search keyword",
                    "status" : "danger"
                })
        else:
            return render(request, "encyclopedia/search.html", {
                    "msg" : "We are unable to find the exact match of what you are looking for. But here something that close:",
                    "status" : "warning",
                    "entries" : entries
                })
    else:
        x = Markdown()
        return render(request, "encyclopedia/wiki.html", {
                "entry": x.convert(entry),
                "topic" : user_input
            })

def newpage(request):
    if not request.POST:
        return render(request, "encyclopedia/newpage.html", {
            "header" : "Create New Page"
        })
    else:
        title = request.POST['title']
        content = request.POST['content']
        entries = search1(title)
        if entries:
            return render(request, "encyclopedia/search.html", {
                "msg" : "The topic that you want to create is already exists in database. You might want to look at the existing topic:",
                "status" : "warning",
                "entries" : entries
            })
        else:
            util.save_entry(title, content)
            entries = [title]
            return render(request, "encyclopedia/search.html", {
                "msg" : "New entry has been saved. Checking it out?",
                "status" : "success",
                "entries" : entries
            })

def edit(request, title = ''):
    if not request.POST:
        if not title:
            return index(request)
        else:
            entry = util.get_entry(title)
            if not entry:
                return render(request, 'encyclopedia/404.html')
            else:
                return render(request, "encyclopedia/newpage.html", {
                        "header" : "Edit Content",
                        "topic" : title,
                        "entry": entry
                    })
    else:
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        entries = [title]
        return render(request, "encyclopedia/search.html", {
            "msg" : "New entry has been saved. Checking it out?",
            "status" : "success",
            "entries" : entries
        })

def random_title():
    entries = util.list_entries()
    title = random.choice(entries)
    return title

def random_entry(request):
    return wiki(request, random_title())
