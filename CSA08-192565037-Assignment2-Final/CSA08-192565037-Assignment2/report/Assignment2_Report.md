# SIMATS ENGINEERING
## PYTHON PROGRAMMING – ASSIGNMENT 2 (CO2)

**Student Name:** Muthupandi C  
**Register Number:** 192565037  
**Department:** CSE – Cyber Security  
**Course Code:** CSA08  
**Assignment:** Individual – Assignment 2  
**Submission Date:** 30/10/2026  
**GitHub Repository:** `https://github.com/<username>/CSA08-192565037-Assignment2`

---

## Introduction
This assignment applies Python decision-making statements, loops, string operations, functions, variable scope, recursion, and performance analysis. Each task is implemented as a separate Python program so that it can be executed and checked independently.

## Q1 – Decisions with Many Boundaries (6 Marks)
**Prediction:** 100 units qualifies for full subsidy; 101 and 200 units qualify for partial subsidy only when a ration card is present; 201 units receives the special elderly exemption only when a household member is above 80.

Separate `if` statements are independent. More than one block can run if conditions overlap. An `if-elif-else` chain selects the first matching branch, so only one branch is selected. In the supplied rules the unit ranges are disjoint, but a chain still communicates the exclusive decision more clearly.

**Design decision:** Use `if-elif-else` for the mutually exclusive consumption bands and a nested `if` for the additional eligibility condition. This keeps each eligibility test beside its band and is easy to modify.

**Alternative:** A Python 3.10 `match` statement could match `units` only after converting ranges to guards, for example `case u if u <= 100:`. A list of `(upper_limit, decision)` pairs can be scanned in order. Both require O(k) worst-case time for k slabs if searched linearly; the decision chain is O(k) in the number of branches and O(1) auxiliary space. A dictionary is not ideal for continuous ranges.

## Q2 – Loops that Count Attempts (4 Marks)
The `while` version is natural when the number of attempts depends on a changing condition, such as a security answer adding two attempts. The `for` version is concise when the maximum number is fixed. A counter updated before checking for a blank input incorrectly consumes an attempt. A counter not updated at all can create an infinite loop.

`break` exits after a correct OTP; `continue` skips blank entries without counting them; `pass` is a no-operation placeholder; loop `else` runs when the loop ends without `break`. The recursive alternative calls itself with the next input index. All versions take O(a) time for a attempts; recursion uses O(a) stack space, while loops use O(1) auxiliary space.

**Changed condition:** Set the maximum to five only after successful security-question verification. Keep blank entries excluded from the attempt count.

## Q3 – Vehicle Registration Validator (6 Marks)
The program removes spaces and hyphens, converts letters to uppercase, then validates the required parts using slices and string methods. It rejects malformed state/district/series/numeric sections.

Strings are immutable, so methods such as `upper()` return a new string rather than changing the original object. For a 10-character string, `s[-4:]` returns the last four characters and `s[4:-4]` returns the two-character series. For a 9-character string, the same slices return the last four characters and the one-character series.

**Alternative:** `re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}", reg)` checks the entire string. Both approaches are O(L) for string length L. Slicing makes each component visible; a regular expression is compact but may be harder for a beginner to maintain.

## Q4 – Building Long Text: `+` or `join()`? (6 Marks)
The program builds identical statements using repeated `+=`, a list/generator with `join`, and f-string line construction. It measures 1,000, 10,000, and 200,000 records over three runs and prints each average.

Strings are immutable, so concatenation may allocate new string objects and copy existing characters. Repeated concatenation can therefore approach O(n²) copied characters in unfavourable cases. `join()` can calculate the final size and build the result efficiently in O(n) time. CPython may optimise some local `+=` patterns, so actual timings must be measured on the student's computer.

**Alternative:** `io.StringIO` supports incremental writes with amortised efficient buffering. Writing directly to a file avoids holding the complete final statement in memory, but adds file I/O and produces a file rather than a string. `join()` needs memory for the parts and final string; file streaming needs a smaller working memory footprint.

