from scipy import signal
# from scipy.signal import tukey, hamming, hanning
import streamlit as st
import numpy as np
import pandas as pd
import os
import plotly.graph_objs as go
from scipy.fftpack import fft, ifft

# title
st.sidebar.title("Stamping Model V1")
select_tool_btn = st.sidebar.selectbox("Choose tool",
                                       ("Signal Analysis", "Envelope Line", "PCA-T2", "Isolation Forest"))

# base = r"G:\sssssss\2020-5-20数据"
base = r"."


# base = r"C:\Users\liu\Desktop\daq_model_06_01_14_43\daq_model"

@st.cache(suppress_st_warning=True)
def load_data(select_file_btn):
    st.write("loading...")
    df = pd.read_csv(select_file_btn, usecols=[1])
    return df


@st.cache(suppress_st_warning=True)
def get_filter_data(data, filter_fs, fs=51200):
    st.write("filtering...")
    b, a = signal.butter(4, 2 * int(filter_fs) / fs, "lowpass")
    filter_data = signal.filtfilt(b, a, data)
    return filter_data


@st.cache(suppress_st_warning=True)
def get_frequency_data(data, fs):
    st.write("fast fft...")
    n = data.size
    NFFT = int(np.power(2, np.ceil(np.log2(n)) + 4))  # 下一个最近二次幂
    fft_y = fft(data, NFFT) / NFFT
    fft_x = fs / 2 * np.linspace(0, 1, NFFT / 2 + 1)

    return fft_x, 2 * abs(fft_y[:int(NFFT / 2 + 1)])


@st.cache(suppress_st_warning=True)
def get_windowed_data(filter_data):
    st.write("windowed...")
    pass


@st.cache(suppress_st_warning=True)
def get_peak_and_cut(filter_data, signal_height=0.02, signal_width=600, cut_length=2000):
    st.write("Peak...")
    peakind = signal.find_peaks(filter_data, height=signal_height, width=signal_width)
    if peakind[0].size > 0:
        # 峰值
        idx = peakind[0][-1]
    else:
        # 最大值
        idx = np.argmax(filter_data)

    cut_sig = filter_data[idx - cut_length:idx + cut_length]
    return cut_sig, idx


# @st.cache(suppress_st_warning=True)
def self_plot1(fig, fig1, data):
    fig.add_trace(
        go.Scatter(x=np.arange(data.size), y=data,
                   mode='lines')
    )
    # plot Frequency
    fft_x, fft_y = get_frequency_data(data, fs=int(fs))
    fig1.add_trace(
        go.Scatter(x=fft_x, y=fft_y,
                   mode='lines')
    )
    fig.update_layout(title_text="Time Domain",
                      title_font_size=20)
    fig1.update_layout(title_text="Frequency Domain",
                       title_font_size=20)
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(fig1, use_container_width=True)


# @st.cache(suppress_st_warning=True)
def self_plot2(fig, fig1, fig2, data, data1, idx):
    fig.add_trace(
        go.Scatter(x=[idx], y=[data[idx]])
    )
    fig.add_trace(
        go.Scatter(x=np.arange(data.size), y=data,
                   mode='lines')
    )
    fig1.add_trace(
        go.Scatter(x=np.arange(data1.size), y=data1,
                   mode='lines')
    )
    # plot Frequency
    fft_x, fft_y = get_frequency_data(data, fs=int(fs))
    fig2.add_trace(
        go.Scatter(x=fft_x, y=fft_y,
                   mode='lines')
    )
    fig.update_layout(title_text="Time Domain",
                      title_font_size=20)
    fig1.update_layout(title_text="Cut Signal",
                       title_font_size=20)
    fig2.update_layout(title_text="Frequency Domain",
                       title_font_size=20)
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)


def self_plot3(fig, fig1, fig2, data, tukey, alpha):
    fig.add_trace(
        go.Scatter(x=np.arange(tukey.size), y=tukey,
                   mode='lines')
    )
    win_data = tukey * data
    fig1.add_trace(
        go.Scatter(x=np.arange(data.size), y=data,
                   mode='lines')
    )
    fig2.add_trace(
        go.Scatter(x=np.arange(win_data.size), y=win_data,
                   mode='lines')
    )
    fig.update_layout(title_text="TuKey Window (alpha=" + str(alpha) + ")",
                      title_font_size=20)
    fig1.update_layout(title_text="Cut Signal",
                       title_font_size=20)
    fig2.update_layout(title_text="Cut Signal * TuKey",
                       title_font_size=20)
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)


@st.cache
def get_csv_sort_file(base, select_floder_btn, full_name=False):
    file_list = os.listdir(
        os.path.join(base, select_floder_btn)
    )
    csv_file = [f for f in file_list if ".csv" in f]
    csv_file.sort(
        key=lambda x: -os.path.getmtime(os.path.join(base, select_floder_btn, x))
    )

    if full_name:
        csv_file = [os.path.join(base, select_floder_btn, f) for f in csv_file]
    else:
        csv_file = [
            i + "  (" + str(round(os.path.getsize(os.path.join(base, select_floder_btn, i)) / 1024 / 1024, 2)) + 'MB)'
            for i in csv_file]
    return csv_file


