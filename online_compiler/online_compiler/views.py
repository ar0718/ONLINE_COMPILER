from rest_framework.decorators import api_view
from rest_framework.response import Response
from online_compiler.models import Code

@api_view(['POST'])
def ide(request):
    language = request.data.get('language')
    code = request.data.get('code')
    if not language or not code:
        return Response({"error": "language and code both are required"}, status=400)
    code_instance = Code()
    code_instance.set_code(code, language)
    code_instance.run_code()
    output = code_instance.get_output_data()
    error = code_instance.get_error_data()
    runtime = code_instance.get_runtime()
    # memory = code_instance.get_memory_used()
    if error:
        return Response({"error": error}, status=500)
    return Response({"output": output, "runtime": runtime}, status=200)       
