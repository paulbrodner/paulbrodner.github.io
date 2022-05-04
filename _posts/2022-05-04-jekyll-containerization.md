---
layout: post
title: Jekyll Containerization
date: 2022-05-04 12:42 +0000
categories: [Tips & Tricks]
tags: [docker]
comments: false
excerpt: How to test my Jekyll blog in Docker
---
After a couple of months, I've started to update again my blog, but at this time (on windows) I got a lot of problems installing, configuring ruby smoothly.

### The Challenge
Easily configure and run my blog on any device without a pain

**Features:**
* I should be able to create a new blog post and update it on my OS
* the blog will run in Docker container and render the updated page as I type

### The Solution
* a) Create a custom Docker image that will have all prerequisites installed
  * all gems are collected from `requirements.txt`
  * at the end the same rake command that we use from command line is called to build and start the blog

```docker
FROM ruby:3.1.2-slim-buster as builder
WORKDIR /site
COPY Gemfile .
RUN apt-get update && \
    apt-get install -y build-essential && \
    bundle config build.ffi --enable-system-libffi && \
    bundle install

EXPOSE 4000

CMD [ "rake", "build", "start"]
```

* b) building the image

```shell
$ docker build -t pbrodner-site .
```

* c) running the "development" image and use current folder as a shared volume - so updates from HOST OS can be rendered successfully

```shell
docker run -v $(pwd):/site -it -p 4000:4000 pbrodner-site
```