import numpy as np
import scipy
import scipy.interpolate
import pickle
import matplotlib.pyplot as plt
import s3fs
import boto3


class EVLoadModel(object):

    def __init__(self, config):

        self.config = config
        self.num_segments = len(config.categories_dict)
        self.labels = list(set(self.config.categories_dict['Label']))
        self.num_labels = len(self.labels)
        self.load_segments = {}

        if self.config.sample_fast:
            self.ev_segmented_load = np.zeros((self.config.num_time_steps, self.num_segments))
            self.ev_labeled_load = np.zeros((self.config.num_time_steps, self.num_labels))
            self.basic_load = np.zeros((self.config.num_time_steps, ))
            self.total_load = np.zeros((self.config.num_time_steps, ))
            self.nonEV_load = np.zeros((self.config.num_time_steps, ))
        else:
            self.ev_segmented_load = np.zeros((self.config.fast_num_time_steps, self.num_segments))
            self.ev_labeled_load = np.zeros((self.config.fast_num_time_steps, self.num_labels))
            self.basic_load = np.zeros((self.config.fast_num_time_steps, ))
            self.total_load = np.zeros((self.config.fast_num_time_steps, ))
            self.nonEV_load = np.zeros((self.config.fast_num_time_steps, ))

    def calculate_basic_load(self, verbose=True, energies_given=None, energy_scale=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0]):

        for segment_number in range(len(self.config.categories_dict['Segment'])):
            if verbose:
                print('Calculating for segment: ', self.config.categories_dict['Segment'][segment_number])
            num_vehicles = self.config.categories_dict['Vehicles'][segment_number]
            if verbose:
                print('Num vehicles:', num_vehicles)

            if num_vehicles > 0:
#                 start_gmm = pickle.load(open(self.config.gmm_folder_path +
#                                              self.config.categories_dict['GMM Sub Path'][segment_number] +
#                                              '_start.p', "rb"))
                
                s3client = boto3.client('s3')
                response = s3client.get_object(Bucket='script.forecast.inputsoutputs', Key='GMMs/'+self.config.categories_dict['GMM Sub Path'][segment_number] +
                                                             '_start.p')
                body = response['Body'].read()
                start_gmm = pickle.loads(body)
                
