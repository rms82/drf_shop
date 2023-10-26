from locust import task , HttpUser

class QuickstartUser(HttpUser):
    
    @task
    def product_list(self):
        self.client.get("/shop/product/")

    @task
    def category_list(self):
        self.client.get("/shop/category/")

    @task
    def post_list(self):
        self.client.get("/blog/post/")

    @task
    def blog_category_list(self):
        self.client.get("/blog/blog_category/")
        