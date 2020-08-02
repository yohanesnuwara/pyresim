# PyReSim

<p align="center">
  <img width="400" height="300" src="https://user-images.githubusercontent.com/51282928/89118699-ebf24d00-d4d1-11ea-92a9-76495358fc6c.png">
</p>

This simulator is built based on explanations in *Petroleum Reservoir Simulation: A Basic Approach* textbook by Abou-Kassem et al (2006), built using Python language. The goal of this simulator is that we understand how a reservoir simulator works. So, we will build from scratch, from a very simple reservoir model to more advanced.

## Simulators Available

|Simulator name|Assumptions|Description|
|:--:|:--:|:--:|
|[`floweq_1d`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/floweq_1d.py),<br>[`floweq_2d`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/floweq_2d.py)<br>[`floweq_3d`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/floweq_3d.py)|Multidimensional, homogeneous,<br> single-phase, rectangular grid,<br> same size grids|Produces flow equations for each grid block|
|[`floweq_well`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/floweq_well.py)|2D, homogeneous, single-phase,<br> cylindrical grid, varying size grid<br> in `r` direction|Produces flow equations for each grid block<br> (well simulation)|

## Cases

|Case No.|Picture|Description|Simulators used|
|:--:|:--:|:--:|:--:|
|1|<div><img src="https://user-images.githubusercontent.com/51282928/88264056-526ab480-ccf5-11ea-9cd0-622b6a57af6b.png" width="300"/></div><br>[Click here for case description](https://github.com/yohanesnuwara/pyresim/blob/master/docs/case_descriptions.md#case-1-1d-rectangular-reservoir-homogeneous-single-phase)|1D reservoir, same size rectangular<br> grid, homogeneous, single-phase|[`floweq_1d`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/floweq_1d.py)|
|2|<div><img src="https://user-images.githubusercontent.com/51282928/88287885-28c58380-cd1d-11ea-915a-80a7bae7df72.png" width="250"/></div><br>[Click here for case description](https://github.com/yohanesnuwara/pyresim/blob/master/docs/case_descriptions.md#case-2-2d-rectangular-reservoir-homogeneous-single-phase)|2D reservoir, same size rectangular<br> grid, homogeneous, single-phase|[`floweq_2d`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/floweq_2d.py)|
|3|<div><img src="https://user-images.githubusercontent.com/51282928/88464930-d638c280-cee8-11ea-8014-59c010afd95b.png" width="300"/></div><br>[Click here for case description](https://github.com/yohanesnuwara/pyresim/blob/master/docs/case_descriptions.md#case-3-3d-rectangular-reservoir-homogeneous-single-phase)|3D reservoir, same size rectangular<br> grid, homogeneous, single-phase|[`floweq_3d`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/floweq_3d.py)|
|4|<div><img src="https://user-images.githubusercontent.com/51282928/88837303-4d7c9800-d202-11ea-8ee4-5221e8e1e298.png" width="200"/></div><br>[Click here for case description](https://github.com/yohanesnuwara/pyresim/blob/master/docs/case_descriptions.md#case-4-2d-cylindrical-reservoir-well-in-the-middle-homogeneous-varying-size-in-radial-direction)|2D reservoir, varying size in radial<br> direction, homogeneous, single-phase|[`floweq_well`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/floweq_well.py)|

## Challenging Case

PyReSim is performed to a more challenging case. This case is obtained from a "Chapter Project" in *Basic Applied Reservoir Simulation* (Ertekin, Abou-Kassem, King; 2001). In this case, the reservoir geometry is complex (irregular boundary, varied grid size) and reservoir property is heterogeneous. [See more details of this case](https://github.com/yohanesnuwara/pyresim/blob/master/docs/challenge_description.md)

<div><img src="https://user-images.githubusercontent.com/51282928/89013581-54a8c080-d33e-11ea-8f96-704e8b263c5c.png" width="300"/>  <img src="https://user-images.githubusercontent.com/51282928/89118272-894b8200-d4ce-11ea-9e02-6d18d3e48583.png" width="650"/></div>

## Using PyReSim for Academic or Industry Use

For any specific need that is unique to your case, and want to use PyReSim for your specific need, you are encouraged to discuss with us. We could provide a tutorial for your need. Presented here are the simulator codes applied to the cases presented above. We hope PyReSim can help to simulate most of your needs.

**Contact**<br>
📧 e-mail: ign.nuwara97@gmail.com

## Contributing to this Work

## Donation

We tirelessly spent days and nights to continuously develop, fine-tune, and improve PyReSim as an open-source Python reservoir simulator program, with the hope that everyone get benefits from. This work is done without direct financial support. If you like (and trust) this work, we would be very glad if you would consider to give us a little gift. Your donation will allow us to spend even more time improving this simulator.

## License

The author chooses Creative Commons BY-NC-ND 4.0 International to license this work. 

<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License</a>.
