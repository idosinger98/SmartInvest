from django.shortcuts import render
from review.models import Review
from review.forms import ReviewForm
from contact.forms import ContactForm
from community.models import Post
from stockAnalysis.views import get_biggest_indices
import json
from django.http import JsonResponse


def home(request, return_after_wrong_symbol=False):
    list_review = Review.objects.get_all_reviews()
    last_three_posts = Post.objects.sort_posts_by_time()[:3]

    response_dict = json.loads(get_biggest_indices(request=request).content)
    best_stocks = [{'name': key, 'price': f"{round(float(value), 2)} USD"} for key, value in response_dict.items()]

    form = ReviewForm()
    from_contant = ContactForm()

    stocks_names = ["PKG", "AAPL", "MSFT", "GOOG", "AMZN", "NVDA", "TSLA", "META", "JPM"]

    sorted_stocks_names = sorted(stocks_names)
    context = {'list_review': list_review, 'form': form, 'from_contant': from_contant,
               'last_three_posts': last_three_posts, 'best_stocks': best_stocks,
               'wrong_symbol': return_after_wrong_symbol, 'stocks_names': sorted_stocks_names}
    return render(request, 'landingPage/landing_page.html', context)
