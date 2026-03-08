
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Recipe

@login_required
@require_POST
def ajax_rate_recipe(request, pk):
    from .models import Recipe, Rating
    recipe = Recipe.objects.get(pk=pk)
    value = int(request.POST.get('rating', 0))
    if value < 1 or value > 5:
        return JsonResponse({'error': 'Некорректная оценка'}, status=400)
    rating, created = Rating.objects.update_or_create(
        user=request.user, recipe=recipe,
        defaults={'value': value}
    )
    avg = recipe.rating_avg()
    return JsonResponse({'success': True, 'avg': avg, 'user_rating': value})

@login_required
@require_POST
def ajax_add_comment(request, pk):
    from .models import Recipe, Comment
    recipe = Recipe.objects.get(pk=pk)
    text = request.POST.get('comment', '').strip()
    if not text:
        return JsonResponse({'error': 'Комментарий не может быть пустым'}, status=400)
    comment = Comment.objects.create(user=request.user, recipe=recipe, text=text)
    return JsonResponse({
        'success': True,
        'username': comment.user.username,
        'text': comment.text,
        'created_at': comment.created_at.strftime('%d.%m.%Y %H:%M')
    })

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('/')
	else:
		form = UserCreationForm()
	return render(request, 'registration/register.html', {'form': form})

@login_required
def recipe_list(request):
	recipes = Recipe.objects.all().order_by('-created_at')
	return render(request, 'recipe_list.html', {'recipes': recipes})

@login_required
def recipe_detail(request, pk):
	from .models import Comment, Rating
	recipe = Recipe.objects.get(pk=pk)
	user_rating = None
	# Обработка POST-запроса для оценки или комментария
	if request.method == 'POST':
		if 'rating' in request.POST and request.POST['rating']:
			value = int(request.POST['rating'])
			rating, created = Rating.objects.update_or_create(
				user=request.user, recipe=recipe,
				defaults={'value': value}
			)
		if 'comment' in request.POST and request.POST['comment'].strip():
			Comment.objects.create(
				user=request.user,
				recipe=recipe,
				text=request.POST['comment'].strip()
			)
		return redirect('recipe_detail', pk=pk)

	comments = recipe.comments.select_related('user').order_by('-created_at')
	if request.user.is_authenticated:
		user_rating = Rating.objects.filter(user=request.user, recipe=recipe).first()
	return render(request, 'recipe_detail.html', {
		'recipe': recipe,
		'comments': comments,
		'user_rating': user_rating,
	})
