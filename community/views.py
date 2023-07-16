from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from community.models import Post, Comment
from users.models import Profile
from django.http import JsonResponse
from community.forms import CreateCommentForm


def community(request):
    posts = Post.objects.sort_posts_by_popularity()
    context = {'posts': posts}
    return render(request, 'community/community.html', context)


def show_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.get_all_comments_on_post(post_id=pk)
    context = {'posts': Post.objects.all().values, 'post': post, 'comments': comments}
    return render(request, 'community/post-details.html', context)


# @csrf_exempt

def like_post(request, post_id, profile_id):
    post = Post.objects.get(pk=post_id)
    is_liked = post.likes.filter(pk=profile_id).exists()
    if is_liked:
        Post.objects.unlike_post(post_id=post_id, profile_id=profile_id)
    else:
        Post.objects.like_post(post_id=post_id, profile_id=profile_id)

    return JsonResponse({'likes': post.likes.count(), 'is_liked': is_liked})


def like_comment(request, comment_id, profile_id):
    comment = Comment.objects.get(pk=comment_id)
    is_liked = comment.likes.filter(pk=profile_id).exists()
    if is_liked:
        Comment.objects.unlike_comment(comment_id=comment_id, profile_id=profile_id)
    else:
        Comment.objects.like_comment(comment_id=comment_id, profile_id=profile_id)

    return JsonResponse({'likes': comment.likes.count(), 'is_liked': is_liked})


def check_like(request, postId):
    post_id = request.GET.get('post_id')
    profile_id = request.GET.get('profile_id')

    post = Post.objects.get(pk=post_id)
    profile = Profile.objects.get(pk=profile_id)

    liked = post.likes.filter(pk=profile_id).exists()

    return JsonResponse({'liked': liked})


def check_comment_like(request, commentId):
    comment_id = request.GET.get('comment_id')
    profile_id = request.GET.get('profile_id')

    comment = Comment.objects.get(pk=comment_id)
    profile = Profile.objects.get(pk=profile_id)

    liked = comment.likes.filter(pk=profile_id).exists()

    return JsonResponse({'liked': liked})


@csrf_exempt
def create_comment(request, post_id, profile_id):
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            publisher = Profile.objects.get(pk=profile_id)
            post = Post.objects.get(pk=post_id)
            # Create the comment
            comment = Comment.objects.comment_post(post_id=post, content=content, publisher_id=publisher)

            post = get_object_or_404(Post, pk=post_id)
            comments = Comment.objects.get_all_comments_on_post(post_id=post_id)
            context = {'posts': Post.objects.all().values, 'post': post, 'comments': comments}

            return render(request, 'community/post-details.html', context)

    # If the request is not a POST request or the form is invalid, render the template with the form
    else:
        form = CreateCommentForm()

    return show_post(request=request, pk=post_id)

# def create_comment(request, postId, profile_id):
#     comment = Comment.objects.get(pk=comment_id)
#     is_liked = comment.likes.filter(pk=profile_id).exists()
#     if is_liked:
#         Comment.objects.unlike_comment(comment_id=comment_id, profile_id=profile_id)
#     else:
#         Comment.objects.like_comment(comment_id=comment_id, profile_id=profile_id)
#
#     return JsonResponse({'likes': comment.likes.count(), 'is_liked': is_liked})
#     template_name = 'post-detail.html'
#     post = get_object_or_404(Post, pk=postId)
#     new_comment = None
#     # Comment posted
#     if request.method == 'POST':
#         comment_form = CreateCommentForm(data=request.POST)
#         if comment_form.is_valid():
#
#             # Create Comment object but don't save to database yet
#             # new_comment = comment_form.save(commit=False)
#             # Assign the current post to the comment
#             content = comment_form.cleaned_data['content']
#             Comment.objects.comment_post(post_id=postId, content=content, publisher_id=profile_id)
#             # new_comment.post = post
#             # # Save the comment to the database
#             # new_comment.save()
#             return render(request, template_name)
#     else:
#         comment_form = CommentForm()
#
#     return render(request, template_name, {'form': comment_form})
#
#
# def post_detail(request, slug):
#     template_name = 'post-detail.html'
#     post = get_object_or_404(Post, slug=slug)
#     comments = post.comments.filter(active=True)
#     new_comment = None
#     # Comment posted
#     if request.method == 'POST':
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#
#             # Create Comment object but don't save to database yet
#             new_comment = comment_form.save(commit=False)
#             # Assign the current post to the comment
#             new_comment.post = post
#             # Save the comment to the database
#             new_comment.save()
#     else:
#         comment_form = CommentForm()
#
#     return render(request, template_name, {'post': post,
#                                            'comments': comments,
#                                            'new_comment': new_comment,
#                                            'comment_form': comment_form})
