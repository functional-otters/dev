# -*- coding: utf-8 -*-
"""functional-otters-extra.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KDC4j0YtCSRFoMtDWrJlF3UONbVqGvQG

## Loading of Steinmetz data

includes some visualizations. foo
"""

#@title Data retrieval
import os, requests

fname = ['steinmetz_st.npz']
fname.append('steinmetz_wav.npz')
fname.append('steinmetz_lfp.npz')

url = ["https://osf.io/4bjns/download"]
url.append("https://osf.io/ugm9v/download")
url.append("https://osf.io/kx3v9/download")

for j in range(len(url)):
  if not os.path.isfile(fname[j]):
    try:
      r = requests.get(url[j])
    except requests.ConnectionError:
      print("!!! Failed to download data !!!")
    else:
      if r.status_code != requests.codes.ok:
        print("!!! Failed to download data !!!")
      else:
        with open(fname[j], "wb") as fid:
          fid.write(r.content)

# #@title Data retrieval
# import os, requests

# fname = []
# for j in range(3):
#   fname.append('steinmetz_part%d.npz'%j)
# url = ["https://osf.io/agvxh/download"]
# url.append("https://osf.io/uv3mw/download")
# url.append("https://osf.io/ehmw2/download")

# for j in range(len(url)):
#   if not os.path.isfile(fname[j]):
#     try:
#       r = requests.get(url[j])
#     except requests.ConnectionError:
#       print("!!! Failed to download data !!!")
#     else:
#       if r.status_code != requests.codes.ok:
#         print("!!! Failed to download data !!!")
#       else:
#         with open(fname[j], "wb") as fid:
#           fid.write(r.content)

# #@title Data loading
# import numpy as np

# alldat = np.array([])
# for j in range(len(fname)):
#   alldat = np.hstack((alldat, np.load('steinmetz_part%d.npz'%j, allow_pickle=True)['dat']))

# # select just one of the recordings here. 11 is nice because it has some neurons in vis ctx.
# dat = alldat[11]
# print(dat.keys())

"""`alldat` contains 39 sessions from 10 mice, data from Steinmetz et al, 2019. Time bins for all measurements are 10ms, starting 500ms before stimulus onset. The mouse had to determine which side has the highest contrast. For each `dat = alldat[k]`, you have the fields below. For extra variables, check out the extra notebook and extra data files (lfp, waveforms and exact spike times, non-binned).

* `dat['mouse_name']`: mouse name
* `dat['date_exp']`: when a session was performed
* `dat['spks']`: neurons by trials by time bins.
* `dat['brain_area']`: brain area for each neuron recorded.
* `dat['ccf']`: Allen Institute brain atlas coordinates for each neuron.
* `dat['ccf_axes']`: axes names for the Allen CCF.
* `dat['contrast_right']`: contrast level for the right stimulus, which is always contralateral to the recorded brain areas.
* `dat['contrast_left']`: contrast level for left stimulus.
* `dat['gocue']`: when the go cue sound was played.
* `dat['response_times']`: when the response was registered, which has to be after the go cue. The mouse can turn the wheel before the go cue (and nearly always does!), but the stimulus on the screen won't move before the go cue.
* `dat['response']`: which side the response was (`-1`, `0`, `1`). When the right-side stimulus had higher contrast, the correct choice was `-1`. `0` is a no go response.
* `dat['feedback_time']`: when feedback was provided.
* `dat['feedback_type']`: if the feedback was positive (`+1`, reward) or negative (`-1`, white noise burst).
* `dat['wheel']`: turning speed of the wheel that the mice uses to make a response, sampled at `10ms`.
* `dat['pupil']`: pupil area  (noisy, because pupil is very small) + pupil horizontal and vertical position.
* `dat['face']`: average face motion energy from a video camera.
* `dat['licks']`: lick detections, 0 or 1.
* `dat['trough_to_peak']`: measures the width of the action potential waveform for each neuron. Widths `<=10` samples are "putative fast spiking neurons".
* `dat['%X%_passive']`: same as above for `X` = {`spks`, `pupil`, `wheel`, `contrast_left`, `contrast_right`} but for  passive trials at the end of the recording when the mouse was no longer engaged and stopped making responses.
* `dat['prev_reward']`: time of the feedback (reward/white noise) on the previous trial in relation to the current stimulus time.
* `dat['reaction_time']`: ntrials by 2. First column: reaction time computed from the wheel movement as the first sample above `5` ticks/10ms bin. Second column: direction of the wheel movement (`0` = no move detected).
"""

