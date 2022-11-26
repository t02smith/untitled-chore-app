import os
from dotenv import load_dotenv

load_dotenv()

# ? run the application using the test database
TEST_MODE = True

config = {
    "resource_uri": os.getenv("TEST_COSMOS_RESOURCE_URI")
    if TEST_MODE
    else os.getenv("COSMOS_RESOURCE_URI"),
    "primary_key": os.getenv("TEST_COSMOS_RESOURCE_PRIMARY_KEY")
    if TEST_MODE
    else os.getenv("COSMOS_RESOURCE_PRIMARY_KEY"),
    "database": os.getenv("TEST_COSMOS_DATABASE_NAME")
    if TEST_MODE
    else os.getenv("COSMOS_DATABASE_NAME"),
}
