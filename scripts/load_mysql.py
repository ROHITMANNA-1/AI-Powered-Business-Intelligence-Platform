"""Load the processed CSV into MySQL using the project's environment settings."""

from pathlib import Path

from dotenv import load_dotenv

from src.data_loader import load_dataframe
from src.database import load_dataframe_to_database


INPUT = Path("data/processed/cleaned_data.csv")


def main() -> None:
    load_dotenv()
    if not INPUT.exists():
        raise FileNotFoundError(f"Run scripts/prepare_dataset.py first: {INPUT}")
    dataframe = load_dataframe(INPUT, INPUT.name)
    table = load_dataframe_to_database(dataframe)
    print(f"Loaded {len(dataframe):,} rows into MySQL table: {table}")


if __name__ == "__main__":
    main()
