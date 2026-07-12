from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from database import client
from bson.objectid import ObjectId
import markdown


public = APIRouter()
template = Jinja2Templates(directory="templates")

@public.get("/", response_class=HTMLResponse)
async def home(request: Request):
    #Fetching data from atlasDB
    hero_data = client.portfolio.hero.find_one({})
    services_cursor = client.portfolio.services.find({})
    projects = client.portfolio.projects.find({})
    blogs = client.portfolio.blog.find({})

    services_data = []
    for service in services_cursor:
        services_data.append({
            "name": service["name"],
            "description": service["description"],
            "deliverables": service["deliverables"],
            "id": str(service["_id"])
        })

    # Handles project cursor
    project_data = []
    for project in projects:
        project_data.append({
            "title": project["title"],
            "problem":project["problem"],
            "solution":project["solution"],
            "learning": project["learnings"],
            "technology":project["technologies"],
            "github":project["github_link"]
        })

    #Handles blog cursor
    blog_data = []
    for blog in blogs:
        blog_data.append({
            "date": blog["date"],
            "title":blog["title"],
            "summary":blog["summary"],
            "about":blog["about"],
            "id": blog["_id"]
        })

    return template.TemplateResponse(request=request, 
                                     name="public/index.html", 
                                     context={
                                         "hero_data":hero_data,
                                         "services_data": services_data,
                                         "project_data": project_data,
                                         "blog_data": blog_data
                                              })


#Handle blog article page
@public.get("/blog/{post_id}", response_class=HTMLResponse)
async def blog_post(request: Request, post_id: str):
    
    #fetching the article from atlasDB
    article = client.portfolio.blog.find_one({"_id": ObjectId(post_id)})

    #converting markdown to html string
    markdown_string = article["content"]
    html_string = markdown.markdown(markdown_string)

    return template.TemplateResponse(request=request, 
                                     name= "public/blog-article.html", 
                                     context={
                                         "article":article,
                                         "html_string": html_string
                                     })

#Blog cards function
@public.get("/blog", response_class=HTMLResponse)
async def blog_card(request: Request):

    print("I am running")

    #Fetching the blog data from AtlasDB
    blogs = client.portfolio.blog.find({})

    #Handles blog cursor
    blog_data = []
    for blog in blogs:
        blog_data.append({
            "date": blog["date"],
            "title":blog["title"],
            "summary":blog["summary"],
            "about":blog["about"],
            "id": blog["_id"]
        })

    return template.TemplateResponse(request=request, 
                                     name= "public/blog.html", 
                                     context={
                                        "blog_data": blog_data
                                     })

#Project cards route
@public.get("/projects", response_class=HTMLResponse)
async def project_cards(request: Request):

    print("I am running")

    #Fetching the blog data from AtlasDB
    projects = client.portfolio.projects.find({})

    #Handles blog cursor
    project_data = []
    for project in projects:
        project_data.append({
            "title":project["title"],
            "problem":project["problem"],
            "learnings":project["learnings"],
            "solution": project["solution"],
            "technologies": project["technologies"],
            "github_link": project["github_link"]
        })

    return template.TemplateResponse(request=request, 
                                     name= "public/projects.html", 
                                     context={
                                        "project_data": project_data
                                     }
                                     )
    