#!/bin/bash

docker run --rm -it -v ${PWD}:/app/workdir \
	   -e PYTHONPATH=/app/workdir \
	   --env-file .env \
	   --network=pg-network \
	   --name flask \
	   -p 5002:5001 \
	   resolutionpy /bin/bash

