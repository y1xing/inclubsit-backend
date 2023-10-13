import csv


def main():
    with open('ClubsData - ClubsInfo.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        values = {}
        for i, row in enumerate(reader):
            for key in row.keys():
                value = row[key]
                value = value.replace("'", "''").replace("’", "''").replace("‘", "''").rstrip()
                if key in values.keys():
                    values[key].append(value)
                else:
                    values[key] = [value]

    with open("output.txt", "w+", encoding="utf-8") as f:
        club_categories = list(set(values["Club_Category"]))
        for category in club_categories:
            f.write(
                f"INSERT INTO ClubCategory (ClubCategoryName) VALUES ('{category}');\n")
        f.write('\n')

        for idx, (club_name, description) in enumerate(zip(values["Club Name"], values["Description"])):
            f.write(
                f"INSERT INTO Club (ClubName, ClubCategoryID, ClubDescription) VALUES ('{club_name}', {club_categories.index(values['Club_Category'][idx]) + 1}, '{description}');\n")
        f.write('\n')


if __name__ == "__main__":
    main()
