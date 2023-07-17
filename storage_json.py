import json

class StorageJson:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_posts(self):
        with open(self.file_path, "r") as blogs_json:
            return json.load(blogs_json)

    def write_posts(self, blog_posts):
        with open(self.file_path, "w") as blogs_json:
            json.dump(blog_posts, blogs_json)
