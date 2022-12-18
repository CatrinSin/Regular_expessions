import csv
import re

num_pattern = r'(\+7|8)?\s*\(*(\d{3})\)*[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})[\s\(]*(доб\.)*[\s]*(\d{4})*[\s]*[\)]*'
num_sub = r'+7(\2)\3-\4-\5 \6\7'

def open_file(file_name):
  with open(file_name, encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
  return contacts_list


def fix_phonebook(phonebook: list, pattern, substitution):
  new_list = []
  for contact in phonebook:
    name = ' '.join(contact[:3]).split(' ')
    organization = contact[3]
    position = contact[4]
    phone = re.sub(pattern, substitution, ''.join(contact[5]))
    email = contact[6]
    new_contact = [name[0], name[1], name[2], organization, position, phone, email]
    new_list.append(new_contact)
  return new_list


def fix_duplicates(new_phonebook: list):
  for i in new_phonebook:
    for j in new_phonebook:
      if i[0] == j[0] and i[1] == j[1] and i is not j:
        if i[2] == '':
          i[2] = j[2]
        if i[3] == '':
          i[3] = j[3]
        if i[4] == '':
          i[4] = j[4]
        if i[5] == '':
          i[5] = j[5]
        if i[6] == '':
          i[6] = j[6]
  contacts_list_updated = list()
  for card in new_phonebook:
    if card not in contacts_list_updated:
      contacts_list_updated.append(card)
  return contacts_list_updated



def write_file(final_file):
  with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_file)

if __name__ == '__main__':
  phonebook = open_file("phonebook_raw.csv")
  fixed_phonebook = fix_phonebook(phonebook, num_pattern, num_sub)
  final_phonebook = fix_duplicates(fixed_phonebook)
  write_file(final_phonebook)
