#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 11:34:26 2020

Script for lesson 6 of "Friends of Tracking" #FoT

Data can be found at: https://github.com/metrica-sports/sample-data

Accompanying video tutorials can be found here: https://www.youtube.com/watch?v=5X1cSehLg6s

GitHub repo: https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking

@author: Laurie Shaw (@EightyFivePoint)
"""

import Metrica_IO as mio
import Metrica_Viz as mviz
import Metrica_Velocities as mvel
import Metrica_PitchControl as mpc
import numpy as np
import pandas as pd

# set up initial path to data
DATADIR = 'data'
game_id = 2 # let's look at sample match 2

tracking_home = pd.read_csv('tracking_home.csv')
tracking_away = pd.read_csv('tracking_away.csv')
events = pd.read_csv('events.csv')

# Calculate player velocities
tracking_home = mvel.calc_player_velocities(tracking_home,smoothing=True, filter_='mooving average')
tracking_away = mvel.calc_player_velocities(tracking_away,smoothing=True, filter_='mooving average')
# **** NOTE *****
# if the lines above produce an error (happens for one version of numpy) change them to the lines below:
# ***************
#tracking_home = mvel.calc_player_velocities(tracking_home,smoothing=True,filter_='moving_average')
#tracking_away = mvel.calc_player_velocities(tracking_away,smoothing=True,filter_='moving_average')

""" **** pitch control for passes leading up to goal 2 **** """


# plot the 3 events leading up to the second goal
mviz.plot_events( events.loc[0:3], color='k', indicators = ['Marker','Arrow'], annotate=False )


# first get model parameters
params = mpc.default_model_params(3)

# evaluated pitch control surface for first pass
PPCF,xgrid,ygrid = mpc.generate_pitch_control_for_event(0, events, tracking_home, tracking_away, params, field_dimen = (106.,68.,), n_grid_cells_x = 50)
mviz.plot_pitchcontrol_for_event( 0, events,  tracking_home, tracking_away, PPCF, xgrid, ygrid, annotate=False )
# evaluated pitch control surface for second pass

PPCF,xgrid,ygrid = mpc.generate_pitch_control_for_event(1, events, tracking_home, tracking_away, params, field_dimen = (106.,68.,), n_grid_cells_x = 50)
fig, ax = mviz.plot_pitchcontrol_for_event( 1, events,  tracking_home, tracking_away, PPCF, xgrid, ygrid, annotate=False )

ax.annotate("33.5%", xy=events.iloc[1][['End X','End Y']], xytext=events.iloc[1][['End X','End Y']])
ax.annotate( "", xy=(-43.95498226902073, -23.70856295986182), xytext=(-22.765,-23.70856295986182), 
            arrowprops=dict( arrowstyle="->" ) )

ax.annotate( '87.1%', xy=(-43.95498226902073, -26.70856295986182),
              xytext=(-43.95498226902073, -26.70856295986182) , va = "bottom", ha="center" )


ax.annotate( "", xy=(-42, -5), xytext=(-22.765,-23.70856295986182), 
            arrowprops=dict( arrowstyle="->" ) )

ax.annotate( '26.8%', xy=(-42, -4.5),
              xytext=(-42, -4.5) , va = "bottom", ha="center" )




