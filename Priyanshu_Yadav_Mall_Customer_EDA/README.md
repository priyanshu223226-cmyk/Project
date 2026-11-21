# Mall Customer EDA

**Student:** Priyanshu Yadav  
**Admission No:** 2026B01010276

This project performs basic exploratory data analysis on the supplied Mall Customers dataset using Python, NumPy, Pandas, and Matplotlib.

## Files

- `mall_customer_eda.py`: reproducible analysis script
- `Mall_Customer_EDA.ipynb`: notebook for interactive analysis
- `REPORT.md`: complete written findings
- `outputs/`: summary tables in CSV format
- `charts/`: the two assigned charts

## Run

From this project folder:

```powershell
python mall_customer_eda.py
```

If Python 3.12 is used with `uv`, the run command is:

```powershell
uv run --python 3.12 --with pandas --with numpy --with matplotlib --with tabulate python mall_customer_eda.py
```

The script reads the original file at `../data/raw/Mall_Customers.csv` and never modifies it.

## Requirements

```text
numpy
pandas
matplotlib
tabulate
```
