from django.shortcuts import render,redirect
from django.contrib.auth.models import Group
from django.db.models import Avg,Count
from django.http import HttpResponse
from .models import Review
from collections import defaultdict

def groups(request):
    current_user = request.user
    if (current_user.is_teacher):
        groups = Group.objects.all()
        group_dict = defaultdict(list)
        query_results = Review.objects.values('group_id','review_no').annotate(marks=Avg('marks')).order_by('group_id','review_no')
        for query_result in query_results:
            group = query_result['group_id']
            review_no = query_result['review_no']
            if (review_no == 2 and group not in group_dict):
                group_dict[group].append(None)
            group_dict[group].append(int(query_result['marks']))
        for group in group_dict:
            if (len(group_dict[group]) < 2):
                group_dict[group].append(None)
        context = {
            'groups': group_dict.items()        
        }
        return render(request,'reviews/groups.html',context)
    else:
        return redirect('home')


def reviews(request,group_id):
    current_user = request.user
    group = Group.objects.filter(id=group_id)
    if (current_user.is_authenticated and current_user.is_teacher and group.exists()):
        group = group[0]
        reviews = Review.objects.filter(group=group)
        context = {
            'reviews': reviews
        }
        return render(request,'reviews/reviews.html',context)
    else:
        return redirect('home')


def create(request):
    current_user = request.user
    if (current_user.is_teacher):
        if (request.method == 'POST'):
            group_id = request.POST['group_id']
            group = Group.objects.filter(id=group_id)
            if (group.exists()):
                group = group[0]
                marks = request.POST['marks']
                review_no = request.POST['review_no']
                review = Review(group=group,marks=marks,review_no=review_no,reviewer=current_user)
                review.save()
                return render(request,'reviews/create.html')
            else:
                return render(request,'reviews/create.html')
        else:
            return render(request,'reviews/create.html')
    else:
        return redirect('home')


def update(request):
    current_user = request.user
    if (current_user.is_teacher):
        review_id = request.POST['id']
        review = Review.objects.get(id=review_id)
        group = review.group
        marks = request.POST['marks']
        review_no = request.POST['review_no']
        reviewer = review.reviewer
        review = Review(id=review_id,group=group,marks=marks,reviewer=reviewer,review_no=review_no)
        review.save()
        print('review saved')
        return redirect('/reviews/reviews/'+str(group.id))
    else:
        return redirect('home')


def delete(request):
    current_user = request.user
    if (current_user.is_teacher):
        review = Review.objects.get(id=request.POST['id'])
        group = review.group
        review.delete()
        return redirect('/reviews/reviews/'+str(group.id))
    else:
        return redirect('home')
