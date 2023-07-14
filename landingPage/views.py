from django.shortcuts import render
from review.models import Review
from review.forms import ReviewForm
from contact.forms import ContactForm
from community.models import Post


def home(request):
    list_review = Review.objects.get_all_reviews()
    last_three_posts = Post.objects.sort_posts_by_time()[:3]
    form = ReviewForm()
    from_contant = ContactForm()
    return render(request, 'landingPage/landing_page.html', {'list_review': list_review, 'form': form,
                                                             'from_contant': from_contant,
                                                             'last_three_posts': last_three_posts})
