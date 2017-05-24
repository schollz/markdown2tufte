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

### Install Python requirements

```
pip install -r requirements.txt
```

## Setup

Make some markdown files and put them in `chapters/`.

The top of the markdown should have some TOML data, e.g.

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
python generate.py
```
