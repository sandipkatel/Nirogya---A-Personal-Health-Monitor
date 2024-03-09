def update_last_line(file_path, given_string):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Check if the last line has the same first 12 characters as the given string
    if lines and lines[-1].startswith(given_string[:10]):
        # Replace the last line entirely with the given string
        lines[-1] = given_string 
    else:
        # Append the given string in a new line
        lines.append(given_string)

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

# # Example usage
# file_path = 'example.txt'
# given_string = 'sradpokharel1234'  # Replace this with your given string
# update_last_line(file_path, given_string)