#@title Import matplotlib and set defaults
from matplotlib import rcParams
from matplotlib import pyplot as plt
rcParams['figure.figsize'] = [20, 4]
rcParams['font.size'] =15
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False
rcParams['figure.autolayout'] = True

#@title Data loading
import numpy as np

#dat_LFP = np.load('steinmetz_lfp.npz', allow_pickle=True)['dat']
#dat_WAV = np.load('steinmetz_wav.npz', allow_pickle=True)['dat']
dat_ST = np.load('steinmetz_st.npz', allow_pickle=True)['dat']

session_idx = 11

# select just one of the recordings here. 11 is nice because it has some neurons in vis ctx.
#dat = dat_LFP[session_idx]
#print(dat.keys())
#dat = dat_WAV[session_idx]
#print(dat.keys())
dat_sess = dat_ST[session_idx]
print(dat_sess.keys())

"""`dat_LFP`, `dat_WAV`, `dat_ST` contain 39 sessions from 10 mice, data from Steinmetz et al, 2019, supplemental to the main data provided for NMA. Time bins for all measurements are 10ms, starting 500ms before stimulus onset (same as the main data). The followin fields are available across the three supplemental files.

* `dat['lfp']`: recording of the local field potential in each brain area from this experiment, binned at `10ms`.
* `dat['brain_area_lfp']`: brain area names for the LFP channels.
* `dat['trough_to_peak']`: measures the width of the action potential waveform for each neuron. Widths `<=10` samples are "putative fast spiking neurons".
* `dat['waveform_w']`: temporal components of spike waveforms. `w@u` reconstructs the time by channels action potential shape.
* `dat['waveform_u]`: spatial components of spike waveforms.
* `dat['ss']`: neurons by trials. Exact spikes times for each neuron and each trial, reference to the stimulus onset. A (neuron,trial) entry can be an empty list if that neuron did not fire at all on that trial.
* `dat['%X%_passive']`: same as above for `X` = {`lfp`, `ss`} but for  passive trials at the end of the recording when the mouse was no longer engaged and stopped making responses.
"""

# groupings of brain regions
regions = ["vis ctx", "thal", "hipp", "other ctx", "midbrain", "basal ganglia", "cortical subplate", "other"]
brain_groups = [["VISa", "VISam", "VISl", "VISp", "VISpm", "VISrl"], # visual cortex
                ["CL", "LD", "LGd", "LH", "LP", "MD", "MG", "PO", "POL", "PT", "RT", "SPF", "TH", "VAL", "VPL", "VPM"], # thalamus
                ["CA", "CA1", "CA2", "CA3", "DG", "SUB", "POST"], # hippocampal
                ["ACA", "AUD", "COA", "DP", "ILA", "MOp", "MOs", "OLF", "ORB", "ORBm", "PIR", "PL", "SSp", "SSs", "RSP"," TT"], # non-visual cortex
                ["APN", "IC", "MB", "MRN", "NB", "PAG", "RN", "SCs", "SCm", "SCig", "SCsg", "ZI"], # midbrain
                ["ACB", "CP", "GPe", "LS", "LSc", "LSr", "MS", "OT", "SNr", "SI"], # basal ganglia
                ["BLA", "BMA", "EP", "EPd", "MEA"] # cortical subplate
                ]

import scipy
import seaborn as sns
from scipy import signal

def plot_corr_matrix(my_matrix):
  fig, ax = plt.subplots(figsize=(10, 8))
  cmax = np.percentile(my_matrix, 95)# Maximum colormap value
  sns.heatmap(my_matrix,cmap=plt.get_cmap('viridis'),vmin=cmax, vmax=-cmax)

