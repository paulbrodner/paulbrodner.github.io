.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

build: ## Build the Docker image
	docker build -t pbrodner-site .

run: ## Run the Docker container
	docker run -v ${PWD}:/site -it -p 4000:4000 pbrodner-site

post: ## Create a new blog post
	@echo "What is the name of this new post?"
	@read post_name; \
	docker run -v ${PWD}:/site -it pbrodner-site bundle exec jekyll post "$$post_name"; \
	echo "\ncategories: [Tips & Tricks]\ntags: [tag1, tag2]\ncomments: false\nexcerpt: INTRODUCTION"
