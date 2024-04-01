
countries_file = open("countries.txt", 'r')
countries_named_entity = open("countries/named_entity.tsv", 'a')

for line in countries_file:
    line = line.strip()
    if line and not line.isupper():
        if line.endswith("*"):
            line = line[:-1]
        if line.endswith(", The"):
            line = line[:-5]
        countries_named_entity.write(line + "\tCountry\n")

countries_named_entity.close()
countries_file.close()
