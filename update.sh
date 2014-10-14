#!/bin/bash
rsync -av --delete --exclude-from localfiles.txt --exclude-from .gitignore ../atlas/code/ .
