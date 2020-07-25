# PyReSim (Python Reservoir Simulator)

Reservoir simulator in Python language (simply building it step-by-step from scratch, to advanced)

<div>
<img src="https://user-images.githubusercontent.com/51282928/85827088-bb6f1300-b7af-11ea-9a1f-eed08adddaff.png" width="400"/><img src="https://user-images.githubusercontent.com/51282928/88214648-b5703300-cc84-11ea-820c-baf233353647.png" width="400"/>
</div>

This simulator is built based on explanations in *Petroleum Reservoir Simulation: A Basic Approach* textbook by Abou-Kassem et al (2006). This simulator is built using Python language. The goal of this simulator is that we understand how a reservoir simulator works. So, we will build from scratch, from a very simple reservoir model to more advanced.

## Simulators Available

|Simulator name|Assumptions|Description|
|:--:|:--:|:--:|
|`floweq_1d`,<br>`floweq_2d`<br>`floweq_3d`|Multidimensional, homogeneous,<br> single-phase, rectangular shape,<br> same size grids|Produces flow equations for each grid block|

## Cases

### Case 1. 1D reservoir, homogeneous, single-phase

<div>
<img src="https://user-images.githubusercontent.com/51282928/88264056-526ab480-ccf5-11ea-9cd0-622b6a57af6b.png" width="500"/>
</div>

> A 5000 ft x 1200 ft x 75 ft horizontal reservoir contains oil that flows
along its length. The reservoir rock porosity and permeability are 0.18 and 15 md,
respectively. The oil FVF and viscosity are 1 RB/STB and 10 cp, respectively. The
reservoir has a well located at 3500 ft from the reservoir left boundary and
produces oil at a rate of 150 STB/D. 

#### Using `floweq_1d` to produce the flow equations in each of the grid blocks
