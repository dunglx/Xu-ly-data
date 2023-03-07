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

throughput_path_output = ""
throughput_path_input = ""

latency_path_output = ""
latency_path_input = ""

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Ham xu ly browse Files throughput input
    def browsefiles_throughput_input():
        global throughput_path_input
        filename = filedialog.askopenfile(initialdir="/home/dunglx/Working/Performance/raw", title="Select a File", filetypes=(("Text files", "*.txt"),("Json files", "*.json"),("All files", "*.*")))
        throughput_path_input = filename
        entry_throughput_input.insert(0, throughput_path_input.name)

    def browsefiles_throughput_output():
        global throughput_path_output
        filename = filedialog.askdirectory()
        print(filename)
        throughput_path_output = filename
        # ??? dung gi cho viec hien thi duong dan output
        label_throughput_output.config(text=throughput_path_output)

    # Ham xu ly browse Files throughput input
    def browsefiles_latency_input():
        global latency_path_input
        filename = filedialog.askopenfile(initialdir="/home/dunglx/Working/Performance/raw", title="Select a File", filetypes=(("Text files", "*.txt"),("Json files", "*.json"),("All files", "*.*")))
        latency_path_input = filename
        entry_throughput_input.insert(0, latency_path_input.name)

    # Ham xu ly khi click vao button Export
    def process_throughput_input():
        global throughput_path_input
        global throughput_path_output
        a = bitrate.array('d', [0.0])  # Mbps
        b = bitrate.array('i', [0])  # seconds
        # a = []
        # b = []
        print("Ket qua da duoc ghi ra file")
        file_name = throughput_path_input.name
        filename, file_extension = os.path.splitext(file_name)
        x = filename.split('/')
        throughput_path_output_will_open = throughput_path_output
        throughput_path_output_will_open += "/"
        throughput_path_output_will_open += x[len(x) - 1]
        max_throughput = 0

        if file_extension == ".json":
            print('File json')
            with open(file_name, 'r') as f:
                data = json.load(f)
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
                max_throughput = int(numpy.max(a))
                print(max_throughput)
                throughput_path_output_will_open += "-max-"
                throughput_path_output_will_open += str(max_throughput)
                throughput_path_output_will_open += "-avg_sent-"
                throughput_path_output_will_open += str(avg_sent)
                throughput_path_output_will_open += "-avg-received-"
                throughput_path_output_will_open += str(avg_received)

                # print(a)
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
                        # Check element nao ma truoc do la MBytes sau la Mbits/sec thi lay no vao mang
                        for i in range(len(substr)):
                            if (substr[i] == "MBytes") and (substr[i + 2] == "Mbits/sec"):
                                a.append(float(substr[i+1]))
                                time += 1
                                b.append(time)
                                break
        else:
            print('Tool khong ho tro dinh dang file nay. Check lai')

        throughput_path_output_will_open += ".csv"
        print("DungLX Test ====")
        print(throughput_path_output_will_open)
        with open(throughput_path_output_will_open, 'w+') as fp:
            writer = csv.writer(fp)
            for x in a: writer.writerow([x])

        # Ve do thi
        plt.plot(b, a, 'go-')
        plt.title('Do thi throughput')
        plt.xlabel('Seconds')
        plt.ylabel('Mbps')
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

    label_tab_throughput = Label(tab_throughput, text="Xu ly ket qua test Throughput (.json, .txt, ...)")
    label_tab_throughput.pack()

    # 2.1.1 Frame input trong Tab Throughput
    frame_throughput_input = Frame(tab_throughput)
    frame_throughput_input.pack()

    label_throughput_input = Label(frame_throughput_input, text="Input: ")
    label_throughput_input.grid(row=0, column=0)

    entry_throughput_input = Entry(frame_throughput_input)
    entry_throughput_input.grid(row=0, column=1)

    button_throughput_input_explore = Button(frame_throughput_input, text="...", command=browsefiles_throughput_input)
    button_throughput_input_explore.grid(row=0, column=2)

    # 2.1.2 Frame output trong Tab Throughput
    frame_throughput_output = Frame(tab_throughput)
    frame_throughput_output.pack()

    label_throughput_output = Label(frame_throughput_output, text="Output: ")
    label_throughput_output.grid(row=0, column=0)

    label_throughput_output = Label(frame_throughput_output, text="Path to output")
    label_throughput_output.grid(row=0, column=1)

    button_throughput_output_explore = Button(frame_throughput_output, text="...", command=browsefiles_throughput_output)
    button_throughput_output_explore.grid(row=0, column=2)

    button_export = Button(tab_throughput, text="Export", command=process_throughput_input)
    button_export.pack()

    # 2.2 Tab Latency
    label_tab_latency = Label(tab_latency, text="Xu ly ket qua test Ping (.json, .txt, ...")
    label_tab_latency.pack()

    window.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# Tasks:
# 1. Thêm các check điều kiện tồn tại file hoặc đường dẫn trước khi thực thi
# 2. Thêm nút settings để cấu hình các thông tin: Đường dẫn file export, ...
# 3. Thêm nút export ra kết quả rồi cấu hình thêm tên, đường dẫn sau đó chọn OK -> Xử lý ra file kết quả
# 4. Chuyển tab trên giao diện chính cho các chức năng xử lý kết quả Throughput và Latency