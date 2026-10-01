import random
import json
import copy
import glob
import os


def questionGenerator(
    folderPath: str | list[str],
    numOfQuestions: int = 10,
    questionsOfEachUnit: dict = None,
) -> list:
    """
    Generates a list of questions from the files in the
    given folderPath or folders, including subfolders. The questions
    are selected randomly from the combined set of files.

    Args:
        - folderPath (str | list[str]): One or more folders with questions
        - numOfQuestions (int): The number of questions to generate
        - questionsOfEachUnit (dict): A dictionary with the number of questions
            to generate from each file. The keys are the names of the files and
            the values the number of questions to generate from each file

    Returns:
        - list: A list with the generated questions
    """
    questions = []

    questionsByFileDict = questionsByFileInFolder(folderPath)
    if not questionsByFileDict:
        raise ValueError(
            "No se encontraron preguntas en archivos Unit*.json "
            "dentro de las carpetas seleccionadas ni sus subcarpetas."
        )
    maxQuestions = sum(questionsByFileDict.values())

    if numOfQuestions > maxQuestions:
        print(
            "There are not enough questions to generate. Some questions will be repeated."
        )

    # Need to generate the number of questions for each file
    if questionsOfEachUnit == None:
        questionsOfEachUnit = {key: 0 for key in questionsByFileDict.keys()}

        while sum(questionsOfEachUnit.values()) < numOfQuestions:
            x = random.choice(list(questionsOfEachUnit.keys()))

            if (
                questionsOfEachUnit[x] < questionsByFileDict[x]
                or numOfQuestions > maxQuestions
            ):
                questionsOfEachUnit[x] += 1

    # Print the files from which don't have more questions
    for f in questionsOfEachUnit.keys():
        if questionsOfEachUnit[f] >= questionsByFileDict[f]:
            print(f"The file {os.path.basename(f)} has no more questions.")

    # Get the questions from each file
    for filePath in questionsOfEachUnit.keys():
        with open(
            filePath,
            "r",
            encoding="utf-8",
        ) as file:
            questionsData = json.load(file)

        numOfQuestionsInUnit = len(questionsData["questions"])

        if questionsOfEachUnit[filePath] <= numOfQuestionsInUnit:
            choosenQuestions = random.sample(
                questionsData["questions"], questionsOfEachUnit[filePath]
            )  # No repeats
        else:
            choosenQuestions = [
                copy.deepcopy(item)
                for item in random.choices(
                    questionsData["questions"], k=questionsOfEachUnit[filePath]
                )  # Allows repeats
            ]

        # Add the folder and the topic to the question
        for q in choosenQuestions:
            q["folder"] = os.path.dirname(filePath)
            fileName = os.path.splitext(os.path.basename(filePath))[0]
            topic = fileName
            for prefix in ("Unit", "modulo", "Final"):
                if topic.startswith(prefix):
                    topic = topic[len(prefix) :]
                    break
            q["question"] = (
                q["question"] + " [Tema " + topic + "]"
            )

        # Add the questions to the list that will be returned
        questions.extend(choosenQuestions)

    return questions


def findPatternFiles(
    pattern=("Unit*.json", "modulo*.json", "Final*.json"), folderPath="."
) -> list:
    """
    Returns a list of files that match the pattern
    in the given folderPath or folders, including subfolders.
    The files are returned with their absolute path, without duplicates.

    Args:
        - pattern (str | tuple[str, ...]): One or more patterns to search for
        - folderPath (str | list[str]): One or more folders to search in

    Returns:
        - list: The list of files that match the pattern
    """
    folders = [folderPath] if isinstance(folderPath, (str, os.PathLike)) else folderPath
    patterns = (pattern,) if isinstance(pattern, str) else pattern
    matchingFiles = {}
    for folder in folders:
        if not os.path.isdir(folder):
            raise ValueError(f"No existe la carpeta de preguntas: {folder}")
        for currentPattern in patterns:
            files = glob.glob(
                os.path.join(
                    glob.escape(os.fspath(folder)), "**", currentPattern
                ),
                recursive=True,
            )
            for file in sorted(files):
                if os.path.isfile(file):
                    absolutePath = os.path.realpath(file)
                    matchingFiles.setdefault(
                        os.path.normcase(absolutePath), absolutePath
                    )

    return list(matchingFiles.values())


def questionsByFileInFolder(folderPath: str | list[str]) -> dict:
    """
    Returns a dictionary with the number questions of all
    the files in the given folderPath or folders, including subfolders.

    Args:
        - folderPath (str | list[str]): One or more folders with questions

    Returns:
        - dict: A dictionary with the questions of the file
            The keys are the names of the files and the values
            the number of questions of each file
    """
    questions = {x: 0 for x in findPatternFiles(folderPath=folderPath)}

    # We go file by file
    for f in questions.keys():
        with open(f, "r", encoding="utf-8") as file:
            questionsData = json.load(file)
            questions[f] = len(questionsData["questions"])

    # Eliminate the files that have no questions
    questions = {k: v for k, v in questions.items() if v > 0}

    return questions


def validFolders() -> dict:
    """
    Get the folders that have questions in them.

    It will return them as the keys of a dictionary,
    being the values a dictionary of the files
    with the number of questions in them.

    Args:
        - None

    Returns:
        - dict: The dictionary with the folders and the
            number of questions in each file
    """
    filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    folders = {
        f: questionsByFileInFolder(os.path.join(filePath, f))
        for f in os.listdir(filePath)
        if os.path.isdir(os.path.join(filePath, f))
    }

    # We eliminate the ones with empty dictionaries (no questions)
    folders = {k: v for k, v in folders.items() if v}

    return folders


def showNumberOfQuestions() -> None:
    """
    Print the number of questions in each folder and file

    Args:
        - None

    Returns:
        - None
    """
    data = validFolders()

    # We order by the name of the folder
    data = dict(sorted(data.items(), key=lambda x: x[0]))

    # Inside each folder, we order by the name of the file
    data = {k: dict(sorted(v.items(), key=lambda x: x[0])) for k, v in data.items()}

    # We print the data
    for folder, files in data.items():
        print(f"{folder}: {sum(files.values())}")
        for file, questions in files.items():
            print(f"\t{os.path.basename(file)}: {questions}")


if __name__ == "__main__":
    showNumberOfQuestions()
