## Custom Compiler

Made with Vue.js, Python, Flask and Docker.

## Setup with Docker

Running this project with Docker simplifies the setup process, as Docker containers handle all the dependencies and
environment configurations. To get started, you will need to have Docker installed on your machine.

## Requirements:

- Docker: Follow the official Docker installation guide for your operating system https://www.docker.com/.

### Building the Docker Image

To build the Docker image for this project, navigate to the project's root directory in your terminal and run:

    docker build -t my-compiler .

This command builds a Docker image named my-compiler based on the instructions in the Dockerfile. It includes the
backend
server, the compiler, and the built frontend.

### Running the Project

After building the image, you can run the project with:

    docker run -p 5000:5000 my-compiler

This command starts a container from the my-compiler image. It maps port 5000 of the container to port 5000 on your host
machine, allowing you to access the application via http://localhost:5000.

## Accessing the Application

With the Docker container running, you can access:

- The web frontend at: http://localhost:5000
- The API endpoints directly via their paths (e.g., http://localhost:5000/api/compile)

## Running Compiler Commands (Optional)

If you need to run specific compiler commands within the Docker container, you can execute commands within the running
container using Docker's exec command. For example:

    docker run -it --entrypoint /bin/bash my-compiler

You can navigate to /app/compiler and run the compiler commands from there. Running tests manually:

    poetry run pytest

Run the compiler on a source code file (include the source code file before build command, in the compiler directory):

    python3 main.py COMMAND path/to/source/code

where `COMMAND` may be one of these:

    interpret
    TODO: add more
