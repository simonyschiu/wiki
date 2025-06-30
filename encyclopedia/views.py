from django.shortcuts import render

# Create your views here.
from . import util
from markdown2 import Markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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
