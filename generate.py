#!/usr/bin/python3
import os
import glob
import shutil
from datetime import datetime
import random
import string

import maya
import toml


def process_chapter_file(chapter_filename):
    chapter = {}
    chapter_content = open(chapter_filename, 'rb').read().decode('utf-8')
    front_matter, markdown_content = chapter_content.split("---", maxsplit=1)
    chapter = toml.loads(front_matter)
    if 'slug' not in chapter:
        chapter['slug'] = os.path.basename(chapter_filename).split(".")[0]
    if chapter['slug'][0] == "/":
        chapter['slug'] = chapter['slug'][1:]
    chapter['date_created_rfc3339'] = maya.parse(
        chapter['date_created']).rfc3339()
    chapter['python_date'] = datetime.strptime(
        chapter['date_created_rfc3339'], '%Y-%m-%dT%H:%M:%S.%fZ')
    chapter['date_created'] = chapter['python_date'].strftime('%b %d %y')
    chapter['markdown'] = markdown_content
    return chapter


def markdown_to_html(mdown):
    t = {'tempfile': ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(10))}
    with open('%(tempfile)s.md' % t, 'w') as f:
        f.write(mdown)
    command = 'pandoc --katex --smart --section-divs --from markdown+tex_math_single_backslash --filter pandoc-sidenote --to html5 --template=tufte --css /assets/tufte.css --css /assets/pandoc.css --css /assets/pandoc-solarized.css --css /assets/tufte-extra.css --output %(tempfile)s.html %(tempfile)s.md' % t
    print(command)
    os.system(command)
    processed_html = open('%(tempfile)s.html' % t, 'r').read()
    os.remove('%(tempfile)s.html' % t)
    os.remove('%(tempfile)s.md' % t)
    return processed_html

if not os.path.isdir("public"):
    os.mkdir("public")
if os.path.isdir("public/assets"):
    shutil.rmtree("public/assets")
shutil.copytree('assets', 'public/assets')


chapter_filenames = glob.glob("chapters/*.md")
chapters = []
for chapter_filename in chapter_filenames:
    chapter = process_chapter_file(chapter_filename)
    chapters.append((chapter['python_date'], chapter))

for sorted_chapter in sorted(chapters, key=lambda tup: tup[0], reverse=True):
    chapter = sorted_chapter[1]
    slug_path = os.path.join("public", chapter['slug'])
    if not os.path.isdir(slug_path):
        print("Making", slug_path)
        os.makedirs(slug_path)
    with open(os.path.join(slug_path, "index.html"), "w") as f:
        f.write(markdown_to_html(chapter['markdown']))

# Generate index
index_markdown = ""
index_markdown += "# Title\n\n"
index_markdown += "## Byline\n\n"
last_date = ""
for i, t in enumerate(sorted(chapters, key=lambda tup: tup[0], reverse=False)):
    t[1]['date'] = last_date
    index_markdown += "\n\n<i>%(date)s</i>\t<h2>[%(title)s](%(slug)s)</h2>" % t[
        1]
    last_date = t[1]['date_created']
index_markdown += "\n\n<i>%s</i>\t<h2>&nbsp;</h2>" % last_date
with open(os.path.join("public", "index.html"), "w") as f:
    f.write(markdown_to_html(index_markdown))
