class EmptyFolderError(Exception):
    """An Error class that will be used when the selected folder is empty"""
    pass


class UnspecifiedFolderError(Exception):
    """An Error class that will be used when user does not select folder"""
    pass


class AbsentOfCSVFileError(Exception):
    """An Error class that will be used when the selected folder does not contain any CSV file"""
    pass