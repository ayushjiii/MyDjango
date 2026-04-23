from django.http import HttpResponse
from django.shortcuts import render , redirect ,get_object_or_404
from datetime import date , datetime
import requests
from .models import Apod
from .forms import Note
from django.core.paginator import Paginator 
from django.contrib import messages
from django.db.models import Q

API_KEY = "KN1bITeMdqekbMBKy6UThFYkm4NouWNaxN3pzP1s"

def fetch_apod(date=None):
        
        try:
            
            if date :
                url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&date={date}"

            else :
                url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"
                
            response = requests.get(url,timeout = 30)
             
            if response.status_code != 200 :
                print(response.status_code)
                print(response.text)
                return None
            
            return response.json()
        
        except Exception as e:
            print("error",e)
            return None

 
def home(request) :
    
    apod_list = []

    selected_date = request.GET.get("date")
    
    if selected_date:
        apod_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    
    else:
        apod_date = date.today()
    
    print("Saving to DB:", apod_date)
        

    if Apod.objects.filter(date=apod_date).exists() :
            
        apod = Apod.objects.get(date=apod_date)
            
        url = apod.url
            
        if "youtu.be" in url :
            url = url.replace("youtu.be/","youtube.com/embed/")            
            
        elif "youtube" in url :
            url = url.replace("watch?v=","embed/")
            
        apod_list.append({
            "title" : apod.title,
            "explanation" : apod.explanation,
            "url" : url,
            "media_type" : apod.media_type})
        
    else :
        
        data = fetch_apod(selected_date)

        if data is None:
            
            apod_list.append ( {"title": "Failed to load",
            "explanation": "API error or rate limit",
            "url": "",
            "media_type": "image"
            } )

        else :
 
            url = data.get("url","")
                
            if "youtu.be" in url :
                url = url.replace("youtu.be/","youtube.com/embed/")            
                
            elif "youtube" in url :
                url = url.replace("watch?v=","embed/")  
                
            apod_list.append ( {"title" : data.get("title","title not found"),
                "explanation" : data.get("explanation","no explanation found"),
                "url" : url ,
                "media_type" : data.get("media_type")} )
            
            print("API DATA RECEIVED")
            
            Apod.objects.create(
                title = data.get("title"),
                explanation = data.get("explanation"),
                url = url,
                media_type = data.get("media_type"),
                date = apod_date
                )
            
    context = {"apod_list": apod_list,
               "today" : date.today().isoformat()}
    
    return render(request,"apod/index.html",context)
         

def history(request):
    
    query = request.GET.get("q","")
    
    queryset= Apod.objects.all()

    if query :
        queryset = queryset.filter(
        Q(title__icontains=query) | Q(explanation__icontains=query)
        ).exclude(
            media_type="video"
        )
    
    sort = request.GET.get("sort","newest")
    
    if sort == "oldest" :
        queryset = queryset.order_by("date")

    elif sort == "title" :
        queryset = queryset.order_by("title")

    elif sort == "title1" :
        queryset = queryset.order_by("-title")

    else :
        queryset = queryset.order_by("-date")
    
    
    paginator = Paginator(queryset, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj,
        "query" : query,
        "sort" : sort,
    }

    return render(request, "apod/history.html", context)


def detail(request,id):
    
    apod = get_object_or_404(Apod, id=id)
    
    if request.method == "POST" :
        form = Note(request.POST,instance=apod)
        
        if form.is_valid():
            form.save()
            messages.success(request,"Note Saved Successfully.")
            return redirect ("detail",id=apod.id)
        
    else :
        
        form = Note(instance=apod)
        
    context = {
        "apod" : apod,
        "form" : form,
    }
    
    return render(request,"apod/detail.html",context) 

def toggle_favourite(request, id):

    apod = get_object_or_404(Apod, id=id)

    apod.favourite = not apod.favourite
    apod.save()

    page = request.GET.get("page", 1)

    source = request.GET.get("source","favourites")

    if source == "favourites" :
        return redirect(f"/favourites/?page={page}")

    return redirect(f"/history/?page={page}")


def favourites(request) :

    queryset = Apod.objects.filter(favourite = True).order_by("-date")
    
    page_number = request.GET.get("page")
    
    paginator = Paginator(queryset,5)
    
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj" : page_obj
    }

    return render(request,"apod/history.html/", context)