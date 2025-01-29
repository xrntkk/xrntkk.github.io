import string

all_characters = string.ascii_letters + string.digits + string.punctuation

with open('fuzz_dictionary.txt', 'w', encoding='utf-8') as file:
    for char in all_characters:
        file.write(char + '\n')

print("success")