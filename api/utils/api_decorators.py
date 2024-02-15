from functools import wraps
from uuid import uuid4


MOCK_CUSTOMER_ID_ = str(uuid4())


def require_customer_id(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(MOCK_CUSTOMER_ID_, *args, **kwargs)

    return wrapper
