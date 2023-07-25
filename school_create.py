import sqlite3

con = sqlite3.connect('db_school.sqlite')
cur = con.cursor()

cur.executescript('''
CREATE TABLE IF NOT EXISTS subjects(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    teachers INTEGER,
      FOREIGN KEY(teachers) REFERENCES teachers(id)
);

CREATE TABLE IF NOT EXISTS majors(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS classes(
    id INTEGER PRIMARY KEY,
    level TEXT NOT NULL,
    course_year TEXT NOT NULL,
    major INTEGER,
      FOREIGN KEY(major) REFERENCES majors(id)
);

CREATE TABLE IF NOT EXISTS teachers_cvs(
    id INTEGER PRIMARY KEY,
    teacher_name TEXT NOT NULL,
    joining_year INTEGER,
    link_to_cv TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS teachers(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    primary_school INTEGER NOT NULL,
    high_school INTEGER NOT NULL,
    cv INTEGER UNIQUE,
      FOREIGN KEY(cv) REFERENCES teachers_cvs(id)
);

CREATE TABLE IF NOT EXISTS teachers_classes(
    teacher_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    PRIMARY KEY (teacher_id, class_id, subject_id),
      FOREIGN KEY(teacher_id) REFERENCES teachers(id),
      FOREIGN KEY(class_id) REFERENCES classes(id),
      FOREIGN KEY(subject_id) REFERENCES subjects(id)
);
''')

cur.executescript('''
ALTER TABLE subjects
RENAME COLUMN teachers TO teacher_id;

ALTER TABLE classes
RENAME COLUMN major TO major_id;

ALTER TABLE teachers
RENAME COLUMN cv TO cv_id;
''')

subjects = [
    # id, name, description (nullable), teachers
    (1, 'English (level 1)', 'English for primary school.', 2),
    (2, 'English (level 2)', 'English for high school.', 2),
    (3, 'Maths', None, 4),
    (4, 'Biology', 'Currently looking for a teacher.', None),
    (5, 'Physics', None, 4),
    (6, 'Music', None, 3),
    (7, 'History (level 1)', 'History for primary school.', 1),
    (8, 'History (level 2)', 'History for high school.', 1),
    (9, 'Christianity', 'Brand new subject - teacher needed.', None),
]

majors = [
    (1, 'Sciences'),
    (2, 'Humanities'),
]

classes = [
    # id, level, course year, major
    (1, 'Primary', '1st year', None),
    (2, 'Primary', '3rd year', None),
    (3, 'High', '3rd year', 1),
    (4, 'Primary', '2nd year', None),
    (5, 'High', '1st year', 2),
    (6, 'High', '2nd year', 2),
]

teachers_cvs = [
    (1, 'Eric Smith', 2009, 'eric_smith_cv.pdf'),
    (2, 'Katia Green', 2012, 'katia_green_cv.pdf'),
    (3, 'Vasiliy Devyatov', None, 'vasiliy_d_cv.pdf'),
]

teachers = [
    # id, name, primary school (pseudo-boolean), high school (pseudo-boolean), cv (nullable)
    (1, 'Eric Smith', 1, 1, 1),
    (2, 'Katia Green', 1, 1, 2),
    (3, 'Bob Marley', 1, 0, None),
    (4, 'Vasiliy Devyatov', 0, 1, 3),
]

teachers_classes = [
    (1, 4, 7),  # Eric Smith (History, primary/high) | 2-primary| History (primary)
    (1, 5, 8),  # Eric Smith (History, primary/high) | 1-high, Humanities | History (high)
    (2, 6, 2),  # Katia Green (English, primary/high) | 2-high, Humanities | English (high)
    (2, 2, 1),  # Katia Green (English, primary/high) | 3-primary| English (primary)
    (3, 1, 6),  # Bob Marley (Music, primary) | 1-primary| Music
    (4, 3, 3),  # Vasiliy Devyatov (Maths, Physics, high) | 3-high, Sciences | Maths
    (4, 3, 5),  # Vasiliy Devyatov (Maths, Physics, high) | 3-high, Sciences | Physics
    (4, 6, 3),  # Vasiliy Devyatov (Maths, Physics, high) | 2-high, Humanities | Maths
    (4, 6, 5),  # Vasiliy Devyatov (Maths, Physics, high) | 2-high, Humanities | Physics
    (4, 5, 3),  # Vasiliy Devyatov (Maths, Physics, high) | 1-high, Humanities | Maths
    (3, 4, 6),  # Bob Marley, (Music, primary) | 2-primary| Music
    (3, 2, 6),  # Bob Marley, (Music, primary) | 3-primary| Music
    (2, 1, 1),  # Katia Green, (English primary/high) | 1-primary| English (primary)
    (1, 3, 8),  # Eric Smith, (History primary/high) | 3-high, Sciences | History (high)
]

cur.executemany('INSERT INTO subjects VALUES(?, ?, ?, ?);', subjects)
cur.executemany('INSERT INTO majors VALUES(?, ?);', majors)
cur.executemany('INSERT INTO classes VALUES(?, ?, ?, ?);', classes)
cur.executemany('INSERT INTO teachers_cvs VALUES(?, ?, ?, ?);', teachers_cvs)
cur.executemany('INSERT INTO teachers VALUES(?, ?, ?, ?, ?);', teachers)
cur.executemany('INSERT INTO teachers_classes VALUES(?, ?, ?);',
                teachers_classes)

con.commit()
con.close()
