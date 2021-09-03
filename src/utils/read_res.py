"Script to determine the path of the scenario results of OSeMBE for the REEEMgame."
#%% Import of needed packages
import os
import sys
from typing import List
import pandas as pd
#%% Get directory names from folder
def get_dirs(path):
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return dirs
#%% Function to go through directories and build scenario names and paths
def build_names(dic,i):
    if i == 0:
        p = dic[i]
        dirs = get_dirs(p)
        dic = {}
        for f in dirs:
            dic[f] = os.path.join(p,f)
        i+=1
    else:
        dic_t = {}
        for s in dic:
            dirs = get_dirs(dic[s])
            if 'res' in dirs:
                i+=1
                dic[s] = os.path.join(dic[s],'res')
            else:
                for d in dirs:
                    dic_t[s+'|'+d] = os.path.join(dic[s],d)
        if bool(dic_t):
            dic = dic_t
    return dic,i
#%% Function to read needed results parameter
def read_res(path,param):
    path_param = os.path.join(path,param) + '.csv'
    df = pd.read_csv(path_param)
    return df
#%% Read pop-projections
def read_pop(path,sheet,header):
    """ Function that reads in population data from excel file.
    """
    df_pop = pd.read_excel(path,sheet,header=header)
    df_pop = df_pop[df_pop['variable']=='Population']
    df_pop['id'] = df_pop.index
    df_pop = pd.wide_to_long(df_pop,["y"],i="id",j="year")
    df_pop.rename(columns={"name":"country","y":"value"},inplace=True)
    df_pop['value'] = df_pop["value"]*1000
    df_pop = df_pop.drop(columns=["unit","code_wb","variable"])
    df_pop = df_pop.reset_index(level=["year"])
    df_pop = df_pop[df_pop["year"]>=2015]
    df_pop = df_pop.reset_index(drop=True)
    return df_pop
#%% Function to read Emission results
def read_emissions(path: str,param: str, emission: List) -> pd.DataFrame:
    """ Read and filter emissions by: country, year, emission
    """
    # path = os.path.join("tests","fixtures") #for testing
    # param = "AnnualTechnologyEmission" #for testing
    # emission = ['CO2'] #for testing
    df = read_res(path,param)
    df['REGION'] = df['TECHNOLOGY'].str[:2]
    df_f = pd.DataFrame(columns=["REGION","EMISSION","YEAR","VALUE"])
    for e in emission:
        df_e = df[df["EMISSION"]==e]
        for r in df_e["REGION"].unique():
            for y in df_e["YEAR"].unique():
                df_f = df_f.append({"REGION": r, "EMISSION": e, "YEAR": y,"VALUE": df_e.loc[(df_e["REGION"]==r)&(df_e["YEAR"]==y),["VALUE"]].sum(axis=0).VALUE}, ignore_index=True)
    df_f = df_f[df_f.VALUE != 0]
    return df
#%% Filter population data
def filter_pop(df,countries):
    """Function to filter a dataframe with population data down to the countries that are in the model.
    """
    mask = df.country.isin(countries['country'])
    df = df[mask]

    return pd.merge(df,countries,on='country')
#%% Convert country codes from ISO3 to ISO2
def main(param):
    param = ['AnnualTechnologyEmission','AnnualTechnologyEmissions']
    dic_scen = {}
    i = 0
    dic_scen = {0: 'results'}
    while i < 2:
        dic_scen, i = build_names(dic_scen,i)
    
    res_files = next(os.walk(dic_scen[list(dic_scen.keys())[0]]), (None,None,[]))[2]

    for p in param:
        f = p + '.csv'
        if f not in res_files:
            print(p+" is not a results parameter.")
    return
#%%
if __name__ == "__main__":


        
    
    dic_scen_res = {}
    df_pop = read_pop('results/pop_projection_NEWAGE.xlsx','MaGe Factors',12)
    osembe_countries = pd.read_csv('osembe_countries.csv')
    df_pop = filter_pop(df_pop,osembe_countries)

# %%
