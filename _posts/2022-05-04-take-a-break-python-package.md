---
layout: post
title: Take-a-Break python package
date: 2022-05-04 15:09 +0000
categories: [Tips & Tricks]
tags: [docker]
comments: true
excerpt: Experiment with python packages, setup and released to community
---

> In 2020 I've started a lot to work with python, so it was the time to create and release a python package in the wild.

### Why
I wanted to learn how I can build a python package, how I can test it and release it to community under [test package](https://test.pypi.org/) first then to [official repository](https://pypi.org/ )

Besides that I wanted to experiment with [tkinter](https://docs.python.org/3/library/tkinter.html) the standard Python interface to the Tcl/Tk GUI toolkit.

### How
As first step I've started to look into [Packaging Projects tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/) to build a generic minimal structure and understand how thigs work.

Then I've started to create a [Makefile](https://www.gnu.org/software/make/manual/make.html) to group tasks that I can run multiple times like: building, install dev dependencies, testing, deploying to public repo, cleaning up afterwards.

Next step was to actual implement the code (details bellow)

## What
The end solution will be an executable python package that will tell me when to **take a break** :), with the following features:
* I can execute it from command line
* I can configure after how many minutes/hours should I take the break
    * add a GUI just for fun - how this works
* The notification will be:
    * a random [joke](http://api.icndb.com/jokes/random ) from
    * a random image taken from [unsplash](https://source.unsplash.com/random) that will be displayed in a full screen form
* when I press ESC the image will disappear
* the application will run in the background    
    
## The end results:
* clone the [source code](https://github.com/paulbrodner/take-a-break)

```shell
$ git clone https://github.com/paulbrodner/take-a-break
```

* install it

```shell
$ pip install .
```

* run it

```shell
$ python -m take_a_break
No one has ever pair-programmed with Chuck Norris and lived to tell about it.
```

This is the full screen image that will show a random image
![](/images/posts/take_a_break.png)
It has also a the joke displayed at the bottom and also some menus to access the settings dialog:

![](/images/posts/take_a_break-settings.png)
Here I can update the link to the url resource and also the reminder alert

