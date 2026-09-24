"""Create the local processed dataset from the downloaded UCI workbook."""

from pathlib import Path

from src.data_cleaning import clean_dataframe
from src.data_loader import load_dataframe


SOURCE = Path("data/raw/uci-online-retail/Online Retail.xlsx")
OUTPUT = Path("data/processed/cleaned_data.csv")


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Download the UCI workbook first: {SOURCE}")
    dataframe = load_dataframe(SOURCE, SOURCE.name)
    cleaned, report = clean_dataframe(dataframe)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUTPUT, index=False)
    print(f"Wrote {len(cleaned):,} rows to {OUTPUT}")
    print(f"Removed duplicates: {report.duplicate_rows_removed:,}")
    print(f"Removed cancellations: {report.cancelled_rows_removed:,}")


if __name__ == "__main__":
    main()
