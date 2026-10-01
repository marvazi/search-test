import ast
import asyncio
import csv
from datetime import datetime

from app.db.session import engine, session_factory
from app.models.document import Document


async def main():
    try:
        async with session_factory() as session:
            with open("data/posts.csv", encoding="utf-8-sig", newline="") as file:
                for row in csv.DictReader(file):
                    document = Document(
                        text=row["text"],
                        rubrics=ast.literal_eval(row["rubrics"]),
                        created_date=datetime.fromisoformat(row["created_date"]),
                    )
                    session.add(document)

            await session.commit()

        print("Данные загружены")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())