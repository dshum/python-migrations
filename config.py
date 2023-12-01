import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    CONNECTION = os.getenv("CONNECTION", "prod")
    PREFIX = "LOCAL_" if CONNECTION == "local" else ""

    DB_NAME = os.getenv(PREFIX + "DB_NAME", "postgres")
    DB_USER = os.getenv(PREFIX + "DB_USER", "postgres")
    DB_PASSWORD = os.getenv(PREFIX + "DB_PASSWORD", "password")
    DB_HOST = os.getenv(PREFIX + "DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv(PREFIX + "DB_PORT", "5432")

    BRANDS_DB_NAME = "brands"

    SSH_HOST = os.getenv("SSH_HOST")
    REMOTE_DB_HOST = os.getenv("REMOTE_DB_HOST")
    REMOTE_DB_PORT = os.getenv("REMOTE_DB_PORT")
    SSH_KEY = os.getenv("SSH_KEY")

    def db_args(self):
        return {
            "db_name": self.DB_NAME,
            "db_user": self.DB_USER,
            "db_password": self.DB_PASSWORD,
            "db_host": self.DB_HOST,
            "db_port": self.DB_PORT,
        }

    def brands_db_args(self):
        return {
            "db_name": self.BRANDS_DB_NAME,
            "db_user": self.DB_USER,
            "db_password": self.DB_PASSWORD,
            "db_host": self.DB_HOST,
            "db_port": self.DB_PORT,
        }

    def ssh_tunnel_args(self):
        return {
            "ssh_host": self.SSH_HOST,
            "remote_db_host": self.REMOTE_DB_HOST,
            "remote_db_port": self.REMOTE_DB_PORT,
            "ssh_key": self.SSH_KEY
        }
