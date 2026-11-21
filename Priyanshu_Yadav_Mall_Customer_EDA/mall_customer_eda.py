from pathlib import Path
import io
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = PROJECT_DIR.parent
DATA_FILE = WORKSPACE_DIR / "data" / "raw" / "Mall_Customers.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"
CHART_DIR = PROJECT_DIR / "charts"
STUDENT_NAME = "Priyanshu Yadav"
ADMISSION_NO = "2026B01010276"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_FILE)

    print("HEAD")
    print(df.head())
    print("\nTAIL")
    print(df.tail())
    print("\nSHAPE")
    print(df.shape)
    print("\nINFO")
    df.info()
    print("\nDESCRIBE")
    print(df.describe(include="all"))

    gender_counts = df["Gender"].value_counts().sort_index()
    gender_counts.to_csv(OUTPUT_DIR / "gender_counts.csv", header=["Count"])

    numeric_columns = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]
    numerical_stats = pd.DataFrame(
        {
            "mean": df[numeric_columns].mean(),
            "median": df[numeric_columns].median(),
            "minimum": df[numeric_columns].min(),
            "maximum": df[numeric_columns].max(),
        }
    )
    numerical_stats.to_csv(OUTPUT_DIR / "numerical_summary.csv")

    # NumPy array use: summarize each assigned numerical column.
    values = df[numeric_columns].to_numpy(dtype=float)
    numpy_stats = pd.DataFrame(
        {
            "column": numeric_columns,
            "numpy_mean": np.mean(values, axis=0),
            "numpy_median": np.median(values, axis=0),
            "numpy_minimum": np.min(values, axis=0),
            "numpy_maximum": np.max(values, axis=0),
        }
    )
    numpy_stats.to_csv(OUTPUT_DIR / "numpy_summary.csv", index=False)

    age_bands = pd.cut(
        df["Age"],
        bins=[17, 27, 37, 47, 57, 67, 200],
        labels=[
            "18-27",
            "28-37",
            "38-47",
            "48-57",
            "58-67",
            "68+",
        ],
        include_lowest=True,
    )
    df["Age Band"] = age_bands
    age_spending = (
        df.groupby("Age Band", observed=True)["Spending Score (1-100)"]
        .agg(["count", "mean"])
        .reset_index()
        .rename(columns={"count": "Customer Count", "mean": "Average Spending Score"})
    )
    age_spending.to_csv(OUTPUT_DIR / "age_band_spending.csv", index=False)

    gender_comparison = (
        df.groupby("Gender")[["Annual Income (k$)", "Spending Score (1-100)"]]
        .mean()
        .reset_index()
        .rename(
            columns={
                "Annual Income (k$)": "Average Annual Income (k$)",
                "Spending Score (1-100)": "Average Spending Score",
            }
        )
    )
    gender_comparison.to_csv(OUTPUT_DIR / "gender_comparison.csv", index=False)

    top_ten = (
        df.sort_values(
            ["Spending Score (1-100)", "CustomerID"],
            ascending=[False, True],
        )
        .head(10)
    )
    top_ten.to_csv(OUTPUT_DIR / "top_10_spending_customers.csv", index=False)

    missing_values = df[numeric_columns + ["Gender", "CustomerID"]].isna().sum()
    duplicate_rows = int(df.duplicated().sum())
    data_quality = pd.DataFrame(
        {
            "check": ["missing_values", "duplicate_rows"],
            "value": [int(missing_values.sum()), duplicate_rows],
        }
    )
    data_quality.to_csv(OUTPUT_DIR / "data_quality.csv", index=False)

    missing_by_column = missing_values.rename("Missing Values").reset_index()
    missing_by_column.columns = ["Column", "Missing Values"]
    missing_by_column.to_csv(OUTPUT_DIR / "missing_values_by_column.csv", index=False)

    # Chart 1: gender count.
    fig, ax = plt.subplots(figsize=(7, 5))
    gender_counts.plot(kind="bar", ax=ax, color=["#4C78A8", "#F58518"])
    ax.set_title("Customer Count by Gender")
    ax.set_xlabel("Gender")
    ax.set_ylabel("Number of Customers")
    ax.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "gender_count_bar.png", dpi=150)
    plt.close(fig)

    # Chart 2: annual income versus spending score.
    fig, ax = plt.subplots(figsize=(7, 5))
    for gender in ["Female", "Male"]:
        subset = df[df["Gender"] == gender]
        ax.scatter(
            subset["Annual Income (k$)"],
            subset["Spending Score (1-100)"],
            label=gender,
            alpha=0.75,
        )
    ax.set_title("Annual Income versus Spending Score")
    ax.set_xlabel("Annual Income (k$)")
    ax.set_ylabel("Spending Score (1-100)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(CHART_DIR / "income_vs_spending_scatter.png", dpi=150)
    plt.close(fig)

    highest_age_band = age_spending.sort_values(
        "Average Spending Score", ascending=False
    ).iloc[0]
    highest_female_income = gender_comparison.loc[
        gender_comparison["Gender"] == "Female",
        "Average Annual Income (k$)",
    ].iloc[0]
    highest_male_income = gender_comparison.loc[
        gender_comparison["Gender"] == "Male",
        "Average Annual Income (k$)",
    ].iloc[0]

    observations = [
        f"{int(gender_counts.idxmax()) if False else gender_counts.index[gender_counts.argmax()]} customers form the larger gender group, with {int(gender_counts.max())} customers.",
        f"The {highest_age_band['Age Band']} age band has the highest average spending score ({highest_age_band['Average Spending Score']:.2f}).",
        f"Average annual income is {highest_female_income:.2f}k for females and {highest_male_income:.2f}k for males; both groups should be compared with their average spending scores.",
    ]

    buf = io.StringIO()
    df.info(buf=buf)
    dataset_info = buf.getvalue()

    report = f"""# Mall Customer EDA Report

**Student:** {STUDENT_NAME}  
**Admission No:** {ADMISSION_NO}  
**Course:** B.Tech CSE, First Year  
**Training:** HCL Data Analytics Training

## Dataset and Inspection

- Source: `data/raw/Mall_Customers.csv`
- Shape: {df.shape[0]} rows and {df.shape[1] - 1} original columns
- Original columns: {", ".join(df.columns[:-1])}

### head()

{df.drop(columns=["Age Band"]).head().to_markdown(index=False)}

### tail()

{df.drop(columns=["Age Band"]).tail().to_markdown(index=False)}

### shape

{df.drop(columns=["Age Band"]).shape}

### info()

```text
{dataset_info}
```

### describe()

{df.drop(columns=["Age Band"]).describe(include="all").to_markdown()}

## Required Analysis

### 1. Customers by Gender

{gender_counts.rename("Customer Count").to_frame().to_markdown()}

### 2. Numerical Summary

{numerical_stats.to_markdown()}

The NumPy-based summary is also available in `outputs/numpy_summary.csv`.

### 3. Highest-Spending Age Band

Age bands used: 18-27, 28-37, 38-47, 48-57, 58-67, and 68+.

{age_spending.to_markdown(index=False)}

The age band with the highest average spending score is **{highest_age_band["Age Band"]}** ({highest_age_band["Average Spending Score"]:.2f}).

### 4. Gender Comparison

{gender_comparison.to_markdown(index=False)}

### 5. Top 10 Customers by Spending Score

{top_ten.to_markdown(index=False)}

### 6. Data Quality

- Missing values: {int(missing_values.sum())}
- Duplicate rows: {duplicate_rows}

Missing values by column:

{missing_by_column.to_markdown(index=False)}

## Charts

![Customer count by gender](charts/gender_count_bar.png)

![Annual income versus spending score](charts/income_vs_spending_scatter.png)

## Observations

1. {observations[0]}
2. {observations[1]}
3. {observations[2]}
"""
    (PROJECT_DIR / "REPORT.md").write_text(report, encoding="utf-8")

    print("\nGENDER COUNTS")
    print(gender_counts)
    print("\nNUMERICAL SUMMARY")
    print(numerical_stats)
    print("\nAGE-BAND SPENDING")
    print(age_spending)
    print("\nGENDER COMPARISON")
    print(gender_comparison)
    print("\nTOP 10")
    print(top_ten)
    print("\nDATA QUALITY")
    print(f"Missing values: {int(missing_values.sum())}")
    print(f"Duplicate rows: {duplicate_rows}")
    print("\nOBSERVATIONS")
    for index, observation in enumerate(observations, start=1):
        print(f"{index}. {observation}")

    create_notebook()


def create_notebook():
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Mall Customer Exploratory Data Analysis\n",
                    "\n",
                    f"Student: {STUDENT_NAME}\n",
                    f"Admission No: {ADMISSION_NO}",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "from pathlib import Path\n",
                    "import numpy as np\n",
                    "import pandas as pd\n",
                    "import matplotlib.pyplot as plt\n",
                    "\n",
                    "workspace = Path('..').resolve()\n",
                    "df = pd.read_csv(workspace / 'data' / 'raw' / 'Mall_Customers.csv')\n",
                    "df.head()",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "print(df.shape)\n",
                    "df.info()\n",
                    "df.describe(include='all')",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "gender_counts = df['Gender'].value_counts().sort_index()\n",
                    "gender_counts.plot(kind='bar', color=['#4C78A8', '#F58518'])\n",
                    "plt.title('Customer Count by Gender')\n",
                    "plt.xlabel('Gender')\n",
                    "plt.ylabel('Number of Customers')\n",
                    "plt.xticks(rotation=0)\n",
                    "plt.tight_layout()\n",
                    "plt.show()",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "for gender in ['Female', 'Male']:\n",
                    "    subset = df[df['Gender'] == gender]\n",
                    "    plt.scatter(subset['Annual Income (k$)'], subset['Spending Score (1-100)'], label=gender, alpha=0.75)\n",
                    "plt.title('Annual Income versus Spending Score')\n",
                    "plt.xlabel('Annual Income (k$)')\n",
                    "plt.ylabel('Spending Score (1-100)')\n",
                    "plt.legend()\n",
                    "plt.tight_layout()\n",
                    "plt.show()",
                ],
            },
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    (PROJECT_DIR / "Mall_Customer_EDA.ipynb").write_text(
        json.dumps(notebook, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
