# ----------------------------------------------------- Imports --------------------------------------------------------
import pymongo
import os
from dotenv import load_dotenv
# ------------------------------------------------ Global Variables ----------------------------------------------------
load_dotenv()
MongoDB_CLIENT = os.getenv('MongoDB_CLIENT')
# --------------------------------------------------- Main Class -------------------------------------------------------
class CricketDatabase:
    def __init__(self):
        if MongoDB_CLIENT is None:
            raise ValueError("MongoDB_CLIENT environment variable is not set")
        self.the_client = pymongo.MongoClient(MongoDB_CLIENT)

# ------------------------------------------------ Connect Database ----------------------------------------------------
    def connect(self):
        try:
            mocs_db = self.the_client["mocsdb"]
            self.db_column = mocs_db["matches"]

            # For Connection Test
            self.the_client.admin.command('ismaster')

        except pymongo.errors.ConnectionFailure as e:
            print(f"Error connecting to MongoDB: {e}")
            return False
        else:
            return True

# -------------------------------------------------- Close Database ----------------------------------------------------
    def close(self):
        if self.the_client:
            self.the_client.close()

# ------------------------------------------------------ Debug ---------------------------------------------------------
if __name__ == "__main__":
    try:
        database = CricketDatabase()
        if database.connect():
            print("Connected to MongoDB successfully")
        else:
            print("Failed to connect to MongoDB")
    except ValueError as e:
        print(f"Error: {e}")
    finally:
        database.close()
