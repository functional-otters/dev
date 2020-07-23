import scipy

import seaborn as sns

import seaborn as sns

def plot_corr_matrix(my_matrix):
  fig, ax = plt.subplots(figsize=(10, 8))
  cmax = np.percentile(my_matrix, 95)# Maximum colormap value
  sns.heatmap(my_matrix,cmap=plt.get_cmap('viridis'),vmin=cmax, vmax=-cmax)

def get_spikes(neuron_idx, trial_idx):
  spike_times = dat['ss'][neuron_idx][trial_idx]
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

num_neurons = len(dat['ss'])
#num_neurons = 10

# neuron_idx_1 = 603 # this is the lucky one
# neuron_idx_2 = 595 # lucky number second

trial_idx = 42     # meaning of life

corr_matrix = np.zeros((num_neurons, num_neurons))

ss_filter = []
for neuron_idx in range(num_neurons):
  s = get_spikes(neuron_idx, trial_idx)
  print(f"s spike times {neuron_idx}: {np.where(s == 1)}")

  s_filter = gen_spikes_filter(s)

  ss_filter.append(s_filter)

corrcoef = np.corrcoef(ss_filter)
corrcoef = np.nan_to_num(corrcoef)
print(corrcoef.shape)
print(corrcoef)
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