#                 energy_gmm = pickle.load(open(self.config.gmm_folder_path +
#                                               self.config.categories_dict['GMM Sub Path'][segment_number] +
#                                               '_energy.p', "rb"))
                
                s3client = boto3.client('s3')
                response = s3client.get_object(Bucket='script.forecast.inputsoutputs', Key='GMMs/'+self.config.categories_dict['GMM Sub Path'][segment_number] +
                                                             '_energy.p')
                body = response['Body'].read()
                energy_gmm = pickle.loads(body)

                # start_times = np.clip(start_gmm.sample(num_vehicles)[0].astype(int).ravel(), 0,
                #                       self.config.categories_dict['Num Time Steps'][segment_number])
                num_ts = self.config.categories_dict['Num Time Steps'][segment_number]
                start_times_init = (self.config.categories_dict['Start Time Scaler'][segment_number]
                                    * start_gmm.sample(num_vehicles)[0]).astype(int).ravel()
                self.starting_start_times = start_times_init
                start_times_init[np.where(start_times_init < 0)] = start_times_init[np.where(start_times_init < 0)] + num_ts
                start_times_init[np.where(start_times_init >= num_ts)] = start_times_init[
                                                                         np.where(start_times_init >= num_ts)] - num_ts
                start_times_init[np.where(start_times_init < 0)] = start_times_init[
                                                                       np.where(start_times_init < 0)] + num_ts
                start_times_init[np.where(start_times_init >= num_ts)] = start_times_init[
                                                                             np.where(
                                                                                 start_times_init >= num_ts)] - num_ts
                # print('Number of negative start times: ', len(start_times_init[np.where(start_times_init < 0)]))
                start_times = np.clip(start_times_init.ravel(), 0, num_ts)
                if energies_given is None:
                    energies = energy_scale[segment_number]*np.clip(energy_gmm.sample(num_vehicles)[0].astype(int).ravel(), 0,
                                       self.config.categories_dict['Energy Clip'][segment_number])
                else:
                    energies = energies_given[segment_number].ravel()
                end_times, load = EVLoadModel.end_times_and_load(self, start_times, energies,
                                                                 self.config.categories_dict['Rate'][segment_number],
                                                                 time_steps_per_hour=self.config.categories_dict['Time Steps Per Hour'][segment_number],
                                                                 num_time_steps=self.config.categories_dict['Num Time Steps'][segment_number])

            else:
                start_times = None
                end_times = None
                energies = None
                if self.config.categories_dict['Segment'][segment_number] == 'Fast':
                    load = np.zeros((self.config.fast_num_time_steps, ))
                else:
                    load = np.zeros((self.config.num_time_steps, ))

            self.load_segments[self.config.categories_dict['Segment'][segment_number]] = {'Num Vehicles': num_vehicles,
                                                                                          'Start Times': start_times,
                                                                                          'End Times': end_times,
                                                                                          'Energies': energies,
                                                                                          'Load': load}

            if self.config.sample_fast:
                if self.config.categories_dict['Time Steps Per Hour'][segment_number] < 60:
                    self.ev_segmented_load[:, segment_number] = load
                else:
                    self.ev_segmented_load[:, segment_number] = load[np.arange(0, self.config.fast_num_time_steps,
                                                                               int(self.config.fast_time_steps_per_hour
                                                                                   / self.config.time_steps_per_hour))]
            else:
                if self.config.categories_dict['Time Steps Per Hour'][segment_number] < 60:
                    xset1 = np.arange(0, self.config.fast_num_time_steps + 1,
                                      int(self.config.fast_time_steps_per_hour / self.config.time_steps_per_hour))
                    xset2 = np.arange(0, self.config.fast_num_time_steps + 1)
                    xset3 = np.arange(0, self.config.fast_num_time_steps)
                    print(np)
                    print(xset1)
                    print(load, load[0])
                    print(xset2)
                    print(xset3)
                    print(np.append(load, load[0]))
                    self.ev_segmented_load[:, segment_number] = \
                        scipy.interpolate.BSpline(xset1, np.append(load, load[0]), xset2)[xset3]
                else:
                    self.ev_segmented_load[:, segment_number] = load

            label_here = self.config.categories_dict['Label'][segment_number]
            label_ind = self.labels.index(label_here)
            self.ev_labeled_load[:, label_ind] += self.ev_segmented_load[:, segment_number].ravel()

        self.basic_load = np.sum(self.ev_segmented_load, axis=1)

    def add_nonEV_load(self, nonEV_load):

        if self.config.sample_fast:
            xset1 = np.arange(0, self.config.num_time_steps + 1, int(self.config.time_steps_per_hour))
            xset2 = np.arange(0, self.config.num_time_steps + 1)
            xset3 = np.arange(0, self.config.num_time_steps)
            self.nonEV_load = 1000*scipy.interpolate.BSpline(xset1, np.append(nonEV_load, nonEV_load[0]), xset2)[xset3]
        else:
            xset1 = np.arange(0, self.config.fast_num_time_steps + 1, int(self.config.fast_time_steps_per_hour))
            xset2 = np.arange(0, self.config.fast_num_time_steps + 1)
            xset3 = np.arange(0, self.config.fast_num_time_steps)
            self.nonEV_load = 1000*scipy.interpolate.BSpline(xset1, np.append(nonEV_load, nonEV_load[0]), xset2)[xset3]

        # 1000 factor is to convert nonEV load into kW from MW
        self.total_load = self.nonEV_load + self.basic_load

    def end_times_and_load(self, start_times, energies, rate, time_steps_per_hour=None, num_time_steps=None):

        if time_steps_per_hour is None:
            time_steps_per_hour = self.config.time_steps_per_hour
        if num_time_steps is None:
            num_time_steps = self.config.num_time_steps
        num = np.shape(start_times)[0]
        load = np.zeros((num_time_steps,))
        end_times = np.zeros(np.shape(start_times)).astype(int)
        for i in range(num):
            length = int(time_steps_per_hour * energies[i] / rate)
            extra_charge = energies[i] - length * rate / time_steps_per_hour
            if (start_times[i] + length) > num_time_steps:
                end_times[i] = int(np.minimum(int(start_times[i]) + length - num_time_steps, num_time_steps))
                load[np.arange(int(start_times[i]), num_time_steps)] += rate * np.ones((num_time_steps - int(start_times[i]),))
                load[np.arange(0, end_times[i])] += rate * np.ones((end_times[i],))
            else:
                end_times[i] = int(start_times[i] + length)
                load[np.arange(int(start_times[i]), end_times[i])] += rate * np.ones((length,))
            if extra_charge > 0:
                if end_times[i] >= num_time_steps:
                    load[0] += extra_charge * time_steps_per_hour
                else:
                    load[end_times[i]] += extra_charge * time_steps_per_hour

        return end_times, load

