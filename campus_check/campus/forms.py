from django import forms
from .models import Review, Enrollment, StudentProfile

class CourseReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('value_for_money', 'teaching_quality', 'course_content', 'job_prospects', 'review_text')
        widgets = {
            'value_for_money': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'teaching_quality': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'course_content': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'job_prospects': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'review_text': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        self.course = kwargs.pop('course')
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        enrollment = Enrollment.objects.filter(user=self.user, courses=self.course).first()
        if not enrollment:
            raise forms.ValidationError("You cannot review a course that you have not enrolled in.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        instance.university = self.course.university
        instance.course = self.course
        if commit:
            instance.save()
        return instance


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['email', 'first_name', 'last_name', 'date_of_birth']

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))