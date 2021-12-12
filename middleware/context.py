
import os

# This is a bad place for this import
import pymysql

def get_db_info():
    """
    This is crappy code.

    :return: A dictionary with connect info for MySQL
    """
    db_info = {
        "host": "mlb-player-stats.chnpzu4a9le6.us-east-1.rds.amazonaws.com",
        "user": "admin",
        "password": "Passw0rd",
        "cursorclass": pymysql.cursors.DictCursor
    }

    return db_info
