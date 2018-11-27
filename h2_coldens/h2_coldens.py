# Import the necessary packages and modules
import matplotlib.pyplot as plt
import numpy as np
import csv
import math

from scipy.constants import Boltzmann
from scipy.optimize import curve_fit

label_font = {'family': 'Times New Roman',
        'color':  'black',
        'weight': 'normal',
        'size': 14,
        }

def plot_h2_coldens(path):
    path += "coldens_H2.txt"
    data_v, data_j, data_en, data_cd = np.loadtxt(path, usecols=(1, 2, 4, 5), comments='!', unpack=True)
    
    marker_list = ['o','^', 'v', 's']
    color_list = ['black', 'red', 'blue', 'green']
    label_list = ['v=0', 'v=1', 'v=2', 'v=3', 'v=4']
    
    fig = plt.figure(figsize=(7.,7.))
    ax = fig.add_subplot(111)
    
    for v in range(0,4):
        en = []
        cd = []
        for k in range(len(data_v)):
            if (v == data_v[k] and v != 0) or (v == 0 and data_v[k] == 0 and data_j[k] != 0 and data_j[k] != 1):
                en += [data_en[k]]
                cd += [data_cd[k]]
        ax.scatter(en, cd, s=45, facecolors='none', marker=marker_list[v], color=color_list[v], label=label_list[v])
         
    ax.set_yscale('log')
    ax.set_ylim(1.e+8, 1.e+21)
    ax.set_xlim(0., 20000.)

    ax.set_xlabel('Level energy, cm$^{-1}$', fontdict=label_font)
    ax.set_ylabel('Column densities, N/g', fontdict=label_font)
    ax.tick_params(labelsize=14)

    plt.title('H$_2$ level column densities', fontdict=label_font)
    plt.legend()
    plt.show()


def plot_h2_dissociation(path):
    path += "sim_data_h2_chemistry.txt"
    data_z, data_diss = np.loadtxt(path, usecols=(0, 7), comments='!', unpack=True)
    
    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(111)
    ax.plot(data_z, data_diss, color='black', label='Bossion et al. 2018')

    ax.set_yscale('log')
    ax.set_ylim(1.e-20, 1.e-15)

    ax.set_xlabel('Length, cm', fontdict=label_font)
    ax.set_ylabel('Dissociation rate, cm^{-3} s^{-1}', fontdict=label_font)
    ax.tick_params(labelsize=12)

    plt.title('H$_2$ dissociation rates', fontdict=label_font)
    plt.legend()
    plt.show()


def plot_h2_coldens_compare(path_list, label_list):
    marker_list = ['o','^', 'v', 's']
    color_list = ['black', 'red', 'blue', 'green']
    fig = plt.figure(figsize=(7.,7.))
    ax = fig.add_subplot(111)
    
    for i in range(len(path_list)):
        fname = path_list[i] + "coldens_H2.txt"
        data_v, data_j, data_en, data_cd = np.loadtxt(fname, usecols=(1, 2, 4, 5), comments='!', unpack=True)
        
        en = []
        cd = []
        for v in range(0,4):    
            for k in range(len(data_v)):
                if (v == data_v[k] and v != 0) or (v == 0 and data_v[k] == 0 and data_j[k] != 0 and data_j[k] != 1):
                     en += [data_en[k]]
                     cd += [data_cd[k]]
        ax.scatter(en, cd, s=45, facecolors='none', marker=marker_list[i], color=color_list[i], label=label_list[i])
         
    ax.set_yscale('log')
    ax.set_ylim(1.e+8, 1.e+21)
    ax.set_xlim(0., 20000.)

    ax.set_xlabel('Level energy, cm$^{-1}$', fontdict=label_font)
    ax.set_ylabel('Column densities, N/g', fontdict=label_font)
    ax.tick_params(labelsize=14)

    plt.title('H$_2$ level column densities', fontdict=label_font)
    plt.legend()
    plt.show()


