# PyReSim*

#### Python reservoir simulation from single-phase simple reservoir to multi-phase complex reservoir 

*) still on work. Progress bar ![40%](https://progress-bar.dev/40)

<p align="center">
  <img width="400" height="250" src="https://user-images.githubusercontent.com/51282928/91322826-60c35900-e7ea-11ea-8e5e-102a0f1a0f79.png">
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
|Reservoir fluid types|Single-phase incompressible fluid (brine), slightly-compressible fluid (undersaturated oil), compressible fluid (gas); Multi-phase reservoir (brine-oil-gas)|
|Solver methods|Matrix inversion (very 3x basic method); explicit; implicit; Crank-Nicholson; many more. |

> (*) These aspects are still not available on the first launch (in November 2020). It will be available on the second launch (afterwards). 

## Teasers

|Teaser No.|Picture|Description|Input data|Simulator|
|:--:|:--:|:--:|:--:|:--:|
|1|<div><img src="https://user-images.githubusercontent.com/51282928/90217017-50929d80-de2a-11ea-8bb1-560b2ff2365c.png" width="200"/></div><br>[Click here for case description](https://github.com/yohanesnuwara/pyresim/blob/master/docs/teaser.md#teaser-1)|A gas-free oil in a 2D reservoir with uniform<br> grid dimension. Reservoir boundary in the west<br> has constant pressure, in the east is sealed (no flow),<br> in the south has pressure gradient, and in the<br> north has constant rate. Five wells penetrates<br> the reservoir, with various wellbore radius,<br> skin, and operating conditions.|[`input file`](https://github.com/yohanesnuwara/pyresim/blob/master/input/teasers/teaser1_input.txt)|[`source code`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/teasers/PyReSim_teaser1.ipynb)|
|2|<div><img src="https://user-images.githubusercontent.com/51282928/90431371-21fb1800-e0f3-11ea-9afc-2921fa94e196.png" width="200"/></div><br>[Click here for case description](https://github.com/yohanesnuwara/pyresim/blob/master/docs/teaser.md#teaser-2)|A 2D reservoir with irregular boundaries<br> hosting a volatile oil. The reservoir is bounded<br> by a constant pressure. 2 wells penetrate into the<br> reservoir, and the flow rate as well as FBHP will be<br> reported after 50 days.<br>|[`input file`](https://github.com/yohanesnuwara/pyresim/blob/master/input/teasers/teaser2_input.txt)|[`source code`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/teasers/PyReSim_teaser2.ipynb)|
|3|<div><img src="https://user-images.githubusercontent.com/51282928/89118863-7b4c3000-d4d3-11ea-918d-8432b110b475.png" width="200"/></div>|The same 2D reservoir in Teaser 2, has now<br> elevations (Pseudo-3D). The reservoir hosts gas.<br> The reservoir is bounded by a constant pressure.<br> 2 wells penetrate into the reservoir, and the flow<br> rate as well as FBHP will be reported after 50 days.|Coming soon|Coming soon|

## Challenging Case

PyReSim will be performed to a more challenging case. This case is obtained from a "Chapter Project" in *Basic Applied Reservoir Simulation* (Ertekin, Abou-Kassem, King; 2001). In this case, the reservoir geometry is complex (irregular boundary, varied grid size) and reservoir property is heterogeneous. [See more details of this case](https://github.com/yohanesnuwara/pyresim/blob/master/docs/challenge_description.md)

<div><img src="https://user-images.githubusercontent.com/51282928/89013581-54a8c080-d33e-11ea-8f96-704e8b263c5c.png" width="300"/>  <img src="https://user-images.githubusercontent.com/51282928/89118272-894b8200-d4ce-11ea-9e02-6d18d3e48583.png" width="650"/></div>

## Open for Contribution!

These is a list contains several options for contributions:
* Help writing and translating a reservoir data into Schlumberger ECLIPSE format, or JSON format
* (Updated more soon)

Let's make PyReSim better together. If you're confident to contribute, please let me know and [mail me](ign.nuwara97@gmail.com)

## License

The author chooses Creative Commons BY-NC-ND 4.0 International to license this work. Please read what's permitted and what's not permitted [here](https://github.com/yohanesnuwara/pyresim/blob/master/LICENSE.md)

<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License</a>.

<!--
**yohanesnuwara/yohanesnuwara** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

## Simulation Cases

### Basic

|Case No.|Picture|Description|Input data|Simulator|
|:--:|:--:|:--:|:--:|:--:|
|1|<div><img src="https://user-images.githubusercontent.com/51282928/90313743-2bd91b80-df39-11ea-9153-3e138a951508.png" width="300"/></div>|A 1D non-elevated reservoir bounded by constant<br> rate in the west side and no flow in the east side. Three wells<br> penetrates the reservoir, with contant rate, similar<br> wellbore size, and no skin.|[`input file`](https://github.com/yohanesnuwara/pyresim/tree/master/input/basic/basic1d_input.txt)<br><br>[`depth file`](https://github.com/yohanesnuwara/pyresim/tree/master/input/basic/basic1d_depth.txt)|[`source code`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/basic/PyReSim_basic1d_case1.ipynb)|

### Intermediate 

> Varying boundary conditions in different sides of the reservoir, and varying well operating conditions, configurations, wellbore radius, and skin.

|Case No.|Picture|Description|Input data|Simulator|
|:--:|:--:|:--:|:--:|:--:|
|1|<div><img src="https://user-images.githubusercontent.com/51282928/90242937-235ce400-de58-11ea-9903-40ce8ef8feae.png" width="300"/></div>|A 1D non-elevated reservoir bounded by constant<br> pressure boundary in the west side and constant<br> pressure gradient in the east side. Five wells<br> penetrates the reservoir, with various wellbore<br> radius, skin, and operating conditions.|[`input file`](https://github.com/yohanesnuwara/pyresim/tree/master/input/intermediate/intermediate1d_input.txt)<br><br>[`depth file`](https://github.com/yohanesnuwara/pyresim/tree/master/input/intermediate/intermediate1d_depth.txt)|[`source code`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/intermediate/PyReSim_intermediate1d_case1.ipynb)|

### Advanced 

> Giving uneven distributions of multiple boundary conditions, and giving elevation to the grid blocks. 

|Case No.|Picture|Description|Input data|Simulator|
|:--:|:--:|:--:|:--:|:--:|
|1|<div><img src="https://user-images.githubusercontent.com/51282928/90243270-c7468f80-de58-11ea-8491-a91612ae20c7.png" width="300"/></div>|A 1D elevated reservoir bounded by constant<br> pressure boundary in the west side and constant<br> pressure gradient in the east side. Five wells<br> penetrates the reservoir, with various wellbore<br> radius, skin, and operating conditions.|[`input file`](https://github.com/yohanesnuwara/pyresim/tree/master/input/advanced/advanced1d_input.txt)<br><br>[`depth file`](https://github.com/yohanesnuwara/pyresim/tree/master/input/advanced/advanced1d_depth.txt)|[`source code`](https://github.com/yohanesnuwara/pyresim/blob/master/simulators/advanced/PyReSim_advanced1d_case1.ipynb)|

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
