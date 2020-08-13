[`template.txt`](https://github.com/yohanesnuwara/pyresim/blob/master/input/template.txt) is the input format for PyReSim. 
Input data in TXT file is used as is. Just input the numbers.

```
from input_output import read_data

filepath = '/.../template.txt'
reservoir_input, well, west_boundary, east_boundary, south_boundary, north_boundary = read_input(filepath)
```
If the program won't run, make sure that you have:

* Inputted the numbers without any space. The program is based on delimiter comma `,`, not comma-space `, `
* Not changed any lines. Here is a piece of example.

The correct one (from `template.txt`), pay attention to the space between the lines.

```
----------------
WELL INPUT
----------------

WELLNAME
A,B,C,D,E

BLOCK COORD X
10,40,10,40,25

BLOCK COORD Y
10,40,40,10,25
```

So this won't run

```
----------------
WELL INPUT
----------------
WELLNAME
A,B,C,D,E
BLOCK COORD X
10,40,10,40,25
BLOCK COORD Y
10,40,40,10,25
```

### Important Notes:

* well should be inputed in order based on their block coordinates
