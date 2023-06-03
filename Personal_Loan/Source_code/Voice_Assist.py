import speech_recognition as BDNhan59_sr
from gtts import gTTS
import playsound
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import customtkinter as customTK
from G4_59BDNhan_Topic import EDA
import G4_59BDNhan_Topic as tp

'''Dictionary of Command'''
eda = EDA()
cmd_dict = {
    'lấy dữ liệu mẫu': eda.get_sampled,
    'lấy hình dạng bảng': eda.get_shaped,
    'lấy mô tả': eda.get_statvl,
    'xóa cột': eda.remove_cols,
    'lấy dữ liệu gốc': eda.load_data
}

'''Lớp trợ lý '''
class Voice_Assits:
    def __init__(self):
        self.prot = customTK.CTk()
        self.prot.geometry("1000x500")
        self.txtKetqua = Text(self.prot, width=500, height=300, pady=0)
        self.txtKetqua.grid(row=1, column=0, padx=8, pady=0)

    def read_out_loud(_, text):
        source = gTTS(text='Kết quả của '+text, lang = 'vi')
        #Mở hộp thoại askstring để điền tên file
        filename = simpledialog.askstring(title="Save tên file mp3", prompt="Vui lòng nhập tên:")
        #Lưu file với đường dẫn
        source.save(filename)
        #Phát âm thanh từ file mp3 vừa lưu
        playsound.playsound('D:/Education/Giáo trình/Python Programming/G4_59_BDNhan_DAHP.PyPro_Topic/'+filename)
    
    def void_assist(self):
        """Hàm nhận diện giọng nói

        Returns:
            string: kết quả của ghi âm
        """        
        BDNhan59_rec = BDNhan59_sr.Recognizer()
        with BDNhan59_sr.Microphone() as source:
            BDNhan59_rec.adjust_for_ambient_noise(source, duration=1)
            ask = messagebox.askokcancel(title="Thông báo", message="Bấm OK để bắt đầu ghi âm lệnh bằng tiếng Việt, trong 5s")
            #Nếu ask == True => đã nhấn OK, sẽ bắt đầu ghi âm, ngược lại thì hoãn ghi âm
            if ask:
                audio_data = BDNhan59_rec.record(source, duration=5)
                try:
                    # recognize_google: nhận diện giọng nói từ google, với ngôn ngữ là Vietnammese
                    text = BDNhan59_rec.recognize_google(audio_data,language='vi')
                    # Dùng dictionary
                    if text == 'xóa cột':
                        kq = cmd_dict[text](tp.lst)
                        tp.lst = []
                    else:
                        kq =cmd_dict[text]()
                except:
                    # Trường hợp không ghi âm được giọng nói
                    text = "Bạn nói gì, mình không hiểu"
                    kq = "Không thực hiện được câu lệnh"
                # gọi hàm phát âm thanh từ file .mp3
                self.read_out_loud(text)
                return kq, text
            
    def text_assist(self, command):
        if command.strip() in cmd_dict:
            try:
                # recognize_google: nhận diện giọng nói từ google, với ngôn ngữ là Vietnammese
                text = command
                if text == 'xóa cột':
                    kq = cmd_dict[text](tp.lst)
                    tp.lst = []
                else:
                    kq =cmd_dict[text]()
            except:
                # Trường hợp không ghi âm được giọng nói
                text = "Bạn ghi gì, mình không hiểu"
                kq = "Không thực hiện được câu lệnh"
            # self.read_out_loud(text)
            return kq, text
        messagebox.showinfo("Cảnh báo", "Câu lệnh không hợp lệ!")

