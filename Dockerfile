FROM ubuntu:latest
LABEL authors="Jammer"

ENTRYPOINT ["top", "-b"]