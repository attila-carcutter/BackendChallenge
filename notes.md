>Customers will post some json data to this api route, and we want to store each Vehicle in the Vehicle-List to a single file. This file should be stored to a folder named like the user_id and the filename should be the id with a ".json" extension.

This is a bit misleading.

A user and a customer can be different terms, moreover customers could have users.

As a general rule, objects should be identified with `<object>_id`.  
So a customer shouldn't been identified with `user_id`, instead with `customer_id`.

Terminology always needs to be used 100% correctly, otherwise misunderstandings will happen.

I understand, customers are here the _users_, but then we should just get rid of the term _user_ and use the **customer**
word everywhere consistently, because it looks like that word is being used by domain experts (people who own the business logic).

---

```python
class ApiDecorators:

    MOCK_CUSTOMER_ID = str(uuid4())

    @staticmethod
    def require_customer_id(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(ApiDecorators.MOCK_CUSTOMER_ID, *args, **kwargs)

        return decorated_function

```

1. `@staticmethod` is anti-OO and should be banned.
2. Class names should be singular. _Clean Code: 25. page_

A class should not have static methods, and if it has only static methods,  
then there is no reason to use a class.

---
```python
from api.utils.api_decorators import ApiDecorators

challenge_api = Blueprint("challenge_api", __name__)

@challenge_api.route("/challenge", methods=["POST"])
@ApiDecorators.require_customer_id
def vehicle_features_post(user_id: str):
```

Decorator based routing isn't ideal, because:
- you have to declare global variables
- routing is divided into multiple places

It's much easier to look at the application's routing if all routes are being declared in one place.
[Starlette](https://www.starlette.io/) (my favorite python web framework) already deprecated decorator based routing.
https://github.com/encode/starlette/blob/74ccb961b3c1b1871aa7ed70a81dd3000e0194da/starlette/applications.py#L201

---
```bash
curl --request POST 'http://localhost:8080/backend/challenge' \
  --header "Content-Type: application/json" \
  --form data=@json/vehicle-features.v1.example.json
```

This is an invalid request, the API will return the proper error message.
Either `content-type` should be `multipart/form-data` or the content should be proper `json`.
This needs to be fixed on the client side.