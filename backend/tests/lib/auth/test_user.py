import pytest
from lib.auth import user, auth
from lib.db import user as userDB


@pytest.fixture
def testUser():
    return userDB.User(
        id=1,
        username="tcs1g20",
        password=auth.pwd_context.hash("password"),
        email="tcs1g20@soton.ac.uk",
        first_name="tom",
        surname="smith",
        disabled=False,
    )


def test_verify_password():
    hashed = auth.pwd_context.hash("password")
    assert user.verify_password("password", hashed)


@pytest.mark.asyncio
async def test_authenticate_user(testUser, monkeypatch):
    async def mock(username=None):
        return testUser

    monkeypatch.setattr(userDB, "get_user_by_username", mock)
    result = await user.authenticate_user("tcs1g20", "password")
    assert result == testUser
