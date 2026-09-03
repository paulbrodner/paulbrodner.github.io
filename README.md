# paulbrodner.github.io
My Personal Blog https://paulbrodner.dev


[![verify](https://github.com/paulbrodner/paulbrodner.github.io/actions/workflows/verify.yml/badge.svg)](https://github.com/paulbrodner/paulbrodner.github.io/actions/workflows/verify.yml)  ![visitors](https://visitor-badge.laobi.icu/badge?page_id=paulbrodner.github.io)


# run everithing in Docker
* build the image
```shell
docker build -t pbrodner-site .
```

* run the image
> this will have a shared volume from host to container, so we can update the site automatically

```
docker run -v ${PWD}:/site -it -p 4000:4000 pbrodner-site
```
* view site under: http://127.0.0.1:4000