from fastapi import FastAPI
from app.auth import init_oauth, login, auth
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# Thêm SessionMiddleware với secret_key
app.add_middleware(SessionMiddleware, secret_key="a1f6248ebd8d1c9c36b77acb807e4dcdf3abf582e4b54f620b0b7c0a2e7fb1c4") 

# Khởi tạo OAuth
init_oauth(app)

@app.get("/")
async def home():
    return HTMLResponse("""
    <a href="/login">Login with Google</a>
    """)

@app.get("/login")
async def google_login(request: Request):
    return await login(request)

@app.get("/auth")
async def google_auth(request: Request):
    return await auth(request)
