# markdown2tufte

A static site generator for generating a Tufte-like website from markdown files.

This is a dead-simple, < 200LOC that leverages some nice Pandoc tools for creating a really nice looking website from markdown files.

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
pip install markdown2tufte
```

## Setup

Create a file `markdown2tufte.toml` with the data about your site. [Copy the example](https://github.com/schollz/markdown2tufte/blob/master/examples/markdown2tufte.toml) and suite it to what you need.

## Run 

```
markdown2tufte 
```

Now you have a static site in the `public/` folder with your website.

## Acknowledgements

This would not exist without:

- [pandoc-sidenote by jez](https://github.com/jez/pandoc-sidenote)
- [tufte-pandoc-css by jez](https://github.com/jez/tufte-pandoc-css)
- [pandoc](http://pandoc.org/)
