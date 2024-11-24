from authlib.integrations.starlette_client import OAuth
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os

# load variables from dotenv (.env)
load_dotenv()

# init OAuth
oauth = OAuth()

# get code from dotenv (.env)
google_client_id = os.getenv("GOOGLE_CLIENT_ID")
google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

# function init OAuth
def init_oauth(app):
    oauth.register(
        name='google',
        client_id="40938157814-2frl095ahoup9gop170rg1iptujtc45b.apps.googleusercontent.com",
        client_secret="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",
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={
            "scope": "openid email profile"
        }
    )

# login with Google
async def login(request: Request):
    redirect_uri = request.url_for('google_auth')
    print("rediract_uri : "+redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)

# handle after user login successfull
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token.get('userinfo')  # get user's info
    print("User information:", user)
    if user:
        # get infor from user 
        user_info = f"""
        <h1>Thông tin người dùng</h1>
        <p><strong>Tên:</strong> {user.get('name', 'Không có thông tin')}</p>
        <p><strong>Email:</strong> {user.get('email', 'Không có thông tin')}</p>
        <p><strong>Tên riêng:</strong> {user.get('given_name', 'Không có thông tin')}</p>
        <p><strong>Họ:</strong> {user.get('family_name', 'Không có thông tin')}</p>
        <p><strong>Hình đại diện:</strong> <img src="{user.get('picture', '')}" alt="Profile Picture" width="100"></p>
        <p><strong>Ngôn ngữ:</strong> {user.get('locale', 'Không có thông tin')}</p>
        <p><strong>ID người dùng:</strong> {user.get('sub', 'Không có thông tin')}</p>
        """
        return HTMLResponse(user_info)
    
    raise HTTPException(status_code=400, detail="Authentication failed")

