#!/bin/sh

key="$(python keygen.py)"
sed "s/\"REPLACE WITH MASTER KEY\"/$key/" exile.py > build.py
pyinstaller -n exile --clean -F build.py
rm -r build.py build exile.spec
