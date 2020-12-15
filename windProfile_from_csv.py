import numpy as np
import matplotlib.pyplot as plt
import DIN_wind_profiles
import pandas as pd

rootDir = 'C:\\Users\\Johannes\\LRZ Sync+Share\\Hydroprojekt\\Simulations\\'
srcFile = rootDir + 'tests_center\\testProfil.csv'
srcDir_list = ['step1\\refinement0\\E_PROFIL\\', 
               'step1\\refinement0\\UNIFORM\\', 
               'step1\\refinement1\\',
               'step1\\refinement2\\',
               #'step1\\', 
               'step2\\', 
               'step3\\E_PROFIL\\', 
               'step3\\UNIFORM\\']

variables_avail = ['AU', 'Iv']

variable =       variables_avail[0]
points_to_plot = ['FK']#, 'rails', 'city']
steps_to_plot =  ['s1']# 's3']#, 's3']
refinements_to_plot = ['r0', 'r1', 'r2']
inlet_condition = ['e']#, 'u']

Din = True

def get_data_to_plot(point_list ,step_list, refinement_list, inlet_condition_list, srcDir_list):
    '''
    returns absolute path of all files related to the parameters set --> next function to plot the content

    naming of .csv files:
        step(s1,s2,s3)_refinement(r0,r1,r2)_inlet(e,u)_point(FK,rails,city)
        e.g.: s1_r0_e_city
    this naming must always be like this and not different
    '''
    rootDir = 'C:\\Users\\Johannes\\LRZ Sync+Share\\Hydroprojekt\\Simulations\\3rd_run\\'
    # source directories of files 
    srcDir_selected = []
    for step in step_list:
        for src in srcDir_list:
            if step[1] == src[4]:
                if step == 's1':
                    for ref in refinement_list:
                        if ref[1] == src[16]:
                            for inlet in inlet_condition_list:
                                if inlet == 'e':
                                    if ref == 'r0' and inlet.upper() == src[18]:
                                        for point in point_list:
                                            srcDir_selected.append(rootDir + src + 
                                                step + '_' + ref + '_' +inlet + '_' + point + '.csv')
                                    elif ref in ['r1' , 'r2']:
                                        for point in point_list:
                                            srcDir_selected.append(rootDir + src + 
                                                step + '_' + ref + '_' +inlet + '_' + point + '.csv')
                                elif inlet == 'u' and ref == 'r0':
                                    if inlet.upper() == src[18]:
                                        for point in point_list:
                                                srcDir_selected.append(rootDir + src + 
                                                    step + '_' + ref + '_' +inlet + '_' + point + '.csv')
                                elif inlet == 'u':# needed since u profile only in refinement 0
                                    if ref in ['r1' , 'r2']:
                                        ref = 'r0' 
                                        src = srcDir_list[1] 
                                        for point in point_list:
                                            srcDir_selected.append(rootDir + src + 
                                                step + '_' + ref + '_' +inlet + '_' + point + '.csv')
                elif step == 's2':
                    for inlet in inlet_condition_list:
                        if inlet == 'e':
                            for point in point_list:
                                srcDir_selected.append(rootDir + src + 
                                    step + '_r2' + '_e' + '_' + point + '.csv')
                        else:
                            continue #no inlet u in step 2
                
                elif step == 's3':
                    for inlet in inlet_condition_list:
                        if inlet.upper() == src[6]:
                            for point in point_list:
                                srcDir_selected.append(rootDir + src +
                                    step + '_r2' + '_' +inlet + '_' + point + '.csv')     

    return srcDir_selected

def get_label(full_file_path):
    f = full_file_path
    if f[-6:-4] == 'FK':
        return f[-14:-4]
    elif f[-8:-4] == 'city':
        return f[-16:-4]
    elif f[-9:-4] == 'rails':
        return f[-17:-4]

def plot_profiles(variable, points, steps, refinements, inlet, Din = True):
    # DIN values 
    vb = 28
    if Din:
        v_z_I,Iv_zI, z_din_I = DIN_wind_profiles.plot_DIN(vb, 'I')
        v_z_II,Iv_z_II, z_din_II = DIN_wind_profiles.plot_DIN(vb, 'II')
        v_z_III,Iv_z_III, z_din_III = DIN_wind_profiles.plot_DIN(vb, 'III')
        v_z_IV,Iv_z_IV, z_din_IV = DIN_wind_profiles.plot_DIN(vb, 'IV')

    selected_data = get_data_to_plot(points_to_plot, steps_to_plot, 
                    refinements_to_plot, inlet_condition, srcDir_list)

    print ('selected data')
    for i in selected_data: print (i)
    print()

    fig = plt.figure('linePlot '+ variable, figsize = (5.4,5))
    ax = fig.add_subplot(111)

    for raw_data in selected_data:
        try:
            data = pd.read_csv(raw_data)
        except FileNotFoundError:
            print (get_label(raw_data), 'was omitted. Check the naming of your files!')
        z = data['Points:2'] - data['Points:2'][0] # normalize
        value = data[variable]
        ax.plot(value, z, '-',label = get_label(raw_data))        

    # ========= DIN ===========
    if Din:
        if variable == 'AU':
            unit = '[m/s]'
            ax.plot(v_z_IV, z_din_IV+z[0], label = 'DIN - category IV', color = 'red', linestyle = '--')
        # TURBULENCE
        elif variable == 'Iv':
            unit = '[-]'
            ax.plot(Iv_z_IV, z_din_IV+z[0], label = 'DIN - category IV', color = 'red', linestyle = '--')

    # === plot settings ========
    ax.set_xlabel(variable + ' ' + unit)
    ax.set_ylabel('z [m]')
    ax.minorticks_on()
    plt.grid(which = 'major')
    plt.grid(which = 'minor', linestyle = ':')
    plt.legend()
    plt.show()

plot_profiles(variable, points_to_plot,steps_to_plot,refinements_to_plot,inlet_condition)