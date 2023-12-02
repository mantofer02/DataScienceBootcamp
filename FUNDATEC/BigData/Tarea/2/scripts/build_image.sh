#!/bin/bash

# Stop and remove the existing container with the same name
docker stop bigdata_container && docker rm bigdata_container

# Build the Docker image
docker build --tag bigdata .

# Run the Docker container
docker run -p 8888:8888 -i -t --name bigdata_container bigdata /bin/bash
