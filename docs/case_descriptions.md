## Simulation Cases 

* 1D one-dimensional
* 2D two-dimensional (regular reservoir geometry)
* 2D two-dimensional (irregular reservoir geometry)
* Cylindrical

For 2D reservoirs, there are two kinds: non-elevated and elevated

Each of these is simulated in five ways: 

* Incompressible (single-phase water or gas-free oil)
* Slightly compressible (single-phase live or volatile oil)
* Compressible (single-phase gas)
* Two-phase oil-water
* Two-phase oil-gas
* Two-phase water-gas
* Three-phase water-oil-gas

### 1D Basic

**Well input data**

|Name|Location|Radius|Skin|Configuration|Condition|Value|
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|A|4|3.5|0|0|Constant rate|-150 STB/D|
|B|8|3.5|0|0|Constant rate|350 STB/D|
|C|10|3.5|0|0|Constant rate|-100 STB/D|

**Reservoir boundary data**

|Boundary|Condition|Value|
|:--:|:--:|:--:|
|West|No flow|0 STB/D|
|East|No flow|0 STB/D|

### 1D Intermediate

**Well input data**

|Name|Location|Radius|Skin|Configuration|Condition|Value|
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|A|1|3.5|1.5|0|Constant FBHP|3,900 psi|
|B|4|2.5|0.1|0|Constant rate|-150 STB/D|
|C|6|2|0|0|Shut-in|0 STB/D|
|D|8|4|0.1|0|Constant rate|250 STB/D|
|E|10|3.5|0|2|Constant rate|-150 STB/D|

**Reservoir boundary data**

|Boundary|Condition|Value|
|:--:|:--:|:--:|
|West|Constant pressure|4,000 psi|
|East|Constant pressure gradient|-0.5 psi/ft|

### 1D Advanced

Well input and reservoir boundary data are similar to **1D Intermediate** case, only now it is elevated. 

### Regular 2D Basic

**Well input data**

|Name|Location|Radius|Skin|Configuration|Condition|Value|
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|A|(10,10)|3.5|0|0|Constant rate|-100 STB/D|
|B|(40,40)|3.5|0|0|Constant rate|-150 STB/D|
|C|(10,40)|3.5|0|0|Constant rate|-100 STB/D|
|D|(40,10)|3.5|0|0|Constant rate|-200 STB/D|
|E|(25,25)|3.5|0|0|Constant rate|500 STB/D|

**Reservoir boundary data**

|Boundary|Condition|Value|
|:--:|:--:|:--:|
|West|Constant pressure|3,000 psi|
|East|Constant pressure|3,000 psi|
|South|Constant pressure|3,000 psi|
|North|Constant pressure|3,000 psi|
