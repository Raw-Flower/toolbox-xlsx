from django.shortcuts import render

# Create your views here.
def index_view(request):
    return render(
        request=request,
        template_name='xlsx/basic/index.html',
        context={}
    )