from django.http import response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import markdown
import urllib
import random

from . import util
from django.urls import reverse


def index(request):
    if request.method == "POST" : # if user search something
        search_key = request.POST['q']
        if search_key in util.list_entries():
            return HttpResponseRedirect(f"wiki/{search_key}")
        return search_result(request, search_key)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    markdown_file = util.get_entry(title)
    if markdown_file == None :
        markdown_file = util.get_entry(title.capitalize()) # try capitalize title then search
        if markdown_file == None: 
            return HttpResponse(f"No results found for {title}")
    md = markdown.Markdown(extensions=['pymdownx.emoji']) # allow markdown emojis translate to html file
    html_file = md.convert(markdown_file)

    return render(request, "encyclopedia/entry_page.html", {
        'html_file' : html_file
    })
    
    
def search_result(request, search_key):
    entries = []
    for entry in util.list_entries() :
        if entry.lower().find(search_key.lower()) != -1 :
            entries.append(entry)
    return render(request, "encyclopedia/search_result.html", {
        'entries_found' : entries, 'search_key' : search_key,
    })

def create_new_page(request) :
    if request.method == "POST":
        title = request.POST['title']
        if title in util.list_entries() and request.POST['isUpdate'] == "":
            return render(request,"encyclopedia/createnewpage.html", {
                'message': f"page {title} is already exist." 
            })
        content = request.POST['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(f"wiki/{title}")
    # case you want to create new page
    return render(request, "encyclopedia/createnewpage.html")

def edit_page(request) :
    title = request.META['HTTP_REFERER']
    res = str.rsplit(title, '/')[-1]
    for title in util.list_entries():
        if res == urllib.parse.quote(title) :
            isUpdate = True;
            content = util.get_entry(title)
            return render(request, "encyclopedia/createnewpage.html", {
                'title': title, 'content': content, 'isUpdate': isUpdate
            })
    return HttpResponseRedirect(reverse("create_new_page"))

def random_page(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(f"wiki/{title}")