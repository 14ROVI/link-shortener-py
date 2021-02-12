#!/bin/bash

docker build -t link_shortener ~/share/link_shortener/
docker stop link_shortener
docker rm link_shortener
docker run -d -p 9812:9812 --restart unless-stopped --name link_shortener link_shortener