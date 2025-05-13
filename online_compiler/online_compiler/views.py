from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def code(request):
    def __init__(self,actual_code, ):
        self.actual_code = actual_code

    return Response({"message": "Hello, world!"})
