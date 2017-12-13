desc "sever jekyl in development mode"
task :start do     
    sh 'bundle exec jekyll serve'
end

desc "test"
task :test do     
    sh 'script/cibuild'
end

task :default => [:start]