def get_spikes(neuron_idx, trial_idx):
  spike_times = dat_sess['ss'][neuron_idx][trial_idx]
  spikes = np.zeros(2500)
  for spike_idx in range(len(spike_times)):
    spike_time = spike_times[spike_idx]
    spike_time_ms = int(spike_time*1000)
    spikes[spike_time_ms] = 1.0
  return spikes

def gen_spikes_filter(spikes):
  sigma = 2 # size of time window
  spikes_normal_filter = scipy.ndimage.gaussian_filter(spikes, sigma)
  return spikes_normal_filter

def corrcoef_between(s1_filter, s2_filter):
  return np.corrcoef(s1_filter, s2_filter)

num_neurons = len(dat_sess['ss'])
num_trials = len(dat_sess['ss'][1])

# neuron_idx_1 = 603 # this is the lucky one
# neuron_idx_2 = 595 # lucky number second

trial_idx = 42     # meaning of life

corr_matrix = np.zeros((num_neurons, num_neurons))

ss_filter = []
for neuron_idx in range(num_neurons):
  s = get_spikes(neuron_idx, trial_idx)
  #print(f"s spike times {neuron_idx}: {np.where(s == 1)}")

  s_filter = gen_spikes_filter(s)
  ss_filter.append(s_filter)

corrcoef = np.corrcoef(ss_filter)
corrcoef = np.nan_to_num(corrcoef)
#print(corrcoef.shape)
#print(corrcoef)
plot_corr_matrix(corrcoef)

# for neuron_idx_1 in range(num_neurons-1):
#   neuron_idx_2 = neuron_idx_1 + 1

#   s1 = get_spikes(neuron_idx_1, trial_idx)
#   s2 = get_spikes(neuron_idx_2, trial_idx)

#   print(f"s1 spike times {neuron_idx_1}: {np.where(s1 == 1)}")
#   print(f"s2 spike times {neuron_idx_2}: {np.where(s2 == 1)}")

#   # plt.figure()
#   # plt.eventplot(np.where(s1 == 1))

#   # plt.figure()
#   # plt.eventplot(np.where(s2 == 1))


#   s1_filter = gen_spikes_filter(s1)
#   s2_filter = gen_spikes_filter(s2)

#   # plt.figure()
#   # plt.plot(s1_filter)

#   # plt.figure()
#   # plt.plot(s2_filter)

#   corrcoef = corrcoef_between(s1_filter, s2_filter)
#   corrcoef = np.nan_to_num(corrcoef)
#   print("corrcoef:", corrcoef)
#   corr_matrix[neuron_idx_1][neuron_idx_1] = 1
#   corr_matrix[neuron_idx_2][neuron_idx_1] = corrcoef[1][0]
#   corr_matrix[neuron_idx_1][neuron_idx_2] = corrcoef[0][1]
#   corr_matrix[neuron_idx_2][neuron_idx_2] = 1

#   # plt.figure()

# print("corr_matrix:", corr_matrix)
# plot_corr_matrix(corr_matrix)

# Plot cross correlation function for two neurons

n1 = gen_spikes_filter(get_spikes(620, trial_idx))
n2 = gen_spikes_filter(get_spikes(580, trial_idx))

corr_all = scipy.signal.correlate(n1, n2, mode='full')

fig, [ax1, ax2, ax3] = plt.subplots(3, 1, figsize=(20, 7))
ax1.plot(n1)
ax1.plot(n2)
ax2.plot(corr_all)
lags, c, _, _ = ax3.xcorr(n1, n2, maxlags=200);

maxlag = lags[np.argmax(c)]
print("max correlation is at lag %d" % maxlag)

plt.acorr(n1, maxlags=200);

# Correlation matrix of instantaneous correlations, averaged over trials

trials = np.arange(10) # Set number of trials

corr_matrices = []

for trial_idx in trials:

  ss_filter = []

  for neuron_idx in range(num_neurons):
    s = get_spikes(neuron_idx, trial_idx)
    s_filter = gen_spikes_filter(s)
    ss_filter.append(s_filter)

  corr_matrix = np.nan_to_num(np.corrcoef(ss_filter))
  corr_matrices.append(corr_matrix)

trial_avg_corr_matrix = np.mean(corr_matrices, axis=0)

