import glob

import mistune
from jinja2 import Template
from htmlmin.minify import html_minify


if __name__ == "__main__":

    with open("blog.tmp.html") as blog_tmp:
        tmp = Template(blog_tmp.read())

    build = {}
    posts = []

    for post in glob.glob("posts/*.md"):

        name = post.split("/")[-1].split(".")[0]
        page_name = f"./{name.lower().replace(' ', '_')}.html"
        posts.append((page_name, name))

        with open(post) as blog_md:
            content = blog_md.read()

        build[page_name] = (post, name, content)

    for page_name, (post, name, content) in build.items():
        with open(post) as blog_md, open(f"build/{page_name}", "w") as blog_html:

            blog_html.write(
                html_minify(
                    tmp.render(
                        title=name,
                        header=name,
                        body=mistune.markdown(content, escape=False),
                        posts=posts,
                    )
                )
            )
    with open("Index.md") as index_md, open("build/index.html", "w") as index_html:
        index_html.write(
            html_minify(
                tmp.render(
                    title="Home",
                    header="Welcome",
                    body=mistune.markdown(index_md.read()),
                    posts=posts,
                )
            )
        )
