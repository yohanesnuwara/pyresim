## `floweq` Documentation

`floweq` is a very basic simulator that produces flow equation of each grid block in the reservoir. To understand properly how reservoir simulator works, understanding flow equation is very important. 

In each block, there is a flow equation that contains pressure as a variable. If a reservoir is discretized into 4x3x3 grid blocks, there will be 36 sets of flow equations. Each of these equations has pressure as a variable. Later, these set of equation will be solved to finally produce the pressure in each block. This is an objective of every reservoir simulator.

Before advancing further, read about **flow equation** [here](https://github.com/yohanesnuwara/pyresim/wiki/Flow-Equations) 

Let's start from 1D, then 2D, and finally advance to 3D. 

### 1D Reservoir

**Block notation**. A 1D reservoir grid blocks are numbered as 1, 2, 3, ..., `n`, with `n` is the number of grid blocks.

**Flow direction**. A 1D reservoir has only one coordinate, the x coordinate. The flow that happens in each grid block therefore has 2 direction, x+ and x-. 

**Reservoir boundary**. A 1D reservoir has two boundary blocks. If indicated by a compass, one boundary is located in the `West` and another one in the `East`. If a 1D reservoir is discretized into `n=5` blocks, grid block 1 and 5 are the boundaries. Grid 2, 3, and 4 is the internal blocks. 

**Flow equation**

![image](https://user-images.githubusercontent.com/51282928/88473162-e2eb0400-cf44-11ea-998d-19935257562f.png)

Each block has a flow equations consisting of **3 terms** in the left-hand side (LHS). **The first 2 terms** are the flow terms (flow in the block), and the **last term** is the source term. 

It has 2 flow terms, because there are 2 flow directions in x+ and x- directions, as `qx+` and `qx-`. 

For internal blocks, all 2 flow terms are the inter-block flow (flow from adjacent blocks). Whereas for boundary blocks, one of the flow term is the boundary flow (flow from the boundary). The `West` boundary, `qx-` is the flow from the boundary. The `East` boundary, `qx+` is the flow from the boundary. 

The boundary flow can vary, depends on the **boundary conditions**. There are 4 boundary conditions, explained more detailed [here](https://github.com/yohanesnuwara/pyresim/wiki/Boundary-Conditions).

**Case 1**

Result:

```
Boundary Block 1: 0.152145 (p2 - p1) + 0.30429 (5000 - p1) + 0.0
Interior Block 2: 0.152145 (p1 - p2) + 0.152145 (p3 - p2) + 0.0
Interior Block 3: 0.152145 (p2 - p3) + 0.152145 (p4 - p3) + 0.0
Interior Block 4: 0.152145 (p3 - p4) + 0.152145 (p5 - p4) + -150.0
Boundary Block 5: 0.152145 (p4 - p5) + 0.0 + 0.0
```

### 2D Reservoir

Result:

```
southwest corner block (1, 1)
Boundary Block (1, 1): 18.257399999999997 (p(2, 1) - p(1, 1)) + 0.0 + 10.330833333333333 (p(1, 2) - p(1, 1)) + 20.661666666666665 (3000 - p(1, 1)) + 0 

west block (1, 2)
Boundary Block (1, 2): 18.257399999999997 (p(2, 2) - p(1, 2)) + 0.0 + 10.330833333333333 (p(1, 3) - p(1, 2)) + 10.330833333333333 (p(1, 1) - p(1, 2)) + 0 

northwest corner block (1, 3)
Boundary Block (1, 3): 18.257399999999997 (p(2, 3) - p(1, 3)) + 0.0 + -125.0 + 10.330833333333333 (p(1, 2) - p(1, 3)) + 0 

south block (2, 1)
Boundary block (2, 1): 18.257399999999997 (p(1, 1) - p(2, 1)) + 18.257399999999997 (p(3, 1) - p(2, 1)) + 10.330833333333333 (p(2, 2) - p(2, 1)) + 20.661666666666665 (3000 - p(2, 1)) + 0 

interior block (2, 2)
Interior block (2, 2): 18.257399999999997 (p(1, 2) - p(2, 2)) + 18.257399999999997 (p(3, 2) - p(2, 2)) + 10.330833333333333 (p(2, 3) - p(2, 2)) + 10.330833333333333 (p(2, 1) - p(2, 2)) + 0 

...
```

### 3D Reservoir

<div>
<img src="https://user-images.githubusercontent.com/51282928/88476192-c0ff7a80-cf60-11ea-8492-54fccd1aebc7.png" width="300"/>
</div>

Result:

```
Bottom southwest corner boundary block
Block (1, 1, 1): [6.0857391419999995 (p(2, 1, 1) - p(1, 1, 1))] + [0.0] + [3.443576675 (p(1, 2, 1) - p(1, 1, 1))] + [8.333333333333332] + [63.39438394383944 (p(1, 1, 2) - p(1, 1, 1)) - (-12.7313389786704)] + [122120.8712] + [0] 

Central southwest corner boundary block
Block (1, 1, 2): [6.0857391419999995 (p(2, 1, 2) - p(1, 1, 2))] + [0.0] + [3.443576675 (p(1, 2, 2) - p(1, 1, 2))] + [8.333333333333332] + [63.39438394383944 (p(1, 1, 3) - p(1, 1, 2)) - (-12.7313389786704)] + [63.39438394383944 (p(1, 1, 1) - p(1, 1, 2)) - (12.7313389786704)] + [0] 

Upper southwest corner boundary block
Block (1, 1, 3): [6.0857391419999995 (p(2, 1, 3) - p(1, 1, 3))] + [0.0] + [3.443576675 (p(1, 2, 3) - p(1, 1, 3))] + [8.333333333333332] + [126.78876788767889 (3000 - p(1, 1, 3) - (-114.58319664000001))] + [63.39438394383944 (p(1, 1, 2) - p(1, 1, 3)) - (12.7313389786704)] + [0] 

Bottom west boundary block
Block (1, 2, 1): [6.0857391419999995 (p(2, 2, 1) - p(1, 2, 1))] + [0.0] + [3.443576675 (p(1, 3, 1) - p(1, 2, 1))] + [3.443576675 (p(1, 1, 1) - p(1, 2, 1))] + [63.39438394383944 (p(1, 2, 2) - p(1, 2, 1)) - (-12.7313389786704)] + [122120.8712] + [0] 

Central west boundary block
Block (1, 2, 2): [6.0857391419999995 (p(2, 2, 2) - p(1, 2, 2))] + [0.0] + [3.443576675 (p(1, 3, 2) - p(1, 2, 2))] + [3.443576675 (p(1, 1, 2) - p(1, 2, 2))] + [63.39438394383944 (p(1, 2, 3) - p(1, 2, 2)) - (-12.7313389786704)] + [63.39438394383944 (p(1, 2, 1) - p(1, 2, 2)) - (12.7313389786704)] + [0] 

...
```
