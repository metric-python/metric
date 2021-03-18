from sqlalchemy.exc import SQLAlchemyError


class BaseError(Exception):
    pass


class AddQueryInvalid(Exception):
    def __init__(self, exception, message="Parameter Add condition is invalid"):
        self.message = message
        self.exception = exception
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: {self.exception}'


class DataValueInvalid(BaseError):
    def __init__(self, exception, message="Invalid value data given"):
        self.message = message
        self.exception = exception
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: {self.exception}'


class NoneTypeValue(BaseError):
    def __init__(self, exception, message="The value is empty or none"):
        self.message = message
        self.exception = exception
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: {self.exception}'
