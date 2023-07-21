#!/bin/bash

if [ -f resources.db ]; then
    rm resources.db
fi
if [ -f log.txt ]; then
    rm log.txt
fi
if [ -f resources.sqlite ]; then
    rm resources.sqlite
fi
if [ -f state_obj.pickle ]; then
    rm state_obj.pickle
fi
if [ -d __pycache__ ]; then
    rm -r __pycache__
fi
