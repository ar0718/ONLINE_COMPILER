import subprocess
import time
from django.db import models

class Code(models.Model):
    language = models.CharField(max_length=50)
    code = models.TextField()
    output_data = models.TextField(blank=True, null=True)
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
    
    def set_code(self, _code, _language):
        self.code = _code
        self.language = _language

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
            if self.language == 'python':
                with open('main.py', 'w') as f:
                    f.write(self.code)
                end_time = start_time = time.time()
                result = subprocess.run(
                    ['python3', 'main.py'],
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
                result = subprocess.run(['java', 'Main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
                end_time = time.time()

            elif self.language == 'c++':
                with open('main.cpp', 'w') as f:
                    f.write(self.code)
                result1 = subprocess.run(['g++', 'main.cpp', '-o', 'main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
                end_time = start_time = time.time()
                result = subprocess.run(['./main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
                end_time = time.time()

            elif self.language == 'c':
                with open('main.c', 'w') as f:
                    f.write(self.code)
                result1 = subprocess.run(['gcc', 'main.c', '-o', 'main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
                end_time = start_time = time.time()
                result = subprocess.run(['./main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
                end_time = time.time()

            else:
                raise ValueError("Unsupported language")

            self.output_data = result.stdout.decode('utf-8')

            if self.language != 'python':
                self.error_data = result1.stderr.decode('utf-8')
            self.error_data = ""
            self.error_data += result.stderr.decode('utf-8')

        except subprocess.TimeoutExpired:
            self.output_data = ""
            self.error_data = "Execution timed out."
        except Exception as e:
            self.output_data = ""
            self.error_data = f"An error occurred: {str(e)}"
        finally:
            runtime = end_time - start_time
            self.runtime = runtime
