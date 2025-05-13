from django.db import models
import subprocess
class Code(models.Model):

    language = models.CharField(max_length=50)
    code = models.TextField()
    output_data = models.TextField(blank=True, null=True)
    error_data = models.TextField(blank=True, null=True)

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

    def run_code(self):
        if self.language == 'python':
            process = subprocess.Popen(['python3', '-c', self.code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif self.language == 'java':
            with open('Main.java', 'w') as f:
                f.write(self.code)
            process = subprocess.Popen(['javac', 'Main.java'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait()
            process = subprocess.Popen(['java', 'Main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif self.language == 'c++':
            with open('main.cpp', 'w') as f:
                f.write(self.code)
            process = subprocess.Popen(['g++', 'main.cpp', '-o', 'main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait()
            process = subprocess.Popen(['./main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif self.language == 'c':
            with open('main.c', 'w') as f:
                f.write(self.code)
            process = subprocess.Popen(['gcc', 'main.c', '-o', 'main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait()
            process = subprocess.Popen(['./main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            raise ValueError("Unsupported language")

        output, error = process.communicate()
        self.output_data = output.decode('utf-8')
        self.error_data = error.decode('utf-8')
