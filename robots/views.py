from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import RobotForm
import json


@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        serial = f"{data.get('model')}-{data.get('version')}"
        data['serial'] = serial
        form = RobotForm(data)

        if form.is_valid():
            form.save()
            response_data = {'message': 'Запись успешно создана'}
            return JsonResponse(response_data, status=201)
        else:
            errors = form.errors
            return JsonResponse(errors, status=400)

    response_data = {'error': 'Method not allowed'}
    return JsonResponse(response_data, status=405)