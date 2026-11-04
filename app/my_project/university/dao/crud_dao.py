import os
from typing import Any

import mysql.connector
import yaml


class CRUDDAO:
    table = ""
    columns: tuple[str, ...] = ()
    required_columns: tuple[str, ...] = ()

    def __init__(self):
        config_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "config", "app.yml")
        )
        with open(config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)["database"]

    def get_connection(self):
        return mysql.connector.connect(**self.config)

    def find_all(self):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(f"SELECT id, {', '.join(self.columns)} FROM {self.table} ORDER BY id")
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

    def find_by_id(self, item_id):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                f"SELECT id, {', '.join(self.columns)} FROM {self.table} WHERE id = %s",
                (item_id,),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    def create(self, data: dict[str, Any]):
        missing = [column for column in self.required_columns if column not in data]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")
        values = {column: data[column] for column in self.columns if column in data}
        if not values:
            raise ValueError("At least one field is required")
        names = tuple(values)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            placeholders = ", ".join(["%s"] * len(names))
            cursor.execute(
                f"INSERT INTO {self.table} ({', '.join(names)}) VALUES ({placeholders})",
                tuple(values[name] for name in names),
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            connection.close()

    def update(self, item_id, data: dict[str, Any]):
        values = {column: data[column] for column in self.columns if column in data}
        if not values:
            raise ValueError("At least one field is required")
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            assignments = ", ".join(f"{name} = %s" for name in values)
            cursor.execute(
                f"UPDATE {self.table} SET {assignments} WHERE id = %s",
                tuple(values.values()) + (item_id,),
            )
            connection.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            connection.close()

    def delete(self, item_id):
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f"DELETE FROM {self.table} WHERE id = %s", (item_id,))
            connection.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            connection.close()
