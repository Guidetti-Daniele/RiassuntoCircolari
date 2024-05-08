from app.Parameters import parameters
from app.Server import app

parameters.init("/app/parameters/parameters.json")
parameters.connection_string = "/app/database/db.sqlite"

if __name__ == "__main__":
    app.run()
