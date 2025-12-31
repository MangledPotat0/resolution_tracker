docker run --rm -it -v ${PWD}:/app/workdir `
	   -p 5001:5000 `
	   -e PYTHONPATH=/app/workdir `
	   --name flask `
	   python-work
