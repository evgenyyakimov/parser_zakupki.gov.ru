import csv

def save_to_csv(orgs):
    file = open('out.csv', mode='w', encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(['title, number, inn, kpp, ogrn, link, email, telefon'])
    for org in orgs:
        writer.writerow(list(org.values()))
    return