def plot_h2_coldens_observations(path_theory, label_theory):
    fig = plt.figure(figsize=(7.,7.))
    ax = fig.add_subplot(111)

    data_err = []
    fname = "../../../observations/Neufeld 2007 H2 column densities.txt"
    data1_j, data_en, data_cd = np.loadtxt(fname, usecols=(0, 1, 5), comments='!', unpack=True)  
    for i in range(len(data_cd)):
        data_cd[i] = math.pow(10., data_cd[i])/(2.*data1_j[i] + 1.)
        if (data1_j[i]%2 == 1):
            data_cd[i] /= 3.
        data_err.append(data_cd[i]*0.25)

    ax.errorbar(data_en, data_cd, yerr=data_err, fmt='o', ms=6, color='blue', mfc='none', label='Neufeld et al. 2007')
     
    fname = "../../../observations/Shinn 2011 IC443 H2 column densities B C G.txt"
    data2_v, data2_j, data_en, data_cd, data_err = np.loadtxt(fname, usecols=(0, 1, 2, 5, 6), comments='!', unpack=True)  
    for i in range(len(data_cd)):
        data_cd[i] = math.pow(10., data_cd[i])/(2.*data2_j[i] + 1)
        if (data2_j[i]%2 == 1):
            data_cd[i] /= 3.
        data_err[i] = (math.pow(10., data_err[i]) - 1.)*data_cd[i]

    ax.errorbar(data_en, data_cd, yerr=data_err, fmt='o', ms=6, color='red', mfc='none', label='Shinn et al. 2011')
    
    fname = "../../../observations/Shinn 2011 IC443 H2 column densities B C G upper limits.txt"
    data3_v, data3_j, data_en, data_cd, data_err = np.loadtxt(fname, usecols=(0, 1, 2, 5, 6), comments='!', unpack=True)  
    
    for i in range(len(data_cd)):
        data_cd[i] = math.pow(10., data_cd[i])/(2.*data3_j[i] + 1)
        if (data3_j[i]%2 == 1):
            data_cd[i] /= 3.
        data_err[i] = (math.pow(10., data_err[i]) - 1.)*data_cd[i]*2

    uplims = np.empty(len(data_cd))
    uplims.fill(1)
    ax.errorbar(data_en, data_cd, yerr=data_err, fmt='o', ms=6, color='red', mfc='none', uplims=uplims)
    
    fname = path_theory + "coldens_H2.txt"
    data_v, data_j, data_en, data_cd = np.loadtxt(fname, usecols=(1, 2, 4, 5), comments='!', unpack=True)
    
    en = []
    cd = []
    for i in range(len(data_j)):
        for k in range(len(data1_j)):
            if (data_j[i] == data1_j[k] and data_v[i] == 0):
                en += [data_en[i]]
                cd += [data_cd[i]]

        for k in range(len(data2_j)):
            if (data_j[i] == data2_j[k] and data_v[i] == data2_v[k]):
                en += [data_en[i]]
                cd += [data_cd[i]]

        for k in range(len(data3_j)):
            if (data_j[i] == data3_j[k] and data_v[i] == data3_v[k]):
                en += [data_en[i]]
                cd += [data_cd[i]]

    ax.scatter(en, cd, s=45, facecolors='none', marker='v', color='black', label = label_theory)       
    ax.set_yscale('log')
    ax.set_ylim(1.e+10, 1.e+21)
    ax.set_xlim(0., 17000.)

    ax.set_xlabel('Level energy, cm$^{-1}$', fontdict=label_font)
    ax.set_ylabel('Column densities, N/g', fontdict=label_font)
    ax.tick_params(labelsize=14)

    plt.title('H$_2$ level column densities', fontdict=label_font)
    plt.legend()
    plt.show()

def ExpFunction(x, a, b, c):
    return a * np.exp(-b * x) + c

def HydrogenOrthoParaCalc(pathList):
    jLowLim = 2
    jUpLim = 8 # must be even
    
    for i in range(len(pathList)):
        fName = pathList[i] + "coldens_H2.txt"
        fDataVibrQ, fDataJ, fDataEn, fDataColDens = np.loadtxt(fName, usecols=(1, 2, 4, 5), comments='!', unpack=True)
        
        enList = []
        colDensList = []
        jList = []
        
        for k in range(len(fDataJ)):
            if (fDataJ[k] >= jLowLim and fDataJ[k] <= jUpLim and fDataVibrQ[k] == 0):
                jList += [fDataJ[k]]
                enList += [fDataEn[k]]
                colDensList += [fDataColDens[k]]
        
        orthoParaRatioList = []
        for k in range(len(jList)):
            if (jList[k]%2 == 1):
                rotTemp = (enList[k-1] - enList[k+1])/(Boltzmann* math.log(colDensList[k-1]/colDensList[k+1]))
        
                a = b = 0. 
                for l in range(len(fDataJ)):
                    if (fDataJ[l]%2 == 1):
                        a += 3.*(2*fDataJ[l] + 1) *math.exp(-fDataEn[l]*1.4387770/rotTemp)
                    else:
                        b += (2*fDataJ[l] + 1) *math.exp(-fDataEn[l]*1.4387770/rotTemp)
 
                orthoParaRatioList += [a/b *colDensList[k] \
                    /math.exp( math.log(colDensList[k-1]) + (enList[k] - enList[k-1])*math.log(colDensList[k+1]/colDensList[k-1])/(enList[k+1] - enList[k-1]) )]
        
        orthoParaRatio = colDens = 0.
        for k in range(len(orthoParaRatioList)):
            orthoParaRatio += orthoParaRatioList[k] *(2*jList[2*k+1] + 1)*colDensList[2*k+1]
            colDens += (2*jList[2*k+1] + 1)*colDensList[2*k+1]
        
        orthoParaRatio /= colDens   
        OptimalParameters = np.polyfit(enList, np.log(colDensList), 1, w = np.sqrt(colDensList))
        
        print(-1.4387770/OptimalParameters[0], orthoParaRatio)




