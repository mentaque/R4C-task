import os
from datetime import datetime, timedelta

from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from openpyxl.workbook import Workbook

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


def download_excel(request):
    workbook = Workbook()

    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday() + 7)

    models = Robot.objects.values('model').distinct()

    for model_info in models:
        model = model_info['model']
        worksheet = workbook.create_sheet(title=model)
        worksheet.append(['Модель', 'Версия', 'Количество за неделю'])

        robots = Robot.objects.filter(
            model=model, created__gte=start_of_week
        ).values('version').annotate(total_quantity=Count('version'))

        for robot in robots:
            worksheet.append([model, robot['version'], robot['total_quantity']])

    default_sheet = workbook.get_sheet_by_name('Sheet')
    workbook.remove(default_sheet)

    file_path = 'robots-info.xlsx'

    workbook.save(file_path)

    with open(file_path, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="robots-info.xlsx"'

    os.remove(file_path)

    return response