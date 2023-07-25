import sqlite3


con = sqlite3.connect('db_school.sqlite')
cur = con.cursor()

# show subjects and their teachers (if any) + comments
cur.execute('''
SELECT subjects.name,
       teachers.name,
       subjects.description
FROM subjects
LEFT JOIN teachers ON subjects.teacher_id = teachers.id;
''')

print()
for result in cur:
    if result[1] is not None:
        result_str = f'The teacher {result[1]} teaches {result[0]}'
        if result[2] is not None:
            result_str += f' ({result[2].strip(".")}).'
        else:
            result_str += '.'
    else:
        result_str = f'A teacher for the subject {result[0]} is absent.'
        if result[2] is not None:
            result_str += f' {result[2]}'
    print(result_str)
print()

# show each class, its major (if any), its teachers
# and the subjects tought to this class by this teacher
cur.execute('''
SELECT classes.level,
       classes.course_year,
       majors.name,
       teachers.name,
       subjects.name
FROM classes
LEFT JOIN majors ON classes.major_id = majors.id
JOIN teachers_classes ON teachers_classes.class_id = classes.id
JOIN teachers ON teachers_classes.teacher_id = teachers.id
JOIN subjects ON teachers_classes.subject_id = subjects.id
ORDER BY classes.level DESC,
         classes.course_year;
''')

primary_count = 0
high_count = 0
humanities_count = 0
sciences_count = 0
print('2023 classes: subjects and teachers assigned:')
for result in cur:
    if result[0] == 'Primary':
        if primary_count < 1:
            print('Primary school (no majors)')
            primary_count += 1
    elif result[0] == 'High':
        if high_count < 1:
            print('High school')
            high_count += 1
    if result[2] == 'Humanities':
        if humanities_count < 1:
            print('Major: Humanities')
            humanities_count += 1
    elif result[2] == 'Sciences':
        if sciences_count < 1:
            print('Major: Sciences')
            sciences_count += 1
    print(f'{result[1]}: {result[4]} - {result[3]}')
print()

# show teachers names, the year they joined school (if any)
# and if ther cv is available (if any)
cur.execute('''
SELECT teachers.name,
       teachers_cvs.joining_year,
       teachers_cvs.link_to_cv
FROM teachers
LEFT JOIN teachers_cvs ON teachers.cv_id = teachers_cvs.id
WHERE teachers.primary_school = 1;
''')

for result in cur:
    if result[1] is not None:
        result_str = (
            f'{result[0]} joined the school in {result[1]}.'
        )
        if result[2] is not None:
            result_str += ' Their CV is available at the school office.'
    else:
        result_str = f'The year when {result[0]} joined the school is unknown.'
    print(result_str)
print()

con.close()
