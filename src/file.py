def update_last_line(file_path, given_string):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if lines and lines[-1].startswith(given_string[:10]):
        lines[-1] = given_string 
    else:
        lines.append(given_string)

    with open(file_path, 'w') as file:
        file.writelines(lines)

