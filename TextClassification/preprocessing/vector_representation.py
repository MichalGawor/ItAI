import os
import pandas as pd
from text_cleaning import read_lines_from_file


datadir = "./../data/cleaned/alt.atheism/49960"



words_in_dataset = pd.DataFrame(columns=('FileID', 'Word', 'Occurrences'))

if __name__ == "__main__":
    for subdir, dirs, files in os.walk(datadir):
        for file in files:
            raw_data = read_lines_from_file(os.path.join(subdir, file))
            words_in_file = pd.DataFrame(columns=('FileID', 'Word', 'Occurrences'))
            for line in raw_data:
                line = str(line)
                for word in line.split():