@st.cache(suppress_st_warning=True)
def load_all_data(files):
    data = {file.split('\\')[-1]: pd.read_csv(file, usecols=[1]).iloc[:, 0][:51200 * 2] for file in files}
    # st.dataframe(pd.DataFrame(data))
    return pd.DataFrame(data)
    # os.path.join(base, select_floder_btn, select_file_btn.split(" ")[0]


@st.cache(suppress_st_warning=True)
def self_all_plot(fig, all_data):
    st.write("plot all...")
    for data in all_data.iteritems():
        fig.add_trace(
            go.Scatter(x=np.arange(data[1].size), y=data[1],
                       mode='lines', showlegend=True)
        )
    fig.update_layout(title_text="Time Domain",
                      title_font_size=20)
    return fig


if select_tool_btn == "Signal Analysis":
    # choose file
    st.sidebar.subheader(select_tool_btn)
    st.header(select_tool_btn)
    # base = r"G:\sssssss\2020-5-20数据"
    # base = r"G:\edgebox_pro\edgebox_final"
    # base = r"C:\Users\liu\Desktop\daq_model_06_01_14_43\daq_model"
    floder = [f for f in os.listdir(base) if "." not in f]
    select_floder_btn = st.sidebar.selectbox("WorkStaion : " + base, floder)
    if select_floder_btn:
        csv_file = get_csv_sort_file(base, select_floder_btn)
        select_file_btn = st.selectbox("Select CSV File", csv_file)
        if select_file_btn:

            df = load_data(os.path.join(base, select_floder_btn, select_file_btn.split(" ")[0]))
            Func = st.sidebar.multiselect("Function Box",
                                          ["低通濾波", "信号截取", "信号加窗"], )
            fs = st.sidebar.number_input("Sample Frequency", value=51200, max_value=100000, min_value=25600, step=1000)

            fig = go.Figure()  # 时域信号
            fig1 = go.Figure()  # 频域信号
            fig2 = go.Figure()  # 窗信号
            if len(Func) >= 1 and Func[0] == "低通濾波":
                Filter_fs = st.sidebar.number_input("Cut-off Frequency", max_value=5000, min_value=100, step=100)
                filter_data = get_filter_data(df.iloc[:, 0], Filter_fs, fs=int(fs))
                # data = filter_data[:]
                if len(Func) == 1:
                    self_plot1(fig, fig1, filter_data)

                if len(Func) >= 2 and Func[1] == "信号截取":
                    # 信号截取
                    signal_height = st.sidebar.number_input("Signal Height", value=0.02, max_value=10.,
                                                            min_value=0.0001, step=0.01)
                    signal_width = st.sidebar.number_input("Signal Width", value=600, max_value=2000, min_value=100,
                                                           step=100)
                    cut_length = st.sidebar.number_input("Cut Length", value=2000, max_value=5000, min_value=200,
                                                         step=100)
                    data, idx = get_peak_and_cut(filter_data, signal_height=signal_height, signal_width=signal_width,
                                                 cut_length=cut_length)
                    if len(Func) == 2:
                        self_plot2(fig, fig1, fig2, filter_data, data, idx)
                    if len(Func) >= 3 and Func[2] == "信号加窗":
                        alpha = st.sidebar.slider("Tukey alpha", max_value=1.0, min_value=0., value=0.75, step=0.1)
                        tukey = signal.windows.tukey(cut_length * 2, alpha=alpha)
                        self_plot3(fig, fig1, fig2, data, tukey, alpha)

            else:
                data = df.iloc[:, 0]
                # Time
                fig.add_trace(
                    go.Scatter(x=np.arange(data.size), y=data,
                               mode='lines')
                )
                # Frequency
                fft_x, fft_y = get_frequency_data(data, fs=int(fs))
                fig1.add_trace(
                    go.Scatter(x=fft_x, y=fft_y,
                               mode='lines')
                )
                fig.update_layout(title_text="Time Domain",
                                  title_font_size=20)
                fig1.update_layout(title_text="Frequency Domain",
                                   title_font_size=20)
                st.plotly_chart(fig, use_container_width=True)
                st.plotly_chart(fig1, use_container_width=True)

elif select_tool_btn == "Envelope Line":
    st.sidebar.subheader(select_tool_btn)
    st.header(select_tool_btn)
    # base = r"G:\sssssss\2020-5-20数据"
    floder = [f for f in os.listdir(base) if "." not in f]
    select_floder_btn = st.sidebar.selectbox("WorkStaion : " + base, floder)
    if select_floder_btn:
        fig = go.Figure()
        csv_file = get_csv_sort_file(base, select_floder_btn, full_name=True)
        all_data = load_all_data(csv_file[:15])
        fig = self_all_plot(fig, all_data)
        st.plotly_chart(fig, use_container_width=True)
        st.selectbox("Next", (1, 2, 3,))
        st.write()
        test_file = st.sidebar.file_uploader("Chosse a CSV file", type="csv")



elif select_tool_btn == "PCA-T2":
    st.sidebar.subheader(select_tool_btn)
    st.header(select_tool_btn)

elif select_tool_btn == "Isolation Forest":
    st.sidebar.subheader(select_tool_btn)
    st.header(select_tool_btn)
