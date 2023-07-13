# Backend

## Getting started

```bash
# Create venv
python3 -m venv venv
# Activate venv
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```

## Running the server

```bash
export FLASK_APP="api.server:create_app()"
flask run
```

The swagger UI can be accessed at `http://127.0.0.1:5000/api/v1/ui/`
