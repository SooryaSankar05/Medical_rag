from src.auth.security import (
    hash_password,
    verify_password
)

password = "Soorya_321"

hashed = hash_password(
    password
)

print(hashed)

print(
    verify_password(
        "Soorya_321",
        hashed
    )
)

print(
    verify_password(
        "wrong_password",
        hashed
    )
)