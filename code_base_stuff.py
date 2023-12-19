import glob
def count_lines_in_directory(directory: str, extension: str = "*.py"):
    """ Counting the number of lines in the directory of this project.
        Note that it is a rough estimate and also, not used progams are counted as well
    """
    lines = 0
    for filename in glob.glob(f"{directory}/**/{extension}", recursive=True):
        with open(filename, "r") as file:
            for line in file:
                lines += 1
    return lines