#!/bin/bash

# install deb package
cat << EOS | sed -e '/^#/d' | xargs sudo apt install -y

# system
git
python3-pip

# app
ffmpeg

# opencv
libatlas3-base
libavcodec57
libavformat57
libgstreamermm-1.0-1
libilmbase12
libjasper1
libopenexr22
libqt4-test
libqtgui4
libswscale4
libtiff5
libwebp6

EOS

# install python library
pip3 install -r requirements.txt
