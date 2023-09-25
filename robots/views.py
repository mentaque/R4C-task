from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import RobotForm
import json

from .models import Robot


@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        model = data.get('model')
        version = data.get('version')

        #Проверка на существующие модели в бд
        if not Robot.objects.filter(model=model, version=version).exists():
            response_data = {'error': f'Робот {model}-{version} не существует в системе'}
            return JsonResponse(response_data, status=400)

        serial = f"{model}-{version}"
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