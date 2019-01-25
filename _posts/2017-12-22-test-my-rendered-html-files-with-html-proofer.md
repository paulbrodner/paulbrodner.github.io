---
layout: post
title: Test my rendered html files with 'html-proofer'
date: 2017-12-22 11:56 +0200
categories: [Tips & Tricks]
tags: [ruby, CI]
---
Now that I defined my [static website](https://github.com/paulbrodner/paulbrodner.github.io), I need a way to test any changes that I will do in future.
Here are the [high level requirements](https://github.com/paulbrodner/paulbrodner.github.io/issues/8) that I want to cover:
![Test My Blog](/images/posts/test-my-blog.png)

After a little research I found out that
[html-proofer](https://github.com/gjtorikian/html-proofer) is doing a good job so far.

### Configuring
* I'm using Gemfiles to manage my gems, so:
```ruby
gem 'html-proofer', '~> 3.0', '>= 3.0.5'
```

* Using Jekyll as framework my generated files are saved under `_sites` folder, so this command will actually run `htmlproofer` over my files, ignoring some predefined urls, hashtags or return code:
```ruby
$ bundle exec htmlproofer ./_site  --url-ignore '/#blog/,/paulbrodner.github.io/,/fb.me/' --http-status-ignore 999
```

* After each commit, I want to automatically test my changes, so I've added [Travis](https://travis-ci.org) as my Continous Integration system.

```ruby
language: ruby
rvm:
- 2.4.1

# I am using using bundler, therefore
# the `install` step will run `bundle install` by default.
script:
- bundle exec jekyll build
- bundle exec htmlproofer ./_site --disable-external --url-ignore '/#blog'


# branch whitelist, only for GitHub Pages
branches:
  only:
  - master
  
env:
  global:
  - NOKOGIRI_USE_SYSTEM_LIBRARIES=true # speeds up installation of html-proofer

sudo: false # route your build to the container-based infrastructure for a faster build

```
In `scripts` section above, I first build my static website which is saved into "_sites" folder then I call htmlproofer on it to do his magic.

{% include idea.html content="The entire source-code can be found on <a href='https://github.com/paulbrodner/paulbrodner.github.io/pull/10'>#10</a> merge-request" %}


Checkout also the current status in Travis: 
[![Build Status](https://travis-ci.org/paulbrodner/paulbrodner.github.io.svg?branch=master)](https://travis-ci.org/paulbrodner/paulbrodner.github.io)
