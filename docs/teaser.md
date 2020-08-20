# Teasers of PyReSim before its Public Launch

## Teaser 1

<p align="center">
  <img width="300" height="300" src="https://user-images.githubusercontent.com/51282928/90217017-50929d80-de2a-11ea-8bb1-560b2ff2365c.png">
</p>

An incompressible gas-free oil in an incompressible 2D reservoir with uniform grid dimension. Reservoir boundary in the west has constant pressure, in the east is sealed (no flow), in the south has pressure gradient, and in the north has constant rate. Five wells penetrates the reservoir, with various wellbore radius, skin, and operating conditions.

Under this condition, pressure distribution in the reservoir behaves like **steady-state** (no change with time), hence, Incompressible (`incompressible`) solver is used. 

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

**Reservoir boundary data**

|Boundary|Condition|Value|
|:--:|:--:|:--:|
|West|Constant pressure|3,000 psi|
|East|No flow|0 STB/D|
|South|Constant pressure gradient|-0.2 psi/ft|
|North|Constant rate|-100 STB/D|

**Well input data**

|Name|Radius|Skin|Condition|Value|
|:--:|:--:|:--:|:--:|:--:|
|A|3.5|1.5|Constant FBHP|2,000 psi|
|B|4|0.1|Constant rate|-600 STB/D|
|C|4.5|0|Constant rate|350 STB/D|
|D|3.5|0.1|Constant FBHP|3,000 psi|
|E|3.2|0|Constant rate|-150 STB/D|

## Teaser 2

<p align="center">
  <img width="500" height="300" src="https://user-images.githubusercontent.com/51282928/90748253-22b2ca80-e2fc-11ea-8b80-e3878aff7f77.png">
</p>

A 2D reservoir with irregular boundaries hosting a volatile oil. The reservoir boundary is sealed of flow. 2 wells (injector and producer) penetrate into the reservoir, and the flow rate as well as FBHP will be reported after 50 days.

The irrregular reservoir is defined as in above figure, as the active blocks (orange color) and the inactive blocks (shaded blue color). Given each block notation.

Different from the Teaser 1, now volatile oil has larger fluid compressibility (`CFLUID`) and larger FVF (`B`). Also the reservoir is an ideal compressible reservoir, with larger pore compressibility `CPORE`. Under this condition, pressure distribution will behave dynamic, hence the Slightly Compressible (`slicomp`) solver is used. 