path = "../../../output_data_1e4/shock_30_h2-h_lique-bossion/"
#plot_h2_coldens(path)


# path = "../../../output_data_2e4/shock_30_h2-h_lique-bossion/"
# plot_h2_dissociation(path)

path_list = []
path_list += ['../../../output_data_2e4/shock_20_h2-h_lique-bossion/']
path_list += ['../../../output_data_2e4/shock_30_h2-h_lique-bossion/']
path_list += ['../../../output_data_2e4/shock_45_h2-h_lique-bossion/']
path_list += ['../../../output_data_2e4/shock_55_h2-h_lique-bossion/']

label_list = []
label_list += ["20 km/s"]
label_list += ["30 km/s"]
label_list += ["45 km/s"]
label_list += ["55 km/s"]
#plot_h2_coldens_compare(path_list, label_list)

path_list = []
path_list += ["../../../output_data_2e4/shock_20_h2-h_lique-bossion_cr100/"]
path_list += ["../../../output_data_2e4/shock_30_h2-h_lique-bossion_cr100/"]
path_list += ["../../../output_data_2e4/shock_45_h2-h_lique-bossion_cr100/"]
path_list += ["../../../output_data_2e4/shock_55_h2-h_lique-bossion_cr100/"]

label_list = []
label_list += ["20 km/s"]
label_list += ["30 km/s"]
label_list += ["45 km/s"]
label_list += ["55 km/s"]
#plot_h2_coldens_compare(path_list, label_list)

path_list = []
path_list += ["../../../output_data_2e5/shock_20_h2-h_lique-bossion/"]
path_list += ["../../../output_data_2e5/shock_30_h2-h_lique-bossion/"]
path_list += ["../../../output_data_2e5/shock_40_h2-h_lique-bossion/"]

label_list = []
label_list += ["20 km/s"]
label_list += ["30 km/s"]
label_list += ["40 km/s"]
#plot_h2_coldens_compare(path_list, label_list)

path_list = []
path_list += ["../../../output_data_2e5/shock_20_h2-h_lique-bossion_cr100/"]
path_list += ["../../../output_data_2e5/shock_30_h2-h_lique-bossion_cr100/"]
path_list += ["../../../output_data_2e5/shock_40_h2-h_lique-bossion_cr100/"]

label_list = []
label_list += ["20 km/s"]
label_list += ["30 km/s"]
label_list += ["40 km/s"]
#plot_h2_coldens_compare(path_list, label_list)

path_list = []
path_list += ['../../../output_data_2e4/shock_30_h2-h_lique-bossion/']
path_list += ['../../../output_data_2e4/shock_30_h2-h_wan/']

label_list = []
label_list += ['Flower']
label_list += ['Wan']
#plot_h2_coldens_compare(path_list, label_list) 

path_list = []
path_list += ["../../../output_data_1e4/shock_30_h2-h_lique-bossion_cr100/"]
path_list += ["../../../output_data_1e4/shock_30_h2-h_lique-bossion_cr100_2b/"]
path_list += ["../../../output_data_1e4/shock_30_h2-h_lique-bossion_cr100_05b/"]

label_list = []
label_list += ["b = 1"]
label_list += ["b = 2"]
label_list += ["b = 0.5"]

#plot_h2_coldens_compare(path_list, label_list)

#plot_h2_coldens_observations('../../../output_data_1e4/shock_30_h2-h_lique-bossion_cr100/', '')

path_list = []
path_list += ['../../../output_data_2e4/shock_20_h2-h_lique-bossion/']
path_list += ['../../../output_data_2e4/shock_30_h2-h_lique-bossion/']
path_list += ['../../../output_data_2e4/shock_45_h2-h_lique-bossion/']
path_list += ['../../../output_data_2e4/shock_55_h2-h_lique-bossion/']
HydrogenOrthoParaCalc(path_list)