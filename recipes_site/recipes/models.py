from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
	title = models.CharField(max_length=200, verbose_name="Название")
	description = models.TextField(verbose_name="Краткое описание")
	full_text = models.TextField(verbose_name="Подробное описание")
	ingredients = models.TextField(verbose_name="Ингредиенты")
	steps = models.TextField(verbose_name="Шаги приготовления")
	image = models.ImageField(upload_to='recipes/', blank=True, null=True, verbose_name="Изображение")
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', verbose_name="Автор")

	def rating_avg(self):
		ratings = self.ratings.all()
		if ratings.exists():
			return round(sum(r.value for r in ratings) / ratings.count(), 2)
		return 0

	def __str__(self):
		return self.title

class Rating(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings', verbose_name="Пользователь")
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings', verbose_name="Рецепт")
	value = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Оценка")

	class Meta:
		unique_together = ('user', 'recipe')

	def __str__(self):
		return f"{self.user.username} - {self.recipe.title}: {self.value}"

class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="Пользователь")
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments', verbose_name="Рецепт")
	text = models.TextField(verbose_name="Текст комментария")
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

	def __str__(self):
		return f"{self.user.username} - {self.recipe.title}"
