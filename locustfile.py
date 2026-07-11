from locust import HttpUser, task, between

class PortfolioUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def visit_home(self):
        self.client.get("/")

    @task(1)
    def visit_dashboard(self):
        self.client.get("/dashboard")

    @task(1)
    def visit_projects(self):
        self.client.get("/projects")

    @task(1)
    def visit_metrics(self):
        self.client.get("/metrics")