from django.shortcuts import render, redirect
from . import util
from markdown2 import markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import randint

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,name):
    content = util.get_entry(name) 
    if content is not None:
        return render(request, "encyclopedia/display.html", {
            "entries": markdown(content), "title":name
        })
    else:
        return render(request,"encyclopedia/page_not.html")

def search(request):
    entries = util.list_entries()
    query = request.GET.get("q", "")
    if query in entries:
        return HttpResponseRedirect(f'{query}')
    results = [entry for entry in entries if query.lower() in entry.lower()]
    if results:
        return render(request, "encyclopedia/search.html", {
            "entries": results,
        })
    else:
        return render(request,"encyclopedia/page_not.html"         
        )

def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if util.get_entry(title) is None:
            util.save_entry(title, content)
            return HttpResponseRedirect(f'{title}')
        else:
            return render(request, "encyclopedia/page_not.html")
    return render(request, "encyclopedia/Create.html")

def edit(request, name):
    if request.method == "POST":
        title = name
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect(entry, title)
    return render(request, "encyclopedia/edit.html",{
        "title":name, "content":util.get_entry(name)
    })

def random(request):
    list1 = util.list_entries()
    t1=randint(0,len(list1)-1)
    return redirect(entry,list1[t1]) 



