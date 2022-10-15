# Installation

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP="api.server:create_app()"
flask run
```
Use `flask run --host=0.0.0.0 --port=5001` on the server.

The swagger UI should be at `http://127.0.0.1:5000/api/v1/ui/`