from jose import jwt, JWTError, ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from models import User, Token, Items, ItemModel, UploadItem

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_token(user: User) -> Token:
    payload = {"sub": user.username}
    token = jwt.encode(payload, key="your_secret_key", algorithm="HS256")
    return Token(access_token=token, token_type="bearer")


def verify_token(token: str):
    try:
        payload = jwt.decode(token, key="your_secret_key",
                             algorithms=["HS256"])
        return payload["sub"]
    except ExpiredSignatureError:
        return None
    except JWTError:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username


@app.get("/protected")
async def protected_endpoint(username: str = Depends(get_current_user)):
    return {"message": f"Hello, {username}!"}


# Example usage:
user = User(username="john", password="password")
token = create_token(user)
print(token.access_token)  # prints the JWT token
print(token.token_type)  # prints "bearer"
