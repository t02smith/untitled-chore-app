# Untitled Chore App

## Info

Run the application and head to [http://localhost/docs](http://localhost/docs)

- [FastAPI docs](https://fastapi.tiangolo.com/)
- [Poetry Basic Usage](https://python-poetry.org/docs/basic-usage/)

## Installation (for testing)

1. Download the [Cosmos DB emulator](https://learn.microsoft.com/en-us/azure/cosmos-db/local-emulator-release-notes)
2. Setup containers called `chores`, `homes`, `timetables`, and `users`
3. Upload the default chore list in [./data/default_chores.json](./data/default_chores.json) to the chores container
4. Follow the run instructions below 

## How to run

### Poetry

> You need Poetry for this. [Download from here.](https://python-poetry.org/docs/#installation)

```bash
# installs the dependencies - does not reinstall poetry
poetry install

# activates the venv (JARET DO THIS STEP)
poetry shell

# runs the python app 
# PYTHON not POETRY
python main.py
```

### Venv

```bash
# creates new virtual environment
python -m venv .venv

# actives that venv
./.venv/Scripts/activate

# downloads all the dependencies
pip install -r requirements.txt

# runs the python app
python main.py
```

### Docker

IGNORE THIS

> You need Docker for this. [Download from here.](https://www.docker.com/)\
> *For deployment*

```bash
docker build -t untitled-chore-app .
docker run -p 80:80 untitled-chore-app
```

## Deployment

To deploy just follow [this tutorial](https://docs.docker.com/cloud/aci-integration/)

```bash
docker context create aci untitled-chore-api
docker --context untitled-chore-api run -p 80:80 nginx
```

## Testing

To test run:

```bash
poetry run pytest ./tests

# or
poetry shell
pytest ./tests
```
