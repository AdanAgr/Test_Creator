from pathlib import Path

from UTILS import exam
from UTILS.configuration import loadConfig


def main():
    try:
        config = loadConfig(Path(__file__).with_name("config.json"))
        exam.examGenerator(**config)
    except (OSError, ValueError) as error:
        raise SystemExit(f"No se pudo generar el examen: {error}") from None


if __name__ == "__main__":
    main()
