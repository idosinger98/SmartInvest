from django.contrib.auth.decorators import login_required
from review.forms import ReviewForm
from review.models import Review
from users.models import Profile
from datetime import datetime
from django.http import HttpResponse


@login_required
def create_review_view(request):
    profile = Profile.objects.filter(user_id=request.user)[0]
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = Review.objects.create(publisher_id=profile, content=form.cleaned_data['content'],
                                           rating=form.cleaned_data['rating'], date=datetime.now())

            review.save()
            return HttpResponse()
        else:
            return HttpResponse()


@login_required
def delete_review(request):
    review = Review.objects.filter(publisher_id__user_id=request.user)[0]
    review.delete()
    return HttpResponse()
