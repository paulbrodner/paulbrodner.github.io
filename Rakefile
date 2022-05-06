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
    sh "bundle exec htmlproofer ./_site  --url-ignore '/#blog/,/paulbrodner.github.io/,/fb.me/' --http-status-ignore 999"
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