---
layout: post
title: SQLite and NodeJS for storing Test Metadata
date: 2022-05-06 08:27 +0000
categories: [Tutorials]
tags: [notejs, sqlite]
comments: false
excerpt: Simple REST API with NodeJS that will store/retrieve data to/from SQLiteDB
---

I like to keep track of the test environments that I'm using, what code is deployed there, from what branch, the git SHA, the date when the environment what created/updated and so on.

We can take this information from CI or other tools but sometimes these doesn't provide all the necessary information.

# The Project
I would like to have a simple REST API that will digest some information that I send to them and store it a database.
>If you want to see the code, check this out: [api_node_template](https://github.com/paulbrodner/api_node_template)

#### Functionalities:
* 1) REST API with CRUD capabilities -> simple as it gets
* 2) can store data to a database
* 3) can display data into a simple dashboard
* 4) containerized so I can deploy it somewhere
  * and small


##### **1) REST API with CRUD capabilities**
> I've chosen NodeJS with Express for my minimalist REST-API experience

First I've created a `package.json` and then I've `npm install` the dependencies.
```javascript
{
  "name": "soul",
  "version": "1.0.0",
  "description": "List test environments",
  "main": "app.js",
  "scripts": {
    "start": "node app.js",
    "test": "echo \"Error: no test specified\"",
    "lint": "eslint ."
  },
  "author": "Paul Brodner",
  "license": "ISC",
  "dependencies": {
    "body-parser": "^1.19.1",
    "express": "^4.17.2",
    "pug": "^3.0.2",
    "sqlite3": "^4.2.0"
  }
}
```
To simplify things, I've created one [app.js](https://github.com/paulbrodner/api_node_template/blob/master/app.js) to handle all my REST functionalities in one place. (this can be enhanced further more)

##### **2) can store data to a database**
For database I will go with [SQLite](https://www.sqlite.org/index.html) because it is fast, self-contained and high-reliable.

When the application is started, the database schema is created (see [app.js](https://github.com/paulbrodner/api_node_template/blob/master/app.js))

##### **3) can display data into a simple dashboard**
For simple HTML dashboard I've chosen a robust, elegant, feature rich template engine called [pug](https://pugjs.org/api/getting-started.html) 

Using pug, I can create the layout and the dashboard page with ease. See [views](https://github.com/paulbrodner/api_node_template/tree/master/views) folder and for CSS, the well-known [Bootstrap](https://getbootstrap.com/)

##### **4) containerized so I can deploy it somewhere**
Yeah, Docker all the way, keeping in mind that the final image should be small. 
For this I've used multi-stage build with docker.

```dockerfile
# ---- Base Node ----
FROM alpine:3.5 AS base
RUN apk add --no-cache nodejs-current tini
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /home/appuser/app
RUN chmod -R 777 /home/appuser/app
ENTRYPOINT ["/sbin/tini", "--"]
COPY package.json .

# ---- Dependencies ----
FROM base AS dependencies
RUN npm set progress=false && npm config set depth 0
RUN npm install --only=production
RUN cp -R node_modules prod_node_modules
RUN npm install

# ---- Release ----
FROM base AS release
COPY --from=dependencies /home/appuser/app/prod_node_modules ./node_modules
COPY . .
EXPOSE 8000
USER appuser
CMD npm run start
```
* I start from a small alpine image that I'm calling `base` (I know, I've used alpine, but it's good for this show project)
* dependencies are installed in a new layer that will inherit `base` image 
* and the final image the `release` stage will use the previous layers to finalize the task.

At the end the size of this image is around: 53MB

```ruby
$ docker images | grep paulbrodner
paulbrodner/environments  latest   d9614f03498e   56 minutes ago      53.4MB
```





