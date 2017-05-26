# encoding=utf8
import sys
import os
import glob
import shutil
from datetime import datetime
import random
import string
import argparse

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


def markdown_to_html(mdown, baseurl):
    t = {'baseurl': baseurl, 'tempfile': ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(10))}
    with open('%(tempfile)s.md' % t, 'w') as f:
        f.write(mdown)
    command = 'pandoc --ascii --katex --smart --section-divs --from markdown --filter pandoc-sidenote --to html5 --template=tufte --css %(baseurl)s/assets/tufte.css --css %(baseurl)s/assets/pandoc.css --css %(baseurl)s/assets/pandoc-solarized.css --css %(baseurl)s/assets/tufte-extra.css --output %(tempfile)s.html %(tempfile)s.md' % t
    print(command)
    os.system(command)
    processed_html = open('%(tempfile)s.html' %
                          t, 'rt', encoding='latin1').read()
    os.remove('%(tempfile)s.html' % t)
    os.remove('%(tempfile)s.md' % t)
    # Modify image links
    processed_html = processed_html.replace(
        'img src="', 'img src="%s/assets/img/' % baseurl)
    return processed_html


def run(config_file):
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

    config = toml.load(open(config_file, 'r'))

    this_dir, this_filename = os.path.split(__file__)

    if not os.path.isdir("public"):
        os.mkdir("public")
    if os.path.isdir("public/assets"):
        shutil.rmtree("public/assets")
    shutil.copytree(os.path.join(this_dir, 'assets'), 'public/assets')
    if not os.path.isdir("public/assets/img"):
        os.mkdir("public/assets/img")
    if not os.path.isfile('tufte.html5'):
        shutil.copyfile(os.path.join(this_dir, 'tufte.html5'), 'tufte.html5')

    if config['images'] != '':
        image_files = os.listdir(config['images'])
        for f in image_files:
            shutil.copyfile(os.path.join(config['images'], f), os.path.join(
                "public", "assets", "img", os.path.basename(f)))

    # Pre-processing of the posts
    for i, post in enumerate(config['post']):
        # Process slug
        if 'slug' not in post:
            post['slug'] = post['filename'].split('.')[0].replace(' ', '-')
        if post['slug'][0] == '/':
            post['slug'] = post['slug'][1:]
        if post['slug'][-1] == '/':
            post['slug'] = post['slug'][:-1]
        slug_path = os.path.join("public", post['slug'])
        if not os.path.isdir(slug_path):
            print("Making", slug_path)
            os.makedirs(slug_path)
        post['baseurl'] = config['baseurl']

    index_markdown = ""
    index_markdown += "# %s\n\n" % config['title']
    index_markdown += "## %s\n\n" % config['subtitle']
    current_subtitle = ""
    for i, post in enumerate(config['post']):
        current_subtitle, post['subtitle'] = post['subtitle'], current_subtitle
        index_markdown += "\n\n<i>%(subtitle)s</i><h2>[%(title)s](%(baseurl)s/%(slug)s/)</h2>" % post

        markdown_content = open(os.path.join(
            config['files'], post['filename']), 'r').read()
        pagination = "### Keep reading...\n\n"
        if i > 0:
            pagination += '&#x21AB;&nbsp;“<i><a href="%(baseurl)s/%(slug)s/">%(title)s</a></i>”' % (
                config['post'][i - 1])
        pagination += "&nbsp;&nbsp;&nbsp;<a href='/'>Home</a>&nbsp;&nbsp;&nbsp;"
        if i < len(config['post']) - 1:
            pagination += '“<i><a href="%(baseurl)s/%(slug)s/">%(title)s</a></i>”&nbsp;&#x21AC;' % (
                config['post'][i + 1])
        markdown_content += "\n\n" + pagination.strip()
        with open(os.path.join(os.path.join("public", post["slug"]), "index.html"), "w") as f:
            f.write(markdown_to_html(markdown_content, config['baseurl']))

    index_markdown += "\n\n<i>%s</i><h2>&nbsp;</h2>" % current_subtitle
    with open(os.path.join("public", "index.html"), "wt", encoding='latin1') as f:
        f.write(markdown_to_html(index_markdown, config['baseurl']))
    os.remove('tufte.html5')

    # Resize images
    os.chdir("public/assets/img")
    os.system("mogrify -filter Triangle -define filter:support=2 -dither None -posterize 136 -quality 60 -define jpeg:fancy-upsampling=off -define png:compression-filter=5 -define png:compression-level=9 -define png:compression-strategy=1 -define png:exclude-chunk=all -interlace none -resize 800x600\> *")
    os.chdir("../../../")


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--config',  help='config file to use')

    args = parser.parse_args()
    if args.config == None:
        if os.path.isfile('markdown2tufte.toml'):
            args.config = 'markdown2tufte.toml'
        else:
            print("Must specify config file")
            return
    run(args.config)

if __name__ == "__main__":
    run('config.toml')
