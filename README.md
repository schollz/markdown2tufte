# book

This is a dead-simple, < 200 line count, really nice looking website for stories / chapters.

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

### Install 

```
pip install tuftebook
```

## Setup

Make some markdown files and put them in some folder, e.g. `examples/chapters/`.

The top of the markdown should have some TOML data:

```
title = "Title that will be shown on index"
date_created = "November 1 2016"
draft = false
slug = "optional-custom-slug"

---

# My stuff starts here
```

## Run 

```
tuftebook --files examples/chapter --images examples/images
```

Now you have a static site in the `public/` folder with your website.

## Acknowledgements

This would not exist without:

- [pandoc-sidenote by jez](https://github.com/jez/pandoc-sidenote)
- [tufte-pandoc-css by jez](https://github.com/jez/tufte-pandoc-css)
- [pandoc](http://pandoc.org/)
