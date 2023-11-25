import csv
import random
import math
import firebase_admin
from copy import deepcopy
from firebase_admin import credentials, auth
from tqdm.auto import tqdm

BASE_STUDENT_ID = 2200000
random.seed(42)

CLUSTER_COURSES = [
    ("BCD - Business, Communication and Design", ["Accountancy", "Air Transport Management",
     "Hospitality Business", "Digital Communications and Integrated Media"]),
    ("ENG - Engineering", ["Aerospace Engineering", "Aircraft Systems Engineering", "Civil Engineering", "Electronics and Data Engineering", "Electrical Power Engineering", "Engineering Systems", "Mechanical Design and Manufacturing Engineering", "Marine Engineering", "Mechatronics Systems", "Mechanical Engineering",
     "Naval Architecture and Marine Engineering", "Naval Architecture", "Robotics Systems", "Offshore Engineering", "Sustainable Infrastructure Engineering (Land)", "Sustainable Infrastructure Engineering (Building Services)", "Sustainable Built Environment", "Systems Engineering (ElectroMechanical Systems)"]),
    ("FCB - Food, Chemical and Biotechnology", ["Chemical Engineering (Joint with Newcastle University)",
     "Chemical Engineering (Joint with Technical University of Munich)", "Pharmaceutical Engineering", "Food Technology"]),
    ("HSS - Health and Social Sciences", ["Diagnostic Radiotherapy", "Dietetics and Nutrition", "Nursing",
     "Occupational Therapy", "Physiotherapy", "Radiation Therapy", "Speech and Language Therapy"]),
    ("ICT - Infocomm Technology", ["Applied Artificial Intelligence", "Applied Computing", "Computer Engineering", "Computer Science in Interactive Media and Game Development", "Computer Science in Real-Time Interactive Simulation", "Computing Science",
     "Digital Supply Chain", "Information and Communications Technology (Information Security)", "Information and Communications Technology (Software Engineering)", "Telematics (Intelligent Transportation Systems Engineering)"])
]


