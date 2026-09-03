desc "start blog locally"
task :start do     
    sh 'bundle exec jekyll serve --force_polling -H 0.0.0.0 -P 4000'
end

desc "build"
task :build do     
    sh "bundle exec jekyll build"
end

desc "test"
task :test do
    sh "bundle exec jekyll build"
    # `/paulbrodner.github.io/` used to sit in --url-ignore, which meant every
    # absolute self-link was skipped and internal links were never validated at
    # all. --url-swap rewrites them back to _site so they are checked locally.
    # Both origins are swapped: the .github.io one still appears in older post
    # bodies, and 301s to the .dev domain.
    # --assume-extension: `permalink: /profile` builds profile.html, so links to
    #   /profile are only resolvable because the server guesses the extension.
    sh "bundle exec htmlproofer ./_site " \
       "--url-ignore '/#blog/,/fb.me/' " \
       "--url-swap 'https\\://paulbrodner.dev:,https\\://paulbrodner.github.io:' " \
       "--assume-extension " \
       "--empty-alt-ignore " \
       "--disable-external " \
       "--http-status-ignore 999"
end

desc "seo regression suite"
task :seo do
    sh "bundle exec jekyll build"
    sh "pytest tests/test_seo.py -v"
end

desc 'new post'
task :post do
    puts "What is the name of this new post?"
    post = STDIN.gets.chomp
    sh "bundle exec jekyll post #{post}"
    puts "
categories: [Tips & Tricks]
tags: [tag1, tag2]
comments: false
excerpt: INTRODUCTION"
end


task :default => [:start]