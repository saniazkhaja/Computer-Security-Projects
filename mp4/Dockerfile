FROM ubuntu:18.04

# Update the package index and install necessary packages
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk wget unzip && \
    rm -rf /var/lib/apt/lists/*

# Download and install apktool
RUN wget https://github.com/iBotPeaches/Apktool/releases/download/v2.6.0/apktool_2.6.0.jar -O /usr/local/bin/apktool.jar && \
    echo '#!/bin/sh' >> /usr/local/bin/apktool && \
    echo 'java -jar /usr/local/bin/apktool.jar "$@"' >> /usr/local/bin/apktool && \
    chmod +x /usr/local/bin/apktool

# Set environment variables
ENV PATH="/usr/local/bin:${PATH}"

ADD cp1_feature_extract .

WORKDIR /mp4_apks

RUN apktool d 49875A9C25EB18945A8E7F27C8188834CFF48070413604D477763EC7A20E9C4A.apk && \
    apktool d 5E06B7510B55B52C94D2AB0D7BB94AAA454860C6F8729BA2842438D92CDB8EEE.apk