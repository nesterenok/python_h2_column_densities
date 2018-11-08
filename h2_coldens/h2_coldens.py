# Import the necessary packages and modules
import matplotlib.pyplot as plt
import numpy as np
import csv

label_font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 12,
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



#
#
#
# path = "../../../output_data_2e4/shock_30_h2-h_lique-bossion/"
# plot_h2_coldens(path)

path = "../../../output_data_2e4/shock_30_h2-h_lique-bossion/"
plot_h2_dissociation(path)