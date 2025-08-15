from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(5000))
    is_complete = db.Column(db.Boolean)

@app.route('/')
def index():
    blog_list = Blog.query.all()

    return render_template("index.html", blog_list=blog_list)

@app.route('/create_new_post')
def create_new_post():
    return render_template("create_new_post.html")

@app.route('/add_blog')
def add_blog():
    title = request.args.get('title')
    title = "New Blog" if title == "" else title
    content = request.args.get('content')
    print(f"{content=} | {title=}")
    new_blog = Blog(title=title, content=content)
    db.session.add(new_blog)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit_template/<int:blog_id>')
def edit_template(blog_id):
    return render_template("edit.html", blog_id=blog_id)

@app.route('/edit/<int:blog_id>')
def edit(blog_id):
    title = request.args.get('title')
    title = "New Blog" if title == "" else title
    content = request.args.get('content')
    selected_blog = Blog.query.filter_by(id=blog_id).first()
    selected_blog.title = title
    selected_blog.content = content
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:blog_id>')
def delete(blog_id):
    selected_blog = Blog.query.filter_by(id=blog_id).first()
    db.session.delete(selected_blog)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()