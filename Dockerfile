FROM ubuntu:latest
LABEL authors="stonechen"

ENTRYPOINT ["top", "-b"]