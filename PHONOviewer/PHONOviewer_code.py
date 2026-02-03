import tkinter as tk
from tkinter import filedialog
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime


#Starting with the widgets on the GUI
Patient_Name = "Not Given"
Patient_Dob = "Not Given"
Patient_Hospital_Number = "Not Given"
#Array to hold patient details
Patient_details_array = [Patient_Name, Patient_Dob, Patient_Hospital_Number]
#address of the audio file:
Audio_Address = ""
#Address to save files in, I.e, the PNG Spectogram, and PDF report
Output_Address = ""
#Length of the sample audio selected:
sample_lenght = 0.0
#Address of the Spect graph picture (once saved)
Spect_address = ""
#Address of the fourier transform picture (once saved)
fourier_address = ""
#current time calculator:
#current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

#creating new text to confirm patient detals have been submitted.
def Confirm_details_trigger():
    Details_submitted = "Patient Details remembered!"
    Confirm_Patient_Submission = tk.Label(root, text=Details_submitted, font=("Arial", 12), background="#D3D3D3")
    Confirm_Patient_Submission.place(x = 270, y = 120)
    save_patient_details_check(Patient_Name_widget.get(), Patient_Dob_widget.get(), Patient_Hospital_Number_widget.get())

#This function takes in the output of the widgets, and reassigns the global variables for patient name, DOB and Hospital Number. Note: this is a hacker's wet dream, must be changed in final version to be more secure.
def save_patient_details_check(Name, DOB, Hospital_Number):
    global Patient_Name
    global Patient_Dob
    global Patient_Hospital_Number
    global Patient_details_array
    Patient_Name = Name
    Patient_Dob = DOB
    Patient_Hospital_Number = Hospital_Number
    Patient_details_array.clear()
    Patient_details_array.append(Patient_Name)
    Patient_details_array.append(Patient_Dob)
    Patient_details_array.append(Patient_Hospital_Number)
    return Patient_details_array

def generate_spectrogram(file_path):
    sample_rate, data = wavfile.read(file_path)
    ####### IM GONNA ASSUME ITS A MONO SIGNAL
    global sample_lenght
    sample_lenght = (len(data) / sample_rate)
    if len(data.shape) == 2:
        data = data[:, 0]
    plt.figure(figsize=(10, 4))
    plt.specgram(data, Fs=sample_rate, NFFT=1024, noverlap=512, cmap='inferno')
    plt.title("Spectrogram")
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    plt.colorbar(label='Intensity [dB]')
    plt.tight_layout()
    plt.savefig(Output_Address)
    plt.savefig(Output_Address+"/Spectrogram_Plot_Sonography.png")
    if Weird_tkinter_variable.get() == 1:
        plt.show()
        
#Generate the fourier transform
def generate_ft(file_path):
    sample_rate, data = wavfile.read(file_path)
    if len(data.shape) == 2:
        data = data[:, 0]
    if data.dtype != np.float32:
        data = data / np.max(np.abs(data))
    fft_data = np.fft.rfft(data)
    freqs = np.fft.rfftfreq(len(data), d=1/sample_rate)
    magnitude = np.abs(fft_data)
    plt.figure(figsize=(10, 4))
    plt.plot(freqs, magnitude, color='darkgreen')
    plt.title("Fourier Transform (Frequency Spectrum)")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(Output_Address+"/Fourier_Plot_Sonography.png")
    if Weird_tkinter_variable.get() == 1:
        plt.show()

#Function to browse for a .wav file, connected to the browse button for the heartbeat recording
def browse_file_Audio(Addy):
    global Audio_Address
    if len(Addy) > 0:
        label3 = tk.Label(root, text="                                                                ", background="#D3D3D3", font=("Arial", 12))
        label3.place(x=50, y=230)
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")], title="Select a .wav to analyse")
        if file_path:
            Audio_Address = file_path
            generate_spectrogram(file_path)
            generate_ft(file_path)
            create_report()
    else:
        label3 = tk.Label(root, text="Select an output destination first!", background="#D3D3D3", font=("Arial", 12), fg="red" )
        label3.place(x=50, y=230)

#Function to browse for the output destination, connected to the browse button where to save the PDF
def browse_file_Output():
    global Output_Address
    file_path = filedialog.askdirectory(title="Select directory to save output report destination")
    if file_path:
        Output_Address = file_path
    #print(Output_Address)

