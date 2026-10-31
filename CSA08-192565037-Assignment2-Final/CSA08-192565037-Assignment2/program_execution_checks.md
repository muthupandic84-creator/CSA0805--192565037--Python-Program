# Program execution checks

Python runtime: 3.13.5

## Task01/task01_subsidy.py
Exit code: 0
```text
ID  Units  Ration  >80  Separate-if result                 Chained result
H1  99     False   False Full subsidy                        Full subsidy
H2  100    True    False Full subsidy                        Full subsidy
H3  101    True    False Partial subsidy                     Partial subsidy
H4  101    False   False No subsidy                          No subsidy
H5  150    True    False Partial subsidy                     Partial subsidy
H6  200    False   True No subsidy                          No subsidy
H7  201    False   False No subsidy                          No subsidy
H8  250    False   True Special elderly exemption           Special elderly exemption

Boundary checks (100, 101, 200, 201):
100 => Full subsidy
101 => Partial subsidy
200 => Partial subsidy
201 => Special elderly exemption

Design decision: use if-elif-else for mutually exclusive unit bands.
Nested checks keep the eligibility conditions close to each band.
```

## Task02/task02_otp.py
Exit code: 0
```text
WHILE DEMO:
Blank entry: not counted
Wrong OTP (1/3)
Wrong OTP (2/3)
OTP verified using while loop
\nFOR RANGE(3) DEMO:
Wrong OTP (1/3)
Wrong OTP (2/3)
Wrong OTP (3/3)
Account locked for 30 minutes
\nRECURSIVE DEMO: Account locked for 30 minutes
\nChanged condition: after successful security answer, call with max_attempts=5.
A while loop handles skipped blank entries and dynamically changed limits more naturally.
```

## Task03/task03_vehicle_validator.py
Exit code: 0
```text
Input                Normalised   Result   Receipt
tn 09 ab 1234        TN09AB1234   valid    TN 09 AB 1234
KA-01-M-0007         KA01M0007    valid    KA 01 M 0007
TN9AB1234            TN9AB1234    INVALID  -
TN 22 1234 AB        TN221234AB   INVALID  -
mh 12 xyz 6789       MH12XYZ6789  INVALID  -
DL-8C-1234           DL8C1234     INVALID  -

Slice inquiry:
TN09AB1234 length = 10 last four = 1234 middle = AB
TN09A1234 length = 9 last four = 1234 middle = A

Strings are immutable: upper() returns a new string; it does not alter the original.
```

## Task04/task04_string_benchmark.py
Exit code: 0
```text

Lines: 1,000 | same output: True
+=      samples=[9.4e-05, 0.000161, 8.6e-05] average=0.000114s
join    samples=[8.9e-05, 7.4e-05, 6.9e-05] average=0.000078s
f-string samples=[0.000108, 0.000173, 6.7e-05] average=0.000116s

Lines: 10,000 | same output: True
+=      samples=[0.001072, 0.001031, 0.000905] average=0.001003s
join    samples=[0.001175, 0.000828, 0.000664] average=0.000889s
f-string samples=[0.000678, 0.000611, 0.000552] average=0.000614s

Lines: 200,000 | same output: True
+=      samples=[0.021398, 0.021011, 0.024905] average=0.022438s
join    samples=[0.018543, 0.018746, 0.018508] average=0.018599s
f-string samples=[0.015278, 0.01381, 0.012403] average=0.013831s
```

## Task05/task05_functions_scope.py
Exit code: 0
```text
Buggy shared default:
['Tea', 'Vada'] ['Tea', 'Vada']
Correct independent defaults:
['Tea'] ['Vada']
Three customer orders: [['Tea'], ['Vada'], ['Coffee']]
Total including GST: Rs 94.50; GST: Rs 4.50
This is local
Global value: SIMATS ENGINEERING
Nonlocal counter: 1 2 3
Buggy default list object: (['Tea', 'Vada'],)
```

## Task06/task06_recursion.py
Exit code: 0
```text
Hand-check values:
n=1: 1
n=2: 2
n=3: 3
n=4: 5
n=5: 8
n=6: 13

Call counts:
n=10: naive=89, calls=0; memo=89, calls=0
n=20: naive=10946, calls=0; memo=10946, calls=0
n=25: naive=121393, calls=0; memo=121393, calls=0
n=30: naive=1346269, calls=0; memo=1346269, calls=0

For n=1000:
memoised result: 70330367711422815821835254877183549770181269836358732742604905087154537118196933579742249494562611733487750449241765991088186363265450223647106012053374121273867339111198139373125598767690091902245245323403501
Loop result for n=1000: 70330367711422815821835254877183549770181269836358732742604905087154537118196933579742249494562611733487750449241765991088186363265450223647106012053374121273867339111198139373125598767690091902245245323403501
The loop avoids recursion depth and uses O(1) extra space.
```

## Task07/task07_redesign.py
Exit code: 0
```text
Q7 redesign: naive recursive stair count -> iterative two-value update
Objective: preserve the answer while reducing repeated calls and stack use.
n=10: same=True, naive=0.000008s, loop=0.000002s
n=20: same=True, naive=0.000657s, loop=0.000002s
n=25: same=True, naive=0.007791s, loop=0.000003s
n=30: same=True, naive=0.100161s, loop=0.000006s
n=1000: result has 209 digits; loop time=0.000053s
Trade-off: iterative version is less directly recursive but uses O(1) extra space.
```
