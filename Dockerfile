FROM ubuntu:16.04

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y git wget

# Install pandoc
RUN wget https://github.com/jgm/pandoc/releases/download/1.18/pandoc-1.18-1-amd64.deb
RUN dpkg --install pandoc-1.18-1-amd64.deb

# Install pandoc-sitenote
RUN wget https://github.com/schollz/pandoc-sidenote/releases/download/v1.0/pandoc-sidenote
RUN chmod +x pandoc-sidenote
RUN mv pandoc-sidenote /usr/local/bin

# Install book
RUN apt-get install -y python3 python3-pip
RUN git clone https://github.com/schollz/book.git
WORKDIR book
RUN python3 -m pip install maya toml
