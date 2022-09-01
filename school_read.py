import sqlite3


con = sqlite3.connect('db_school.sqlite')
cur = con.cursor()

# show subjects and their teachers (if any) + comments
cur.execute('''
SELECT subjects.name,
       teachers.name,
       subjects.description
FROM subjects
LEFT JOIN teachers ON subjects.teachers = teachers.id;
''')

for result in cur:
    print(result)
print()

# show each class, its major (if any), its teachers
# and the subjects they study with these teachers
cur.execute('''
SELECT classes.stage,
       classes.course_year,
       majors.name,
       teachers.name,
       subjects.name
FROM classes
JOIN teachers_classes ON teachers_classes.class_id = classes.id
JOIN teachers ON teachers_classes.teacher_id = teachers.id
LEFT JOIN majors ON classes.major = majors.id
JOIN subjects ON teachers_classes.subjects = subjects.id
ORDER BY classes.stage DESC,
         classes.course_year;
''')

for result in cur:
    print(result)
print()

# show teachers names, the year they joined school (if any)
# and the link to their cv (if any)
cur.execute('''
SELECT teachers.name,
       teachers_cvs.joining_year,
       teachers_cvs.link_to_cv
FROM teachers
LEFT JOIN teachers_cvs ON teachers.cv = teachers_cvs.id
WHERE teachers.primary_school = 1;
''')

for result in cur:
    print(result)
print()

con.close()
