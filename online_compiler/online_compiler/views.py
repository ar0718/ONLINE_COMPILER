from rest_framework.decorators import api_view
from rest_framework.response import Response
from online_compiler.models import Code
from django.contrib.auth.models import User
from online_compiler.models import Problem
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

@api_view(['POST'])
def add_problem(request):
    jwt_token = request.data.get('jwt')
    try:
         jwt.decode(jwt_token, SECRET, algorithms="HS256")
    except jwt.ExpiredSignatureError:
        return Response({"error": "Token has expired"}, status=401)
    except  jwt.InvalidTokenError as e:
        return Response({"error": f"Invalid token {e}"}, status=401)
    title = request.data.get('title')
    description = request.data.get('description')
    input_format = request.data.get('input_format') 
    output_format = request.data.get('output_format')
    if not title or not description or not input_format or not output_format:
        return Response({"error": "title, description, input_format and output_format all are required"}, status=400)
    cnt = Problem.objects.count()
    problem_instance = Problem(_problem_id = cnt, _title=title, _description=description, _input_format=input_format, _output_format=output_format)
    # problem_instance.problem_id = "problem" + str(cnt + 1)
    problem_instance.save()
    return Response({"message": "Problem added successfully"}, status=201)
@api_view(['GET'])
def get_problem(request):
    cnt  = Problem.objects.count()
    if cnt == 0:
        return Response({"error": "No problems available"}, status=400)
    problems = Problem.objects.all()
    # problems.delete()
    problem_list = []
    for problem in problems:
        a = 0
        problem_list.append({
            "problem_id": problem.problem_id,
            "title": problem.title,
            "description": problem.description,
            "input_format": problem.input_format,
            "output_format": problem.output_format,
            "solve_count": problem.solve_count
        })
    return Response({"problems": problem_list}, status=200)
