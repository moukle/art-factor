# Backend for ArtFactor
## Usage
``` sh
pip install --user pipenv       # add pipenv to $PATH if not found
pipenv install                  # install required packages
pipenv run python server.py     # launch server
```

## API Usage
Launch server and visit [the servers swagger documentation](http://localhost:5000/api/ui/) for HTTP REST documentation.

## Requests
http://localhost:5000/api/fact

## Docker 
- switch into the project's `root` directory (i.e. ./artfactor)
- build the docker image

``` shell
docker build -t quiz .
```
- run the docker image


``` shell
docker run -it --network host quiz
```

- the server should now run under: http://192.168.99.100:5000/api/fact (otherwise: check `docker-machine ip`)