## Q5 – Functions, Parameters and Scope (7 Marks)
A mutable default list is created once when the function is defined. The buggy `order=[]` parameter is reused across calls, so the second customer receives the first customer's item. Using `order=None` and creating a fresh list inside the function fixes the issue.

Positional arguments are useful for short, ordered values; keyword arguments improve clarity; default arguments support common values. Python functions can return multiple values as a tuple, demonstrated by returning both total and GST.

A local name exists inside a function. A global name is defined at module level and can be read inside a function. `global` is needed when rebinding a module-level name. `nonlocal` allows an inner function to rebind a variable in its enclosing function, demonstrated with a counter closure. Global mutation is usually avoided because it creates hidden dependencies and makes testing harder.

## Q6 – Recursion and Its Limits (8 Marks)
The base case is `n <= 1`, which returns one way. The recursive case is `ways(n-1) + ways(n-2)`. For n=5, calls branch into n=4 and n=3; those calls branch again, repeating values such as n=3 and n=2. Plain recursion has exponential time, approximately O(φⁿ), and O(n) maximum call-stack space.

Memoisation stores each computed result, reducing time to O(n), with O(n) cache and recursion stack space. The iterative version retains only the previous two values, giving O(n) time and O(1) auxiliary space. The memoised recursive version may raise `RecursionError` at n=1000 because Python enforces a recursion-depth limit. The iterative method is the safer deployment choice for 1,000 steps; increasing the recursion limit can risk exhausting the C stack and is not the preferred fix.

Expected values for n=1 to 6 are 1, 2, 3, 5, 8, 13.

## Q7 – Diagnose, Redesign and Validate (13 Marks)
**Selected program:** Q6 plain recursive stair counting.

**A. Diagnosis:** The naive function recursively recomputes the same smaller stair counts many times. Its call count grows exponentially as n increases.

**B. Objective:** Preserve the exact answer while reducing time growth to O(n), avoiding recursive stack growth, and using O(1) auxiliary memory.

**C. Revised design:** Maintain only two values: the number of ways for the previous step and the current step. For each next step, add the two values and shift the pair. This removes repeated subproblem calculations.

**Pseudocode:**
1. If n is zero or one, return one.
2. Set previous = 1 and current = 1.
3. Repeat from step 2 through n: next = previous + current; previous = current; current = next.
4. Return current.

**D. Prediction:** The iterative solution will produce the same results, run in linear time, and complete n=1000 without a recursion-depth error.

**E. Validation:** `Task07/task07_redesign.py` compares both versions for n=10, 20, 25, and 30 using identical inputs, reports whether results match, and measures elapsed time. It also runs the iterative version for n=1000. Run it locally to record machine-specific timings.

**F. Evaluation:** The objective is met if outputs match and the iterative implementation completes n=1000 with O(1) auxiliary space. The original recursive version is useful for explaining the recurrence and is concise for small n, but it is unsuitable for large inputs because of repeated work and stack growth.

## Complexity Summary

| Task / Approach | Time Complexity | Auxiliary Space |
|---|---:|---:|
| Q1 decision chain | O(k) branches | O(1) |
| Q2 loop | O(a) | O(1) |
| Q2 recursive attempts | O(a) | O(a) stack |
| Q3 normalise/validate | O(L) | O(L) for new normalised string |
| Q4 join | O(n) output work | O(n) output/parts |
| Q4 repeated concatenation | Up to O(n²) copying | Up to O(n) output |
| Q5 add one item | O(1) amortised | O(1) extra per new order |
| Q6 naive recursion | O(φⁿ) | O(n) stack |
| Q6 memoisation | O(n) | O(n) cache + stack |
| Q6 iterative | O(n) | O(1) |
| Q7 iterative redesign | O(n) | O(1) |

## Conclusion
The assignment demonstrates how choosing the correct control structure and data-handling approach improves correctness, readability, and performance. Testing boundary inputs and measuring execution time are important because theoretical complexity and actual timings describe different aspects of program behaviour.

## Appendix – Execution Evidence
Run each `.py` file from the project root and save genuine terminal screenshots in the matching task folder if required by faculty. Record your own benchmark results because timings vary by hardware and Python version.