#Generation of report function
def create_report():
    report = FPDF()
    report.add_page()
    report.set_font("Arial", size=12)
    report.image(Output_Address+"/Spectrogram_Plot_Sonography.png", x=10, y=10, w=180)
    report.image(Output_Address+"/Fourier_Plot_Sonography.png", x=10, y=80, w=180)
    report.set_xy(10, 100+50)
    report.cell(0, 10, "Patient Name: " + Patient_details_array[0])
    report.set_xy(10, 110+50)
    report.cell(0, 10, "Date of Birth: " + Patient_details_array[1])
    report.set_xy(10, 120+50)
    report.cell(0, 10, "Hospital Number: " + Patient_details_array[2])
    report.set_xy(10, 130+50)
    report.cell(0, 10, "Length of sample in seconds: " + str(sample_lenght))
    report.output(Output_Address+"/" + datetime.now().strftime("%Y-%m-%d %H-%M-%S") +" Sonography Report.pdf" )
    Successful_Generation_prompt = tk.Label(root, text="Report successfully saved to " + Output_Address + " at\n" + datetime.now().strftime("%Y-%m-%d %H-%M-%S"), font=("Arial", 8), background="#D3D3D3", fg="red")
    Successful_Generation_prompt.place(x=50, y=350)

root = tk.Tk()    #initialise the GUI, root = class constructor
#Create some basic GUI  setting in the background
root.title("Heart sound recordings visualisation application")
root.configure(background="#D3D3D3")
root.minsize(800, 400)
root.maxsize(800, 400)
root.geometry("400x400+50+50")

#Information on how to use the Sonograph
Header_label = "This application analyses the length of an uploaded recording and produces a spectrogram and fourier transform plot \n designed to aid analysis of digital recordings of heart sounds. Please note that this is a test version of the program. \nThe output from this program is not to be used for clinical decision making. "
Patient_detail_label = "          Patient Name                          Patient DOB XX/XX/XXXX    Patient Hospital Number"

Header_title = tk.Label(root, text=Header_label, font=("Arial", 10), background="#D3D3D3")
Header_title.place(x=40, y=0)

Info_about_Textboxes = tk.Label(root, text=Patient_detail_label, font=("Arial", 12), background="#D3D3D3")
Info_about_Textboxes.place(x=10, y=65)

#Creating input box widgets
Patient_Name_widget = tk.Entry(root, width=30)
Patient_Dob_widget = tk.Entry(root, width=30)
Patient_Hospital_Number_widget = tk.Entry(root, width=30)

#Telling the widgets where to go
Patient_Name_widget.place(x=20+30,y=90)
Patient_Dob_widget.place(x=20+200+30,y=90)
Patient_Hospital_Number_widget.place(x=20+200+200+30,y=90)

#Creating a submit button
submit_btn = tk.Button(root, text="Submit Patient Details", command=Confirm_details_trigger)
submit_btn.place(x=50, y=120)

#Create a button to browse for a .wav (And label it, with the next 5 lines)
label = tk.Label(root, text="Select a .wav file to analyse and create the report in the defined directory:", background="#D3D3D3", font=("Arial", 12))
label.place(x=50, y=270)

browse_btn1 = tk.Button(root, text="Browse", command=lambda:browse_file_Audio(Output_Address))
browse_btn1.place(x=50, y=295)

#Creating an instructions sheet:
Instructions_label = tk.Label(root, text="INSTRUCTIONS:\nStep 1:\n Enter patient details.\n\nStep 2:\n Select output destination.\n\nStep 3:\n Select a .wav file & a\nreport will be generated\nautomatically.", background="#D3D3D3", font=("Arial", 12), fg="salmon")
Instructions_label.place(x=600, y=130)

#Create an address to save and output to.
label2 = tk.Label(root, text="Select a save destination for the output report:", background="#D3D3D3", font=("Arial", 12))
label2.place(x=50, y=170)

browse_btn2 = tk.Button(root, text="Browse", command=browse_file_Output)
browse_btn2.place(x=50, y=200)

#Creating a checkbox for to check if the user wants an output 
#variable needs to be the tkinter version of an int, since the mainloop will ensure its constantly updated while running.
Weird_tkinter_variable = tk.IntVar() 
# 0 = unchecked, 1 = checked
Checkbox_4_Graphs = tk.Checkbutton(root, text="Show output graphics before saving report", variable=Weird_tkinter_variable, background="#D3D3D3")
Checkbox_4_Graphs.place(x=120, y=295)

root.mainloop() #loops over & updates if the user clicks anything. Don't remove