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

|Name|Radius|Skin|Condition|Value|
|:--:|:--:|:--:|:--:|:--:|
|A|3.5|0|Constant rate|-150 STB/D|
|B|3.5|0|Constant rate|350 STB/D|
|C|3.5|0|Constant rate|-100 STB/D|

**Reservoir boundary data**

|Boundary|Condition|Value|
|:--:|:--:|:--:|
|West|No flow|0 STB/D|
|East|No flow|0 STB/D|

### 1D Intermediate

**Well input data**

|Name|Radius|Skin|Condition|Value|
|:--:|:--:|:--:|:--:|:--:|
|A|3.5|1.5|Constant FBHP|3,900 psi|
|B|2.5|0.1|Constant rate|-150 STB/D|
|C|2|0|Shut-in|0 STB/D|
|B|4|0.1|Constant rate|250 STB/D|
|C|3.5|0|Constant rate|-150 STB/D|

**Reservoir boundary data**

|Boundary|Condition|Value|
|:--:|:--:|:--:|
|West|Constant pressure|4,000 psi|
|East|Constant pressure gradient|-0.5 psi/ft|

### 1D Advanced

Well input and reservoir boundary data are similar to **1D Intermediate** case, only now it is elevated. 
