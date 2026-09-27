from app.core.security import hash_password
from app.core.security import verify_password

password = "Password123"

hashed = hash_password(password)

print("Password :", password)
print("Hash     :", hashed)

print(
    verify_password(
        password,
        hashed
    )
)
