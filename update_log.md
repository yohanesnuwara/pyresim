### Update Log

17/08/2020
* modify `lhs_coeffs1d_welltype` and `rhs_constant1d_welltype` to include `slicomp` (slightly compressible solver) for 1D reservoir
* modify `read_input` to include reading `CFLUID` variable from input .TXT data
* upload 2 benchmark 1D data: `benchmark1d_incomp` and `benchmark1d_slicomp`
* 1D incompressible, 1D slightly compressible, 2D incompressible PASS the benchmark test

18/08/2020
* upload benchmark data for slightly compressible simulation for 2D reservoir, `benchmark2d_2x2_slicomp`
* modify `lhs_coeffs2d_welltype` and `rhs_constant2d_welltype` to include `slicomp` (slightly compressible solver) for 2D reservoir
* successfully created 2D simulation of slightly compressible
* successfully created the well FBHP and rate simulation from 2D slightly compressible simulation

19/08/2020
* update function `lhs_coeffs1d_welltype`, `lhs_coeffs2d_welltype`, `rhs_constant1d_welltype`, and `rhs_constant2d_welltype` for Slightly Compressible solver 1D and 2D
* add function `well1d_report_slicomp` and `well2d_report_slicomp` to calculate FBHP and rate of a well of interest, under Slightly Compressible simulation
* 1D slightly compressible and 2D slightly compressible PASS the benchmark test
* create `irregularity.py` that contains functions to handle irregular reservoir geometry
