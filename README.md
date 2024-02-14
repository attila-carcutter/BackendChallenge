# Car Cutter - Backend Challenge

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Task

### As a backend developer you get the task to implement an API route using Python

... which accepts json data from our customers and store certain parts of it to the filesystem.</br>
Since this is a pretty simple task, we want you to think of best practices, edge cases and good software engineering.

Please fork our repo and implement the challenge in `src/core/challenge_api.py`.

Customers will post some json data to this api route, and we want to store each `Vehicle` in the `Vehicle-List` to a single file.
This file should be stored to a folder named like the `user_id` and the filename should be the `id` with a ".json" extension.

Once you are done, just create a pull request to `base:develop`. Please leave a comment what you think about the task and how long it took you to finish.


### Setup
To get started, install the following system level dependencies:
- [`python3.7`](https://www.python.org/downloads/)
- [`direnv`](https://direnv.net/) for managing the development environment
- [`poetry`](https://python-poetry.org/) for package manager


After the dependencies are installed, all you need to do is entering the project with your terminal,
and running `direnv allow` (see https://direnv.net/).


### Running the development server
```bash
cli api-server vehicle-features
```

By default, the API is now reachable at `http://127.0.0.1:8080/backend/` </br>
Our customers will post json files to the route `/challenge`.
We provide a [json schema](https://github.com/carcutter/BackendChallenge/blob/develop/json/vehicle-features.v1.schema.json) and an [example](
    https://github.com/carcutter/BackendChallenge/blob/develop/json/vehicle-features.v1.example.json).

Expect our customers to post their data with different approaches like:
```bash
curl --location --request POST 'http://localhost:8080/backend/challenge' \
  --header "Content-Type: application/json" \
  --data @json/vehicle-features.v1.example.json
```
or
```bash
curl --request POST 'http://localhost:8080/backend/challenge' \
  --header "Content-Type: application/json" \
  --form data=@json/vehicle-features.v1.example.json
```
