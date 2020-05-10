# FoT-LastRow-Liverpool-Challenge
Entry to a Friends of Tracking Liverpool FC Challenge. 

Video of the presentation:
(https://www.youtube.com/watch?v=dCrSrjjFXyg&feature=youtu.be)

This repository is based on the repositories from Friends of Tracking github
https://github.com/Friends-of-Tracking-Data-FoTD/Last-Row and 
https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking

To see the code used for experiments, go to /notebooks/main.py

The additional functions used for the presentation can be found in /scripts/liverpool_fot.py

Presentation: FoT competition.odp


Technical remarks and limitations:

1)The comparison between the player is limited due to LastRow data not containing all player's numbers for all games. Therefore not all possible information is included.

2)The estimate for max_speed was done with sliding moving average algorithm with a window of 20 (1 s).

3)The graphs that are in presentation were done afterwards and the code for them is not in this repository. However, the data was not changed, so anyone can reproduce the plots using the code from Friends of Tracking github.

4)For Pitch Control plot I used a modified version of the Laurie Shaw's code from Friends of Tracking github.

