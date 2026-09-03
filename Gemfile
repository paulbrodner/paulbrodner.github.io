source 'https://rubygems.org'
gem 'github-pages'
gem 'jekyll-compose', group: [:jekyll_plugins]
gem 'html-proofer', '~> 3.0', '>= 3.0.5'
gem "webrick", "~> 1.7"
# Declared explicitly: `bundle exec rake` fails in CI otherwise. Ruby ships rake
# as a default gem, so it resolves locally, but a strict bundle refuses to run
# any executable that is not in the Gemfile.
gem "rake"