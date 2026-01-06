# Resolution Tracker

This is a simple web app made with flask to intake user input to a postgres
database and render data of user's choice.

I built this because I wanted an easy way to log and view my progress towards
my New Year's resolutions in 2026.

# How do use this:
1. Clone this repository and run `docker build -t resolutionpy .` to build the docker container.
2. Edit the `dotenv_template` to fill in the env variables and save it as `.env`.
3. Run `docker compose up [-d]` To launch the containers. (-d to detach the stdout from terminal).

NOTE: this service is running without a WSGI, and I did not build this with any security in mind. You probably shouldn't connect your instance of the service to the internet.
