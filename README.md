# Node TODO Challenge
Challenge solution. Jesús Gil (jgilnom)

# Requirements and Steps:
- Define API_URL env variable with the following value needed by the console cli:
  *http://127.0.0.1:3000*
  Of course we could miss and hard-code this variable in the python code, but to allow customization in real hypothetical environments and to hide the real API URL from the code.

- If not installed, install tabulate with pip:
  *pip install tabulate*

- Run docker-commpose up in the root folder of the repository

- Run todo-cli-apis.py with Python passing the different options supported and arguments needed. Some examples:
  todo-cli-apis.py test
  todo-cli-apis.py create --description dummy_item
  todo-cli-apis.py delete --description dummy_item
  todo-cli-apis.py get_all --format json

# Security
To increase security, the different connection strings, urls and passwords were moved to ENV VARIABLES in the following files:
- database.js
- todo-cli-apis.py

In order to make it easy to run and out-of-the-box solution, the following ENV variables were included in the docker-compose.yml but of course, in a real environment these variables would be readed from some Secrets Manager and mapped into the container in run-time using external-secrets in example:
- MONGO_INITDB_ROOT_USERNAME
- MONGO_INITDB_ROOT_PASSWORD
- MONGODB_URI

# CI/CD
The repository includes 3 Github Workflows to:
- Docker Build-Push the docker image to DockerHub in case that consuming from other real environment is needed
- Python Validate the console cli
- Node NPM validate and test