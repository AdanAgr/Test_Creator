import json
from pathlib import Path


def loadConfig(configPath: str | Path) -> dict:
    """Read exam settings, resolving question folders relative to the config file."""
    configPath = Path(configPath).resolve()
    with configPath.open("r", encoding="utf-8") as configFile:
        config = json.load(configFile)

    if not isinstance(config, dict):
        raise ValueError("La configuración debe ser un objeto JSON.")

    folders = config.get("folders")
    if (
        not isinstance(folders, list)
        or not folders
        or any(not isinstance(folder, str) or not folder.strip() for folder in folders)
    ):
        raise ValueError("'folders' debe ser una lista no vacía de rutas de carpetas.")

    folderPaths = []
    for folder in folders:
        folderPath = (configPath.parent / folder).resolve()
        if not folderPath.is_dir():
            raise ValueError(f"No existe la carpeta de preguntas: {folderPath}")
        folderPaths.append(str(folderPath))

    numExams = config.get("numExams", 1)
    numOfQuestions = config.get("numOfQuestions", 30)
    for name, value in [("numExams", numExams), ("numOfQuestions", numOfQuestions)]:
        if type(value) is not int or value <= 0:
            raise ValueError(f"'{name}' debe ser un entero mayor que cero.")

    style = config.get("style", "default")
    if style not in ("default", "legacy", "dark"):
        raise ValueError("'style' debe ser 'default', 'legacy' o 'dark'.")

    return {
        "folderPath": folderPaths,
        "numberOfExams": numExams,
        "numberOfQuestions": numOfQuestions,
        "style": style,
    }
