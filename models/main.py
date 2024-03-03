from db import DB
from sqlalchemy import Column, Text, Integer
from user import Base

database = DB()
log_name = "Test_log"
fields = ["col1", "col2"]
attrs = {'__tablename__': log_name}
attrs['id'] = Column(Integer, primary_key=True)
for field in fields:
    field_type = Text
    length = None
    attrs[field] = Column(field_type(length=length))

log = type(log_name, (Base,), attrs)
database.create_table(log)
result = database.get_tables()
print(result)
database.del_log(log_name)
result = database.get_tables()
print(result)
