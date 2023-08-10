from django.shortcuts import render
from django.core.paginator import Paginator
from community.models import Post


def community(request):
    posts = Post.objects.order_by('-time')
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    paginated_posts = paginator.get_page(page_number)

    context = {
        'paginated_posts': paginated_posts
    }

    return render(request, 'community/community.html', context)
