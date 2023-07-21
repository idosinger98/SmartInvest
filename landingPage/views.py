from django.shortcuts import render
from review.models import Review
from review.forms import ReviewForm
from contact.forms import ContactForm
from community.models import Post
from stockAnalysis.views import get_biggest_indices
import json
from django.http import JsonResponse


def home(request):
    list_review = Review.objects.get_all_reviews()
    last_three_posts = Post.objects.sort_posts_by_time()[:3]

    response_dict = json.loads(get_biggest_indices(request=request).content)
    best_stocks = [{'name': key, 'price': f"{round(float(value), 2)} USD"} for key, value in response_dict.items()]

    form = ReviewForm()
    from_contant = ContactForm()
    context = {'list_review': list_review, 'form': form, 'from_contant': from_contant,
               'last_three_posts': last_three_posts, 'best_stocks': best_stocks}
    return render(request, 'landingPage/landing_page.html', context)
