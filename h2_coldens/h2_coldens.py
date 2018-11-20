# Import the necessary packages and modules
import matplotlib.pyplot as plt
import numpy as np
import csv
import math

label_font = {'family': 'Times New Roman',
        'color':  'black',
        'weight': 'normal',
        'size': 14,
        }

def plot_h2_coldens(path):
    path += "coldens_H2.txt"
    data_v, data_j, data_en, data_cd = np.loadtxt(path, usecols=(1, 2, 4, 5), comments='!', unpack=True)
    
    en_v0 = []
    cd_v0 = []
    en_v1 = []
    cd_v1 = []
    en_v2 = []
    cd_v2 = []
    en_v3 = []
    cd_v3 = []

    i = 0
    for v in data_v:
        if v == 0 and data_j[i] != 0 and data_j[i] != 1:
            en_v0 += [data_en[i]]
            cd_v0 += [data_cd[i]]
        elif v == 1:
            en_v1 += [data_en[i]]
            cd_v1 += [data_cd[i]]
        elif v == 2:
            en_v2 += [data_en[i]]
            cd_v2 += [data_cd[i]]
        elif v == 3:
            en_v3 += [data_en[i]]
            cd_v3 += [data_cd[i]]
        i += 1

    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(111)
    ax.scatter(en_v0, cd_v0, s=10, marker='o', color='black', label='v = 0')
    ax.scatter(en_v1, cd_v1, s=15, marker='^', color='red', label='v = 1')
    ax.scatter(en_v2, cd_v2, s=30, marker='x', color='green', label='v = 2')
    ax.scatter(en_v3, cd_v3, s=30, marker='+', color='blue', label='v = 3')

    ax.set_yscale('log')
    ax.set_xlabel('Level energy, cm^{-1}', fontdict=label_font)
    ax.set_ylabel('Column densities, N/g', fontdict=label_font)
    ax.tick_params(labelsize=12)

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

    data_en = []
    data_cd = []
    fname = "../../../observations/Neufeld 2007 H2 column densities.txt"
    data1_j, data_en, data_cd = np.loadtxt(fname, usecols=(0, 1, 5), comments='!', unpack=True)  
    for i in range(len(data_cd)):
        data_cd[i] = math.pow(10., data_cd[i])/(2.*data1_j[i] + 1.)
        if (data1_j[i]%2 == 1):
            data_cd[i] /= 3.

    ax.scatter(data_en, data_cd, s=45, facecolors='none', marker='o', color='blue', label='Neufeld et al. 2007')
    
    data_en = []
    data_cd = []
    fname = "../../../observations/Shinn 2011 IC443 H2 column densities B C G.txt"
    data2_v, data2_j, data_en, data_cd = np.loadtxt(fname, usecols=(0, 1, 2, 5), comments='!', unpack=True)  
    for i in range(len(data_cd)):
        data_cd[i] = math.pow(10., data_cd[i])/(2.*data2_j[i] + 1)
        if (data2_j[i]%2 == 1):
            data_cd[i] /= 3.

    ax.scatter(data_en, data_cd, s=45, facecolors='none', marker='o', color='red', label='Shinn et al. 2011')
    
    data_en = []
    data_cd = []
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

    ax.scatter(en, cd, s=45, facecolors='none', marker='v', color='black', label = label_theory)       
    ax.set_yscale('log')
    ax.set_ylim(1.e+10, 1.e+21)
    ax.set_xlim(0., 20000.)

    ax.set_xlabel('Level energy, cm$^{-1}$', fontdict=label_font)
    ax.set_ylabel('Column densities, N/g', fontdict=label_font)
    ax.tick_params(labelsize=14)

    plt.title('H$_2$ level column densities', fontdict=label_font)
    plt.legend()
    plt.show()

#
# path = "../../../output_data_2e4/shock_30_h2-h_lique-bossion/"
# plot_h2_coldens(path)

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

plot_h2_coldens_observations('../../../output_data_2e4/shock_30_h2-h_lique-bossion_cr1000/', '')