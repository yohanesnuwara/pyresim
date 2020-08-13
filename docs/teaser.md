## Teaser 1

An incompressible gas-free oil in an incompressible 2D reservoir with uniform grid dimension. Reservoir boundary in the west has constant pressure, in the east is sealed (no flow), in the south has pressure gradient, and in the north has constant rate. Five wells penetrates the reservoir, with various wellbore radius, skin, and operating conditions.

**Reservoir input data**

|Geometry and property|Value|
|:--:|:--:|
|Number of grid blocks in x-direction|50|
|Number of grid blocks in y-direction|50|
|Grid block length|100 ft|
|Grid block width|150 ft|
|Grid block thickness|75 ft|
|Permeability in x-direction|150 md|
|Permeability in y-direction|100 md|
|Porosity|0.2|
|Formation compressibility|0 sip|
|Oil viscosity|3.5 cp|
|Oil FVF|1|

> An incompressible gas-free oil means it has `B` or FVF equals 1. An incompressible reservoir means it has pore compressibility `CPORE` equals 0. Check out the [input file](https://github.com/yohanesnuwara/pyresim/blob/master/input/teaser1.txt)

Under this condition, pressure distribution in the reservoir behaves like **steady-state** (no change with time), hence, `incompressible` solver is used. 
