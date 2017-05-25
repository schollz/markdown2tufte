# encoding=utf8
import sys
import os
import glob
import shutil
from datetime import datetime
import random
import string
import argparse

import maya
import toml


def which(program):
    """Determines whether program exists
    """
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    raise


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
    command = 'pandoc --ascii --katex --smart --section-divs --from markdown --filter pandoc-sidenote --to html5 --template=tufte --css /assets/tufte.css --css /assets/pandoc.css --css /assets/pandoc-solarized.css --css /assets/tufte-extra.css --output %(tempfile)s.html %(tempfile)s.md' % t
    print(command)
    os.system(command)
    processed_html = open('%(tempfile)s.html' %
                          t, 'rt', encoding='latin1').read()
    os.remove('%(tempfile)s.html' % t)
    os.remove('%(tempfile)s.md' % t)
    return processed_html


def run(files, images):
    try:
        pandoc = which("pandoc")
    except:
        print("""pandoc not found, install with 
        
wget https://github.com/jgm/pandoc/releases/download/1.18/pandoc-1.18-1-amd64.deb
dpgk --install pandoc-1.18-1-amd64.deb
""")
        return

    try:
        pandoc = which("pandoc-sidenote")
    except:
        print("""pandoc-sidenote not found, install with 
        
wget https://github.com/schollz/pandoc-sidenote/releases/download/v1.0/pandoc-sidenote
chmod +x pandoc-sidenote
sudo mv pandoc-sidenote /usr/local/bin
""")
        return

    this_dir, this_filename = os.path.split(__file__)

    if not os.path.isdir("public"):
        os.mkdir("public")
    if os.path.isdir("public/assets"):
        shutil.rmtree("public/assets")
    shutil.copytree(os.path.join(this_dir, 'assets'), 'public/assets')
    if not os.path.isdir("public/assets/img"):
        os.mkdir("public/assets/img")
    shutil.copyfile(os.path.join(this_dir, 'tufte.html5'), 'tufte.html5')

    if images != '' and images != None:
        image_files = os.listdir(images)
        for f in image_files:
            shutil.copyfile(os.path.join(images,f), os.path.join("public","assets","img",os.path.basename(f)))


    chapter_filenames = glob.glob(os.path.join(files, "*.md"))
    chapters = []
    for chapter_filename in chapter_filenames:
        chapter = process_chapter_file(chapter_filename)
        chapters.append((chapter['python_date'], chapter))

    sorted_chapters = list(sorted(chapters, key=lambda tup: tup[0], reverse=False))
    for i, sorted_chapter in enumerate(sorted_chapters):
        chapter = sorted_chapter[1]
        slug_path = os.path.join("public", chapter['slug'])
        if not os.path.isdir(slug_path):
            print("Making", slug_path)
            os.makedirs(slug_path)
        markdown_content = chapter['markdown']
        pagination = "### Keep reading...\n\n"
        if i > 0:
            pagination += '&#x21AB;&nbsp;“<i><a href="/%(slug)s/">%(title)s</a></i>”' % sorted_chapters[i-1][1]             
        pagination += "&nbsp;&nbsp;&nbsp;<a href='/'>Home</a>&nbsp;&nbsp;&nbsp;"
        if i < len(chapters)-1:
            pagination += '“<i><a href="/%(slug)s/">%(title)s</a></i>”&nbsp;&#x21AC;' % sorted_chapters[i+1][1] 
        markdown_content += "\n\n" + pagination.strip()
        with open(os.path.join(slug_path, "index.html"), "w") as f:
            f.write(markdown_to_html(markdown_content))

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
    with open(os.path.join("public", "index.html"), "wt", encoding='latin1') as f:
        f.write(markdown_to_html(index_markdown))
    os.remove('tufte.html5')

    # Resize images
    os.chdir("public/assets/img")
    os.system("mogrify -filter Triangle -define filter:support=2 -dither None -posterize 136 -quality 75 -define jpeg:fancy-upsampling=off -define png:compression-filter=5 -define png:compression-level=9 -define png:compression-strategy=1 -define png:exclude-chunk=all -interlace none -resize 450x337\> *")
    os.chdir("../../../")


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--files',  help='folder to files')
    parser.add_argument('--images', help='folder to the images')

    args = parser.parse_args()
    if args.files == None:
        print("Must specify where markdown files are, with\n\n--files location/to/markdown/files")
    run(args.files, args.images)
