# Database initial data
from app.schemas.teacher import Teacher

INITIAL_DATA = {
    'teacher': [
        Teacher(name="بشار").dict(),
        Teacher(name="علياء").dict(),
    ],
}


# This method receives a table, a connection and inserts data to that table.
def initialize_table(target, connection, **kw):
    tablename = str(target)
    if tablename in INITIAL_DATA and len(INITIAL_DATA[tablename]) > 0:
        connection.execute(target.insert(), INITIAL_DATA[tablename])
