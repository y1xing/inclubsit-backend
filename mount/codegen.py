import csv
import random
import math
import bcrypt
import firebase_admin
from firebase_admin import credentials, auth
from tqdm.auto import tqdm

BASE_STUDENT_ID = 2200000
random.seed(42)


def main():
    initialise = None

    cred = credentials.Certificate("key.json")
    app = firebase_admin.initialize_app(cred, {
        'storageBucket': 'inclubsit.appspot.com'
    })

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

    with open("initialise.sql", "w+", encoding="utf-8") as f:
        # Include initialisation
        f.write(initialise)
        club_categories = list(set(values["Club_Category"]))
        # Insert club categories
        print("Inserting Club Categories")
        for category in club_categories:
            f.write(
                f"INSERT INTO ClubCategory (ClubCategoryName) VALUES ('{category}');\n")
        f.write('\n')

        # Insert clubs
        print("Inserting Clubs")
        for idx, (club_name, description) in enumerate(zip(values["Club Name"], values["Description"])):
            f.write(
                f"INSERT INTO Club (ClubName, ClubCategoryID, ClubDescription) VALUES ('{club_name}', {club_categories.index(values['Club_Category'][idx]) + 1}, '{description}');\n")
        f.write('\n')

        # Insert students
        print("Inserting Students")
        pairs, students = generate_student_club_pairs(
            club_names=values["Club Name"])
        for i, student in enumerate(tqdm(students)):
            student_id = BASE_STUDENT_ID + i
            username = student.replace(' ', '').lower()
            email = f'{student_id}@sit.singaporetech.edu.sg'
            f.write(
                f"INSERT INTO Account (StudentID, Username, Email, FirstName, LastName) VALUES ({student_id}, '{username}', '{email}', '{student.split()[0]}', '{student.split()[1]}');\n")
            authenticate_user(email, str(student_id))
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

    return random.choice(FIRST_NAMES) + ' ' + random.choice(LAST_NAMES)


def generate_student_club_pairs(num_students=200, club_names=None, num_clubs=20, num_clubs_per_student=5, student_leader_pct=0.1):
    if club_names is None:
        club_names = [f"Club {i}" for i in range(num_clubs)]
    students = []
    while len(students) < num_students:
        students.append(generate_names())
        students = list(set(students))
    student_club_pairs = {club_name: [] for club_name in club_names}
    for i, student in enumerate(students):
        clubs = random.choices(club_names, k=num_clubs_per_student)
        student_data = {"name": student, "role": 2,
                        "student_id": BASE_STUDENT_ID + i}
        for club in clubs:
            student_club_pairs[club].append(student_data)
    # Add student leaders
    for club in club_names:
        num_leaders = math.ceil(
            len(student_club_pairs[club]) * student_leader_pct)
        leaders = random.choices(student_club_pairs[club], k=num_leaders)
        for leader in leaders:
            leader["role"] = 1

    return student_club_pairs, students


if __name__ == "__main__":
    main()
