# [SOLUTION]
from pathlib import Path

import pandas as pd
import pytest

from validate_project import load_sales_data, summarize_sales


def test_summarize_sales_calculates_expected_totals():
    df = pd.DataFrame(
        {"region": ["North", "South"], "orders": [2, 3], "revenue": [100.0, 150.0]}
    )
    summary = summarize_sales(df)
    assert summary["rows"] == 2
    assert summary["total_orders"] == 5
    assert summary["total_revenue"] == pytest.approx(250.0)


def test_load_sales_data_rejects_missing_required_columns(tmp_path: Path):
    bad_file = tmp_path / "bad_sales.csv"
    bad_file.write_text("region,orders\nNorth,12\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Missing required columns"):
        load_sales_data(bad_file)
# [/SOLUTION]
