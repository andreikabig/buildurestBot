from peewee import *

con = SqliteDatabase("storage.sqlite")

class BaseModel(Model):
    class Meta:
        database = con

class Roles(BaseModel):
    id = AutoField(column_name="id")
    name = TextField(column_name="name")

    class Meta:
        table_name = "Roles"

class Users(BaseModel):
    id = AutoField(column_name="id")
    chat_id = IntegerField(column_name="chat_id", null=False)
    is_bot = TextField(column_name="is_bot", null=False)
    first_name = TextField(column_name="first_name", null=False)
    last_name = TextField(column_name="last_name", null=False)
    username = TextField(column_name="username", null=True)
    language_code = TextField(column_name="language_code", null=False)
    role = ForeignKeyField(Roles, on_delete="cascade", on_update="cascade", to_field="id")
    about = TextField(column_name="about", null=True)

    class Meta:
        table_name = "Users"

class RestType(BaseModel):
    id = AutoField(column_name="id")
    name = TextField(column_name="name", null=False)

    class Meta:
        table_name = "RestTypes"

class Rest(BaseModel):
    id = AutoField(column_name="id")
    name = TextField(column_name="name", null=False)
    description = TextField(column_name="description", null=True)
    price = IntegerField(column_name="price", null=False)
    rest_type = ForeignKeyField(RestType, on_delete="cascade", on_update="cascade", to_field="id")

    class Meta:
        table_name = "Rests"

class Orders(BaseModel):
    id = AutoField(column_name="id")
    user = ForeignKeyField(Users, on_delete="cascade", on_update="cascade", to_field="id")
    rest = ForeignKeyField(Rest, on_delete="cascade", on_update="cascade", to_field="id")

    class Meta:
        table_name = "Orders"


if __name__ == "__main__":
    Roles.create_table()
    Users.create_table()
    RestType.create_table()
    Rest.create_table()
    Orders.create_table()

    con.close()