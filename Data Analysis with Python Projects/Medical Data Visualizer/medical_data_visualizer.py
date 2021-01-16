import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv',sep=',')

# Add 'overweight' column
overweight_condition = [
    df['weight'] / (df['height']/100)**2 <= 25,
    df['weight'] / (df['height']/100)**2 > 25
    ]

overweight_result = [
    0,
    1
    ]

df['overweight'] = np.select(overweight_condition,overweight_result)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df.loc[df['cholesterol'] == 1, 'cholesterol'] = 0
df.loc[df['cholesterol'] > 1, 'cholesterol'] = 1

df.loc[df['gluc'] == 1, 'gluc'] = 0
df.loc[df['gluc'] > 1, 'gluc'] = 1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df,id_vars=['cardio'],value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active','overweight'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the collumns for the catplot to work correctly.
    df_cat = df_cat.groupby(['cardio','variable', 'value'], as_index = False).size().rename(columns={'size':'total'})

    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(
        x='variable',
        y='total',
        hue='value',
        kind='bar',
        col='cardio',
        data=df_cat,
        legend=True
        ).fig()

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[
            (df['ap_lo'] <= df['ap_hi']) &
            (df['height'] >= df['height'].quantile(0.025)) &
            (df['height'] <= df['height'].quantile(0.975)) &
            (df['weight'] >= df['weight'].quantile(0.025)) &
            (df['weight'] <= df['weight'].quantile(0.975)) 
            ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(corr)

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(9,9))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr,mask=mask,vmax=0.3,center=0,linewidth=0.1,square='true',annot=True,fmt='.1f',cbar_kws={'ticks':[-0.08,0,0.08,0.16,0.24],'shrink':0.5},annot_kws={'size':7})

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
