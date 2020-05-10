#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This code is a part of Mikhail Bulygin's entry to the FoT Liverpool FC challenge.

The functions used here are inspired with the code taken from 
https://github.com/Friends-of-Tracking-Data-FoTD/Last-Row and 
https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking

The functions are used for different experiments represented in the main file 
"""

from matplotlib import pyplot as plt
from shapely.geometry.point import Point
import numpy as np
from shapely.geometry import Polygon
import pandas as pd
import footyviz


#set the default parameters
X_SIZE = 105
Y_SIZE = 68

BOX_HEIGHT = (16.5*2 + 7.32)/Y_SIZE*100
BOX_WIDTH = 16.5/X_SIZE*100

GOAL = 7.32/Y_SIZE*100

GOAL_AREA_HEIGHT = 5.4864*2/Y_SIZE*100 + GOAL
GOAL_AREA_WIDTH = 5.4864/X_SIZE*100

SCALERS = np.array([X_SIZE/100, Y_SIZE/100])
pitch_polygon = Polygon(((0,0), (0,100), (100,100), (100,0)))



#calculate_area based on the voronoi diagram from footyviz
def calculate_area(dfFrame):
    polygons = {}
    area = 0
    vor, dfVor = footyviz.calculate_voronoi(dfFrame)
    for index, region in enumerate(vor.regions):
        if not -1 in region:
            if len(region)>0:
                try:
                    pl = dfVor[dfVor['region']==index]
                    pl = pl[pl['team'] == 'attack']
                    polygon = Polygon([vor.vertices[i] for i in region]/SCALERS).intersection(pitch_polygon)
                    polygons[pl.index[0]] = polygon
                    x, y = polygon.exterior.xy
                    area += PolyArea(x,y) 
                except IndexError:
                    pass
                except AttributeError:
                    pass

    return area


#get area of a polygon's xy coordinates
def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))




#calculate how much area was gained
def space_gained(dfFrame_start, dfFrame_end):
    area_start = calculate_area(dfFrame_start)
    area_end = calculate_area(dfFrame_end)
    return (area_end - area_start)/ (10000 - area_start)



#get possession from the tracking data
def get_possession_df(df):
    #get a DataFrame for Ball position
    dfBall = df.reset_index()[df.reset_index().player==0].set_index('frame')[['x', 'y']]

    #temporary DataFrame with all player's position relative to the ball 
    dfTemp = df.reset_index().set_index('frame').join(dfBall, rsuffix='_ball')
    dfTemp = dfTemp[dfTemp.player!=0]
    dfTemp['dif_x'] = dfTemp['x'].sub(dfTemp['x_ball'])
    dfTemp['dif_y'] = (dfTemp['y'] - dfTemp['y_ball'])

    #DataFrame with all the frames where a player touches or has close control of the ball.
    dfPossession = dfTemp[((dfTemp[['dif_x', 'dif_y']]==0).sum(axis=1))==2].reset_index()
    dfPossession.player_num = dfPossession.player_num.astype('Int64')
    return dfPossession



#count the area of intersection of the attacking player's voronoi diagram and the XG zone
def is_in_box(data, direction, play):
    
    cross = {}
    for i in data.player_num.unique():
        cross[i] = 0    
        
    pos = get_possession_df(data.loc[play])
    
    for i in range(pos.iloc[-1]['frame']):    
        polygons = {}
        dfFrame = footyviz.get_frame(data.loc[play], i/20)
        vor, dfVor = footyviz.calculate_voronoi(dfFrame)
        for index, region in enumerate(vor.regions):
            if not -1 in region:
                if len(region)>0:
                    try:
                        pl = dfVor[dfVor['region']==index]
                        pl = pl.loc[pl['player_num'] != '']
                        polygon = Polygon([vor.vertices[i] for i in region]/SCALERS).intersection(pitch_polygon)
                        polygons[pl.index[0]] = polygon
                        x, y = polygon.exterior.xy
                        if direction[play] == 'True':
                            if cross[pl.iloc[0]['player_num']] < count_xg_coef(polygon, direction, play):
                                    cross[pl.iloc[0]['player_num']] = count_xg_coef(polygon, direction, play)
                        else:
                            if cross[pl.iloc[0]['player_num']] < count_xg_coef(polygon, direction, play):
                                cross[pl.iloc[0]['player_num']] = count_xg_coef(polygon, direction, play)

                    except IndexError:
                        pass
                    except AttributeError:
                        pass


    return cross



#count the coeficient for intersection with XG subzones and update it
def count_xg_coef(polygon, direction, play):
    area = 0
    if direction[play] == 'True':
        p_1 = Point(94.5, 30)
        circle_1 = p_1.buffer(11.0)
        p_2 = Point(97.5, 30)
        circle_2 = p_2.buffer(8)
        p_3 = Point(100.5, 30)
        circle_3 = p_3.buffer(4.8)
    else:
        p_1 = Point(10.5, 30)
        circle_1 = p_1.buffer(11.0)
        p_2 = Point(7.5, 30)
        circle_2 = p_2.buffer(8)
        p_3 = Point(4.5, 30)
        circle_3 = p_3.buffer(4.8)
    if polygon.intersection(circle_3).area > 0:
        area += polygon.intersection(circle_3).area * 3
    if polygon.intersection(circle_2).area > 0: 
        area += polygon.intersection(circle_2).area * 2
    if polygon.intersection(circle_1).area > 0: 
        area += polygon.intersection(circle_1).area 
    return area
        



#draw XG circles
def draw_xg_circle (fig, ax, distance_x,distance_y,radius,color, e_color):
    p = Point(distance_x,distance_y)
    circle = p.buffer(radius)
    x,y = circle.exterior.xy
    x = np.array(x) / 1.05
    y = np.array(y) / 0.6
    ax.fill(x, y, alpha=0.5, fc=color, ec=e_color)
    return


def draw_xg(fig, ax):
    draw_xg_circle(fig, ax, 10.5, 30 ,11, color = 'y' , e_color = 'k')
    draw_xg_circle(fig, ax, 7.5, 30 ,8, color = 'g' , e_color = 'k')
    draw_xg_circle(fig, ax, 4.5, 30 ,4.8, color = 'k' , e_color = 'k')
    
    draw_xg_circle(fig, ax, 94.5, 30 ,11, color = 'y' , e_color = 'k')
    draw_xg_circle(fig, ax, 97.5, 30 ,8, color = 'g' , e_color = 'k')
    draw_xg_circle(fig, ax, 100.5, 30 ,4.8, color = 'k' , e_color = 'k')
    plt.show()
    return fig, ax




#calculate players velocities and speed, iif a draw variable is set as True plot the frame with velocities
def calc_player_velocities(dfFrame,data, t,fig = '', ax ='' , draw = True):
    frame = t * 20
    pitch = dfFrame
    try:
        prev_pitch = footyviz.get_frame(data, t=(frame - 1)/20 )
    except KeyError:
        if draw:
            return fig, ax, dfFrame, pitch
        else:
            return pitch
    
    pitch['vx'] = (pitch['x'] - prev_pitch['x']) / 0.05 
    pitch['vy'] = (pitch['y'] - prev_pitch['y']) / 0.05
    pitch['speed'] = np.sqrt(pitch['vx']**2 + pitch['vy']**2)
    
    pitch = pitch[1:]
    
    if draw == True: 
        fig, ax, dfFrame = footyviz.draw_frame(data, t=frame/20)
        ax.quiver(pitch['x'], pitch['y'], pitch['vx'], pitch['vy'], color='k', scale_units='inches', scale=10.,width=0.0015,headlength=5,headwidth=3,alpha=0.7)
        return fig, ax, dfFrame, pitch
    if draw == False:
        return pitch
    
    
    
    
# get the velocities data for the whole play event    
def get_speed_vel(data,play,draw):
    pos = get_possession_df(data.loc[play])
    full_vel = pd.DataFrame(columns = ['Unnamed: 0', 'bgcolor', 'dx', 'dy', 'edgecolor', 'player_num', 'team',
       'x', 'y', 'z', 'vx', 'vy', 'speed'])
    
    for i in range(pos.iloc[-1]['frame']):
        dfFrame = footyviz.get_frame(data.loc[play], t=i/20)
        speed_vel = calc_player_velocities(dfFrame,data.loc[play],t=i/20,draw = draw)
        full_vel= pd.concat([full_vel,speed_vel])
        
    return full_vel


#convert data to the format of PitchControl model described in Laurie Shaw's tutorial
def convert_data (data,passes, play):
    game = data.loc[play]
    game_home = game.loc[game['team'] == 'attack']
    game_away = game.loc[game['team'] == 'defense']
    game_ball = game[game['team'].isnull()]
    players_home = game_home.player.unique()
    players_away = game_away.player.unique()
    
    tracking_data_home = pd.DataFrame(columns = ['Period', 'Time [s]', 'Home_11_x', 'Home_11_y', 'Home_1_x', 'Home_1_y',
       'Home_2_x', 'Home_2_y', 'Home_3_x', 'Home_3_y', 'Home_4_x', 'Home_4_y',
       'Home_5_x', 'Home_5_y', 'Home_6_x', 'Home_6_y', 'Home_7_x', 'Home_7_y',
       'Home_8_x', 'Home_8_y', 'Home_9_x', 'Home_9_y', 'Home_10_x',
       'Home_10_y', 'ball_x', 'ball_y'])
    
    tracking_data_away = pd.DataFrame(columns = ['Period', 'Time [s]', 'Away_11_x', 'Away_11_y', 'Away_1_x', 'Away_1_y',
       'Away_2_x', 'Away_2_y', 'Away_3_x', 'Away_3_y', 'Away_4_x', 'Away_4_y',
       'Away_5_x', 'Away_5_y', 'Away_6_x', 'Away_6_y', 'Away_7_x', 'Away_7_y',
       'Away_8_x', 'Away_8_y', 'Away_9_x', 'Away_9_y', 'Away_10_x',
       'Away_10_y', 'ball_x', 'ball_y'])
    
    for i in range (len(players_home)):
        tracking_data_home[f'Home_{i+1}_x'] = game.loc[game['player']==players_home[i]]['x']
        tracking_data_home[f'Home_{i+1}_x'] = tracking_data_home[f'Home_{i+1}_x']/100*106 - 53
        tracking_data_home[f'Home_{i+1}_y'] = game.loc[game['player']==players_home[i]]['y']
        tracking_data_home[f'Home_{i+1}_y'] = tracking_data_home[f'Home_{i+1}_y'] /100*68 - 34
        
    for i in range (len(players_away)):
        tracking_data_away[f'Away_{i+1}_x'] = game.loc[game['player']==players_away[i]]['x']
        tracking_data_away[f'Away_{i+1}_x'] = tracking_data_away[f'Away_{i+1}_x']/100*106 - 53
        tracking_data_away[f'Away_{i+1}_y'] = game.loc[game['player']==players_away[i]]['y']
        tracking_data_away[f'Away_{i+1}_y'] = tracking_data_away[f'Away_{i+1}_y']/100*68 - 34
        
    tracking_data_home['ball_x'], tracking_data_home['ball_y'] = game_ball['x'], game_ball['y'] 
    tracking_data_home['ball_x'] = tracking_data_home['ball_x']/100*106 - 53
    tracking_data_away['ball_y'], tracking_data_away['ball_y'] = game_ball['x'], game_ball['y'] 
    tracking_data_away['ball_y'] = tracking_data_away['ball_y']/100*68 - 34
    
    tracking_data_home['Period']=1
    tracking_data_away['Period']=1
    tracking_data_home['Time [s]'] = [x/20 for x in range(len(tracking_data_home))]
    tracking_data_away['Time [s]'] = [x/20 for x in range(len(tracking_data_away))]
    
    tracking_data_home = tracking_data_home.dropna(axis = 1, how = 'all')
    tracking_data_away = tracking_data_away.dropna(axis = 1, how ='all')
    
    events = passes.loc[passes['play'] == play]
    events.rename(columns={'from_team':'Team',
                           'from_frame':'Start Frame', 
                           'to_frame': 'End Frame', 
                           'from_player_num':'From',
                           'to_player_num':'To',
                           'from_x':'Start X',
                           'from_y':'Start Y',
                           'to_x':'End X',
                           'to_y':'End Y'},inplace = True)
    events['Team'] = 'Home'
    events['Type'] = 'PASS'
    events['Period'] = 1
    events['Start Time [s]'] = events['Start Frame']/20 
    events['End Time [s]'] = events['End Frame']/20
    events['Start X'] = events['Start X']/100*106 - 53
    events['Start Y'] = events['Start Y']/100*68 - 34
    events['End X'] = events['End X']/100*106 - 53
    events['End Y'] = events['End Y']/100*68 - 34
    
    return tracking_data_home, tracking_data_away, events
    



#count passes for every player to all the pass targets
def passing(passes):
    players = {9:'Roberto Firmino',
               11:'Mohamed Salah', 
               10:'Sadio Mané',  
               8:'Naby Keïta',  
               5:'Georginio Wijnaldum',  
               4:'Virgil van Dijk',
               20:'Adam Lallana', 
               26:'Andrew Robertson', 
               14:'Jordan Henderson', 
               66:'Trent Alexander-Arnold',
               7:'James Milner',
               27:'Divock Origi',
               12:'Joe Gomez',  
               3:'Fabinho', 
               32:'Joël Matip', 
               23:'Xherdan Shaqiri', 
               15:'Alex Oxlade-Chamberlain'}
    
    passers = passes['from_player_num'].unique()
    passee = passes['to_player_num'].unique()
    list_source = []
    list_value = []
    list_target = []
    for s in passers:
        temp = passes.loc[passes['from_player_num'] == s]
        for t in passee:
            list_source.append(s)
            list_value.append(len(temp.loc[temp['to_player_num']==t]))
            list_target.append(t)
            
    df = {'source':list_source,'value':list_value,'target':list_target}
    passdf = pd.DataFrame(df)
    passdf = passdf[(passdf != 0).all(1)]
    passdf = passdf.replace({'source':players})
    passdf = passdf.replace({'target':players})
    return passdf