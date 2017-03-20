FROM python:3.5.2
MAINTAINER Yohei Kikuta <diracdiego@gmail.com>

RUN pip3 install jupyter \
    feedparser \
    --upgrade google-cloud
