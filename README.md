# paulbrodner.github.io
My Personal Blog https://paulbrodner.github.io


[![Build Status](https://travis-ci.org/paulbrodner/paulbrodner.github.io.svg?branch=master)](https://travis-ci.org/paulbrodner/paulbrodner.github.io)  ![visitors](https://visitor-badge.laobi.icu/badge?page_id=paulbrodner.github.io)


# run everithing in Docker
* build the image
```shell
docker build -t pbrodner-site .
```

* run the image
> this will have a shared volume from host to container, so we can update the site automatically

```
docker run -v $(pwd):/site -it -p 4000:4000 pbrodner-site bash
```
* view site under: http://127.0.0.1:4000