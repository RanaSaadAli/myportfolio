# Personal Portfolio Website

A dynamic portfolio website built with FastAPI and MongoDB, designed to showcase skills, projects, and services. Features a secure admin panel for managing all content without touching code.

## Why I Built This

I wanted a professional online presence where I could showcase my work, but I didn't want to edit HTML files every time I updated my content. So I built a custom admin panel that lets me manage everything — projects, services, hero section — directly through a web interface.

## Tech Stack

**Backend:** FastAPI, Python  
**Templating:** Jinja2  
**Database:** MongoDB Atlas  
**Containerization:** Docker, Docker Compose  
**CI/CD:** GitHub Actions  
**Monitoring:** Prometheus, Grafana  
**Orchestration:** Kubernetes (Minikube)  
**Registry:** Docker Hub  

## Features

**Public Portfolio:**
- Hero/intro section
- Services section showcasing offered services
- Projects section with proof of work
- Contact section

**Admin Panel:**
- Secure cookie-based authentication using HMAC signing
- Full CRUD operations for projects, services, and hero content
- No code changes required to update portfolio content

## DevOps Implementation

- **Docker** — fully containerized application with optimized multi-layer Dockerfile
- **CI/CD** — GitHub Actions pipeline automatically builds and pushes updated Docker image to Docker Hub on every push to main
- **Monitoring** — Prometheus scrapes application metrics, visualized through Grafana dashboards with request rate and response time tracking
- **Kubernetes** — deployed on local Minikube cluster with Deployment (2 replicas), Service for traffic routing, and Secrets for secure credential management

## Running Locally

Pull and run the image directly from Docker Hub:

```bash
docker pull saadali96/portfolio:latest
```

Create a `.env` file with the following variables:
secret_key=your_secret_key
uri=your_mongodb_connection_string
admin_password=your_admin_password
Then run:

```bash
docker run -p 8000:8000 --env-file .env saadali96/portfolio:latest
```

Visit `http://localhost:8000`

## Docker Hub

`saadali96/portfolio:latest`

## Author

Rana Saad Ali Khan  
[GitHub](https://github.com/RanaSaadAli) | [LinkedIn](www.linkedin.com/in/rana-saad-ali-khan) | [Docker Hub](https://hub.docker.com/repository/docker/saadali96/portfolio)