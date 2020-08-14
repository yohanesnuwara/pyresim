# PyReSim*

#### Python reservoir simulation from single-phase simple reservoir to multi-phase complex reservoir 

*) still on work. Progress bar ![30%](https://progress-bar.dev/30)

<p align="center">
  <img width="400" height="300" src="https://user-images.githubusercontent.com/51282928/90232288-a5dca800-de46-11ea-8b11-2d4bdbf3186e.png">
</p>

> This repository is still worked on. However, each week or so, there will be a teaser posted in my LinkedIn, about one reservoir simulation case and how PyReSim is used to solve. It will be scheduled for launch once all simulators have been set up and complete (scheduled in November 2020). See my progress bar to keep updated, stay tuned!

## Aspects simulated in *PyReSim*

|Aspects|Availability|
|:--:|:--|
|Reservoir geometry|Regular 1D and 2D; 2D cylindrical well simulation; 2D reservoir with different elevations; 2D reservoir with irregular boundaries; 3D reservoir (*)|
|Reservoir property|Homogeneous (both isotropic & anisotropic permeability); heterogeneous (*)|
|Boundary conditions|Specified flow rate; Specified pressure; Specified pressure gradient; No flow|
|Well details|Diameter; skin factor; location at the grid block (center, edge, or corner)|
|Well-operating conditions|Specified flow rate (producer/injector well); Specified flowing borehole pressure (FBHP); Specified pressure gradient; Shut-in|
|Reservoir fluid types|Single-phase incompressible fluid (brine), slightly-compressible fluid (undersaturated oil), compressible fluid (gas); Multi-phase reservoir (brine-oil-water)|
|Solver methods|Matrix inversion (very 3x basic method); explicit; implicit; Crank-Nicholson; many more. |

> (*) These aspects are still not available on the first launch (in November 2020). It will be available on the second launch (afterwards). 

## Teasers

|Teaser No.|Picture|Description|Input data|Simulator|
|:--:|:--:|:--:|:--:|:--:|
|1|<div><img src="https://user-images.githubusercontent.com/51282928/90217017-50929d80-de2a-11ea-8bb1-560b2ff2365c.png" width="200"/></div><br>[Click here for case description](https://github.com/yohanesnuwara/pyresim/blob/master/docs/teaser.md#teaser-1)|A gas-free oil in a 2D reservoir with uniform<br> grid dimension. Reservoir boundary in the west<br> has constant pressure, in the east is sealed (no flow),<br> in the south has pressure gradient, and in the<br> north has constant rate. Five wells penetrates<br> the reservoir, with various wellbore radius,<br> skin, and operating conditions.|[`input file`](https://github.com/yohanesnuwara/pyresim/blob/master/input/teaser1.txt)|[`source code`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/PyReSim_teaser1.ipynb)|

## Simulation Cases

### Basic

|Case No.|Picture|Description|Input data|Simulator|
|:--:|:--:|:--:|:--:|:--:|

### Intermediate 

> Varying boundary conditions in different sides of the reservoir, and varying well operating conditions, configurations, wellbore radius, and skin.

|Case No.|Picture|Description|Input data|Simulator|
|:--:|:--:|:--:|:--:|:--:|

### Advanced 

> Giving uneven distributions of multiple boundary conditions, and giving elevation to the grid blocks. 

|Case No.|Picture|Description|Input data|Simulator|
|:--:|:--:|:--:|:--:|:--:|

## Challenging Case

PyReSim will be performed to a more challenging case. This case is obtained from a "Chapter Project" in *Basic Applied Reservoir Simulation* (Ertekin, Abou-Kassem, King; 2001). In this case, the reservoir geometry is complex (irregular boundary, varied grid size) and reservoir property is heterogeneous. [See more details of this case](https://github.com/yohanesnuwara/pyresim/blob/master/docs/challenge_description.md)

<div><img src="https://user-images.githubusercontent.com/51282928/89013581-54a8c080-d33e-11ea-8f96-704e8b263c5c.png" width="300"/>  <img src="https://user-images.githubusercontent.com/51282928/89118272-894b8200-d4ce-11ea-9e02-6d18d3e48583.png" width="650"/></div>

## License

The author chooses Creative Commons BY-NC-ND 4.0 International to license this work. Please read what's permitted and what's not permitted [here](https://github.com/yohanesnuwara/pyresim/blob/master/LICENSE.md)

<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License</a>.

<!--
**yohanesnuwara/yohanesnuwara** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

## Cases

|Case No.|Picture|Description|Simulator|
|:--:|:--:|:--:|:--:|
|1|<div><img src="https://user-images.githubusercontent.com/51282928/88264056-526ab480-ccf5-11ea-9cd0-622b6a57af6b.png" width="300"/></div><br>[Click here for case description](https://github.com/yohanesnuwara/pyresim/blob/master/docs/case_descriptions.md#case-1-1d-rectangular-reservoir-homogeneous-single-phase)|1D reservoir, same size rectangular<br> grid, homogeneous, single-phase|[`floweq_1d`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/floweq_1d.py)|
|2|<div><img src="https://user-images.githubusercontent.com/51282928/88287885-28c58380-cd1d-11ea-915a-80a7bae7df72.png" width="250"/></div><br>[Click here for case description](https://github.com/yohanesnuwara/pyresim/blob/master/docs/case_descriptions.md#case-2-2d-rectangular-reservoir-homogeneous-single-phase)|2D reservoir, same size rectangular<br> grid, homogeneous, single-phase|[`floweq_2d`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/floweq_2d.py)|
|3|<div><img src="https://user-images.githubusercontent.com/51282928/88464930-d638c280-cee8-11ea-8014-59c010afd95b.png" width="300"/></div><br>[Click here for case description](https://github.com/yohanesnuwara/pyresim/blob/master/docs/case_descriptions.md#case-3-3d-rectangular-reservoir-homogeneous-single-phase)|3D reservoir, same size rectangular<br> grid, homogeneous, single-phase|[`floweq_3d`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/floweq_3d.py)|
|4|<div><img src="https://user-images.githubusercontent.com/51282928/88837303-4d7c9800-d202-11ea-8ee4-5221e8e1e298.png" width="200"/></div><br>[Click here for case description](https://github.com/yohanesnuwara/pyresim/blob/master/docs/case_descriptions.md#case-4-2d-cylindrical-reservoir-well-in-the-middle-homogeneous-varying-size-in-radial-direction)|2D reservoir, varying size in radial<br> direction, homogeneous, single-phase|[`floweq_well`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/floweq_well.py)|

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
