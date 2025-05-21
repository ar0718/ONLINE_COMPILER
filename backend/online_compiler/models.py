import subprocess
import time
import signal
from django.db import models

class Code(models.Model):
    language = models.CharField(max_length=50)
    code = models.TextField()
    output_data = models.TextField(blank=True, null=True)
    input_data = models.TextField(blank=True, null=True)
    error_data = models.TextField(blank=True, null=True)
    runtime = models.FloatField(blank=True, null=True)
    memory_used = models.FloatField(blank=True, null=True)

    def __init__(self):
        self.runtime = None
        self.language = None
        self.code = None
        self.output_data = None
        self.error_data = None
        self.memory_used = None
        self.input_data = None
    
    def set_code(self, _code, _language):
        self.code = _code
        self.language = _language
    
    def set_code(self, _code, _language, _input_data=None):
        self.input_data = _input_data
        self.code = _code
        self.language = _language
    def get_input_data(self):
        return self.input_data
    def get_code(self):
        return self.code
    
    def get_language(self):
        return self.language
    
    def get_output_data(self):
        return self.output_data
    
    def get_error_data(self):
        return self.error_data
    
    def get_runtime(self):
        return self.runtime
    
    def get_memory_used(self):
        return self.memory_used
    
    def run_code(self):
        try:
            input_data = self.input_data
            if self.language == 'python':
                with open('main.py', 'w') as f:
                    f.write(self.code)
                end_time = start_time = time.time()
                result = subprocess.run(
                    ['python3', 'main.py'],
                    input=input_data,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout = 3
                )
                end_time = time.time()

            elif self.language == 'java':
                with open('Main.java', 'w') as f:
                    f.write(self.code)
                result1 = subprocess.run(['javac', 'Main.java'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
                end_time = start_time = time.time()
                result = subprocess.run(['java', 'Main'],input = input_data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
                end_time = time.time()


            elif self.language == 'c++':
                with open('main.cpp', 'w') as f:
                    f.write(self.code)
        
                result1 = subprocess.run(['g++', 'main.cpp', '-o', 'main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
                end_time = start_time = time.time()
                result = subprocess.run(['./main'], input = input_data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
                end_time = time.time()
   

            elif self.language == 'c':
                with open('main.c', 'w') as f:
                    f.write(self.code)
                result1 = subprocess.run(['gcc', 'main.c', '-o', 'main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
                end_time = start_time = time.time()
                result = subprocess.run(['./main'],input = input_data,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
                end_time = time.time()


            else:
                raise ValueError("Unsupported language")

            self.output_data = result.stdout.decode('utf-8')

            self.error_data = ""
            if self.language != 'python':
                self.error_data = result1.stderr.decode('utf-8')
            self.error_data += result.stderr.decode('utf-8')
            if result.returncode != 0 and self.error_data == "":
                signum = -result.returncode
                sig_name = signal.Signals(signum).name
                self.error_data += f'{sig_name}'
            # self.error_data += f'{result.returncode}'

        except subprocess.TimeoutExpired:
            self.output_data = ""
            self.error_data = "Execution timed out. You have exceeded the time limit of 3 seconds."
        finally:
            
            runtime = end_time - start_time
            self.runtime = runtime
            

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    def __init__(self):
        self.username = None
        self.password = None
    def set_user(self, _username, _password):
        self.username = _username
        self.password = _password
    def get_username(self):
        return self.username
    def get_password(self):
        return self.password

class Problem(models.Model):
    problem_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()
    solve_count = models.IntegerField()
    sub = models.IntegerField()
    def set_problem(self, _title, _description, _input_format, _output_format, _solve_count, _problem_id, _sub):
        self.solve_count = _solve_count
        self.problem_id = _problem_id
        self.title = _title
        self.description = _description
        self.input_format = _input_format
        self.output_format = _output_format
        self.sub = _sub
    def get_solve_count(self):
        return self.solve_count
    def get_problem_id(self):
        return self.problem_id
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_input_format(self):
        return self.input_format
    def get_output_format(self):
        return self.output_format  
    def get_sub(self):
        return self.sub
    

def equal_ingnore_whitespace(str1, str2):
    str1 = str1.replace(" ", "")
    str1 = str1.replace("\n", "")
    str2 = str2.replace(" ", "")
    str2 = str2.replace("\n", "")
    return str1 == str2

class Problem_solve(models.Model):
    problem_id = models.IntegerField()
    username = models.CharField(max_length=100)

def checker(problem_id, user_code, language, username):
    problem = Problem.objects.get(problem_id=problem_id)
    input_data = problem.input_format
    output_data = problem.output_format
    code_instance = Code()
    code_instance.set_code(user_code, language, input_data.encode('utf-8'))
    code_instance.run_code()
    # return code_instance.get_output_data(), output_data
    if equal_ingnore_whitespace(code_instance.get_output_data(), output_data) and code_instance.get_error_data() == "":
        problem_solve = Problem_solve.objects.filter(problem_id=problem_id, username=username)
        if(problem_solve.exists()):
            return True
        problem.solve_count += 1
        problem.sub += 1
        problem_solve_instance = Problem_solve(problem_id=problem_id, username=username)
        problem_solve_instance.save()
        # change the problem solve count stored in the database
        Problem.objects.filter(problem_id=problem.problem_id).update(solve_count=problem.solve_count)
        Problem.objects.filter(problem_id=problem.problem_id).update(sub=problem.sub)
        # problem.save()
        return True
    else:
        problem.sub += 1
        problem.save()
        return False
    