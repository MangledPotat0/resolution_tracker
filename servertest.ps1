docker run --rm -it -v ${PWD}:/app/workdir `
	   -p 5001:5000 `
	   -e PYTHONPATH=/app/workdir `
	   --env-file .env `
	   --network=pg-network `
	   --name flask `
	   python-work