def stacked_figure(xrange, part1, part2, part3, part4, part5, part6, full,
                   legend_labels=['Res L1', 'Res L2', 'WP', 'Fast', 'Public', 'Fleet', 'Total'], num_parts=6,
                   savestr=None):
    ylabel = 'MW'
    if np.max(full) >= 100000:
        scale = 1000
        ylabel = 'GW'
        part1 = part1 / scale
        part2 = part2 / scale
        part3 = part3 / scale
        part4 = part4 / scale
        part5 = part5 / scale
        part6 = part6 / scale
        full = full / scale

    plt.figure(figsize=(8, 5))
    if num_parts > 0:
        plt.plot(xrange, part1, 'C0')
        plt.fill_between(xrange, 0, part1, color='C0', alpha=0.5)
    if num_parts > 1:
        plt.plot(xrange, part1 + part2, 'C1')
        plt.fill_between(xrange, part1, part1 + part2, color='C1', alpha=0.5)
    if num_parts > 2:
        plt.plot(xrange, part1 + part2 + part3, 'C2')
        plt.fill_between(xrange, part1 + part2, part1 + part2 + part3, color='C2', alpha=0.5)
    if num_parts > 3:
        plt.plot(xrange, part1 + part2 + part3 + part4, 'C3')
        plt.fill_between(xrange, part1 + part2 + part3, part1 + part2 + part3 + part4, color='C3', alpha=0.5)
    if num_parts > 4:
        plt.plot(xrange, part1 + part2 + part3 + part4 + part5, 'C4')
        plt.fill_between(xrange, part1 + part2 + part3 + part4, part1 + part2 + part3 + part4 + part5, color='C4',
                         alpha=0.5)
    if num_parts > 5:
        plt.plot(xrange, part1 + part2 + part3 + part4 + part5 + part6, 'C5')
        plt.fill_between(xrange, part1 + part2 + part3 + part4 + part5, part1 + part2 + part3 + part4 + part5 + part6,
                         color='C5', alpha=0.5)
    plt.plot(xrange, full, 'k')

    plt.xlabel('Hour of day')
    plt.ylabel(ylabel)
    plt.xlim([0, 23.75])
    plt.ylim([0, 1.1*np.max(full)])
    plt.legend(labels=legend_labels)
    plt.tight_layout()
    if savestr is not None:
        plt.savefig(savestr, bbox_inches='tight')

    plt.show()

    return plt


def stacked_figure_withl2(xrange, part1, part2, part3, part4, part5, part6, part7, full, legend_labels, num_parts=7,
                          savestr=None, show=True):
    ylabel = 'MW'
    if np.max(full) >= 100000:
        scale = 1000
        ylabel = 'GW'
        part1 = part1 / scale
        part2 = part2 / scale
        part3 = part3 / scale
        part4 = part4 / scale
        part5 = part5 / scale
        part6 = part6 / scale
        part7 = part7 / scale
        full = full / scale

    plt.figure(figsize=(8, 5))
    if num_parts > 0:
        plt.plot(xrange, part1, 'C0')
        plt.fill_between(xrange, 0, part1, color='C0', alpha=0.5)
    if num_parts > 1:
        plt.plot(xrange, part1 + part2, 'C1')
        plt.fill_between(xrange, part1, part1 + part2, color='C1', alpha=0.5)
    if num_parts > 2:
        plt.plot(xrange, part1 + part2 + part3, 'C2')
        plt.fill_between(xrange, part1 + part2, part1 + part2 + part3, color='C2', alpha=0.5)
    if num_parts > 3:
        plt.plot(xrange, part1 + part2 + part3 + part4, 'C3')
        plt.fill_between(xrange, part1 + part2 + part3, part1 + part2 + part3 + part4, color='C3', alpha=0.5)
    if num_parts > 4:
        plt.plot(xrange, part1 + part2 + part3 + part4 + part5, 'C4')
        plt.fill_between(xrange, part1 + part2 + part3 + part4, part1 + part2 + part3 + part4 + part5, color='C4',
                         alpha=0.5)
    if num_parts > 5:
        plt.plot(xrange, part1 + part2 + part3 + part4 + part5 + part6, 'C5')
        plt.fill_between(xrange, part1 + part2 + part3 + part4 + part5, part1 + part2 + part3 + part4 + part5 + part6,
                         color='C5', alpha=0.5)
    if num_parts > 6:
        plt.plot(xrange, part1 + part2 + part3 + part4 + part5 + part6 + part7, 'C6')
        plt.fill_between(xrange, part1 + part2 + part3 + part4 + part5 + part6, part1 + part2 + part3 + part4 + part5 + part6 + part7,
                         color='C6', alpha=0.5)

    plt.plot(xrange, full, 'k')

    plt.xlabel('Hour of day')
    plt.ylabel(ylabel)
    plt.xlim([0, 23.75])
    plt.ylim([0, 1.1*np.max(full)])
    plt.legend(labels=legend_labels)
    plt.tight_layout()
    if savestr is not None:
        plt.savefig(savestr, bbox_inches='tight')

    if show:
        plt.show()

    return plt
