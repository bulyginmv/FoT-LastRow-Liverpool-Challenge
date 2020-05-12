# FoT-LastRow-Liverpool-Challenge
Entry to a Friends of Tracking Liverpool FC Challenge. 

Video of the presentation:
(https://www.youtube.com/watch?v=dCrSrjjFXyg&feature=youtu.be)

This repository is based on the repositories from Friends of Tracking GitHub
https://github.com/Friends-of-Tracking-Data-FoTD/Last-Row and 
https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking

To see the code used for experiments, go to /notebooks/main.py

The additional functions used for the presentation can be found in /scripts/liverpool_fot.py

Presentation: FoT competition.odp


Technical remarks and limitations:

  1) The comparison between the player is limited due to LastRow data not containing all player's numbers for all games. Therefore not all possible information is included.

  2) To get the results of the player_cut_off model, I used the data from the passing events dataframe. I compared the x-axis coordinates before the pass and x-axis coordinates after the pass was received. From the tracking data, we know the positions of the players, so the result of this model was the number of players that fell in between the two ball coordinates at the moment of receiving. The result can also be negative if a player does a pass that increases the number of opponents in front of the ball.  
  An interesting moment was adjusting the model to the direction of play. Yet, I decided that due to the small size of the dataset we can fill in this information manually. However, in the future, this operation should be automized.

  3) For pass_gaining_space I used the data from the Voronoi diagrams. The sum of the polygon areas was used to estimate the Liverpool's space at the moment. The samples were taken 2 times. One at the start of the pass, and second at the time of receiving. The difference between the two samples produced the gained space. Once again this result, in theory, can be negative.  
  To adjust the significance of passes from different distances I normalized the difference by the amount of space that the opponent had at the moment of the pass. That way a long pass from the midfield can be as valuable as short pass inside the box, as they get the same percentage of opponent's space. Even though the long pass would likely bring more area to the team. 

  4) The Pitch Control model was a modified version of Laurie Shaw's code from Friends of Tracking GitHub. The data for this model is quite different, so I wrote a function to convert LastRow's data to the format of the pitch control model. This was done for both tracking and event data. 

  5) The estimate for max_speed was done with a sliding moving average algorithm with a window of 20 (1 s). The same was done for average speed estimate. In the graph, data for the max speed is the best result in all of the games presented in the dataset. The average is the mean overall samples in each game and the average for all the games. The sliding moving average gave a very compelling result. However, this is still an estimation and if we would want to study speed more closely other algorithms can be used.

  6) To get the XG_space information, I once again used data from the Voronoi diagrams, sampling each frame from the start until the last frame of possession. The last frame of the possession is the last time a player could have received a pass into the space he created, so sampling afterward would only bring the noise to the data. The function returned maximum value that each player presented in the data received during the play. The area of the XG zone was set arbitrarily because the was not enough data in the dataset (19 goals) and no counterexamples of players missing the target. Also, I could not get XG data on Liverpool from another source in time, so I decided on this experiment to set in myself based on common assumptions about the XG zone. In the future, it would be interesting to try this experiment on the actual XG data for Liverpool.  
  The result for this experiment evaluated the ability of a player to find free space inside the opponent's XG zone. I also used a system of coefficients to reflect different areas of XG. So, if a player was able to find a space in the circle closet to the goal, we would take the intersection of his area with that circle and multiply it by 3, the same was done with the intersection of the second ring, but with a coefficient of 2. And for the last ring, the area was not changed. The sum of all three areas is the result of the frame. One limitation of that technic is that if not all players are listed in the data. For example, for the Salah goal vs. Bournemouth, there was a lot of space created by Andrew Robertson in the XG zone, but because he was not listed in the data, that run was not counted in the results. For the graph, I decided to compare only forwards as they are more or less in the same predicament to find the XG space.

  7) The passing was counted based on the passing dataframe presented in the notebook that came with the dataset. I decided to omit the players that gave less than 2 passes, as this information would not tell us anything and would create noise.

  8) Possession time was calculated with the dataframe of possession that came with the dataset. I subtracted the start frame from the end frame and converted the results to seconds.

  9) The graphs that are in the presentation were done afterward and the code for them is not in this repository. However, the data was not changed, so anyone can reproduce the plots using the code from Friends of Tracking GitHub or other plotting technics.
