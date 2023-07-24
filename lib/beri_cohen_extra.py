from os.path import join as pjoin, basename
from glob import glob

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

from lib.file_utils import get_dms_pfc_paths_all
from lib.calculation import get_firing_rate_window

behaviour_root = pjoin('data', 'behaviour_data')
relative_value_root = pjoin('data', 'prpd')
spike_data_root = pjoin('data', 'spike_times', 'sessions')

significan_p_threshold = 0.05

def firing_rate_vs_relative_value():
    # instead of spliting to R and L trials
    # plot the firing rate vs relative value
    # for all trials
    # go through each sessions and load up the behaviour data
    # as well as the relative values
    relative_values = []
    firing_rates = []


def pastP_futureP_vs_relative_value():
    # go through each sessions and load up the behaviour data 
    # as well as the relative values
    relative_values_past_R_pfc = []
    relative_values_past_L_pfc = []
    relative_values_future_R_pfc = []
    relative_values_future_L_pfc = []

    relative_values_future_R_pfc_response = []
    relative_values_future_L_pfc_response = []
    relative_values_past_R_pfc_response = []
    relative_values_past_L_pfc_response = []


    relative_values_past_R_dms = []
    relative_values_past_L_dms = []
    relative_values_future_R_dms = []
    relative_values_future_L_dms = []

    relative_values_future_R_dms_response = []
    relative_values_future_L_dms_response = []
    relative_values_past_R_dms_response = []
    relative_values_past_L_dms_response = []

    relative_values_pfc_all = []
    relative_values_dms_all = []

    relative_values_pfc_all_response = []
    relative_values_dms_all_response = []

    pfc_firing_all = []
    dms_firing_all = []

    pfc_firing_all_response = []
    dms_firing_all_response = []

    pfc_firing_rates_past_R = []
    pfc_firing_rates_past_L = []
    pfc_firing_rates_future_R = []
    pfc_firing_rates_future_L = []

    pfc_firing_rates_past_R_response = []
    pfc_firing_rates_past_L_response = []
    pfc_firing_rates_future_R_response = []
    pfc_firing_rates_future_L_response = []

    dms_firing_rates_past_R = []
    dms_firing_rates_past_L = []
    dms_firing_rates_future_R = []
    dms_firing_rates_future_L = []

    dms_firing_rates_past_R_response = []
    dms_firing_rates_past_L_response = []
    dms_firing_rates_future_R_response = []
    dms_firing_rates_future_L_response = []

    for session in glob(pjoin(behaviour_root, '*.csv')):
        session_name = basename(session).split('.')[0]
        relative_values = np.load(pjoin(relative_value_root, session_name+'.npy'))
        session_data = pd.read_csv(session)
        cue_time = np.array(session_data['cue_time'].values)

        # get the trials where the last trial was a right and left response
        past_R_indices = np.where(session_data['trial_response_side'].values[:-1] == 1)[0]
        past_L_indices = np.where(session_data['trial_response_side'].values[:-1] == -1)[0]
        past_R_indices = past_R_indices + 1
        past_L_indices = past_L_indices + 1

        # get the trials where the next trial was a right and left response
        future_R_indices = np.where(session_data['trial_response_side'].values[1:] == 1)[0]
        future_L_indices = np.where(session_data['trial_response_side'].values[1:] == -1)[0]
        future_R_indices = future_R_indices - 1
        future_L_indices = future_L_indices - 1

        # load up the spike data
        for pfc_cell in glob(pjoin(spike_data_root, session_name, 'pfc_*')):
            pfc_cell_name = basename(pfc_cell).split('.')[0]
            pfc_cell_data = np.load(pfc_cell)

            # get the firing rate of the cell
            firing_rates = get_firing_rate_window(cue_time, pfc_cell_data, window_left=-1, window_right=-0.5)
            firing_rates = np.array(firing_rates)

            firing_rates_response = get_firing_rate_window(cue_time, pfc_cell_data, window_left=0, window_right=1.5)
            firing_rates_response = np.array(firing_rates_response)

            # check if the firing rates and relative values are # strongly correlated using pearson correlation
            # continue if p value
            if np.std(firing_rates) != 0 and stats.pearsonr(firing_rates, relative_values)[1] < significan_p_threshold:
                firing_rates = (firing_rates - np.mean(firing_rates)) / np.std(firing_rates)
                # if pearson's r < 0 then flip the relative values
                # so that the firing rate is positively correlated with relative values
                if stats.pearsonr(firing_rates, relative_values)[0] < 0:
                    relative_values = -relative_values

                # get the firing rates for the past and future trials
                pfc_firing_rates_past_R.extend(firing_rates[past_R_indices])
                pfc_firing_rates_past_L.extend(firing_rates[past_L_indices])
                pfc_firing_rates_future_R.extend(firing_rates[future_R_indices])
                pfc_firing_rates_future_L.extend(firing_rates[future_L_indices])

                relative_values_future_L_pfc.extend(relative_values[future_L_indices])
                relative_values_future_R_pfc.extend(relative_values[future_R_indices])
                relative_values_past_L_pfc.extend(relative_values[past_L_indices])
                relative_values_past_R_pfc.extend(relative_values[past_R_indices])

                relative_values_pfc_all.extend(relative_values)
                pfc_firing_all.extend(firing_rates)
            
            if np.std(firing_rates_response) != 0 and stats.pearsonr(firing_rates_response, relative_values)[1] < significan_p_threshold:
                firing_rates_response = (firing_rates_response - np.mean(firing_rates_response)) / np.std(firing_rates_response)

                if stats.pearsonr(firing_rates_response, relative_values)[0] < 0:
                    relative_values = -relative_values

                # get the firing rates for the past and future trials
                pfc_firing_rates_past_R_response.extend(firing_rates_response[past_R_indices])
                pfc_firing_rates_past_L_response.extend(firing_rates_response[past_L_indices])
                pfc_firing_rates_future_R_response.extend(firing_rates_response[future_R_indices])
                pfc_firing_rates_future_L_response.extend(firing_rates_response[future_L_indices])

                relative_values_future_L_pfc_response.extend(relative_values[future_L_indices])
                relative_values_future_R_pfc_response.extend(relative_values[future_R_indices])
                relative_values_past_L_pfc_response.extend(relative_values[past_L_indices])
                relative_values_past_R_pfc_response.extend(relative_values[past_R_indices])

                relative_values_pfc_all_response.extend(relative_values)
                pfc_firing_all_response.extend(firing_rates_response)

        for dms_cell in glob(pjoin(spike_data_root, session_name, 'dms_*')):
            dms_cell_name = basename(dms_cell).split('.')[0]
            dms_cell_data = np.load(dms_cell)

            # get the firing rate of the cell
            firing_rates = get_firing_rate_window(cue_time, dms_cell_data, window_left=-1, window_right=-0.5)
            firing_rates = np.array(firing_rates)            

            firing_rates_response = get_firing_rate_window(cue_time, dms_cell_data, window_left=0, window_right=1.5)
            firing_rates_response = np.array(firing_rates_response)

            if np.std(firing_rates) != 0 and stats.pearsonr(firing_rates, relative_values)[1] < significan_p_threshold:
                if stats.pearsonr(firing_rates, relative_values)[0] < 0:
                    relative_values = -relative_values

                firing_rates = (firing_rates - np.mean(firing_rates)) / np.std(firing_rates)
                # get the firing rates for the past and future trials
                dms_firing_rates_past_R.extend(firing_rates[past_R_indices])
                dms_firing_rates_past_L.extend(firing_rates[past_L_indices])
                dms_firing_rates_future_R.extend(firing_rates[future_R_indices])
                dms_firing_rates_future_L.extend(firing_rates[future_L_indices])

                relative_values_future_L_dms.extend(relative_values[future_L_indices])
                relative_values_future_R_dms.extend(relative_values[future_R_indices])
                relative_values_past_L_dms.extend(relative_values[past_L_indices])
                relative_values_past_R_dms.extend(relative_values[past_R_indices])

                relative_values_dms_all.extend(relative_values)
                dms_firing_all.extend(firing_rates)

            if np.std(firing_rates_response) != 0 and stats.pearsonr(firing_rates_response, relative_values)[1] < significan_p_threshold:
                if stats.pearsonr(firing_rates_response, relative_values)[0] < 0:
                    relative_values = -relative_values

                firing_rates_response = (firing_rates_response - np.mean(firing_rates_response)) / np.std(firing_rates_response)
                # get the firing rates for the past and future trials
                dms_firing_rates_past_R_response.extend(firing_rates_response[past_R_indices])
                dms_firing_rates_past_L_response.extend(firing_rates_response[past_L_indices])
                dms_firing_rates_future_R_response.extend(firing_rates_response[future_R_indices])
                dms_firing_rates_future_L_response.extend(firing_rates_response[future_L_indices])

                relative_values_future_L_dms_response.extend(relative_values[future_L_indices])
                relative_values_future_R_dms_response.extend(relative_values[future_R_indices])
                relative_values_past_L_dms_response.extend(relative_values[past_L_indices])
                relative_values_past_R_dms_response.extend(relative_values[past_R_indices])

                relative_values_dms_all_response.extend(relative_values)
                dms_firing_all_response.extend(firing_rates_response)

    # discretize the relative values into 20 bins
    relative_values_past_L_dms = np.digitize(relative_values_past_L_dms, bins=np.linspace(-1, 1, 10))
    relative_values_past_R_dms = np.digitize(relative_values_past_R_dms, bins=np.linspace(-1, 1, 10))
    relative_values_future_L_dms = np.digitize(relative_values_future_L_dms, bins=np.linspace(-1, 1, 10))
    relative_values_future_R_dms = np.digitize(relative_values_future_R_dms, bins=np.linspace(-1, 1, 10))

    relative_values_past_L_pfc = np.digitize(relative_values_past_L_pfc, bins=np.linspace(-1, 1, 10))
    relative_values_past_R_pfc = np.digitize(relative_values_past_R_pfc, bins=np.linspace(-1, 1, 10))
    relative_values_future_L_pfc = np.digitize(relative_values_future_L_pfc, bins=np.linspace(-1, 1, 10))
    relative_values_future_R_pfc = np.digitize(relative_values_future_R_pfc, bins=np.linspace(-1, 1, 10))

    relative_values_past_L_dms_response = np.digitize(relative_values_past_L_dms_response, bins=np.linspace(-1, 1, 10))
    relative_values_past_R_dms_response = np.digitize(relative_values_past_R_dms_response, bins=np.linspace(-1, 1, 10))
    relative_values_future_L_dms_response = np.digitize(relative_values_future_L_dms_response, bins=np.linspace(-1, 1, 10))
    relative_values_future_R_dms_response = np.digitize(relative_values_future_R_dms_response, bins=np.linspace(-1, 1, 10))

    relative_values_past_L_pfc_response = np.digitize(relative_values_past_L_pfc_response, bins=np.linspace(-1, 1, 10))
    relative_values_past_R_pfc_response = np.digitize(relative_values_past_R_pfc_response, bins=np.linspace(-1, 1, 10))
    relative_values_future_L_pfc_response = np.digitize(relative_values_future_L_pfc_response, bins=np.linspace(-1, 1, 10))
    relative_values_future_R_pfc_response = np.digitize(relative_values_future_R_pfc_response, bins=np.linspace(-1, 1, 10))

    relative_values_pfc_all = np.digitize(relative_values_pfc_all, bins=np.linspace(-1, 1, 10))
    relative_values_dms_all = np.digitize(relative_values_dms_all, bins=np.linspace(-1, 1, 10))

    relative_values_pfc_all_response = np.digitize(relative_values_pfc_all_response, bins=np.linspace(-1, 1, 10))
    relative_values_dms_all_response = np.digitize(relative_values_dms_all_response, bins=np.linspace(-1, 1, 10))

    
    relative_values_past_L_dms = relative_values_past_L_dms * 0.2 - 1
    relative_values_past_R_dms = relative_values_past_R_dms * 0.2 - 1
    relative_values_future_L_dms = relative_values_future_L_dms * 0.2 - 1
    relative_values_future_R_dms = relative_values_future_R_dms * 0.2 - 1

    relative_values_past_L_pfc = relative_values_past_L_pfc * 0.2 - 1
    relative_values_past_R_pfc = relative_values_past_R_pfc * 0.2 - 1
    relative_values_future_L_pfc = relative_values_future_L_pfc * 0.2 - 1
    relative_values_future_R_pfc = relative_values_future_R_pfc * 0.2 - 1

    relative_values_past_L_dms_response = relative_values_past_L_dms_response * 0.2 - 1
    relative_values_past_R_dms_response = relative_values_past_R_dms_response * 0.2 - 1
    relative_values_future_L_dms_response = relative_values_future_L_dms_response * 0.2 - 1
    relative_values_future_R_dms_response = relative_values_future_R_dms_response * 0.2 - 1

    relative_values_past_L_pfc_response = relative_values_past_L_pfc_response * 0.2 - 1
    relative_values_past_R_pfc_response = relative_values_past_R_pfc_response * 0.2 - 1
    relative_values_future_L_pfc_response = relative_values_future_L_pfc_response * 0.2 - 1
    relative_values_future_R_pfc_response = relative_values_future_R_pfc_response * 0.2 - 1

    relative_values_pfc_all = relative_values_pfc_all * 0.2 - 1
    relative_values_dms_all = relative_values_dms_all * 0.2 - 1

    relative_values_pfc_all_response = relative_values_pfc_all_response * 0.2 - 1
    relative_values_dms_all_response = relative_values_dms_all_response * 0.2 - 1

    pfc_firing_rates_past_R = np.array(pfc_firing_rates_past_R)
    pfc_firing_rates_past_L = np.array(pfc_firing_rates_past_L)
    pfc_firing_rates_future_R = np.array(pfc_firing_rates_future_R)
    pfc_firing_rates_future_L = np.array(pfc_firing_rates_future_L)

    dms_firing_rates_past_R = np.array(dms_firing_rates_past_R)
    dms_firing_rates_past_L = np.array(dms_firing_rates_past_L)
    dms_firing_rates_future_R = np.array(dms_firing_rates_future_R)
    dms_firing_rates_future_L = np.array(dms_firing_rates_future_L)

    # plot the firing rates vs relative values as line plots with 
    # shaded error bars for the standard error
    # with R and L trials sharing the same plot
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    sns.lineplot(x=relative_values_past_R_pfc, y=pfc_firing_rates_past_R, ax=axes[0, 0], errorbar=('ci', 68), label='past R')
    sns.lineplot(x=relative_values_past_L_pfc, y=pfc_firing_rates_past_L, ax=axes[0, 0], errorbar=('ci', 68), label='past L')
    sns.lineplot(x=relative_values_future_R_pfc, y=pfc_firing_rates_future_R, ax=axes[0, 1], errorbar=('ci', 68), label='future R')
    sns.lineplot(x=relative_values_future_L_pfc, y=pfc_firing_rates_future_L, ax=axes[0, 1], errorbar=('ci', 68), label='future L')

    sns.lineplot(x=relative_values_past_R_dms, y=dms_firing_rates_past_R, ax=axes[1, 0], errorbar=('ci', 68), label='past R')
    sns.lineplot(x=relative_values_past_L_dms, y=dms_firing_rates_past_L, ax=axes[1, 0], errorbar=('ci', 68), label='past L')
    sns.lineplot(x=relative_values_future_R_dms, y=dms_firing_rates_future_R, ax=axes[1, 1], errorbar=('ci', 68), label='future R')
    sns.lineplot(x=relative_values_future_L_dms, y=dms_firing_rates_future_L, ax=axes[1, 1], errorbar=('ci', 68), label='future L')
    
    axes[0, 0].set_title('Past trials')
    axes[0, 1].set_title('Future trials')
    axes[0, 0].set_ylabel('PFC firing rate')
    axes[1, 0].set_ylabel('DMS firing rate')
    axes[1, 0].set_xlabel('Relative value')
    axes[1, 1].set_xlabel('Relative value')

    # set the x asis to [-1, 1]
    axes[0, 0].set_xticks([-1, 0, 1])
    axes[0, 1].set_xticks([-1, 0, 1])
    axes[1, 0].set_xticks([-1, 0, 1])
    axes[1, 1].set_xticks([-1, 0, 1])

    fig.suptitle('PFC firing rate vs relative value')

    # another figure for the response period
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    sns.lineplot(x=relative_values_past_R_pfc_response, y=pfc_firing_rates_past_R_response, ax=axes[0, 0], errorbar=('ci', 68), label='past R')
    sns.lineplot(x=relative_values_past_L_pfc_response, y=pfc_firing_rates_past_L_response, ax=axes[0, 0], errorbar=('ci', 68), label='past L')
    sns.lineplot(x=relative_values_future_R_pfc_response, y=pfc_firing_rates_future_R_response, ax=axes[0, 1], errorbar=('ci', 68), label='future R')
    sns.lineplot(x=relative_values_future_L_pfc_response, y=pfc_firing_rates_future_L_response, ax=axes[0, 1], errorbar=('ci', 68), label='future L')
    sns.lineplot(x=relative_values_past_R_dms_response, y=dms_firing_rates_past_R_response, ax=axes[1, 0], errorbar=('ci', 68), label='past R')
    sns.lineplot(x=relative_values_past_L_dms_response, y=dms_firing_rates_past_L_response, ax=axes[1, 0], errorbar=('ci', 68), label='past L')
    sns.lineplot(x=relative_values_future_R_dms_response, y=dms_firing_rates_future_R_response, ax=axes[1, 1], errorbar=('ci', 68), label='future R')
    sns.lineplot(x=relative_values_future_L_dms_response, y=dms_firing_rates_future_L_response, ax=axes[1, 1], errorbar=('ci', 68), label='future L')

    axes[0, 0].set_title('Past trials')
    axes[0, 1].set_title('Future trials')
    axes[0, 0].set_ylabel('PFC firing rate')
    axes[1, 0].set_ylabel('DMS firing rate')

    axes[1, 0].set_xlabel('Relative value')
    axes[1, 1].set_xlabel('Relative value')

    # set the x asis to [-1, 1]
    axes[0, 0].set_xticks([-1, 0, 1])
    axes[0, 1].set_xticks([-1, 0, 1])
    axes[1, 0].set_xticks([-1, 0, 1])
    axes[1, 1].set_xticks([-1, 0, 1])

    fig.suptitle('firing rate vs relative value (response period)')
    plt.show()

    # another figure for all trials
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    sns.lineplot(x=relative_values_pfc_all, y=pfc_firing_all, ax=axes[0, 0], errorbar=('ci', 68))
    sns.lineplot(x=relative_values_dms_all, y=dms_firing_all, ax=axes[0, 1], errorbar=('ci', 68))
    sns.lineplot(x=relative_values_pfc_all_response, y=pfc_firing_all_response, ax=axes[1, 0], errorbar=('ci', 68))
    sns.lineplot(x=relative_values_dms_all_response, y=dms_firing_all_response, ax=axes[1, 1], errorbar=('ci', 68))

    axes[0, 0].set_title('BG')
    axes[0, 1].set_title('Response period')
    axes[0, 0].set_ylabel('PFC firing rate')
    axes[1, 0].set_ylabel('DMS firing rate')
    
    axes[1, 0].set_xlabel('Relative value')
    axes[1, 1].set_xlabel('Relative value')

    # set the x asis to [-1, 1]
    axes[0, 0].set_xticks([-1, 0, 1])
    axes[0, 1].set_xticks([-1, 0, 1])
    axes[1, 0].set_xticks([-1, 0, 1])
    axes[1, 1].set_xticks([-1, 0, 1])

    fig.suptitle('firing rate vs relative value (all trials)')
    plt.show()


