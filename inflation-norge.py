#!/usr/bin/env python
# coding: utf-8

# In[1]:


# # # Konsumgruppe DF

import pandas as pd

from IPython.display import display
import matplotlib.pyplot as plt

df_produkter = pd.read_csv("Tabell_03014_Detaljer.csv", encoding='ISO-8859-1',sep='\t')
df_produkter['konsumgruppe'] = df_produkter['konsumgruppe'].astype(str)
df_produkter = df_produkter.drop(columns=list(df_produkter.columns[2:39]))
df_produkter = df_produkter.drop(columns=["statistikkvariabel"])
df_produkter.rename(columns={"konsumgruppe":"Konsumgruppe"}, inplace=True)

df_produkter


# In[2]:


# # # Lønn DF

df_lønn = pd.read_csv("Tabell_11419_Lønn.csv", encoding='ISO-8859-1',sep='\t')
df_lønn = df_lønn[(df_lønn["kjønn"] == "Begge kjønn") & (df_lønn["yrke"] == "Alle yrker") & (df_lønn["sektor"] == "Sum alle sektorer")]
df_lønn = df_lønn.drop(columns=["statistikkvariabel","statistikkmål","kjønn","yrke","sektor"] + [col for col in df_lønn.columns if "Heltidsansatte" in col or "Deltidsansatte" in col])
df_lønn.rename(columns=lambda x: x.replace(" I alt", ""), inplace=True)

df_lønn = df_lønn.replace(to_replace='.', value=0)

df_lønn.rename(columns={"næring (SN2007)":"Næring"}, inplace=True)

df_lønn


# In[46]:


# # # Plot Data

konsumgruppe_label = widgets.Label('Select Konsumgruppe:')
options_konsumgruppe = ['Konsumgruppe'] + df_produkter['Konsumgruppe'].unique().tolist()
dropdown_konsumgruppe = widgets.Dropdown(options=options_konsumgruppe)
display(widgets.VBox([konsumgruppe_label, dropdown_konsumgruppe]))


naering_label = widgets.Label('Select Næring:')
options_naering = ['Næring'] + df_lønn['Næring'].unique().tolist()
dropdown_naering = widgets.Dropdown(options=options_naering)
display(widgets.VBox([naering_label, dropdown_naering]))


plot_button = widgets.Button(description='Plot Combined Graph', visible=False)
display(plot_button)


def plot_data(data):
    data.iloc[:, 1:] = data.iloc[:, 1:].astype(float)
    plt.plot(data.columns[1:], data.iloc[0, 1:].astype(float))

def update_plot_konsumgruppe(change):
    global Konsumgruppe_df
    Konsumgruppe_df = df_produkter[df_produkter['Konsumgruppe'] == change.new]
    plot_data(Konsumgruppe_df)

def update_plot_naering(change):
    global Næring_df
    Irke_df = df_lønn[df_lønn['Næring'] == change.new]
    Irke_df.iloc[:, 1:] = Irke_df.iloc[:, 1:].astype(float)
    Næring_df = Irke_df.iloc[:, 1:].pct_change(axis=1) * 100
    Næring_df = pd.concat([Irke_df.iloc[:, 0], Næring_df], axis=1)
    plot_data(Næring_df)


def plot_combined(button):
    plot_data_combined(Konsumgruppe_df, Næring_df)

def plot_data_combined(df1, df2):
    plt.figure(figsize=(12, 8))
    plt.plot(df1.columns[1:], df1.iloc[0, 1:].astype(float))
    plt.plot(df2.columns[1:], df2.iloc[0, 1:].astype(float))
    plt.xlabel("Year")
    plt.ylabel("Percentage Variation")
    plt.title("Percentage variation by Year")
    plt.show()

dropdown_konsumgruppe.observe(update_plot_konsumgruppe, names='value')
dropdown_naering.observe(update_plot_naering, names='value')
plot_button.on_click(plot_combined)

