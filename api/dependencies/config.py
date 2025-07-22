from dotenv import load_dotenv
import os
load_dotenv()
class conf:
    db_host = "localhost"
    db_name = "sandwich_maker_api"
    db_port = 3306
    db_user = "root"
    db_password = os.getenv("SQL_PASSWORD")
    app_host = "localhost"
    app_port = 8000