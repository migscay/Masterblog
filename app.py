from flask import Flask, render_template, request, redirect, url_for, request, session
import os.path, json
from storage_json import StorageJson

app = Flask(__name__)
app.secret_key = "secret_key"

"""
read and load into session, existing blog posts
"""
# create file if not existing
if not os.path.isfile('blogs.json'):
    with open('blogs.json', "w") as blogs_json:
        pass

blog_posts = []
last_record_id = 0
blogs = StorageJson("blogs.json")

blog_posts = blogs.read_posts()


@app.route('/')
def index():
    # if blog posts have not yet been loaded
    if "blog_posts" not in session:

        last_record_id = blog_posts[len(blog_posts) - 1]['id']
        session["last_record_id"] = last_record_id
        session["blog_posts"] = blog_posts

    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        last_record_id = session["last_record_id"]
        blog_posts = session["blog_posts"]

        new_blog = {}
        last_record_id += 1
        new_blog['id'] = last_record_id
        new_blog['author'] = request.form['author']
        new_blog['title'] = request.form['title']
        new_blog['content'] = request.form['content']

        blog_posts.append(new_blog)

        #write blog posts to json file
        blogs.write_posts(blog_posts)

        #save in sessionblog_posts
        session["last_record_id"] = last_record_id
        session["blog_posts"] = blog_posts

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete():

    if request.method == 'POST':

        # retrieve in session
        blog_posts = session["blog_posts"]
        for post in blog_posts:
            post_to_be_deleted = next(post for post in blog_posts if post["id"] == int(request.args.get('id')))
        try:
            blog_posts.remove()
            last_record_id = blog_posts[len(blog_posts) - 1]['id']

            # write blog posts to json file
            blogs.write_posts(blogpost_to_be_deleted_posts)

            # save in sessionblog_posts
            session["last_record_id"] = last_record_id
            session["blog_posts"] = blog_posts
            return redirect(url_for('index'))
        except KeyError:
            print(f"Post {post_to_be_deleted} doesn't exist!")


    record_id = int(request.args.get('id'))
    blog_posts = session["blog_posts"]
    post_to_be_deleted = {}
    for post in blog_posts:
        post_to_be_deleted = next(post for post in blog_posts if post["id"] == record_id)

    return render_template('delete.html')


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        # retrieve in session
        blog_posts = session["blog_posts"]
        post_id_to_be_updated = int(request.args.get("id"))
        try:
            for post in blog_posts:
                print(f"post id {type(post['id'])}, form id {type(request.form['author'])}")
                if post["id"] == post_id_to_be_updated:
                    post["author"] = request.form["author"]
                    post["title"] = request.form["title"]
                    post["content"] = request.form["content"]

            # write blog posts to json file
            with open("blogs.json", "w") as blogs_json:
                json.dump(blog_posts, blogs_json)

            # save in sessionblog_posts
            session["blog_posts"] = blog_posts
        except KeyError:
            print(f"Something went wrong in updating the post!")

        return redirect(url_for('index'))

    record_id = int(request.args.get('id'))
    blog_posts = session["blog_posts"]
    post_to_be_updated = {}
    for post in blog_posts:
        post_to_be_updated = next(post for post in blog_posts if post["id"] == record_id)

    #print(post_to_be_deleted["author"])
    #print(post_to_be_deleted["title"])
    #print(post_to_be_deleted["content"])

    #save in session
    session["post_to_be_updated"] = post_to_be_updated

    return render_template('update.html')


if __name__ == '__main__':
    app.run()