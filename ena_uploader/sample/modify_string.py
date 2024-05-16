with open('metadata_example.xml', 'r') as file:
    original_string = file.read()

# Iterate through the string and insert newline between "><"
modified_string = ""
for i in range(len(original_string)):
    modified_string += original_string[i]
    if original_string[i:i+2] == '><':
        modified_string += '\n'

# Write the modified string back to the file
with open('file_A_modified.xml', 'w') as file:
    file.write(modified_string)
