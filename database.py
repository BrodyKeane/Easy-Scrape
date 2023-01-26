from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String
from app import app

db = SQLAlchemy(app)

class Database:
    def create_table(name, column_names):
        table = type(name, (db.Model), {})
        for column_name in column_names:
            setattr(table, column_name, Column(String(50)))
        return table

    def populate_table(self, table, containers):
        for container in containers:
            self._populate_row(table, container)
        db.session.commit()

    def _populate_row(self, table, container):
        new_row = table()
        for data_tag in self.data_tags:
            try:
                value = container.find(data_tag).text
                setattr(new_row, data_tag, value)
            except:
                setattr(new_row, data_tag, 'value not found')
        db.session.add(new_row)