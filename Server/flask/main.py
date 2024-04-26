import os
from app.Parameters import parameters
from app.Server import app

parameters.init(os.getenv("PARAMETERS_PATH", "parameters/parameters.json"))
parameters.connection_string = os.getenv("DB_PATH", "database/database.db")

if __name__ == "__main__":
    app.run()
