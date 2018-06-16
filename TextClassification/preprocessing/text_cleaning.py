import os
import re
import time

rootdir = "./../data/raw/"
targetdir = "./../data/cleaned/"


def read_lines_from_file(path):
    with open(path, 'rb') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines


def write_lines_to_file(path, lines):
    file = open(path, 'w+')
    for line in lines:
        file.write(line)


def prune_lines(text_lines):
    # Prune lines with metadata and e-mail addresses
    pruned_text = []
    for line in text_lines:
        line = str(line)
        if "From:" in line:
            continue
        elif "Subject:" in line:
            continue
        elif '@' in line:
            continue
        else:
            # If line is not pruned from the text prune words from it
            pruned_text.append(prune_words(line))
    return pruned_text


def prune_words(line):
    pruned_line = ""
    # Split the line by whitespaces
    for word in line.split():
        # Check if contains any letter
        if re.search('[a-zA-Z]', word):
            # Switch to lower case
            word = word.lower()
            # Remove greentext
            pruned_line += word.replace(">", "")
            pruned_line += ' '
    return pruned_line

if __name__ == "__main__":
    if not os.path.exists(targetdir):
        os.makedirs(targetdir)
        print(targetdir)
    for subdir, dirs, files in os.walk(rootdir):
        if not os.path.exists(os.path.join(targetdir, os.path.basename(subdir))):
            os.makedirs(os.path.join(targetdir, os.path.basename(subdir)))
            for file in files:
                print("Worinking on file: ", os.path.join(subdir, file))
                start_time = time.time()
                raw_data = read_lines_from_file(os.path.join(subdir, file))
                cleaned_data = prune_lines(raw_data)
                write_lines_to_file(os.path.join(targetdir, os.path.basename(subdir), file), cleaned_data)
                finishi_time = time.time()
                print("Saved pruned file to: ", os.path.join(targetdir, os.path.basename(subdir), file))
                print("It took ", finishi_time-start_time, 's')
