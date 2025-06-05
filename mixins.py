from django.contrib import messages
from django.shortcuts import redirect

class CheckTypeParameter:
    def dispatch(self, request, *args, **kwargs):
        type_parameter = request.GET.get('type')
        allow_parameter_types = ['export','import']
        
        if not type_parameter:
            messages.error(request=self.request, message='Type parameter is mandatory in the last view, please send and try again.')
            return redirect('xlsx:config_grid')
        
        if type_parameter not in allow_parameter_types:
            messages.error(request=self.request, message='Type parameter value is currently wrong, please ensure type parameter value is export or import and check again.')
            return redirect('xlsx:config_grid')
        
        return super().dispatch(request, *args, **kwargs)
    