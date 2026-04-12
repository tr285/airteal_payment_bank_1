import mysql.connector
import psycopg2
from psycopg2.extras import RealDictCursor
from config.settings import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseAbstractionLayer:
    def __init__(self):
        self.mysql_conn = None
        self.pg_conn = None
        self._active_db = None
        self.connect()

    def connect(self):
        # 1. Try MySQL First
        try:
            self.mysql_conn = mysql.connector.connect(
                host=settings.MYSQL_HOST,
                user=settings.MYSQL_USER,
                password=settings.MYSQL_PASSWORD,
                database=settings.MYSQL_DATABASE,
                port=settings.MYSQL_PORT
            )
            if self.mysql_conn.is_connected():
                self._active_db = 'mysql'
                logger.info("Successfully connected to Primary DB (MySQL).")
                self.initialize_schema()
                return
        except Exception as e:
            logger.warning(f"MySQL Connection failed: {e}. Falling back to Supabase.")

        # 2. Fallback to Supabase (PostgreSQL)
        if settings.SUPABASE_DB_URL:
            try:
                self.pg_conn = psycopg2.connect(settings.SUPABASE_DB_URL)
                self._active_db = 'postgres'
                logger.info("Successfully connected to Fallback DB (Supabase/PostgreSQL).")
                self.initialize_schema()
                return
            except Exception as e:
                logger.error(f"Supabase Connection failed: {e}.")
        
        logger.error("No database connections available!")

    def _get_cursor(self):
        if self._active_db == 'mysql' and self.mysql_conn:
            # Reconnect if ping fails
            if not self.mysql_conn.is_connected():
                self.connect()
            return self.mysql_conn.cursor(dictionary=True)
        elif self._active_db == 'postgres' and self.pg_conn:
            # PostgreSQL connection check
            if self.pg_conn.closed != 0:
                self.connect()
            return self.pg_conn.cursor(cursor_factory=RealDictCursor)
        raise Exception("No active database connection")

    def execute(self, query, params=None):
        """Execute a query that doesn't return data (INSERT, UPDATE, DELETE)"""
        # Convert parameter placeholders from %s to ? or similar if needed?
        # Both mysql-connector and psycopg2 support %s placeholders.
        cursor = self._get_cursor()
        try:
            cursor.execute(query, params)
            if self._active_db == 'mysql':
                self.mysql_conn.commit()
            else:
                self.pg_conn.commit()
        except Exception as e:
            if self._active_db == 'mysql':
                self.mysql_conn.rollback()
            else:
                self.pg_conn.rollback()
            raise e
        finally:
            cursor.close()

    def fetchall(self, query, params=None):
        """Execute a query and return all results"""
        cursor = self._get_cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()

    def fetchone(self, query, params=None):
        """Execute a query and return a single result"""
        cursor = self._get_cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchone()
        finally:
            cursor.close()
            
    def commit(self):
        """Commit transaction"""
        if self._active_db == 'mysql' and self.mysql_conn:
            self.mysql_conn.commit()
        elif self._active_db == 'postgres' and self.pg_conn:
            self.pg_conn.commit()

    def rollback(self):
        """Rollback transaction"""
        if self._active_db == 'mysql' and self.mysql_conn:
            self.mysql_conn.rollback()
        elif self._active_db == 'postgres' and self.pg_conn:
            self.pg_conn.rollback()

    def initialize_schema(self):
        """Create tables if they don't exist"""
        mysql_schema = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(100) NOT NULL,
                mobile VARCHAR(15) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                balance DECIMAL(15, 2) DEFAULT 0.00,
                role VARCHAR(10) DEFAULT 'user'
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sender_id INT NOT NULL,
                receiver_id INT NOT NULL,
                amount DECIMAL(15, 2) NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        ]

        pg_schema = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                full_name VARCHAR(100) NOT NULL,
                mobile VARCHAR(15) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                balance DECIMAL(15, 2) DEFAULT 0.00,
                role VARCHAR(10) DEFAULT 'user'
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                sender_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                receiver_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                amount DECIMAL(15, 2) NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        ]

        schema_to_run = mysql_schema if self._active_db == 'mysql' else pg_schema

        for query in schema_to_run:
            self.execute(query)


# Singleton instance
db = DatabaseAbstractionLayer()
