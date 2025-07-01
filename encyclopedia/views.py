from django.shortcuts import render
from random import randint

# Create your views here.
from . import util
from markdown2 import Markdown


def index(request):
    list_entries = util.list_entries()
    keyword = request.GET.get("q")
    if keyword is None:
        return render(request, "encyclopedia/index.html", {
            "heading": "All pages",
            "entries": list_entries
        })
    
    keyword = keyword.strip()
    matched_entries = []
    for entry in list_entries:
        if keyword.lower() == entry.lower():
            return wiki_page(request, entry)
        if keyword.lower() in entry.lower():
            matched_entries.append(entry)
    if len(matched_entries) == 0:
        heading = "No matched pages for " + keyword
    else:
        heading = "Matched pages for " + keyword        
    return render(request, "encyclopedia/index.html", {
        "heading": heading,
        "entries": matched_entries
    })


def wiki_page(request, title):
    content = util.get_entry(title)
    if content is None:
        content = "No such wiki exists!"
    else:
        html_converter = Markdown()
        content = html_converter.convert(content)
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "content": content
    })


def new(request):
    if request.method != "POST":
        return render(request, "encyclopedia/new.html")
    
    title = request.POST.get("title").strip()
    content = request.POST.get("content").strip()
    if title.lower() in [entry.lower() for entry in util.list_entries()]:
        return_code = 1
    else:
        util.save_entry(title, content)
        return_code = 0
    return render(request, "encyclopedia/new.html", {
        "title": title,
        "content": content,
        "return_code": return_code
    })

def edit(request, title):
    if request.method != "POST":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
    content = request.POST.get("content").strip()
    util.save_entry(title, content)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content,
        "return_code": 0
    })

def random(request):
    list_entries = util.list_entries()
    page_id = randint(0, len(list_entries)-1)
    return wiki_page(request, list_entries[page_id])
