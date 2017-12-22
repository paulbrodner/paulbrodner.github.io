---
layout: post
title: Test my rendered html files with 'html-proofer'
date: 2017-12-22 11:56 +0200
categories: [Tips & Tricks]
tags: [Ruby, CI]
---
[html-proofer](https://github.com/gjtorikian/html-proofer) seems to do a good job so far, testing [my static website](https://github.com/paulbrodner/paulbrodner.github.io). 

* I'm using Gemfiles to manage my gems, so:
```ruby
gem 'html-proofer', '~> 3.0', '>= 3.0.5' #added in Gemfile
```

* Using Jekyll as framework my generated files are saved under `_sites` folder, so this command will actually run `htmlproofer` over my files disabling external link checks and ingnoring #blog hashtag that is failing in Travis:
```ruby
$ bundle exec htmlproofer ./_site --disable-external --url-ignore '/#blog'
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
In `scripts` section I build my static website into "_sites" folder then I call htmlproofer on it to do his magic.

{% include idea.html content="The entire source-code can be found on <a href='https://github.com/paulbrodner/paulbrodner.github.io/pull/10'>#10</a> merge-request" %}
![Test My Blog](/images/posts/test-my-blog.png)

Checkout also the current status in Travis: 
[![Build Status](https://travis-ci.org/paulbrodner/paulbrodner.github.io.svg?branch=master)](https://travis-ci.org/paulbrodner/paulbrodner.github.io)
