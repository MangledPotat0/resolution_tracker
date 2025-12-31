docker run --rm -it `
	--name testdb `
	-e POSTGRES_DB=testdb `
	-e POSTGRES_USER=testuser `
	-e POSTGRES_PASSWORD=testpass `
	--network=pg-network `
	-p 5432:5432 `
	postgres:latest
