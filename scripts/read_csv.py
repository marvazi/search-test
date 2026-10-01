import ast
import csv
from datetime import datetime
from pathlib import Path


CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "posts.csv"


def main():
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        row = next(reader)

    text = row["text"]
    created_date = datetime.fromisoformat(row["created_date"])
    rubrics = ast.literal_eval(row["rubrics"])

    if not isinstance(rubrics, list) or not all(
        isinstance(rubric, str) for rubric in rubrics
    ):
        raise ValueError("rubrics должен быть списком строк")

    print("Текст:", text)
    print("Дата:", created_date)
    print("Рубрики:", rubrics)

    print("Тип даты:", type(created_date))
    print("Тип рубрик:", type(rubrics))


if __name__ == "__main__":
    main()