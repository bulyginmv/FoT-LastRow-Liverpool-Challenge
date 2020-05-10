#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 18:26:30 2020

@author: mikhail
"""
import numpy as np
import pandas as pd
from math import isnan
import sys, os
sys.path.insert(0, os.path.abspath('../scripts/'))
import footyviz
import liverpool_fot


#load the data
data = pd.read_csv('../datasets/positional_data/liverpool_2019.csv', index_col=('play', 'frame'))
passes = pd.read_csv('../datasets/positional_data/liverpool_2019_passes.csv')



#choose Liverpool's events and drop the nan values
passes = passes[passes['from_team'] == 'attack']
dfpas = passes.dropna()



#set the list of games and the direction of Liverpool's attack
plays = list(data.index.get_level_values('play').unique())
direct = ['True','True','False','False','False','False','True','True','False','True','True','False','True','False','False','False','False','False','True'] 
direction = dict(zip(plays,direct))



#define variables for the experiments
space = {}
time = {}
cut = {}
box = {}
max_speed = {}
avr_speed = {}
pas_space = []
player_cut = []

for i in dfpas.from_player_num.unique():
    space[i] = []
    time[i] = []
    cut[i] = []

for i in data.loc[data['team']=='attack'].player_num.unique():
    box[i] = []
    max_speed[i] = []
    avr_speed[i] = []
    
box_mean = {}    
box = {k: box[k] for k in box if not isnan(k)}

#Experiment 1: calculate possesion time before each pass
dfpas['possesiom_time'] = (dfpas['to_frame'] - dfpas['from_frame'])/20

    
#Experiment 2: calculate area gained from making a pass
for ix,pas in dfpas.iterrows():
    area_start = pas['from_frame']
    area_end = pas['to_frame']
    space[pas['from_player_num']].append(liverpool_fot.space_gained(footyviz.get_frame(data.loc[pas['play']], area_start/20),footyviz.get_frame(data.loc[pas['play']], area_end/20)))
    pas_space.append(liverpool_fot.space_gained(footyviz.get_frame(data.loc[pas['play']], area_start/20),footyviz.get_frame(data.loc[pas['play']], area_end/20)))    
    
dfpas['space_gained'] = pas_space

for i in dfpas.from_player_num.unique():
    space[i] = np.mean(space[i])
    
for ix,pas in dfpas.iterrows():
    time[pas['from_player_num']].append(pas.loc['possesiom_time'])
    
    



#Experiment 3: how many players does the player cut off on average
for ix,pas in dfpas.iterrows():
    cut_start = pas['from_frame']
    cut_end = pas['to_frame']
    frame_start = footyviz.get_frame(data.loc[pas['play']], cut_start/20)
    frame_end = footyviz.get_frame(data.loc[pas['play']], cut_end/20)
    if direction[pas['play']]=='True':
        cut[pas['from_player_num']].append(sum(frame_end.loc[frame_end['team'] == 'defense']['x'] < pas['to_x']) - sum(frame_start.loc[frame_start['team'] == 'defense']['x'] < pas['from_x']))
        player_cut.append(sum(frame_end.loc[frame_end['team'] == 'defense']['x'] < pas['to_x']) - sum(frame_start.loc[frame_start['team'] == 'defense']['x'] < pas['from_x']))
    else:
        cut[pas['from_player_num']].append(-1*(sum(frame_end.loc[frame_end['team'] == 'defense']['x'] < pas['to_x']) - sum(frame_start.loc[frame_start['team'] == 'defense']['x'] < pas['from_x'])))
        player_cut.append(-1*(sum(frame_end.loc[frame_end['team'] == 'defense']['x'] < pas['to_x']) - sum(frame_start.loc[frame_start['team'] == 'defense']['x'] < pas['from_x'])))
   
dfpas['player_cut'] = player_cut


for i in dfpas.from_player_num.unique():
    cut[i] = np.mean(cut[i])






#Experiment 4: how much space can a player find in opponents xg area   
for play in plays:
    temp = liverpool_fot.is_in_box(data, direction, play)
    for k in box.keys():
        box[k].append(temp[k])
        
for i in box.keys():
    box_mean[i] = np.mean(box[i])
        

#convert data to the format of PitchControl model described in L
    
    
    

#Experiment 5: what is the maximum and average speed of the players    
for i in plays:
    full_vel = liverpool_fot.get_speed_vel(data,play = i, draw = False)
    for k in max_speed.keys():
        max_speed[k].append(full_vel.loc[full_vel['player_num'] == k]['speed'].rolling(window = 20).mean().max())
        avr_speed[k].append(full_vel.loc[full_vel['player_num'] == k]['speed'].rolling(window = 20).mean().mean())
        



#Experiment 6: get the passing information
passdf = liverpool_fot.passing(passes)





#Experiment 7: convert data for the PitchControl model
play = 'ENTER_THE_GAME_IN_QUESTION'
tracking_home, tracking_away, events = liverpool_fot.convert_data(data,passes, play = play)