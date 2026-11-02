# CSA08 Assignment 3 – Python Programming (CO3)

**Student:** Muthupandi C  
**Register Number:** 192565037  
**Course Code:** CSA0805  
**Submission Date:** 03/11/2026  
**Python:** Python 3.10+ (standard library only)

## Repository contents
- `Q1_Lists/` – rainfall records, slicing and moving averages
- `Q2_Tuples/` – tuple keys, grid aliasing and copying
- `Q3_Dictionaries/` – complaint frequency and grouping
- `Q4_Sets/` – elective clash detection
- `Q5_List_Comprehension/` – sensor cleaning and conversions
- `Q6_Nested_Data/` – railway timetable and station index
- `Q7_Contact_Merging/` – contact normalisation and merging
- `Assignment3_Report.docx` – report in the supplied Assignment 1 sample style

## Libraries
All programs use only the Python standard library. No external packages are required.
See `requirements.txt`.

## Run commands
Run from the repository root:
```bash
python Q1_Lists/task01_rainfall.py
python Q2_Tuples/task02_tuples_copying.py
python Q3_Dictionaries/task03_complaints.py
python Q4_Sets/task04_electives.py
python Q5_List_Comprehension/task05_sensor_cleaning.py
python Q6_Nested_Data/task06_railway.py
python Q7_Contact_Merging/task07_contact_merge.py
```

## Notes on measurements
Each program prints timing and/or memory measurements on the computer where it is executed. Timing values depend on processor, operating system, Python build and system load. Run every program yourself and capture screenshots of the actual output for the final submission. Do not copy timing values from another computer.

## GitHub commit plan
Create the repository named `CSA08-192565037-Assignment3`. Commit each task separately after running it:
1. Add Q1 and commit.
2. Add Q2 and commit.
3. Continue through Q7.
4. Add report, README and requirements file.
5. Copy the GitHub repository URL to the report cover page and submit it to faculty.

## Important design note
Q7 merges contacts using a normalised phone number. Contacts without a phone number cannot reliably be identified as the same person from a name alone, so they are retained separately. This limitation is discussed in the report.


## Execution screenshots
Actual Visual Studio Code terminal screenshots supplied after running each task are stored in the corresponding task folder as `execution_screenshot.png`. They are also included in the report appendix.

| Task | Screenshot |
|---|---|
| Q1 | `Q1_Lists/execution_screenshot.png` |
| Q2 | `Q2_Tuples/execution_screenshot.png` |
| Q3 | `Q3_Dictionaries/execution_screenshot.png` |
| Q4 | `Q4_Sets/execution_screenshot.png` |
| Q5 | `Q5_List_Comprehension/execution_screenshot.png` |
| Q6 | `Q6_Nested_Data/execution_screenshot.png` |
| Q7 | `Q7_Contact_Merging/execution_screenshot.png` |

Benchmark timings in the screenshots are machine-specific measurements from the submitted execution. Re-run the programs if measurements are required on another computer.
