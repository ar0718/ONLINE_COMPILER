from rest_framework.decorators import api_view
from rest_framework.response import Response
from online_compiler.models import Code
from django.contrib.auth.models import User
import jwt
import bcrypt

SECRET = "knsa9837982980!!@@@@!!@@!@@@!@kjsnknknkjnajknk"

@api_view(['POST'])
def ide(request):
    language = request.data.get('language')
    code = request.data.get('code')
    input_data = request.data.get('input')
    input_data = input_data.encode('utf-8')
    if not language or not code:
        return Response({"error": "language and code both are required"}, status=400)
    code_instance = Code()
    if input_data:
        code_instance.set_code(code, language, input_data)
    else:
        code_instance.set_code(code, language)
    code_instance.run_code()
    output = code_instance.get_output_data()
    error = code_instance.get_error_data()
    runtime = code_instance.get_runtime()
    if error:
        return Response({"error": error}, status=500)
    return Response({"output": output, "runtime": runtime}, status=200)       

@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    password = hashed.decode('utf-8')
    if not username or not password:
        return Response({"error": "username and password both are required"}, status=400)
    if User.objects.filter(username=username).exists() :
        return Response({"error": "Username already exists"}, status=300)
    user_instance = User(username=username, password=password)
    user_instance.save()
    return Response({"message": "User created successfully"}, status=201)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({"error": "username and password both are required"}, status=400)
    password_stored = User.objects.get(username=username).password
    if not User.objects.filter(username=username).exists():
        return Response({"error": "wrong username or password"}, status=300)

    elif not bcrypt.checkpw(password.encode('utf-8'), password_stored.encode('utf-8')):
        return Response({"error": "wrong username or password"}, status=300)
    else:
        jwt_secret = jwt.encode({"username": username}, SECRET, algorithm="HS256")
        return Response({"message": "successfully logged in", "jwt": jwt_secret}, status=200)

