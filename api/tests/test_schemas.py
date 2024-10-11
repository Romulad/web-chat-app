from datetime import datetime

import pytest
from pydantic import ValidationError

from ..app import schemas


class TestUserSchema:
    def test_user_email_validation(self):
        data = {"email": "testgmail.com", "first_name": "myFirstname"}
        with pytest.raises(ValidationError):
            schemas.User(**data)

    def test_user_firstName_validation(self):
        data = {"email": "test@gmail.com", "last_name": "myLastName"}
        with pytest.raises(ValidationError):
            schemas.User(**data)
    
    def test_user_schema_field(self):
        data = {
            "email": "test@gmail.com", 
            "first_name": "myFirstname",
            "created_at": str(datetime.now())
        }

        result = schemas.User(**data)
        assert hasattr(result, "email")
        assert hasattr(result, "first_name")
        assert hasattr(result, "created_at")
        assert hasattr(result, "last_name")
        assert isinstance(result.created_at, datetime)


class TestUserWithPasswordSchema:
    def test_user_password_validation(self):
        data = {"email": "test@gmail.com", "first_name": "myLastName"}
        with pytest.raises(ValidationError) as exc_info:
            schemas.UserWithPassword(**data)
        assert exc_info.value.errors()[0]['loc'][0] == "password"