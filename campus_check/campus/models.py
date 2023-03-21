from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Avg
from django.template.defaultfilters import slugify

class Location(models.Model):
    name = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Locations'

class Degree(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Degrees'

class University(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    degree = models.ManyToManyField(Degree, related_name='universities')
    logo = models.ImageField(upload_to='university_logos')
    description = models.TextField()
    website = models.URLField()
    contact_email = models.EmailField()
    slug = models.SlugField(unique=True)
    average_rating = models.FloatField(default=0)  #Xuanming Feng

    @property
    def avg_rating(self):
        course_reviews = Review.objects.filter(course__university=self)
        if course_reviews.exists():
            value_for_money_avg = course_reviews.aggregate(Avg('value_for_money'))['value_for_money__avg']
            teaching_quality_avg = course_reviews.aggregate(Avg('teaching_quality'))['teaching_quality__avg']
            course_content_avg = course_reviews.aggregate(Avg('course_content'))['course_content__avg']
            job_prospects_avg = course_reviews.aggregate(Avg('job_prospects'))['job_prospects__avg']
            return (value_for_money_avg + teaching_quality_avg + course_content_avg + job_prospects_avg) / 4
        else:
            return None
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(University, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Universities'

class Course(models.Model):
    name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=10)
    description = models.TextField()
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='courses')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.course_code}: {self.name}"
    class Meta:
        verbose_name_plural = 'Courses'


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    university = models.ForeignKey('University', on_delete=models.CASCADE)
    degree = models.ForeignKey('Degree', on_delete=models.CASCADE)
    courses = models.ManyToManyField('Course', related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.university} ({self.degree})'

    class Meta:
        verbose_name_plural = 'Enrollments'

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.ForeignKey('University', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    value_for_money = models.IntegerField()
    teaching_quality = models.IntegerField()
    course_content = models.IntegerField()
    job_prospects = models.IntegerField()
    review_text = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.university} ({self.course})'
    
    class Meta:
        verbose_name_plural = 'Reviews'


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}\'s profile'

    class Meta:
        verbose_name_plural = 'StudentProfiles'
