# local modules

# Get the application instance
import config

connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yaml")

if __name__ == "__main__":
    connex_app.run(debug=True, host="0.0.0.0", port=5001)
