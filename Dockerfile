FROM ruby:3.1-slim-bookworm AS builder
WORKDIR /site

# Install system dependencies required for building native gems and Jekyll
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      git \
      libffi-dev \
      pkg-config && \
    rm -rf /var/lib/apt/lists/* && \
    bundle config build.ffi --enable-system-libffi

# Leverage Docker layer caching for bundler by copying Gem specification files first
COPY Gemfile Gemfile.lock* ./
RUN bundle install

# Expose the Jekyll server port
EXPOSE 4000

# Ensure gems are in sync with the mounted repo on container start, then build and start
CMD ["/bin/sh", "-lc", "bundle install && rake build start"]