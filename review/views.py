from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from review.forms import ReviewForm
from review.models import Review
from users.models import Profile
from datetime import datetime
from django.contrib import messages


@login_required
def createReviewView(request):
    profile = Profile.objects.filter(user_id=request.user)[0]
    if request.method == 'GET':
        form = ReviewForm()
        return render(request, 'review/create_review.html', {'form': form})
    elif request.method == 'POST':
        form = ReviewForm(request.POST)
        if Review.objects.filter(publisher_id=profile):
            messages.error(request, "You have already given a review on the site")
        elif form.is_valid():
            review = Review.objects.create(publisher_id=profile, content=form.cleaned_data['content'],
                                           rating=form.cleaned_data['rating'], date=datetime.now())
            review.save()
            return redirect('change_password')
        else:
            messages.error(request, "You must enter rating")

    return render(request, 'review/create_review.html', {'form': form})
