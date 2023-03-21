from django.shortcuts import render, redirect, get_object_or_404
from .models import University, Course, Degree, Review, Enrollment, StudentProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CourseReviewForm, StudentProfileForm
from django.db.models import Avg, Sum
from django.http import JsonResponse
from django.db.models import Q



@login_required
def student_profile(request):
    try:
        profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        profile = StudentProfile(user=request.user)
        profile.save()

    reviews = Review.objects.filter(user=request.user)
    ratings_by_course = {}

    for review in reviews:
        if review.course_id not in ratings_by_course:
            ratings_by_course[review.course_id] = {
            'value_for_money': [review.value_for_money],
            'teaching_quality': [review.teaching_quality],
            'course_content': [review.course_content],
            'job_prospects': [review.job_prospects],
            'review_text': [review.review_text],
        }
        else:
            ratings_by_course[review.course_id]['value_for_money'].append(review.value_for_money)
            ratings_by_course[review.course_id]['teaching_quality'].append(review.teaching_quality)
            ratings_by_course[review.course_id]['course_content'].append(review.course_content)
            ratings_by_course[review.course_id]['job_prospects'].append(review.job_prospects)
            ratings_by_course[review.course_id]['review_text'].append(review.review_text)

    courses = Course.objects.all()

    for course in courses:
        if course.id in ratings_by_course:
            course.avg_rating = sum(ratings_by_course[course.id]['value_for_money'][:3]) / (4 * len(ratings_by_course[course.id]['value_for_money'][:3]))
            course.review_text = ratings_by_course[course.id]['review_text'][0]
        else:
            course.avg_rating = None
            course.review_text = None

    form = StudentProfileForm(instance=profile)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('universities:student_profile'))

    context = {
        'form': form,
        'courses': courses
    }

    return render(request, 'campus/student_profile.html', context)


@login_required
def submit_review(request, course_name_slug):
    course = get_object_or_404(Course, slug=course_name_slug)
    user = request.user
    try:
        enrollment = Enrollment.objects.get(user=user, courses=course)
    except Enrollment.DoesNotExist:
        enrollment = None

    if request.method == 'POST':
        form = CourseReviewForm(request.POST, course=course, user=user)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.user = user
            review.university = course.university
            review.save()
            return HttpResponseRedirect(reverse('universities:course_detail', args=[course.slug]))
    else:
        form = CourseReviewForm(course=course, user=user)

    return render(request, 'campus/submit_review.html', {'form': form, 'course': course, 'enrollment': enrollment})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('universities:university_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request, 'campus/index.html')



def university_list(request):
    universities = University.objects.all()
    search_term = request.GET.get('search')

    if search_term:
        # search across different fields
        universities = universities.filter(Q(name__icontains=search_term) | 
                                           Q(location__name__icontains=search_term) | 
                                           Q(degree__name__icontains=search_term) | 
                                           Q(courses__name__icontains=search_term))

    university_ratings = {}
    for university in universities:
        course_ratings = []
        courses = university.courses.all()
        for course in courses:
            reviews = course.review_set.all()
            if reviews:
                course_rating = (reviews.aggregate(
                    Avg('value_for_money'))['value_for_money__avg'] +
                                     reviews.aggregate(
                        Avg('teaching_quality'))['teaching_quality__avg'] +
                                     reviews.aggregate(
                        Avg('course_content'))['course_content__avg'] +
                                     reviews.aggregate(
                        Avg('job_prospects'))['job_prospects__avg']) / 4
                course_ratings.append(course_rating)
        if course_ratings:
            university_rating = sum(course_ratings) / len(course_ratings)
            university_ratings[university] = university_rating

    context = {
        'university_ratings': university_ratings,
    }
    return render(request, 'campus/university_list.html', context)


def university_detail(request, university_name_slug):
    university = get_object_or_404(University, slug=university_name_slug)
    courses = Course.objects.filter(university=university)
    course_ratings = []
    for course in courses:
        reviews = course.review_set.all()
        if reviews:
            course_rating = (reviews.aggregate(
                Avg('value_for_money'))['value_for_money__avg'] +
                                 reviews.aggregate(
                    Avg('teaching_quality'))['teaching_quality__avg'] +
                                 reviews.aggregate(
                    Avg('course_content'))['course_content__avg'] +
                                 reviews.aggregate(
                    Avg('job_prospects'))['job_prospects__avg']) / 4
            course_ratings.append(course_rating)
    if course_ratings:
        university_rating = sum(course_ratings) / len(course_ratings)
    else:
        university_rating = None
    context = {
        'university': university,
        'courses': courses,
        'university_rating': university_rating,
    }
    return render(request, 'campus/university_detail.html', context)



def course_detail(request, course_name_slug):
    course = get_object_or_404(Course, slug=course_name_slug)
    reviews = Review.objects.filter(course=course)
    rating = 0
    if reviews:
        rating = (reviews.aggregate(Sum('value_for_money'))['value_for_money__sum'] +
                  reviews.aggregate(Sum('teaching_quality'))['teaching_quality__sum'] +
                  reviews.aggregate(Sum('course_content'))['course_content__sum'] +
                  reviews.aggregate(Sum('job_prospects'))['job_prospects__sum']) / (4 * reviews.count())

    return render(request, 'campus/course_detail.html', {'course': course, 'rating': rating, 'reviews': reviews})


