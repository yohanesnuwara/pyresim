[`template.txt`](https://github.com/yohanesnuwara/pyresim/blob/master/input/template.txt) is the input format for PyReSim. 
Input data in TXT file is used as is. Do not modify the lines, and just input the numbers and information. Any change in the line will make the program won't run. 

```
from input_output import read_data

filepath = '/.../template.txt'
xi, yi, dx, dy, dz, kx, ky, kz, poro, rho, cpore, mu, B, well, boundary = read_input(filepath)
```

### Important Notes:

* well should be inputed in order based on their block coordinates
