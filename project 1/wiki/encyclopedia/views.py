from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import markdown
from . import util


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
    md = markdown.Markdown(extensions=['pymdownx.emoji'])
    html_file = md.convert(markdown_file)
    return HttpResponse(html_file)
    
def search_result(request, search_key):
    entries = []
    for entry in util.list_entries() :
        if entry.lower().find(search_key.lower()) != -1 :
            entries.append(entry)
    return render(request, "encyclopedia/search_result.html", {
        'entries_found' : entries, 'search_key' : search_key,
    })

def create_new_page(request) :
    if request.method == "POST" :
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })

    return render(request, "encyclopedia/createnewpage.html")