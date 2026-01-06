# Resolution Tracker

This is a simple web app made with flask to intake user input to a postgres
database and render data of user's choice.

I built this because I wanted an easy way to log and view my progress towards
my New Year's resolutions in 2026.

# How do use this:
1. Clone this repository and run `docker build -t resolutionpy .` to build the docker container.
2. Edit the `dotenv_template` to fill in the env variables and save it as `.env`.
3. Run `docker compose up [-d]` To launch the containers. (-d to detach the stdout from terminal).

# Some Notes:
- This service is running without a WSGI, and I did not build this with any security in mind. You probably shouldn't connect your instance of the service to the internet.
- There will be more features added to this and some of them may break existing features. I am going to do my best to not need to change the database schema.
- I've never used html beyond simple hello world static sites, and I've never touched htmx at all before, so they're probably not in the best shape.

# TODO:
- Finish writing tests so that future extensions to projects can actually progress in test driven approach
- Flask routing in `app/routes/` has a lot of redundant stuff that can be cleaned up nicely
- Flask routing in `app/routes` have no module and function docstrings because I was rewriting them completely too many times
- I broke the activity logs update function at some point and just noticed it AFTER compiling a new Dockerfile so I am going to make that a later problem to fix.
- I am realizing `activity_type` interface and workflow needs units displayed. Never show quantities without units!!!!
