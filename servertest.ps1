docker run --rm -it -v ${PWD}:/app/workdir `
	   -e PYTHONPATH=/app/workdir `
	   --env-file .env `
	   --network=pg-network `
	   --name flask `
	   -p 5001:5001 `
	   resolutionpy /bin/bash