plot_corr_matrix(trial_avg_corr_matrix)

# Time-lagged correlations, averaged over trials, for a given lag

lag = -20   # Set lag
trials = np.arange(100)  # Set number of trials
num_neurons = len(dat_sess['ss'])

coeffs_all = []

for trial_idx in trials:

  neurons = []
  neurons_lagged = []

  for neuron_idx in range(num_neurons):
    n = gen_spikes_filter(get_spikes(neuron_idx, trial_idx))
    neurons.append(n)
    n_lagged = np.roll(n, lag)
    neurons_lagged.append(n_lagged)

  coeffs = [np.corrcoef(neurons[x], neurons_lagged[x])[1, 0] for x in range(num_neurons)]
  coeffs = np.nan_to_num(coeffs)
  coeffs_all.append(coeffs)

max_corr = np.max(coeffs_all)
location = np.where(coeffs_all == np.amax(coeffs_all))

print("Max correlation at lag {} is {}".format(lag, max_corr))

print("Neurons with this correlation are {} {}".format(location[0], location[1]))

# Calculate max lag for each pair of neurons

trials = np.arange(1)

num_neurons = 50

lag_range = 10  # lags to calculate over in the cross-correlation function

max_lags_matrix_all = []

for trial_idx in trials:

  max_lags_matrix = np.zeros((num_neurons, num_neurons))
  corr_matrix_resp_lag = np.zeros((num_neurons, num_neurons))

  spikes_filter_list = []

  for neuron_idx1 in range(num_neurons):

    # generate smoothed spike sequence for first neuron
    n1 = gen_spikes_filter(get_spikes(neuron_idx1, trial_idx))

    for neuron_idx2 in range(neuron_idx1+1, num_neurons):

        # generate smoothed spike sequence for second neuron
        n2 = gen_spikes_filter(get_spikes(neuron_idx2, trial_idx))

        # calculate cross correlation at each lag, find lag with max correlation
        lags, c, _, _ = plt.xcorr(n1, n2, maxlags=lag_range)
        plt.close()
        max_lag = lags[np.argmax(c)]


        corr = np.nan_to_num(c[max_lag])

        # put max lag into location in matrix
        max_lags_matrix[neuron_idx1, neuron_idx2] = max_lag
        corr_matrix_resp_lag[neuron_idx1, neuron_idx2] = corr

    max_lags_matrix_all.append(max_lags_matrix)

avg_max_lags_matrix = np.mean(max_lags_matrix_all, axis=0)

plot_corr_matrix(max_lags_matrix)  # visualise max lags for each neuron pair

plot_corr_matrix(corr_matrix_resp_lag)

# find pairs of neurons with "large" correlation

np.where(corr_matrix_resp_lag > 0.05)

# look at cross-correlation function for these neurons over trials

cs = []

for trial in range(100):
  n1 = gen_spikes_filter(get_spikes(49, trial))
  n2 = gen_spikes_filter(get_spikes(28, trial))
  lags, c, _, _ = plt.xcorr(n1, n2, usevlines=False, linestyle='-', marker=None, linewidth=2, maxlags=200);
  cs.append(c)

# plot mean of cross correlation function

plt.plot(lags, np.mean(cs, axis=0), lw=4)
plt.plot(lags, np.mean(cs, axis=0) + np.std(cs, axis=0), c='r')
plt.plot(lags, np.mean(cs, axis=0) - np.std(cs, axis=0))

# for each neuron, get indices and lags of neurons which correlate highly with it

threshold = 0.01  # need to determine statistically

index_list = []
lags_list = []

for neuron in range(num_neurons):
  indices = np.where(corr_matrix_resp_lag[neuron] > threshold)  # which neurons the neuron is "highly" correlated to
  resp_lags = max_lags_matrix[neuron][indices]  # respective lags for each of these correlations

  index_list.append(indices)
  lags_list.append(resp_lags)

print(np.array(index_list))

trial_idx = 42

corr = scipy.stats.pearsonr(gen_spikes_filter(get_spikes(634, trial_idx)), gen_spikes_filter(get_spikes(618, trial_idx)))
print(corr)

