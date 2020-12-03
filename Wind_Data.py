import numpy as np 
import matplotlib.pyplot as plt
import glob 

path = 'C:\\Users\\Johannes\\Documents\\TUM\\0_MASTER\\4. Master\\Hydroprojekt\\HYD_WindData\\'
files = glob.glob(path + '*muc.txt')

# READ DATA
counter = 0 
defaults = 0
for years in files:
    # if counter >= 1:
    #     break
    try:
        if counter == 0:
            windSpeedData = np.loadtxt(years, delimiter = ';', skiprows = 1, usecols = 3)
        else:    
            decadeData = np.loadtxt(years, delimiter = ';', skiprows = 1, usecols = 3)
            windSpeedData = np.concatenate((windSpeedData, decadeData), axis = 0)  
    except ValueError:
        defaults += 1
        continue
    counter +=1 

print ('total values:', len(windSpeedData),'defaults:', defaults, 'max:', max(windSpeedData))

windTimeSeries = windSpeedData[windSpeedData >= 0.0]
# for i, value in enumerate(windTimeSeries):
#     if value > 100:
#         np.delete(windTimeSeries, i)


yAxes = 'Predicted hourly wind speed m/s'
diagramTitle = 'Hourly wind speed prediction'
gust_m = np.mean(windTimeSeries)
gust_std = np.std(windTimeSeries)

##########   EXTREME VALUE ANALYSIS   ###########################
##1. Gumbel Method
gust_sorted = np.sort(windTimeSeries)
max_rank = len(gust_sorted) # the highest rank 
rank = np.arange(1, max_rank + 1) # the rank of ordered wind speed values. 

gumbel_prob_nonexc = rank / (max_rank + 1)
gumbel_red_var = -np.log(-np.log(gumbel_prob_nonexc))
[gumbel_slope, gumbel_mode] = np.polyfit(gumbel_red_var, gust_sorted, 1)
return_period = np.arange(10, 1000, 10)
gumbel_predicted_gustwind = gumbel_mode + gumbel_slope * (-np.log(-np.log(1-1/return_period)))

##2. Gringorton
gringorten_prob_nonexc = (rank - 0.44) /(max_rank + 0.12)
gringorten_red_var = -np.log(-np.log(gringorten_prob_nonexc))
[gringorten_slope, gringorten_mode] = np.polyfit(gringorten_red_var, gust_sorted,1)
gringorten_predicted_gustwind = gringorten_mode + gringorten_slope * (-np.log(-np.log(1-1/return_period)))

##3. Method of moments
moments_slope = np.sqrt(6)/np.pi * gust_std
moments_mode  = gust_m - 0.5772 * moments_slope
moments_predicted_gustwind = moments_mode + moments_slope * (-np.log(-np.log(1-1/return_period)))

##4. Plot all
def plot_wind_prediction(n_years_return_period, timeSeries):   

    gumbel_predicted_gustwind_rp = gumbel_mode + gumbel_slope * (-np.log(-np.log(1-1/n_years_return_period)))
    gringorten_predicted_gustwind_rp = gringorten_mode + gringorten_slope * (-np.log(-np.log(1-1/n_years_return_period)))
    moments_predicted_gustwind_rp = moments_mode + moments_slope * (-np.log(-np.log(1-1/n_years_return_period)))
    

    fig = plt.figure(figsize=(15, 6))
    # ax1 wird eine figure zugewiesen mit einer reihe und 2 spalten ax1 erhält index 1
    ax1 = fig.add_subplot(1,2,1)
    ax1.plot(return_period, gumbel_predicted_gustwind, label ='Gumbel\'s method')
    #ax1.plot(return_period, gringorten_predicted_gustwind, label ='Gringorten\'s method')
    ax1.set_xlim(left = 0, right = 200)
    #ax1.plot(return_period, moments_predicted_gustwind, label ='Method of moments')
    # # vertical line showing return period
    ax1.vlines(n_years_return_period, min(moments_predicted_gustwind), max(moments_predicted_gustwind),
               colors='k', linestyles='--', label = 'return period = ' + str(n_years_return_period))
    # # text box with results           
    ax1.text(100,moments_predicted_gustwind_rp,'Predicted gust wind for ' + str(n_years_return_period) + 
            ' year return period (m/s)\n' + ' Gumbel Method =' + str(round(gumbel_predicted_gustwind_rp,2)) + 
            '\n Gringorten Method =' + str(round(gringorten_predicted_gustwind_rp,2)) +
            '\n Method of moments =' + str(round(moments_predicted_gustwind_rp,2)) )
    ax1.set_ylabel(yAxes)
    ax1.set_xlabel('Return period (Years)')
    ax1.set_title(diagramTitle)
    ax1.legend()
    ax1.grid(True)

    x = np.linspace(0, len(timeSeries), num = len(timeSeries))
    ax2 = fig.add_subplot(1,2,2)
    ax2.plot(x, timeSeries)
    ax2.grid(True)

    # log axes
    # ax2 = fig.add_subplot(1,2,2)
    # ax2.plot(return_period, gumbel_predicted_gustwind, label ='Gumbel\'s method')
    # ax2.scatter(n_years_return_period, gumbel_predicted_gustwind_rp)
    # ax2.plot(return_period, gringorten_predicted_gustwind, label ='Gringorten\'s method')
    # ax2.scatter(n_years_return_period, gringorten_predicted_gustwind_rp)
    # ax2.plot(return_period, moments_predicted_gustwind, label ='Method of moments')
    # ax2.scatter(n_years_return_period, moments_predicted_gustwind_rp)
    # ax2.set_xscale('log')
    # ax2.set_ylabel(yAxes)
    # ax2.set_xlabel('Return period (years)')
    # ax2.set_title(diagramTitle)
    # ax2.legend()
    # ax2.grid(True)

    # show plot
    plt.show()

plot_wind_prediction(50, windTimeSeries)
