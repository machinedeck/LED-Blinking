# Load the necessary libraries
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
import serial
import time

# Initialize the serial communication
serial_comm = serial.Serial("COM8", 57600, timeout = 1)
time.sleep(2)

# Initialize the main interface
interface = Tk()
bg = "gray"
interface.title("LED Blinking")
interface.config(bg = bg)
interface.geometry("270x155")

# Initiliaze the parameters for updating the plot so it is moving
# visually
# This is the time the LED is ON; half the period of a square wave
high_time = 0
reset = 0
adder = 0
stat = 1


# Check if integer function
def check(number):
    if "." in number:
        new_number = number.replace(".", "", 1)
        sum_ = 0
        for element in new_number:
            if element.isdigit() == True:
                sum_ += 0
            else:
                sum_ += 1

        if sum_ != 0:
            type_ = 0
        else:
            type_ = 1

    elif number == "":
        type_ = ""

    else:
        sum_ = 0
        for element in number:
            if element.isdigit() == True:
                sum_ += 0
            else:
                sum_ += 1

        if sum_ != 0:
            type_ = 0
        else:
            if int(number) > 1000 or int(number) < 0:
                type_ = "0-1000 ONLY"
            else:
                type_ = 2

    return type_
    
def enter(press_enter):
    global value, high_time, adder, stat
    value = text.get()
    text.delete(0, END)
    # check = 1
    now = label2.cget("text")
    # print(check, value)
    type_ = check(value)
    if type_ == 0:
        value_ = "INVALID"
    elif type_ == 1:
        value_ = "INVALID"
    elif type_ == 2:
        value_ = value
    elif type_ == "":
        value_ = ""
    elif type_ == "0-1000 ONLY":
        value_ = type_

    
    if value_ == "INVALID" or value_ == "0-1000 ONLY":
        label3.config(text = value_, fg = "red", font = ("Helvetica", 10, "bold"))
    elif type_ == 2:
        label3.config(text = value_, fg = "green2", font = ("Helvetica", 10, "bold"))
        high_time = int(value_)
        # reset = 1
        adder = 0
        stat = 1
        serial_comm.write(f'{high_time}\n'.encode())
    
text = Entry(interface, bg = "black", fg = "green", font = ("Helvetica", 25), justify = "right")
text.place(x = 20, y = 45, width = 230, height = 60)
text.bind("<Return>", enter)
# value = ""
label1 = Label(interface, bg = bg, fg = "black", font = ("Helvetica", 10), anchor = "w")
label1.place(x = 20, y = 20)
label1.config(text = "Enter value here [in ms]:")

label2 = Label(interface, bg = bg, fg = "black", font = ("Helvetica", 10), anchor = "w")
label2.place(x = 20, y = 110)

label3 = Label(interface, bg = "gray25", fg = "green2", font = ("Helvetica", 10, "bold"), anchor = "w")
label3.place(x = 162, y = 110, width = 87)
# now = text.get()
# if len(now) > 0:
#     if now == float(now):
#         if now == int(now):
#             nowint = int(now)
#             if nowint >= 0 and nowint < 1000:
#                 # value = 0
#                 check = 1
#             else:
#                 value = "INVALID"
#                 check = 1
#         else:
#             value = "INVALID"
#             check = 1
# elif now == "":
#     value = ""
#     check = 0
# else:
#     value = "INVALID"
#     check = 1

# if check == 0:
#     value_ = ""
# elif check == 1:
#     value_ = value
label2.config(text = "Current high time [ms]: ")
# label2.config(text = value)



interface_new = Toplevel(interface)
interface_new.title("Blinking Waveform")
# root.geometry()
fontsize = 9.5
fig, ax = plt.subplots(figsize = (7, 5))
x = np.linspace(0, 2000, 2000)
y = np.zeros_like(x)
line, = ax.plot(x, y, color = "limegreen", linewidth = 2)
ax.set_xlabel("Time [ms]", fontsize = fontsize)
ax.set_ylabel("Normalized Pulse", fontsize = fontsize)
ax.set_xlim(0, 2000)
ax.set_ylim(0, 1.1)
ax.set_facecolor("black")
ax.minorticks_on()
ax.tick_params(axis = "both", labelsize = fontsize)
ax.tick_params(axis = "x", labelrotation = 0, which = "major", length = 2)
ax.tick_params(which = "major", length = 7)
ax.grid(which = "major", color = "limegreen", alpha = 0.2)
ax.grid(which = "minor", color = "limegreen", alpha = 0.1, linestyle = "--")
# ax.tick_params(which = "minor", length = )
# plt.plot(x, [])
# plt.show()
canvas = FigureCanvasTkAgg(fig, master = interface_new)
canvas.get_tk_widget().pack(fill=BOTH, expand = True)

def moving_plot():
    # start_time = time.perf_counter()
    global y, adder, stat, high_time
    
    if stat == 1 and adder < high_time:
        y = np.delete(y, 0)
        y = np.append(y, 1)
        adder += 1
    elif stat == -1 and adder < high_time:
        y = np.delete(y, 0)
        y = np.append(y, 0)
        adder += 1
    elif adder != 0 and adder == high_time:
        adder = 0
        stat = -stat
    elif high_time == 0:
        y = np.delete(y, 0)
        y = np.append(y, 0)

    # if reset == 1:
    #     adder = 0
    #     stat = 1
    #     reset = 0

    # last -= 1
    # ax.plot(x, y, color = "limegreen", linewidth = 2)
    line.set_ydata(y)
    canvas.draw()
    # ax.clear()
    interface_new.after(20, moving_plot)
    # end_time = time.perf_counter()
    # print(end_time - start_time)

    # if np.sum(y) >= 100
    
# start_time = time.time()    
moving_plot()
# end_time = time.time()
# # def update_plot():
interface.mainloop()
plt.close()

serial_comm.close()
    
# text.bind("<Return>", on_enter)
# interface.mainloop()