def main():
    initialise = None

    # ! UNCOMMENT TO CREATE USERS IN FIREBASE
    # cred = credentials.Certificate("key.json")
    # app = firebase_admin.initialize_app(cred, {
    #     'storageBucket': 'inclubsit.appspot.com'
    # })

    with open('template.sql', 'r', encoding='utf-8') as f:
        initialise = f.read()
    with open('ClubsData - ClubsInfo.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        values = {}
        for i, row in enumerate(reader):
            for key in row.keys():
                value = row[key]
                value = value.replace("'", "''").replace(
                    "’", "''").replace("‘", "''").rstrip()
                if key in values.keys():
                    values[key].append(value)
                else:
                    values[key] = [value]
    with open('ClubsData - ClubCategoryInformation.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        club_cat_values = {}
        club_categories_by_id = []
        for i, row in enumerate(reader):
            for key in row.keys():
                value = row[key]
                value = value.replace("'", "''").replace(
                    "’", "''").replace("‘", "''").rstrip()
                if key in club_cat_values.keys():
                    club_cat_values[key].append(value)
                else:
                    club_cat_values[key] = [value]

        f.seek(0)
        rows = csv.reader(f)
        for idx, row in enumerate(rows):
            if idx > 0:
                club_categories_by_id.append(row[0])

    with open("initialise.sql", "w+", encoding="utf-8") as f:
        # Include initialisation
        f.write(initialise)
        club_categories = list(set(values["Club_Category"]))

        # Insert clusters
        print("Inserting Clusters")
        for cluster_name, _ in CLUSTER_COURSES:
            f.write(
                f"INSERT INTO Cluster (ClusterName) VALUES ('{cluster_name}');\n")

        # Insert courses
        print("Inserting Courses")
        for cluster_id, (_, courses) in enumerate(CLUSTER_COURSES):
            for course in courses:
                f.write(
                    f"INSERT INTO CourseInformation (CourseName, ClusterID) VALUES ('{course}', {cluster_id + 1});\n")

        # Insert club categories info
        print("Inserting Club Categories Information")
        for idx, (club_cat, description) in enumerate(zip(club_cat_values["ClubCategory"], club_cat_values['Description'])):
            f.write(
                f"INSERT INTO ClubCategory (ClubCategoryName, CategoryDescription) VALUES ('{club_cat}', '{description}');\n"
            )

        # Insert clubs
        print("Inserting Clubs")
        for idx, (club_name, description, train_dates, train_loc) in enumerate(zip(values["Club Name"], values["Description"], values["Training_Dates"], values["Training Locations"])):
            club_email = f'sit_{club_name.replace(" ", "").lower()}@sit.singaporetech.edu.sg'
            club_insta = f'@sit_{club_name.replace(" ", "").lower()}'
            f.write(
                f"INSERT INTO Club (ClubName, ClubCategoryID, ClubDescription, ClubTrainingDates, ClubTrainingLocations, ClubEmail, ClubInstagram) VALUES ('{club_name}', {club_categories_by_id.index(values['Club_Category'][idx]) + 1}, '{description}', '{train_dates}', '{train_loc}', '{club_email}', '{club_insta}');\n")
        f.write('\n')

        # Insert students
        print("Inserting Students")
        pairs, students = generate_student_club_pairs(
            club_names=values["Club Name"])
        courses = [name for x in CLUSTER_COURSES for name in x[1]]
        for i, student in enumerate(tqdm(students)):
            student_id = BASE_STUDENT_ID + i
            email = f'{student_id}@sit.singaporetech.edu.sg'
            course_id = courses.index(random.choice(courses)) + 1
            gender = random.choice(['male', 'female'])
            f.write(
                f"INSERT INTO Account (StudentID, Email, FirstName, LastName, MatriculationYear, CourseID, Gender) VALUES ({student_id}, '{email}', '{student.split()[0]}', '{student.split()[1]}', 2022, '{course_id}', '{gender}');\n")
            # ! UNCOMMENT TO CREATE USERS IN FIREBASE
            # authenticate_user(email, str(student_id))
        f.write('\n')

        # Insert into ClubMember
        print("Inserting Club Membership")
        for club_name, students in pairs.items():
            club_id = values["Club Name"].index(club_name) + 1
            for student_data in students:
                f.write(
                    f"INSERT INTO ClubMember (ClubID, StudentID, AccountTypeID) VALUES ({club_id}, {student_data['student_id']}, {student_data['role']});\n")


def authenticate_user(email, student_id):
    user = auth.create_user(
        uid=student_id,
        email=email,
        password="password"
    )


def generate_names():
    FIRST_NAMES = ['Ethan', 'Aiden', 'Nathan', 'Nathaniel', 'Lucas', 'Isaac', 'Caleb', 'Evan',
                   'Matthew', 'Joshua', 'Adam', 'Asher', 'Jayden', 'Julian', 'Ian', 'Kayden',
                   'Luke', 'Matthias', 'George', 'Gabriel']
    LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller',
                  'Wilson', 'Moore', 'Lee', 'Tan', 'Zhang', 'Wong', 'Ho', 'Chen', 'Liu',
                  'Yang', 'Huang', 'Zhao', 'Wu']
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)

    return f"{first_name} {last_name}"


def generate_student_club_pairs(num_students=200, club_names=None, num_clubs=20, num_clubs_per_student=5, student_leader_pct=0.1, min_leaders=3):
    if club_names is None:
        club_names = [f"Club {i}" for i in range(num_clubs)]
    students = []
    while len(students) < num_students:
        students.append(generate_names())
        students = list(set(students))
        students.sort()
    student_club_pairs = {club_name: [] for club_name in club_names}
    for i, student in enumerate(students):
        clubs = random.sample(club_names, k=num_clubs_per_student)
        student_data = {"name": student, "role": 1,
                        "student_id": BASE_STUDENT_ID + i}
        for club in clubs:
            student_club_pairs[club].append(deepcopy(student_data))
    # Add student leaders
    for club in club_names:
        num_leaders = max(math.ceil(
            len(student_club_pairs[club]) * student_leader_pct), min_leaders)
        leaders = random.sample(
            list(range(len(student_club_pairs[club]))), k=num_leaders)
        for i, leader_idx in enumerate(leaders):
            student_club_pairs[club][leader_idx]["role"] = min(i + 2, 4)

    return student_club_pairs, students


if __name__ == "__main__":
    main()
