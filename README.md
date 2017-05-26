# markdown2tufte

A static site generator for generating a Tufte-like website from markdown files.

This is a dead-simple, < 200LOC that leverages some nice Pandoc tools for creating a really nice looking website from markdown files.

## Quickstart (Docker)

```
docker pull schollz/markdown2tufte
wget https://raw.githubusercontent.com/schollz/markdown2tufte/master/examples/markdown2tufte.toml
nano markdown2tufte.toml # specify your directory/files
docker run -it -v `pwd`:/data markdown2tufte /bin/bash -c "cd /data && markdown2tufte && useradd $USER && chown -R $USER:$USER public/"
```

## Requirements


### Install `pandoc` version 1.18

```
wget https://github.com/jgm/pandoc/releases/download/1.18/pandoc-1.18-1-amd64.deb
dpgk --install pandoc-1.18-1-amd64.deb
```

### Install `pandoc-sidenote`

```
wget https://github.com/schollz/pandoc-sidenote/releases/download/v1.0/pandoc-sidenote
chmod +x pandoc-sidenote
sudo mv pandoc-sidenote /usr/local/bin
```

Follow [these instructions](https://github.com/jez/pandoc-sidenote) if you don't want to run this binary.

### Install `imagemagick`

```
apt-get install imagemagick
```

### Install `markdown2tufte`

```
pip install markdown2tufte
```

## Setup

Create a file `markdown2tufte.toml` with the data about your site. [Copy the example](https://github.com/schollz/markdown2tufte/blob/master/examples/markdown2tufte.toml) and suite it to what you need.

## Run 

Just run

```
markdown2tufte 
```

and now you have a static site in the `public/` folder with your website.

## Acknowledgements

This would not exist without:

- [pandoc-sidenote by jez](https://github.com/jez/pandoc-sidenote)
- [tufte-pandoc-css by jez](https://github.com/jez/tufte-pandoc-css)
- [pandoc](http://pandoc.org/)
