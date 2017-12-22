desc "start blog locally"
task :start do     
    sh 'bundle exec jekyll serve'
end

desc "test"
task :test do     
    sh "bundle exec jekyll build"
    sh "bundle exec htmlproofer ./_site  --url-ignore '/#blog/,/paulbrodner.github.io/,/fb.me/' --http-status-ignore 999"
end


namespace :drafts do 
    desc 'new draft'
    task :new do
        puts "What is the name of this new draft?"
        draft = STDIN.gets.chomp
        sh "bundle exec jekyll draft #{draft}"
    end

    desc 'list draft'
    task :list do
        puts "Available drafts:"
        Dir["./_drafts/**/*.md"].each do |draft|
            puts draft
        end
    end

    desc 'publish draft'
    task :publish do        
        sh 'rake drafts:list'
        puts "What draft ?"
        draft = STDIN.gets.chomp
        puts "What date ? (i.e 2017-12-25):"
        date = STDIN.gets.chomp
        if date.empty?
            sh "bundle exec jekyll publish #{draft}"
        else 
            "bundle exec jekyll publish #{draft} --date #{date}"
        end        
    end
end

desc 'new post'
task :post do
    puts "What is the name of this new post?"
    post = STDIN.gets.chomp
    sh "bundle exec jekyll post #{post}"
end


task :default => [:start]