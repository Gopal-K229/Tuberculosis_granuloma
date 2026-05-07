#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests
import glob
import os
from collections import defaultdict
#%%
plt.rcParams.update({'font.size': 18, 'font.family': 'Arial'})
dfs = glob.glob("repli/*/*/CellBasedOutput.csv")
dfs = sorted(dfs)   # <-- optional, but helps
grouped = defaultdict(list)
for fpath in dfs:
    parent_name = os.path.basename(os.path.dirname(os.path.dirname(fpath)))
    grouped[parent_name].append(fpath)
for key in grouped:
    grouped[key] = sorted(grouped[key])
dfslist = [grouped[key] for key in sorted(grouped)]

# %%
def pop_plot_with_std(indf):
    df_list = [pd.read_csv(file) for file in indf]

    columns = np.arange(0, 20001, 50)
    mtbdf    = pd.DataFrame(columns=columns)
    infmacdf = pd.DataFrame(columns=columns)
    m2df     = pd.DataFrame(columns=columns)
    macrodf  = pd.DataFrame(columns=columns)
    tcelldf  = pd.DataFrame(columns=columns)
    for i in range(len(df_list)):
        df = df_list[i]
        mtbpop=[]
        infmacpop=[]
        m2pop=[]
        macropop=[]
        tcellpop=[]
        for mcs in np.arange(0,20001,50):
            count1=df[(df['cell_type'] == 'mtb') & (df['mcs'] == mcs)].shape[0]
            mtbpop.append(count1)
            count2=df[(df['cell_type'] == 'inf_mac') & (df['mcs'] == mcs)].shape[0]
            infmacpop.append(count2)
            count3=df[(df['cell_type'] == 'm2') & (df['mcs'] == mcs)].shape[0]
            m2pop.append(count3)
            count4=df[(df['cell_type'] == 'macro') & (df['mcs'] == mcs)].shape[0]
            macropop.append(count4)
            count5=df[(df['cell_type'] == 'Tcell') & (df['mcs'] == mcs)].shape[0]
            tcellpop.append(count5)
        mtbdf.loc[i] = mtbpop
        infmacdf.loc[i] = infmacpop
        m2df.loc[i] = m2pop
        macrodf.loc[i] = macropop
        tcelldf.loc[i] = tcellpop
    mtbpop = mtbdf.mean(axis=0)
    infmacpop = infmacdf.mean(axis=0)
    m2pop = m2df.mean(axis=0)
    macropop = macrodf.mean(axis=0)
    tcellpop = tcelldf.mean(axis=0)
    mtbstd = mtbdf.std(axis=0)
    infmacstd = infmacdf.std(axis=0)
    m2std = m2df.std(axis=0)
    macrostd = macrodf.std(axis=0)
    tcellstd = tcelldf.std(axis=0)
    mcs_vals = np.arange(0, 20001, 50)
    plt.figure(figsize=(12, 6))
    # plt.plot(mcs_vals, infmacpop, color='#0000ff', label="inf_mac")
    # plt.fill_between(mcs_vals, infmacpop - infmacstd, infmacpop + infmacstd, color='#0000ff', alpha=0.2)
    plt.plot(mcs_vals, mtbpop, color='#B22222', label="mtb")
    plt.fill_between(mcs_vals, mtbpop - mtbstd, mtbpop + mtbstd, color='#ff0000', alpha=0.2)
    # plt.plot(mcs_vals, m2pop, color="#c9c904", label="m2")
    # plt.fill_between(mcs_vals, m2pop - m2std, m2pop + m2std, color="#c9c904", alpha=0.2)
    # plt.plot(mcs_vals, macropop, color='#008000', label="macro")
    # plt.fill_between(mcs_vals, macropop - macrostd, macropop + macrostd, color='#008000', alpha=0.2)
    # plt.plot(mcs_vals, tcellpop, color="#a5a2a2ff", label="T cell")
    # plt.fill_between(mcs_vals, tcellpop - tcellstd, tcellpop + tcellstd, color="#a5a2a2ff", alpha=0.2)
    plt.xlabel("Monte Carlo Steps (MCS)")
    plt.ylabel("Cell Count")
    # plt.title("Cell Population Dynamics (Mean ± Std Dev)")
    # plt.legend()
    # plt.tight_layout()
    plt.show()





#%%
for i in dfslist:
    pop_plot_with_std(i)
# %%
pop_plot_with_std(dfslist[4])
# %%
