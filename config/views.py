from django.shortcuts import redirect

def home(request):
    return redirect('schema-swagger-ui')