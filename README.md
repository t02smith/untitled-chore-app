# Untitled Chore App

## Info

- [FastAPI docs](https://fastapi.tiangolo.com/)
- [Poetry Basic Usage](https://python-poetry.org/docs/basic-usage/)

## How to run

### Poetry

> You need Poetry for this. [Download from here.](https://python-poetry.org/docs/#installation)

```bash
poetry install
poetry shell
python main.py
```

### Docker

> You need Docker for this. [Download from here.](https://www.docker.com/)\
> *For deployment*

```bash
docker build -t untitled-chore-app .
docker run -p 80:80 untitled-chore-app
```

### Venv

```bash
python -m venv .venv
./.venv/Scripts/activate
pip install -r requirements.txt
python main.py
```
