# ninja
from ninja import NinjaAPI
from ninja import Schema
from ninja import UploadedFile, File
from ninja.security import django_auth
# django
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.exceptions import ValidationError
# pydantic
from pydantic import BaseModel, ValidationError, field_validator
#api
from api.models import Message, Profile_Picture, CustomUser
# python
import re
import vercel_blob
from typing import List
from io import BytesIO
# Pillow
from PIL import Image, UnidentifiedImageError

# 5 KB
MAX_FILE_SIZE = 5 * 1024

SLUG = re.compile(r'^[a-zA-Z0-9-_]+$')
ALNUMERIC_SPACE = re.compile(r'^[a-zA-Z0-9 ]+$')


api = NinjaAPI(csrf=True, auth=django_auth)

class UserIn(Schema):
    username: str
    password: str

    @field_validator('*')
    def alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v


class UserOut(Schema):
    id: str
    username: str

    @field_validator('id')
    def slug(cls, v):
        assert SLUG.match(v), 'must be slug'
        return v

    @field_validator('username')
    def alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

class MessageIn(Schema):
    content: str

    @field_validator('*')
    def alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

class MessageOut(Schema):
    id: int
    uuid: str
    content: str
    author: str
    profile_picture: str

    @field_validator('uuid')
    def slug(cls, v):
        assert SLUG.match(v), 'must be slug'
        return v

    @field_validator('content')
    def alphanumeric_space(cls, v):
        assert ALNUMERIC_SPACE.match(v), 'must be alphanumeric or space'
        return v

    @field_validator('author')
    def alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

class ReturnMessage(Schema):
    message: str

    @field_validator('*')
    def alphanumeric_space(cls, v):
        assert ALNUMERIC_SPACE.match(v), 'must be alphanumeric or space'
        return v
    
class ReturnError(Schema):
    error: str

    @field_validator('*')
    def alphanumeric_space(cls, v):
        assert ALNUMERIC_SPACE.match(v), 'must be alphanumeric or space'
        return v


@api.get("/csrf", auth=None)
@ensure_csrf_cookie
@csrf_exempt
def get_csrf_token(request):
    return HttpResponse('{"csrfToken": "' + f'{get_token(request)}' + '"}', content_type='application/json')

@api.post("/login", response={200: ReturnMessage, 401: ReturnError}, auth=None)
def login_user(request, payload: UserIn):
    try:
        user = authenticate(username=payload.username, password=payload.password)
        if user is not None:
            login(request, user)
            return 200, {"message": "Login successful"}
    except Exception as e:
        print(e)
        return 401, {"error": "Invalid credentials"}
    return 401, {"error": "Invalid credentials"}

@api.post("/logout", response={200: ReturnMessage, 400: ReturnError})
def logout_user(request):
    try:
        logout(request)
    except Exception as e:
        return 400, {"error": "Logout failed"}
    return 200, {"message": "Logout successful"}

@api.get("/session", response={200: UserOut, 401: ReturnError})
def session_status(request):
    try:
        if request.user.is_authenticated:
            return 200, {"username": f"{request.user.username}", "id": str(request.user.id)}
        
    except Exception as e:
        return 401, {"error": "User is not logged in"}
    return 401, {"error": "User is not logged in"}


@api.post("/user", response={200:ReturnMessage, 400: ReturnError}, auth=None)
def create_user(request, payload: UserIn):
    try:
        user = CustomUser(**payload.dict())
        user.save()
    except IntegrityError as e:
        if 'UNIQUE constraint failed' in str(e):
            return 400, {"error": "Username already exists"}
        return 400, {"error": "User creation failed"}
    except ValidationError as e:
        return 400, {"error": "User creation failed"}
    except Exception as e:
        return 400, {"error": "User creation failed"}
    return 200, {"message": "User created successfully"}


# REMOVE
# @api.get("/user", response={200: List[UserOut], 500:ReturnError})
# def list_users(request):
#     try:
#         users = CustomUser.objects.all()
#         user_list = []
#         for user in users:
#             user_list.append({
#                 "id": str(user.id),
#                 "username": user.username,
#             })
#     except Exception as e:
#         print(e)
#         return 500, {"error": "User retrieval failed"}
#     return 200, user_list


