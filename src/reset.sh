#!/bin/bash

if [ -f resources.db ]; then
    rm resources.db
fi
if [ -f ../log.txt ]; then
    rm ../log.txt
fi
if [ -d __pycache__ ]; then
    rm -r __pycache__
fi

python db.py