# Seltel Backend

Standalone FastAPI REST API for the Seltel e-commerce platform. Deployable to any Python-compatible server.

## Requirements

- Python 3.12+
- MongoDB 7+

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGO_USERNAME` | MongoDB username | `""` |
| `MONGO_PASSWORD` | MongoDB password | `""` |
| `MONGO_DB_HOST` | MongoDB host | `mongo` |
| `MONGO_DB_PORT` | MongoDB port | `27017` |
| `MONGO_DB_NAME` | Database name | `seltel` |
| `SECRET_KEY` | JWT signing key | - |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry (minutes) | `30` |
| `CORS_ORIGINS` | Allowed CORS origins | `["http://localhost:5173"]` |
| `DEBUG` | Dev mode (enables Swagger) | `false` |

## Run

```bash
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

Production:

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000 --workers 4
```

API docs (when DEBUG=true): `http://localhost:8000/docs`

## Docker

```bash
docker build -t seltel-backend .
docker run -p 8000:8000 --env-file .env seltel-backend
```

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## API Endpoints

### Auth
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/auth/signup` | Register | No |
| POST | `/auth/login` | Login | No |
| GET | `/auth/me` | Current user | Yes |

### Products
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/api/v1/products/` | List products | No |
| GET | `/api/v1/products/{id}` | Get product | No |
| POST | `/api/v1/products/` | Create product | No |
| PUT | `/api/v1/products/{id}` | Update product | No |
| DELETE | `/api/v1/products/{id}` | Delete product | No |

### Health
| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/info` | App info |

## Project Structure

```
seltel-backend/
├── src/
│   ├── app.py              # FastAPI app factory
│   ├── main.py             # Entry point
│   ├── config/settings.py  # Pydantic Settings
│   ├── database/           # MongoDB connection
│   ├── models/             # Pydantic models
│   ├── auth/               # JWT authentication
│   ├── routers/            # API routes
│   └── middlewares/         # CORS middleware
├── tests/                  # pytest tests
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── ruff.toml
├── .env.example
└── .gitignore
```
