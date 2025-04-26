# Django импорты
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, JsonResponse
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Celery импорты
from celery import current_app   
from celery.result import AsyncResult

# Локальные импорты
from .models import *
from mainapp.utils import *
from tasks import *
from utils.redis_client import redis_client

# Стандартные библиотеки Python
import json
import os

# Главная страница
def mainpage(request):
    apps = App.objects.all()
    context = {'apps': apps}
    return render(request, 'mainapp/index.html', context)


# Страница транскрибации
def extract_audio(request):
    ip_address = get_client_ip(request)  

    if request.method == "GET":
        redis_data = redis_client.get(ip_address) 

        if redis_data:
            redis_data = json.loads(redis_data)
            return render(request, 'mainapp/extract_audio.html', {**redis_data})
        else:
            return render(request, 'mainapp/extract_audio.html')

    if request.method == "POST" and request.FILES.get('file'):
        uploaded_file = request.FILES['file']  
        language = request.POST.get('language', 'auto')
        accuracy = int(request.POST.get('accuracy', 2)) 

        # Генерируем уникальное имя для файла
        file_name = get_unique_filename(uploaded_file.name)
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name)

        # Создаем запись в Redis о статусе
        redis_client.set(ip_address, json.dumps({
            "upload_status": "in_progress",
            "transcribe_status": "pending",
            "transcribed_text": ""
        }))
        
        # Сохраняем файл на сервер
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Создаем запись о файле в БД
        uploaded_file_record = UploadedFile.objects.create(
            ip_address=ip_address,
            file_path=f'uploads/{file_name}',
            file_name=file_name
        )

        # Запуск задачи загрузки файла
        task = upload_file_task.apply_async(args=[ip_address, save_path, language, accuracy])
        redis_client.set(f"{ip_address}_task_id", task.id)  # Сохраняем task_id в Redis

        # Отправляем ответ с данными на страницу
        return render(request, 'mainapp/extract_audio.html', {'upload_status': 'in_progress'})

    return render(request, 'mainapp/extract_audio.html')


# Удаления данных пользователя из Redis
@csrf_exempt  
def delete_ip_record(request):

    if request.method == "POST":
        ip = get_client_ip(request) 

        # Проверяем, есть ли запись в Redis
        if redis_client.exists(ip):
            redis_client.delete(ip)  # Удаляем запись

            # Получаем task_id из Redis
            task_id = redis_client.get(f"{ip}_task_id")
            if task_id:
                task = AsyncResult(task_id, app=current_app)  
                task.revoke(terminate=True)

            return JsonResponse({"message": "Данные и задача удалены"}, status=200)

        else:
            return JsonResponse({"message": "Запись не найдена"}, status=404)

    return JsonResponse({"message": "Неверный метод запроса"}, status=400)


@csrf_exempt
def check_upload_status(request):
    ip = request.META.get('REMOTE_ADDR') 

    client_data = redis_client.get(ip)

    if client_data:
        return JsonResponse({'status': 'found', 'client_data': client_data})
    else:
        return JsonResponse({'status': 'not_found'})
    


# ИЗОБРАЖЕНИЕ
def extract_photo(request):
    ip_address = get_client_ip(request)  

    if request.method == "GET":
        
        redis_data = redis_client.get(ip_address) 

        if redis_data:
            redis_data = json.loads(redis_data)
            return render(request, 'mainapp/extract_photo.html', {**redis_data})
        else:
            return render(request, 'mainapp/extract_photo.html')

    if request.method == "POST" and request.FILES.get('file'):
        uploaded_file = request.FILES['file']  

        # Генерируем уникальное имя для файла
        file_name = get_unique_filename(uploaded_file.name)
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name)

        # Создаем запись в Redis о статусе
        redis_client.set(ip_address, json.dumps({
            "upload_status": "in_progress",
            "transcribe_status": "pending",
            "transcribed_text": ""
        }))
        
        # Сохраняем файл на сервер
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Создаем запись о файле в БД
        uploaded_file_record = UploadedFile.objects.create(
            ip_address=ip_address,
            file_path=f'uploads/{file_name}',
            file_name=file_name
        )

        # Запуск задачи загрузки файла
        task = upload_img_task.apply_async(args=[ip_address, save_path])
       
        redis_client.set(f"{ip_address}_task_id", task.id)  # Сохраняем task_id в Redis

        return render(request, 'mainapp/extract_photo.html', {'upload_status': 'in_progress'})

    return render(request, 'mainapp/extract_photo.html')



# PDF
def extract_pdf(request):
    ip_address = get_client_ip(request)  

    if request.method == "GET":
        redis_data = redis_client.get(ip_address)

        if redis_data:
            redis_data = json.loads(redis_data)
            return render(request, 'mainapp/extract_pdf.html', {**redis_data})
        else:
            return render(request, 'mainapp/extract_pdf.html')

    if request.method == "POST" and request.FILES.get('file'):
        uploaded_file = request.FILES['file']  

        # Генерируем уникальное имя для файла
        file_name = get_unique_filename(uploaded_file.name)
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name)

        # Создаем запись в Redis о статусе
        redis_client.set(ip_address, json.dumps({
            "upload_status": "in_progress",
            "transcribe_status": "pending",
            "transcribed_text": ""
        }))
        
        # Сохраняем файл на сервер
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Создаем запись о файле в БД
        uploaded_file_record = UploadedFile.objects.create(
            ip_address=ip_address,
            file_path=f'uploads/{file_name}',
            file_name=file_name
        )

        # Запуск задачи загрузки файла
        task = upload_pdf_task.apply_async(args=[ip_address, save_path])
       
        redis_client.set(f"{ip_address}_task_id", task.id)  # Сохраняем task_id в Redis

        return render(request, 'mainapp/extract_pdf.html', {'upload_status': 'in_progress'})

    return render(request, 'mainapp/extract_pdf.html')