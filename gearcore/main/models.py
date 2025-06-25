from django.db import models

class MainPage(models.Model):
    description = models.TextField(verbose_name="Текст на голонвій")
    
    class Meta:
        verbose_name = 'головна сторінка'
        verbose_name_plural = 'головні сторінки'


class Slide(models.Model):
    image = models.FileField(upload_to="slides", verbose_name='зображення слайду')
    description = models.TextField(max_length=500, verbose_name='опис до зображення', null=True, blank=True)
    alt = models.CharField(max_length=100, verbose_name='що на картинці? ', null=True, blank=True)
    order = models.PositiveSmallIntegerField(default=0, verbose_name='позиція слайду')
    main_page = models.ForeignKey(
        MainPage, 
        on_delete=models.RESTRICT, 
        related_name='slides',
        verbose_name="Головна сторінка"
    )
    
    class Meta:
        verbose_name = "слайд"
        verbose_name_plural = "слайди"
        ordering = ["order"]

    def __str__(self):
        return f'Слайд - {self.order}'





