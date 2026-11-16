# CSA08 Assignment 5 – CO5
Student: Muthupandi C
Register Number: 192565037
Course: Python Programming
Case study: City Air-Quality Monitoring Network

## Required libraries
Install the libraries into the SAME Python interpreter selected in VS Code:
```powershell
python -m pip install -r requirements.txt
```
If using the Python 3.15 interpreter shown in the terminal, run:
```powershell
& "C:\Users\MUTHUPANDI\AppData\Local\Programs\Python\Python315\python.exe" -m pip install -r requirements.txt
```
The assignment specifically requires pandas for Task 3 and matplotlib for Task 1 charts. If a library is missing, that part of the task cannot be fully executed.

## Run the tasks
Run these commands from the assignment root:
```powershell
python Task01_B1_Cleaning_Pipeline/cleaning_pipeline.py
python Task02_B2_Adversarial_Data/adversarial_sql.py
python Task03_B3_Performance_Comparison/benchmark_methods.py
python Task04_B4_AI_and_Index/final_decision.py
```

## Task notes
- Task 1: CSV validation, cleaning, min-max normalisation, SQLite storage, SQL summaries and charts.
- Task 2: malformed input tests, encoding mismatch, executemany, parameterised SELECT and SQL injection demonstration.
- Task 3: daily means using Python csv loops, pandas groupby and SQL GROUP BY for 1, 12 and 120 stations; timing and cProfile evidence.
- Task 4: 50 complaint sentiment examples, extractive summary, parameterised chatbot and index performance test on a larger SQLite dataset.

Benchmark timings vary by computer. Re-run the programs on the submission computer and retain the actual terminal output. Add the working GitHub repository URL to the report and commit each task progressively.
