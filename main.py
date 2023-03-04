# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import csv
import os.path
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import array as bitrate
import json
import matplotlib.pyplot as plt
import datetime
import numpy


throughput_path_output = '/home/dunglx/Working/Performance/csv/result.csv'
throughput_path_input = '/home/dunglx/Working/Performance/raw'

latency_path_output = '/home/dunglx/Working/Performance/csv/result.csv'
latency_path_input = '/home/dunglx/Working/Performance/raw'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Ham xu ly browse Files throughput input
    def browsefiles_throughput_input():
        global throughput_path_input
        filename = filedialog.askopenfile(initialdir="/home/dunglx/Working/Performance/raw", title="Select a File", filetypes=(("Text files", "*.txt"),("Json files", "*.json"),("All files", "*.*")))
        throughput_path_input = filename
        entry_throughput_input.insert(0, throughput_path_input.name)

    # Ham xu ly browse Files throughput input
    def browsefiles_latency_input():
        global latency_path_input
        filename = filedialog.askopenfile(initialdir="/home/dunglx/Working/Performance/raw", title="Select a File", filetypes=(("Text files", "*.txt"),("Json files", "*.json"),("All files", "*.*")))
        latency_path_input = filename
        entry_throughput_input.insert(0, latency_path_input.name)

    # Ham xu ly khi click vao button Export
    def export_configuration():
        # Khi click vao button Export bat len mot cua so moi de cau hinh xu ly file ket qua
        # Export window
        window_export = Toplevel(window)
        window_export.geometry("500x500")
        window_export.title("Cau hinh export")
        Label(window_export, text="This is export window").pack()

        # Frame cho cau hinh
        dir_export_frame = Frame(window_export)
        dir_export_frame.pack()
        label_dir = Label(dir_export_frame, text="Output")
        label_dir.grid(row=0, column=0)
        entry_dir = Entry(dir_export_frame)
        entry_dir.grid(row=0, column=1)
        button_dir = Button(dir_export_frame, text="...")
        button_dir.grid(row=0, column=2)

        button_process = Button(window_export, text="OK", command=process_throughput_input)
        button_process.pack()
        dir_export = filedialog.askdirectory()
        global path_csv
        path_csv = dir_export
        print(path_csv)

    def process_throughput_input():
        a = bitrate.array('d', [0.0])  # Mbps
        b = bitrate.array('i', [0])  # seconds
        # a = []
        # b = []
        print("Ket qua da duoc ghi ra file")
        file_name = path_raw.name
        filename, file_extension = os.path.splitext(file_name)
        # print(file_extension)
        if file_extension == ".json":
            print('File json')
            with open(file_name, 'r') as f:
                data = json.load(f)
                print(data)
                # Xử lý data
                intervals = data['intervals']
                # Khoi tao
                st = 0
                # Chu kỳ lấy mẫu (s): Bao lau thi lay mau 1 lan
                timeslot = 1

                for i in intervals:
                    stream = i['streams']
                    for j in stream:
                        st += 1
                        Mbps = j['bits_per_second'] / 1000000
                        if (st % timeslot) == 0:
                            a.append(Mbps)
                            b.append(st)
                end = data['end']
                sum_sent = end['sum_sent']
                avg_sent = int(sum_sent['bits_per_second'] / 1000000)
                sum_received = end['sum_received']
                avg_received = int(sum_received['bits_per_second'] / 1000000)
                sum_avg = 'avg_received:' + f'{avg_received}' + ' --- ' + 'avg_sent:' + f'{avg_sent}'
                print(sum_avg)
                print(a)
        elif file_extension == ".txt":
            # print('File text')
            with open(file_name, 'r') as fp:
                lines = fp.readlines()
                time = 0
                for line in lines:
                    if "- - - -" in line:
                        print('Exit from here')
                        break
                    else:
                        substr = line.split()
                        print(substr)
                        # Check element nao ma truoc do la MBytes sau la Mbits/sec thi lay no vao mang
                        for i in range(len(substr)):
                            print(i)
                            if (substr[i] == "MBytes") and (substr[i + 2] == "Mbits/sec"):
                                a.append(float(substr[i+1]))
                                print(substr[i+1])
                                time += 1
                                b.append(time)
                                break
                print(a)
        else:
            print('Tool khong ho tro dinh dang file nay. Check lai')

        with open(path_csv, 'w+') as fp:
            writer = csv.writer(fp)
            for x in a: writer.writerow([x])

        # Ve do thi
        plt.plot(b, a, 'go-')
        plt.title('Do thi throughput')
        plt.xlabel('Seconds')
        plt.ylabel('Mbps')
        max_throughput = numpy.max(a)
        print(max_throughput)
        x_text = (b[len(b)-1] // 2)
        y_text = (max_throughput // 2)
        current_time = datetime.datetime.now()
        plt.text(x_text, y_text - 15, current_time)
        plt.text(x_text, y_text - 30, "Max throughput: ")
        plt.text(x_text + 8, y_text - 30, max_throughput)
        plt.show()

    # 1. Tao cua so giao dien chinh
    window = Tk()
    window.title('Tool xu ly ket qua Test')
    window.geometry("500x500")
    window.config(background="white")

    # 2. Tao cac tabs tren cua so chinh
    tabsystem = ttk.Notebook(window)
    tab_throughput = Frame(tabsystem)
    tab_latency = Frame(tabsystem)

    # 2.1 Tab throughput
    tabsystem.add(tab_throughput, text="Throughput")
    tabsystem.add(tab_latency, text="Latency")
    tabsystem.pack(expand=1, fill="both")

    label_file_explorer = Label(tab_throughput, text="Xu ly ket qua test Throughput (.json, .txt, ...")
    label_file_explorer.pack()

    # 2.1.1 Frame input trong Tab Throughput
    frame_throughput_input = Frame(tab_throughput)
    frame_throughput_input.pack()

    label_throughput_input = Label(frame_throughput_input, text="Input: ")
    label_throughput_input.grid(row=0, column=0)

    entry_throughput_input = Entry(frame_throughput_input)
    entry_throughput_input.grid(row=0, column=1)

    button_throughput_explore = Button(frame_throughput_input, text="...", command=browsefiles_throughput_input)
    button_throughput_explore.grid(row=0, column=2)

    # 2.1.2 Frame output trong Tab Throughput
    frame_throughput_output = Frame(tab_throughput)
    frame_throughput_output.pack()

    label_throughput_output = Label(frame_throughput_output, text="Output: ")
    label_throughput_output.grid(row=0, column=0)

    label_throughput_output = Entry(frame_throughput_input)
    label_throughput_output.grid(row=0, column=1)

    button_throughput_explore = Button(frame_throughput_input, text="...", command=browsefiles_throughput_output)
    button_throughput_explore.grid(row=0, column=2)

    button_export = Button(tab_throughput, text="Export", command=export_configuration)
    button_export.pack()

    # 2.2 Tab Latency

    window.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# Tasks:
# 1. Thêm các check điều kiện tồn tại file hoặc đường dẫn trước khi thực thi
# 2. Thêm nút settings để cấu hình các thông tin: Đường dẫn file export, ...
# 3. Thêm nút export ra kết quả rồi cấu hình thêm tên, đường dẫn sau đó chọn OK -> Xử lý ra file kết quả
# 4. Chuyển tab trên giao diện chính cho các chức năng xử lý kết quả Throughput và Latency