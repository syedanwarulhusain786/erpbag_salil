from django.shortcuts import render

# Create your views here.
def orders(request):
    # Your delete logic here
    
    
    template_name = 'productandservices/services/add_service.html'  # Replace with your actual template name
    context = {}
    return render(request, template_name, context)