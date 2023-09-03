from django.shortcuts import render
from review.models import Review
from review.forms import ReviewForm
from community.models import Post
from stockAnalysis.views import get_biggest_indices
import json
from landingPage.forms import ContactForm
from django.http import HttpResponse, HttpResponseBadRequest
from utils.email_utils import connectedApiAndSendEmail
from dotenv import load_dotenv
from users.models import Profile
from stockAnalysis.models import StockSymbol, AnalyzedStock

load_dotenv()


def home(request, return_after_wrong_symbol=False):
    list_review = Review.objects.get_all_reviews()
    last_three_posts = Post.objects.get_posts_with_image(
        [post.id for post in Post.objects.sort_posts_by_time()[:3]]
    )
    for post in last_three_posts:
        post.stock_image = json.loads(post.stock_image).get('image', None)

    response_dict = json.loads(get_biggest_indices(request=request).content)
    best_stocks = [{'name': key, 'price': f"{round(float(value), 2)} USD"} for key, value in response_dict.items()]
    form = ReviewForm()
    from_contant = ContactForm()
    stocks_names = StockSymbol.objects.values_list('symbol', flat=True)
    sorted_stocks_names = sorted(stocks_names)
    clients = Profile.objects.count()
    posts = Post.objects.count()
    review_avg = Review.objects.get_average_rating()
    my_analysis = AnalyzedStock.objects.filter(analyst_id=request.user).count() if request.user.is_authenticated else 0

    # Check if the user is authenticated before filtering by user ID
    if request.user.is_authenticated:
        review_by_user = Review.objects.filter(publisher_id__user_id=request.user.id)
    else:
        review_by_user = None

    context = {'list_review': list_review, 'form': form, 'from_contant': from_contant,
               'last_three_posts': last_three_posts, 'best_stocks': best_stocks,
               'wrong_symbol': return_after_wrong_symbol, 'stocks_names': sorted_stocks_names, 'clients': clients,
               'posts': posts, 'review_by_user': review_by_user, 'my_analysis': my_analysis, 'review': review_avg}

    return render(request, 'landingPage/landing_page.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            body = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message'],
            }
            message = f"Name: {body['name']}<br><br>Email: {body['email']}<br><br>Message: {body['message']}"
            if connectedApiAndSendEmail(subject_str=form.cleaned_data['subject'], content=message):
                return HttpResponse()

    return HttpResponseBadRequest()
