import tkinter as tk
from tkinter import simpledialog
import cv2
import os
import PIL.Image, PIL.ImageTk
import camera
import model

class App:
    def __init__(self, window=tk.Tk(), window_title="Group 10 camera classifier"):
        self.window = window
        self.window_title = window_title
        self.window.configure(bg='#577399')
        self.counters=[1, 1]
        self.model = model.Model()
        self.auto_predict = False
        self.camera = camera.Camera()
        self.init_gui()
        self.delay=10
        self.update()
        #self.window.attributes('-topmost', True)
        self.window.attributes(True)
        self.window.mainloop()

    def init_gui(self):
        self.canvas = tk.Canvas(self.window, width = self.camera.width, height = self.camera.height)
        self.canvas.pack()

        self.btn_toggleauto= tk.Button(self.window, text="Auto Prediction",bg="#f7f7ff", width= 50, command=self.auto_predict_toggle, borderwidth=1, relief="raised", padx=5, pady=5)
        self.btn_toggleauto.pack(anchor=tk.CENTER, expand = True)

        self.classname_one = simpledialog.askstring("class name One", "Enter the name of the first class:", parent =self.window)
        self.classname_two = simpledialog.askstring("class name Two", "Enter the name of the Second class:", parent =self.window)

        self.btn_class_one = tk.Button(self.window, text = self.classname_one, width= 50, command = lambda: self.save_for_class(1), borderwidth=1, relief="raised", padx=5, pady=5)
        self.btn_class_one.pack(anchor=tk.CENTER, expand= True)

        self.btn_class_two = tk.Button(self.window, text = self.classname_two, width= 50, command = lambda: self.save_for_class(2), borderwidth=1, relief="raised", padx=5, pady=5)
        self.btn_class_two.pack(anchor=tk.CENTER, expand= True)

        self.btn_train = tk.Button(self.window, text= "Train Model", bg="#f7f7ff", width=50, command= lambda: self.model.train_model(self.counters), borderwidth=1, relief="raised", padx=5, pady=5)
        self.btn_train.pack(anchor=tk.CENTER, expand= True)

        self.btn_predict = tk.Button(self.window, text= "Predict", bg="#f7f7ff", width=50, command=self.predict, borderwidth=1, relief="raised", padx=5, pady=5)
        self.btn_predict.pack(anchor=tk.CENTER, expand= True)

        # self.btn_reset = tk.Button(self.window, text="Reset", bg="#f7f7ff", width= 50, command=self.reset, borderwidth=1, relief="raised", padx=5, pady=5)
        # self.btn_reset.pack(anchor=tk.CENTER, expand= True)

        self.class_label = tk.Label(self.window, text= "Objects")
        self.class_label.config(font=("sans serif", 10))
        self.class_label.pack(anchor=tk.CENTER, expand= True)


    def auto_predict_toggle(self):
        self.auto_predict = not self.auto_predict

    def save_for_class(self, class_num):
        ret, frame = self.camera.get_frame()
        if not os.path.exists('1'):
            os.mkdir('1')
        if not os.path.exists('2'):
            os.mkdir('2')
        
        cv2.imwrite(f"{class_num}/frame{self.counters[class_num-1]}.jpg",cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY))
        img = PIL.Image.open(f"{class_num}/frame{self.counters[class_num-1]}.jpg")
        img.thumbnail((150, 150), PIL.Image.ANTIALIAS)
        img.save(f"{class_num}/frame{self.counters[class_num-1]}.jpg")

        self.counters[class_num-1] += 1

    # def reset(self):
    #     for directory in ['1', '2']:
    #         for file in os.listdir(directory):
    #             file_path = os.path.join(directory, file)
    #             if os.path.isfile(file_path):
    #                 os.unlink(file_path)

    #     self.counters= [1, 1]
    #     self.model = model.Model()
    #     self.class_label.config(text = 'CLASS')
    
    def update(self):
        if self.auto_predict:
            self.predict()

        ret, frame = self.camera.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0,image=self.photo, anchor = tk.NW)

        self.window.after(self.delay, self.update)

    def predict(self):
        frame = self.camera.get_frame()
        prediction = self.model.predict(frame)
       

        if prediction == 1:
            self.class_label.config(text= self.classname_one)
            return self.classname_one
        elif prediction == 2:
            self.class_label.config(text= self.classname_two)
            return self.classname_two
        








