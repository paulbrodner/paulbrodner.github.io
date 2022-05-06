#!/usr/bin/env bash
docker run -v $(pwd):/site -it -p 4000:4000 pbrodner-site bash