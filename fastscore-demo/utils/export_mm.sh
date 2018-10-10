#!/bin/bash
docker run -i --rm -v fastscore_db-data:/volume busybox sh -c 'cd /volume && tar -cOvzf - . ' > mysql/db-data-volume-export.tgz
