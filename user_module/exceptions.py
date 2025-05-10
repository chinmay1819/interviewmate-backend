from pymongo.errors import PyMongoError

class DatabaseError(PyMongoError):
    pass

class ProvidedValueError(ValueError):
    pass