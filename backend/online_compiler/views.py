from rest_framework.decorators import api_view
from rest_framework.response import Response
from online_compiler.models import Code
from django.contrib.auth.models import User
from online_compiler.models import Problem
from online_compiler.models import checker
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
    if error :
        return Response({"error": error}, status=500)
    return Response({"output": output, "runtime": runtime, "error":""}, status=200)       

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
    return Response({"message": "User created successfully", "error": ""}, status=201)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({"error": "username and password both are required"}, status=400)
    if not User.objects.filter(username=username).exists():
        return Response({"error": "wrong username or password"}, status=300)
    password_stored = User.objects.get(username=username).password
    if not bcrypt.checkpw(password.encode('utf-8'), password_stored.encode('utf-8')):
        return Response({"error": "wrong username or password"}, status=300)
    else:
        jwt_secret = jwt.encode({"username": username}, SECRET, algorithm="HS256")
        return Response({"message": "successfully logged in", "jwt": jwt_secret, "error":""}, status=200)

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
    problem_instance = Problem(solve_count = 0,problem_id = cnt, title=title, description=description, input_format=input_format, output_format=output_format, sub = 0 )
    # problem_instance.problem_id = "problem" + str(cnt + 1)
    problem_instance.save()
    return Response({"message": "Problem added successfully", "error":""}, status=201)
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
            # "input_format": problem.input_format,
            # "output_format": problem.output_format,
            "solve_count": problem.solve_count,
            "total_submissions": problem.sub
            
        })
    return Response({"problems": problem_list, "error":""}, status=200)
@api_view(['POST'])
def submit_code(request):
    jwt_token = request.data.get('jwt')
    try:
         jwt.decode(jwt_token, SECRET, algorithms="HS256")
    except jwt.ExpiredSignatureError:
        return Response({"error": "Token has expired"}, status=401)
    except  jwt.InvalidTokenError as e:
        return Response({"error": f"Invalid token {e}"}, status=401)
    username = jwt.decode(jwt_token, SECRET, algorithms="HS256")["username"]
    problem_id = request.data.get('problem_id')
    user_code = request.data.get('code')
    language = request.data.get('language')
    if not problem_id or not user_code or not language:
        return Response({"error": "problem_id, code and language all are required"}, status=400)
    result = checker(problem_id, user_code, language, username)
    # return Response({"result": result}, status=200)
    # return Response({"resul": f"{result}"}, status=200)
    if result:
        return Response({"message": "Code is correct", "error":"", "code":"0"}, status=200)
    else:
        return Response({"message": "Code is incorrect", "error":"", "code" : "1"}, status=400)

