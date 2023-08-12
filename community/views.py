from django.shortcuts import render
from django.core.paginator import Paginator
from community.models import Post, Comment
from django.contrib.auth.decorators import login_required
from community.forms import PostForm, CommentForm
from stockAnalysis.models import AnalyzedStock
from django.utils import timezone
from django.http import HttpResponse
from users.models import Profile


def community(request):
    posts = Post.objects.order_by('-time')
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)

    context = {
        'paginated_posts': paginated_posts
    }

    return render(request, 'community/community.html', context)


@login_required
def create_post_view(request, pk):
    analyzedStock = AnalyzedStock.objects.filter(id=pk).first()
    post = Post.objects.filter(analysis_id=analyzedStock).first()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            if post:
                post.description = form.cleaned_data['description']
                post.title = form.cleaned_data['title']
                post.likes = 0
                post.time = timezone.now()
                post.save()
            else:
                post = Post.objects.create(analysis_id=analyzedStock, description=form.cleaned_data['description'],
                                           title=form.cleaned_data['title'], likes=0, time=timezone.now())
                post.save()
        else:
            return render(request, 'community/create_post.html', {'form': form, 'pk': pk})
    else:
        form = PostForm()
    return render(request, 'community/create_post.html', {'form': form, 'pk': pk})


def post_deatils(request, pk):
    post = Post.objects.filter(id=pk).first()
    comments = Comment.objects.get_all_comments_on_post(post.id)
    return render(request, 'community/post-details.html', {'post': post, 'comments': comments})


@login_required
def comment(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post = Post.objects.filter(id=post_id).first()
            profile = Profile.objects.filter(user_id=request.user).first()
            create_comment = Comment.objects.create(publisher_id=profile,
                                                    content=form.cleaned_data['content'],
                                                    post_id=post,
                                                    likes=0,
                                                    time=timezone.now())
            create_comment.save()
            return HttpResponse()

    return HttpResponse()
