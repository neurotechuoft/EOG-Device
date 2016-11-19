import csv
from biosppy.signals import tools as st
import matplotlib.pyplot as plt
import numpy as np
import uinput
import time



if __name__ == '__main__':

    data_ch1 = []
    data_ch2 = []
    # INTERPRET EACH LINE
    #with open('2016-8-23_17-52-48.csv', 'rb') as ecg_file:
    # with open('OpenBCI-RAW-aaron_ecg_1.csv', 'rb') as ecg_file:
    with open('./../../../../Data-Repository/EOG-Data/Nov-15-2016/CSV'
              '/OpenThenCenterRightCenterLeftCycles.csv', 'rb') as \
            ecg_file:

        ecg_reader = csv.reader(ecg_file, delimiter=',')

        counter = 0

        for row in ecg_reader:
            #print(row)
            #print("\n")

            data_ch1.append(float(str(row[0])))
            data_ch2.append(float(str(row[1])))

            counter+= 1

    data_ch1_arr = np.array(data_ch1)
    data_ch2_arr = np.array(data_ch2)


    sampling_rate = 960.0  # sampling rate
    Ts = 1.0 / sampling_rate  # sampling interval
    sm_size = int(0.08 * sampling_rate) #
    t = []
    eye_left = []

    for i in range(0, len(data_ch1)):
        t.append(i*Ts)

    order = int(0.3 * sampling_rate)

    # Filter Data
    filtered_data_ch1, _, _ = st.filter_signal(signal=data_ch1_arr,
                                               ftype='FIR',
                                               band='bandpass',
                                               order=order,
                                               frequency=[2, 50],
                                               sampling_rate=sampling_rate)

    filtered_data_ch2, _, _ = st.filter_signal(signal=data_ch2_arr,
                                               ftype='FIR',
                                               band='bandpass',
                                               order=order,
                                               frequency=[2, 50],
                                               sampling_rate=sampling_rate)


    # Smooth
    filtered_data_ch1, _ = st.smoother(signal=filtered_data_ch1,
                                       kernel='hamming',
                                       size=sm_size, mirror=True)

    filtered_data_ch2, _ = st.smoother(signal=filtered_data_ch2,
                                       kernel='hamming',
                                       size=sm_size, mirror=True)

    # Peaks
    max_peaks = st.find_extrema(signal=filtered_data_ch1, mode='max')

    # Find Gestures
    for i in range(0, len(filtered_data_ch1)):
        if(i in max_peaks):
            eye_left.append(500)
        else:
            eye_left.append(0)


    # print(filtered_data)

    plt.plot(t, filtered_data_ch1, 'r')
    # plt.plot(t, filtered_data_ch2, 'b')
    # plt.plot(t, data, 'b')
    plt.xlabel("Time")
    plt.ylabel("Amplitude (V)")

    plt.show()

    # device = uinput.Device([
    #     uinput.BTN_LEFT,
    #     uinput.BTN_RIGHT,
    #     uinput.REL_X,
    #     uinput.REL_Y,
    # ])
    #
    # for i in filtered_data:
    #     device.emit(uinput.REL_X, (int) (i*10))
    #     device.emit(uinput.REL_Y, (int) (i*10))
    #     time.sleep(0.1)