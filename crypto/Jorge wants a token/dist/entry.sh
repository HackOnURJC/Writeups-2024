#!/bin/bash
docker build -t crypto-hard .
docker run -d -p 1337:1337 crypto-hard