# @api.delete("/user/{user_id}", response={200:ReturnMessage, 404:ReturnError, 500:ReturnError})
# def delete_user(request, user_id: str):
#     try:
#         user = CustomUser.objects.get(id=user_id)
#         user.delete()
#     except CustomUser.DoesNotExist:
#         return 404, {"error": "User not found"}
#     except Exception as e:
#         print(e)
#         return 500, {"error": "User deletion failed"}
#     return 200, {"message": "User deleted successfully"}

@api.post("/upload", response={200:ReturnMessage, 400:ReturnError})
def upload_profile_picture(request, file: UploadedFile = File(...)):
    try:
        # file name check:
        if '0x00' in file.name:
            return 400, {"error": "Image upload failed"}
        name_parts = file.name.rsplit(".", 1)
        if len(name_parts) != 2:
            return 400, {"error": "Invalid file name"}
        basename, ext = name_parts
        if ext not in ['jpg', 'png']:
            return 400, {"error": "Invalid file name"}
        if len(basename) > 255:
            return 400, {"error": "Invalid file name"}
        if re.match(r'^[a-zA-Z0-9-_]+$', basename) is None:
            return 400, {"error": "Invalid file name"}
        
        # Check MIME type
        content_type = file.content_type
        if content_type not in ['image/jpeg', 'image/png']:
            return 400, {"error": "Unsupported file type"}
        
        file_data = file.read()
        if not file_data:
            return 400, {"error": "File is empty"}
        if len(file_data) > MAX_FILE_SIZE:
            return 400, {"error": "File too large"}
        
        # Validate content
        try:
            img = Image.open(BytesIO(file_data))
            img.verify()  # validate file integrity
        except UnidentifiedImageError:
            return 400, {"error": "Invalid file"}
        except Exception:
            return 400, {"error": "Invalid file"}
        
        # Sanitize image
        img = Image.open(BytesIO(file_data))
        img = img.convert("RGB")  
        img = img.resize((64, 64))

        safe_buffer = BytesIO()
        img.save(safe_buffer, format="PNG") 
        safe_buffer.seek(0)

        user = CustomUser.objects.get(id=request.user.id)
        uploaded_file = vercel_blob.put(f'{request.user.id}', safe_buffer.read(), {})
        profile_picture, created = Profile_Picture.objects.get_or_create(user=user)
        profile_picture.profile_picture = uploaded_file['downloadUrl']
        profile_picture.save()
        return 200, {"message": "Image uploaded successfully"}
    except ValidationError:
        return 400, {"error": "Image upload failed"}
    except Exception as e:
        print(e)
        return 400, {"error": "Image upload failed"}


@api.post("/message", response={200:ReturnMessage, 400:ReturnError})
def create_message(request, payload: MessageIn):
    try:
        author = CustomUser.objects.get(id=request.user.id)
        message = Message(content=payload.content, author=author)
        message.save()
    except CustomUser.DoesNotExist:
        return 400, {"error": "Message creation failed"}
    except ValidationError:
        return 400, {"error": "Message creation failed"}
    except Exception as e:
        print(e)
        return 400, {"error": "Message creation failed"}
    return 200, {"message": "Message created successfully"}

@api.get("/message", response={200: List[MessageOut], 400: ReturnError})
def list_message(request):
    try:
        messages = Message.objects.all()
        message_list = []
        for message in messages:
            profile_picture_obj, created = Profile_Picture.objects.get_or_create(user=message.author)
            message_list.append({
                "id": message.id,
                "uuid": str(message.uuid),
                "content": message.content,
                "author": message.author.username,
                "profile_picture": profile_picture_obj.profile_picture if profile_picture_obj.profile_picture else "",
            })
    except Exception as e:
        print(e)
        return 400, {"error": "Message retrieval failed"}
    return 200, message_list

@api.delete("/message/{message_uuid}", response={200: ReturnMessage, 400: ReturnError})
def delete_message(request, message_uuid: str):
    try:
        message = Message.objects.get(uuid=message_uuid)
        if request.user != message.author or request.user.username != message.author.username or request.user.id != message.author.id:
            return 400, {"error": "Message deletion failed"}

        message.delete()
    except Message.DoesNotExist:
        return 400, {"error": "Message deletion failed"}
    except Exception as e:
        print(e)
        return 400, {"error": "Message deletion failed"}
    return 200, {"message": "Message deleted successfully"}

