# [SOLUTION]
from pathlib import Path

import pandas as pd

DATA_PATH = Path("data/sample_sales.csv")
REQUIRED_COLUMNS = {"region", "orders", "revenue"}


def load_sales_data(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    return df


def summarize_sales(df) -> dict:
    return {
        "rows": int(len(df)),
        "total_orders": int(df["orders"].sum()),
        "total_revenue": float(df["revenue"].sum()),
    }

def calculate_average_order_value(total_revenue, total_orders):
    if total_orders == 0:
        return 0.0
    return float(total_revenue / total_orders)

def main() -> None:
    df = load_sales_data()
    summary = summarize_sales(df)
    print(f"Loaded rows: {summary['rows']}")
    print(f"Total orders: {summary['total_orders']}")
    print(f"Total revenue: ${summary['total_revenue']:,.2f}")


if __name__ == "__main__":
    main()
# [/SOLUTION]
