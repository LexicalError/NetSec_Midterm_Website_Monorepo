from ninja import NinjaAPI
from ninja import Schema
from api.models import Message, Profile_Picture
from django.contrib.auth.models import User
from typing import List
from ninja import UploadedFile, File
from ninja.security import django_auth
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
import vercel_blob


# api = NinjaAPI(csrf=True, auth=django_auth)
api = NinjaAPI()


@api.get("/csrf", auth=None)
@ensure_csrf_cookie
@csrf_exempt
def get_csrf_token(request):
    return HttpResponse('{"csrfToken": ' + f'{get_token(request)}' + '}', content_type='application/json')


class UserIn(Schema):
    username: str
    password: str

class UserOut(Schema):
    id: int
    username: str

class MessageIn(Schema):
    content: str

class MessageOut(Schema):
    id: int
    content: str
    author: str
    profile_picture: str

class ReturnMessage(Schema):
    message: str

class ReturnError(Schema):
    error: str

@api.post("/login", response={200: ReturnMessage, 401: ReturnError})
def login_user(request, payload: UserIn):
    user = authenticate(username=payload.username, password=payload.password)
    if user is not None:
        login(request, user)
        return 200, {"message": "Login successful"}
    return 401, {"error": "Invalid credentials"}

@api.post("/logout", response={200: ReturnMessage, 401: ReturnError})
def logout_user(request):
    logout(request)
    return 200, {"message": "Logout successful"}

@api.get("/session", response={200: UserOut, 401: ReturnError})
def session_status(request):
    if request.user.is_authenticated:
        return 200, {"username": f"{request.user.username}", "id": f"{request.user.id}"}
    return 401, {"error": "User is not logged in"}


@api.post("/user", response={200:ReturnMessage, 400: ReturnError, 500:ReturnError})
def create_user(request, payload: UserIn):
    try:
        user = User.objects.create_user(**payload.dict())
    except IntegrityError as e:
        if 'UNIQUE constraint failed' in str(e):
            return 400, {"error": "Username already exists"}
        print(e)
        return 500, {"error": "User creation failed"}
    except Exception as e:
        print(e)
        return 500, {"error": "User creation failed"}
    return 200, {"message": "User created successfully"}

@api.get("/user", response={200: List[UserOut], 500:ReturnError})
def list_users(request):
    try:
        users = User.objects.all()
    except Exception as e:
        print(e)
        return 500, {"error": "User retrieval failed"}
    return 200, users


@api.delete("/user/{user_id}", response={200:ReturnMessage, 404:ReturnError, 500:ReturnError})
def delete_user(request, user_id: int):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
    except User.DoesNotExist:
        return 404, {"error": "User not found"}
    except Exception as e:
        print(e)
        return 500, {"error": "User deletion failed"}
    return 200, {"message": "User deleted successfully"}

@api.post("/upload", response={200:ReturnMessage, 500:ReturnError})
def upload_profile_picture(request, file: UploadedFile = File(...)):
    try:
        uploaded_file = vercel_blob.put(f'{request.user}', file.file.read(), {})
        user = User.objects.get(username=request.user)
        profile_picture, created = Profile_Picture.objects.get_or_create(user=user)
        profile_picture.profile_picture = uploaded_file['downloadUrl']
        profile_picture.save()
        return 200, {"message": "Image uploaded successfully"}
    except Exception as e:
        print(e)
        return 500, {"error": "Image upload failed"}




@api.post("/message", response={200:ReturnMessage, 401: ReturnError, 404:ReturnError, 500:ReturnError})
def create_message(request, payload: MessageIn):
    try:
        if not request.user.is_authenticated:
            return 401, {"error": "User not authenticated"}
        author = User.objects.get(username=request.user)
        Message.objects.create(content=payload.content, author=author)
    except User.DoesNotExist:
        return 404, {"error": "User not found"}
    except Exception as e:
        print(e)
        return 500, {"error": "Message creation failed"}
    return 200, {"message": "Message created successfully"}

@api.get("/message", response={200: List[MessageOut], 500: ReturnError})
def list_message(request):
    try:
        messages = Message.objects.all()
        message_list = []
        for message in messages:
            profile_picture = None
            profile_picture_obj = Profile_Picture.objects.get(user=message.author)
            message_list.append({
                "id": message.id,
                "content": message.content,
                "author": message.author.username,
                "profile_picture": profile_picture_obj.profile_picture,
            })
    except Exception as e:
        print(e)
        return 500, {"error": "Message retrieval failed"}
    return 200, message_list

@api.delete("/message/{message_id}", response={200: ReturnMessage, 404: ReturnError, 500: ReturnError})
def delete_message(request, message_id: int):
    try:
        message = Message.objects.get(id=message_id)
        message.delete()
    except Message.DoesNotExist:
        return 404, {"error": "Message not found"}
    except Exception as e:
        print(e)
        return 500, {"error": "Message deletion failed"}
    return 200, {"message": "Message deleted successfully"}

