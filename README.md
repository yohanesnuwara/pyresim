# PyReSim (Python Reservoir Simulator)

Reservoir simulator in Python language (simply building it step-by-step from scratch, to advanced)

<div>
<img src="https://user-images.githubusercontent.com/51282928/85827088-bb6f1300-b7af-11ea-9a1f-eed08adddaff.png" width="400"/><img src="https://user-images.githubusercontent.com/51282928/88214648-b5703300-cc84-11ea-820c-baf233353647.png" width="400"/>
</div>

This simulator is built based on explanations in *Petroleum Reservoir Simulation: A Basic Approach* textbook by Abou-Kassem et al (2006), built using Python language. The goal of this simulator is that we understand how a reservoir simulator works. So, we will build from scratch, from a very simple reservoir model to more advanced.

## Simulators Available

|Simulator name|Assumptions|Description|
|:--:|:--:|:--:|
|[`floweq_1d`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/floweq_1d.py),<br>[`floweq_2d`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/floweq_2d.py)<br>[`floweq_3d`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/floweq_3d.py)|Multidimensional, homogeneous,<br> single-phase, rectangular shape,<br> same size grids|Produces flow equations for each grid block|

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

#### Using [`floweq_1d`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/floweq_1d.py) to produce the flow equations in each of the grid blocks

### Case 2. 2D reservoir, homogeneous, single-phase

<div>
<img src="https://user-images.githubusercontent.com/51282928/88287885-28c58380-cd1d-11ea-915a-80a7bae7df72.png" width="500"/>
</div>

> 4x3 reservoir. A well located in grid block 7 produces at a rate of 4000
STB/D. AIIgridblocks have Δx = 250 ft, Δy = 300 ft, h = 100 ft, kx = 270 md,
and ky = 220 md. The FVF and viscosity of the flowing fluid are 1.0 RB/STB and 2
cp, respectively. The reservoir south boundary is maintained at 3000 psia, the
reservoir west boundary is sealed off to flow, the reservoir east boundary is kept
at a constant pressure gradient of O. 1 psi/ft, and the reservoir loses fluid across its
north boundary at a rate of 500 STB/D.

#### Using [`floweq_2d`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/floweq_2d.py) to produce the flow equations in each of the grid blocks

### Case 2. 3D reservoir, homogeneous, single-phase

<div>
<img src="https://user-images.githubusercontent.com/51282928/88464930-d638c280-cee8-11ea-8014-59c010afd95b.png" width="500"/>
</div>

> 4x3x3 reservoir. All grid blocks have
Δx = 250 ft, Δy = 30Oft, Δz = 33.333 ft, kx = 270 md, ky = 220 md, and kz = 50 md.
The FVF, density, and viscosity of the flowing fluid are 1.0 RB/STB, 55 Ibm/ft3,
and 2 cp, respectively.

#### Using [`floweq_3d`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/floweq_3d.py) to produce the flow equations in each of the grid blocks
