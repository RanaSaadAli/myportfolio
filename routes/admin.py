from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from database import client
from bson.objectid import ObjectId
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import os
from itsdangerous import Signer

admin = APIRouter()
template = Jinja2Templates(directory="templates")

load_dotenv()
password = os.getenv("admin_password")
secret_key = os.getenv("secret_key")
s = Signer(secret_key)

def is_authenticated(request: Request):
    cookie = request.cookies.get("session")
    try:
        s.unsign(cookie)
        return True
    except Exception as e:
        return False

# route to get login-page
@admin.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return template.TemplateResponse(request=request, name="admin/login.html")

# route to handle post request of login page
@admin.post("/login")
async def verify_user(request: Request):
    user_password = await request.form()
    user_pass = user_password["password"]
    if user_pass == password:
        signed = s.sign("authenticated").decode("utf-8")
        response = RedirectResponse(url="/admin/dashboard", status_code=303)
        response.set_cookie(key="session", value=signed)
        return response
    return RedirectResponse(url="/admin/login", status_code=303)

# Route to admin dashboard panel
@admin.get("/dashboard", response_class=HTMLResponse)
async def admin_panel(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    return template.TemplateResponse(request=request, name="admin/dashboard.html")

# manage-blog Route
@admin.get("/manage-blog", response_class=HTMLResponse)
async def manage_blog(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    blogs = client.portfolio.blog.find({})
    blog_data = []
    for blog in blogs:
        blog_data.append({
            "date": blog["date"],
            "title": blog["title"],
            "summary": blog["summary"],
            "about": blog["about"],
            "id": str(blog["_id"])
        })
    return template.TemplateResponse(request=request, name="admin/manage-blog.html", context={"blog_data": blog_data})

# route to handle post request of manage-blog.html
@admin.post("/manage-blog")
async def update_blog_post(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    form = await request.form()
    formdict = dict(form)
    client.portfolio.blog.insert_one(formdict)
    return RedirectResponse(url="/admin/manage-blog", status_code=303)

# Get Edit blogs articles
@admin.get("/blog/edit/{post_id}", response_class=HTMLResponse)
async def edit_blog(request: Request, post_id: str):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    single_blog_data = client.portfolio.blog.find_one({"_id": ObjectId(post_id)})
    single_blog_data["id"] = str(single_blog_data["_id"])
    return template.TemplateResponse(request=request, name="admin/edit-blog.html", context={"post": single_blog_data})

# Post Edit blog post route
@admin.post("/blog/edit/{post_id}")
async def update_blog(request: Request, post_id: str):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    form = await request.form()
    formdict = dict(form)
    client.portfolio.blog.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": formdict}
    )
    return RedirectResponse(url="/admin/manage-blog", status_code=303)

# Delete blog post route
@admin.get("/blog/delete/{post_id}")
async def delete_blog(request: Request, post_id: str):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    client.portfolio.blog.delete_one({"_id": ObjectId(post_id)})
    return RedirectResponse(url="/admin/manage-blog", status_code=303)

# Manage-projects route
@admin.get("/manage-projects", response_class=HTMLResponse)
async def manage_projects(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    projects = client.portfolio.projects.find({})
    project_data = []
    for project in projects:
        project_data.append({
            "title": project["title"],
            "problem": project["problem"],
            "solution": project["solution"],
            "learning": project["learnings"],
            "technology": project["technologies"],
            "github": project["github_link"],
            "id": str(project["_id"])
        })
    return template.TemplateResponse(request=request, name="admin/manage-projects.html", context={"project_data": project_data})

# route to handle project post request
@admin.post("/manage-projects")
async def add_project(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    form = await request.form()
    formdict = dict(form)
    client.portfolio.projects.insert_one(formdict)
    return RedirectResponse(url="/admin/manage-projects", status_code=303)

# Edit project post route
@admin.get("/project/edit/{post_id}", response_class=HTMLResponse)
async def get_project(request: Request, post_id: str):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    single_project_data = client.portfolio.projects.find_one({"_id": ObjectId(post_id)})
    single_project_data["id"] = str(single_project_data["_id"])
    return template.TemplateResponse(request=request, name="admin/edit-project.html", context={"post": single_project_data})

# Route to post edited data to mongoDB
@admin.post("/project/edit/{post_id}")
async def post_updated_project(request: Request, post_id: str):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    form = await request.form()
    formdict = dict(form)
    client.portfolio.projects.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": formdict}
    )
    return RedirectResponse(url="/admin/manage-projects", status_code=303)

# Delete project post route
@admin.get("/project/delete/{post_id}")
async def delete_project(request: Request, post_id: str):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    client.portfolio.projects.delete_one({"_id": ObjectId(post_id)})
    return RedirectResponse(url="/admin/manage-projects", status_code=303)

# route to display hero page
@admin.get("/hero", response_class=HTMLResponse)
async def hero_editing(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    hero = client.portfolio.hero.find_one({})
    return template.TemplateResponse(request=request, name="admin/manage-hero.html", context={"hero": hero})

# route to post hero data
@admin.post("/manage-hero")
async def post_hero_data(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    form = await request.form()
    formdict = dict(form)
    client.portfolio.hero.update_one({}, {"$set": formdict})
    return RedirectResponse(url="/admin/hero", status_code=303)

# route to get manage-services page
@admin.get("/services", response_class=HTMLResponse)
async def services(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    services = client.portfolio.services.find({})
    services_data = []
    for service in services:
        services_data.append({
            "name": service["name"],
            "description": service["description"],
            "deliverables": service["deliverables"],
            "id": str(service["_id"])
        })
    return template.TemplateResponse(request=request, name="admin/manage-services.html", context={"services_data": services_data})

# route to handle post request of services
@admin.post("/services")
async def post_service(request: Request):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    form = await request.form()
    formdict = dict(form)
    client.portfolio.services.insert_one(formdict)
    return RedirectResponse(url="/admin/services", status_code=303)

# route for edit-services.html page
@admin.get("/service/edit/{post_id}", response_class=HTMLResponse)
async def get_edit_services(request: Request, post_id: str):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    single_service = client.portfolio.services.find_one({"_id": ObjectId(post_id)})
    single_service["id"] = str(single_service["_id"])
    return template.TemplateResponse(request=request, name="admin/edit-services.html", context={"single_service": single_service})

# route to handle post request to edit services
@admin.post("/service/edit/{post_id}")
async def post_update_service(request: Request, post_id: str):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    form = await request.form()
    formdict = dict(form)
    client.portfolio.services.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": formdict}
    )
    return RedirectResponse(url="/admin/services", status_code=303)

# route to handle delete request for services
@admin.get("/service/delete/{post_id}")
async def delete_service(request: Request, post_id: str):
    if not is_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=303)
    client.portfolio.services.delete_one({"_id": ObjectId(post_id)})
    return RedirectResponse(url="/admin/services", status_code=303)


#============================== Logout-route===============================

@admin.get("/logout",response_class=HTMLResponse)
async def logout(request: Request):
    response = RedirectResponse(url="/admin/login")
    response.delete_cookie("session")
    return response