import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_check_project.settings')

import django
django.setup()
from campus.models import University, Course, Location, Degree, User, Enrollment

def populate():
        email = 'student@gmail.com'
        user = User.objects.create_user(email, email, 'password')
        # Enroll the user in a course at a university
        university = University.objects.first()
        degree = Degree.objects.first()
        course = Course.objects.first()
        enrollment = Enrollment.objects.create(user_email=email, university=university, degree=degree)
        enrollment.courses.add(course)
#     scotland_universities = [
#     {
#         'name': 'University of Glasgow',
#         'location': {
#             'name': 'Glasgow',
#             'latitude': 55.8721,
#             'longitude': -4.2882
#         },
#         'degree': {
#             'name': 'Computer Science',
#             'description': 'This degree focuses on computer programming, algorithms, data structures, and computer systems.'
#         },
#         'courses': [
#             {
#                 'name': 'Programming Foundations',
#                 'course_code': 'COMP08012',
#                 'description': 'This course introduces students to the fundamental concepts of computer programming.'
#             },
#             {
#                 'name': 'Algorithms and Data Structures',
#                 'course_code': 'COMP08020',
#                 'description': 'This course covers the design and analysis of algorithms and the implementation of data structures.'
#             }
#         ],
#         'logo': 'https://www.gla.ac.uk/media/Media_569052_smxx.jpg',
#         'description': 'The University of Glasgow is a public research university located in Glasgow, Scotland. It was founded in 1451 and is the fourth-oldest university in the English-speaking world.',
#         'website': 'https://www.gla.ac.uk/',
#         'contact_email': 'enquiries@gla.ac.uk'
#     }
# ]

#     for uni_data in scotland_universities:
#         location_data = uni_data['location']
#         location = add_location(
#             location_data['name'],
#             location_data['latitude'],
#             location_data['longitude']
#         )
#         degree_data = uni_data['degree']
#         degree = add_degree(
#             degree_data['name'],
#             degree_data['description']
#         )
#         uni = add_university(
#             uni_data['name'],
#             uni_data['logo'],
#             uni_data['description'],
#             uni_data['website'],
#             uni_data['contact_email'],
#             location
#         )
#         add_uni_location_degree(uni, location, degree)
#         for course_data in uni_data['courses']:
#             add_course(
#                 uni,
#                 course_data['name'],
#                 course_data['course_code'],
#                 course_data['description']
#             )


# def add_university(name, logo, description, website, contact_email, location):
#     u = University.objects.get_or_create(
#         name=name,
#         logo=logo,
#         description=description,
#         website=website,
#         contact_email=contact_email,
#         location=location
#     )[0]
#     u.save()
#     return u


# def add_location(name, latitude, longitude):
#     l = Location.objects.get_or_create(
#         name=name,
#         latitude=latitude,
#         longitude=longitude
#         )[0]
#     l.save()
#     return l

# def add_degree(name, description):
#     d = Degree.objects.get_or_create(
#         name=name,
#         description=description
#         )[0]
#     d.save()
#     return d

# def add_course(university, name, course_code, description):
#     c = Course.objects.get_or_create(
#         university=university,
#         name=name,
#         course_code=course_code,
#         description=description
#         )[0]
#     c.save()
#     return c

# def add_uni_location_degree(university, location, degree):
#     university.location = location
#     university.degree.set([degree])
#     university.save()



if __name__ == '__main__':
    print('Starting population script...')
    populate()