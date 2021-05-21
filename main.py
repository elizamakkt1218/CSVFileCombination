import tkinter as tk
from tkinter.filedialog import askdirectory
import csv
import os
import utilities

absolute_file_paths = []


def get_file_path():
    """
    Prompts user to select the folder for Combining CSV files

    :parameter: None
    :return: The relative paths of all files contained in the folder
    :exception:
    1. UnspecifiedFolderError
    2. EmptyFolderError
    3. AbsenceOfCSVFileError
    """

    tk.Tk().withdraw()
    folder_path = ''
    try:
        folder_path = askdirectory(title='Select Folder')
        # Raise UnspecifiedFolderError when user did not select a folder
        if folder_path == '/':
            raise utilities.UnspecifiedFolderError('Please select a folder.')
        # Return None and stop the program when user click "Cancel"
        elif folder_path == '':
            return None
    except utilities.UnspecifiedFolderError:
        print('Please select a folder.')
        get_file_path()

    relative_file_paths = []

    try:
        relative_file_paths = os.listdir(folder_path)

        # Raise EmptyFolderError when the folder is empty
        if not relative_file_paths:
            raise utilities.EmptyFolderError('Empty Folder!')

        # The index of the two lists: relative_file_paths and absolute_file_paths are the same
        for files in relative_file_paths:
            ext = files.rpartition('.')[-1]
            if ext != 'csv':
                relative_file_paths.remove(files)
                continue
            absolute_file_paths.append(folder_path + '/' + files)

        # Raise AbsentOfCSVFileError when no csv file exists
        if not absolute_file_paths:
            raise utilities.AbsentOfCSVFileError('No CSV File Exists.')

    except utilities.EmptyFolderError:
        print(folder_path + '\n' + 'The folder is empty.')

    except utilities.AbsentOfCSVFileError:
        print('No CSV File Exists.')

    return relative_file_paths


def read():
    """
    Reads all the CSV files and save the data as lists

    :parameter: None
    :return: a list of csv_reader objects(converted into lists)
    :exception: None
    """
    # Call get_file_path Method
    # if it returns none, return to its caller
    relative_file_paths = get_file_path()
    if not relative_file_paths:
        return

    # Convert all the csv_reader objects into lists and save them to a list
    index = 0
    file_reader = []
    for file in absolute_file_paths:
        with open(file, newline='') as csv_file:
            file_reader.append(list(csv.reader(csv_file)))

        # Rename the column name into filenames
        if index >= 1:
            # Skip the first column if the files are loaded as the second one or onwards
            for row in file_reader[index]:
                row.pop(0)
            file_reader[index][0][0] = os.path.splitext(relative_file_paths[index])[0]
        else:
            file_reader[index][0][1] = os.path.splitext(relative_file_paths[index])[0]
        index += 1

    return file_reader


def write():
    """
    Writes all the data into a new CSV file called 'output.csv'

    :return: None
    :parameter: None
    :exception: None
    """
    # Call read Method
    file_reader = read()
    if not file_reader:
        return

    # Write the data to the "output.csv" file
    count = 0
    while count < len(file_reader):
        if count == 0:
            with open('output.csv', 'w', newline='')as csv_file:
                writer = csv.writer(csv_file)
                for row in file_reader[0]:
                    writer.writerow(row)
            csv_file.close()
            count += 1
        else:
            length = 0
            with open('output.csv', 'r', newline='') as input_file:
                reader = list(csv.reader(input_file))
            with open('output.csv', 'w', newline='')as append_file:
                writer = csv.writer(append_file)
                for input_row in reader:
                    writer.writerow(input_row + file_reader[count][length])
                    length += 1
                append_file.close()
            count += 1

    print('Output file has been saved to the current directory.')


def main():
    write()


if __name__ == "__main__":
    main()


