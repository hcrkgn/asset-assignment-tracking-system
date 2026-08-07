from app.utils.security import check_password, hash_password


def test_password_is_hashed_and_verifies_correctly():
    password = "admin123"
    hashed_password = hash_password(password)

    assert hashed_password != password
    assert check_password(password, hashed_password)


def test_wrong_password_does_not_verify():
    hashed_password = hash_password("admin123")

    assert not check_password("wrong-password", hashed_password)
