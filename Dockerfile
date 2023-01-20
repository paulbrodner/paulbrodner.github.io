FROM ruby:3.1.2-slim-buster as builder
WORKDIR /site
COPY Gemfile .
RUN apt-get update && \
    apt-get install -y build-essential && \
    bundle config build.ffi --enable-system-libffi

RUN cat Gemfile && bundle install

EXPOSE 4000

CMD [ "rake", "build", "start"]