from django.db import models


from django.db import models

class App(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название приложения")
    description = models.TextField(verbose_name="Описание приложения", help_text="Можно использовать HTML-теги")
    image = models.ImageField(upload_to='app_images/', verbose_name="Изображение")
    link = models.URLField(verbose_name="Ссылка на приложение")

    class Meta:
        verbose_name = "Приложение"
        verbose_name_plural = "Список приложений" 

    def __str__(self):
        return self.name
    

from django.utils.timezone import now

class UploadedFile(models.Model):
    ip_address = models.GenericIPAddressField()  
    upload_time = models.DateTimeField(default=now)  
    file_path = models.FileField(upload_to='uploads/')  
    file_name = models.CharField(max_length=255)  

    class Meta:
        verbose_name = "Статистика и данные"
        verbose_name_plural = "Статистика и данные " 

    def __str__(self):
        return f"{self.file_name} ({self.ip_address})"


class GraphicsSettings(models.Model):  
    enable_graphics = models.BooleanField(default=False, verbose_name="Включить графику")

    def __str__(self):
        return "Настройки графики"