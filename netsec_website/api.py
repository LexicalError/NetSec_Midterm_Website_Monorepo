from ninja import NinjaAPI
from ninja import Schema
from api.models import User, Message
from typing import List
from django.core.files.storage import FileSystemStorage
from ninja import UploadedFile, File

STORAGE = FileSystemStorage()

api = NinjaAPI()

class UserIn(Schema):
    username: str
    password: str

class UserOut(Schema):
    id: int
    username: str
    password: str

class MessageIn(Schema):
    content: str
    author_id: int

class MessageOut(Schema):
    id: int
    content: str
    author_id: int

class ReturnMessage(Schema):
    message: str

@api.post("/user", response={200:ReturnMessage, 500:ReturnMessage})
def create_user(request, payload: UserIn):
    try:
        user = User.objects.create(**payload.dict())
    except Exception as e:
        print(e)
        return 500, {"error": "User creation failed"}
    return 200, {"message": "User created successfully"}

@api.get("/user", response={200: List[UserOut], 500:ReturnMessage})
def list_users(request):
    try:
        users = User.objects.all()
    except Exception as e:
        print(e)
        return 500, {"error": "User retrieval failed"}
    return 200, users

@api.delete("/user/{user_id}", response={200:ReturnMessage, 404:ReturnMessage, 500:ReturnMessage})
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

@api.post("/upload", response={200:ReturnMessage, 500:ReturnMessage})
def upload_profile_picture(request, file: UploadedFile = File(...)):
    try:
        filename = STORAGE.save(file.name, file)
    except Exception as e:
        print(e)
        return 500, {"error": "File upload failed"}
    return 200, {"message": "File uploaded successfully", "filename": filename}


@api.post("/message", response={200:ReturnMessage, 404:ReturnMessage, 500:ReturnMessage})
def create_message(request, payload: MessageIn):
    try:
        author = User.objects.get(id=payload.author_id)
        Message.objects.create(content=payload.content, author=author)
    except User.DoesNotExist:
        return 404, {"error": "User not found"}
    except Exception as e:
        print(e)
        return 500, {"error": "Message creation failed"}
    return 200, {"message": "Message created successfully"}

@api.get("/message", response={200: List[MessageOut], 500: ReturnMessage})
def list_message(request):
    try:
        messages = Message.objects.all()
    except Exception as e:
        print(e)
        return 500, {"error": "Message retrieval failed"}
    return 200, messages

@api.delete("/message/{message_id}", response={200: ReturnMessage, 404: ReturnMessage, 500: ReturnMessage})
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

