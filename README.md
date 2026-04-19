# discord-api-template

This is a clean and minimal Python REST API template built with [FastAPI](https://fastapi.tiangolo.com/) and [Uvicorn](https://www.uvicorn.org/). It is designed to be used as a starting point for Discord companion API services, standalone HTTP backends that Discord bots call over the network instead of bundling heavy dependencies locally.

## Features

* FastAPI with automatic OpenAPI documentation at `/docs`.
* Bearer token authentication shared across all protected endpoints.
* A `GET /health` endpoint for uptime monitoring.
* Configuration via environment variables using `pydantic-settings`. No values are hardcoded.
* Structured JSON logging with a configurable log level.
* `pyproject.toml` with the `hatchling` build backend and pinned dependency ranges.
* `Dockerfile` and `docker-compose.yml` for containerized deployment.
* A test suite with `pytest` covering health, auth rejection, and a template endpoint.

## Prerequisites

* [Docker](https://docs.docker.com/get-docker/) and Docker Compose for containerized setup.

Running without Docker requires Python 3.12 or newer.

## Setup

Copy the environment template and fill in the required values:

```bash
cp .env.example .env
```

Then start the service:

```bash
docker-compose up --build
```

The API listens on port `8000` by default.

To run without Docker:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
uvicorn api_template.main:app --reload
```

## Configuration

All configuration is read from environment variables or from a `.env` file in the project root.

| Variable | Required | Default | Description |
|---|---|---|---|
| `DISCORD_API_SECRET` | Yes | — | Shared bearer token. Callers must send this value in the `Authorization` header. |
| `LOG_LEVEL` | No | `INFO` | Log verbosity. Accepts standard Python logging levels. |

## Project structure

```
discord-api-template/
├── src/api_template/
│   ├── main.py         # FastAPI application, lifespan, and route definitions.
│   ├── config.py       # Environment variable reader via pydantic-settings.
│   ├── auth.py         # Bearer token dependency used to protect endpoints.
│   └── models.py       # Pydantic request and response models.
├── tests/
│   └── test_api.py     # Health check and auth tests.
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── .env.example
```

## Creating a new API from this template

Use the GitHub template button to create a new repository based on this project. Then follow these steps to customize it:

1. **Rename the package.** In `pyproject.toml`, change the project `name` and the `packages` path under `[tool.hatch.build.targets.wheel]`. Rename the `src/api_template/` directory to match (e.g. `src/media_api/`). Update the import paths in all source files and in `Dockerfile`.

2. **Add your dependencies.** Edit the `dependencies` list in `pyproject.toml`.

3. **Add configuration variables.** Extend the `Settings` class in `config.py` and document new variables in `.env.example`.

4. **Add startup and shutdown logic.** Use the `lifespan` context manager in `main.py` to load models, open connections, or perform any one-time initialisation.

5. **Add endpoints.** Define new routes in `main.py`. Use `dependencies=[Depends(require_auth)]` to protect them. Add request and response models to `models.py`.

6. **Remove the template endpoint.** Delete the `/template/echo` route and the `TemplateRequest`/`TemplateResponse` models once you have your own routes in place.

7. **Update the `docker-compose.yml` port.** Change `8000:8000` to the port assigned to your service.

8. **Write tests.** Add test functions to `tests/test_api.py`.

## Running tests

```bash
pip install -e ".[dev]"
pytest
```

## Calling protected endpoints

All endpoints except `/health` require a bearer token in the `Authorization` header:

```http
POST /template/echo HTTP/1.1
Authorization: Bearer your-secret-here
Content-Type: application/json

{"text": "hello"}
```

Discord bots calling this API should use `httpx.AsyncClient` with the token set as a default header:

```python
import httpx

client = httpx.AsyncClient(
    base_url="http://localhost:8000",
    headers={"Authorization": "Bearer your-secret-here"},
)
```

## Related services

The following APIs were built from this template and can serve as fuller implementation examples.

| Service | Description |
|---|---|
| [discord-api-media](https://github.com/Lempki/discord-api-media) | Resolves YouTube and SoundCloud track metadata and stream URLs. |
| [discord-api-scraper](https://github.com/Lempki/discord-api-scraper) | Scrapes structured data from external websites. |
| [discord-api-scheduler](https://github.com/Lempki/discord-api-scheduler) | Schedules persistent reminders delivered via Discord webhooks. |
| [discord-api-morshu](https://github.com/Lempki/discord-api-morshu) | Generates Morshu TTS audio and video from text. |

