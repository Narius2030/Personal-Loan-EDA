'''Thư viện cho GUI (winform)'''
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from tkinter import simpledialog
import customtkinter as customTK
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Voice_Assist import Voice_Assits
from G4_59BDNhan_Topic import EDA
import G4_59BDNhan_Topic as tp
from G4_Pre_Att_59BDNhan import SELECTCOL
from G4B14EX7_Game_59BDNhan import play_game

customTK.set_appearance_mode("Light")
customTK.set_default_color_theme("blue")

class FGUI:
    '''Đối tượng'''
    bot = Voice_Assits()
    eda = EDA()
    eda.load_data()
    '''Form'''
    root = customTK.CTk()
    '''Frame'''
    fKetqua = Frame(root)
    fTTcol = Frame(root)
    '''TextBox'''
    txtKetQua59 = Text(fKetqua, width=128, height=28, border=4)
    txtChiSoK = Text(fTTcol, width=20, height=1, border=4)
    txtBoundzc = Text(fTTcol, width=20, height=1, border=4)
    
    txtSelectedCols = Text(fTTcol, width=20, height=12, border=4)
    '''Combobox'''
    cboOutput = ttk.Combobox(fTTcol, values=None)
    '''Menu bar'''
    menubar = Menu(root)
    '''Label'''
    lblChiSoK = tk.Label(fTTcol, text="Số k/giá trị tương quan ngưỡng")
    lblOutputAttr = tk.Label(fTTcol, text="Thuộc tính output")
    lblBoundzc = tk.Label(fTTcol, text="Mức zscore ngưỡng")
    lblSelectedCols = tk.Label(fTTcol, text="Thuộc tính đang chọn")
    '''Button'''
    btnDlCol = Button(fTTcol, text = "Delete Attributes", width = 23, background='red', fg='white')
    btnRLCol = Button(fTTcol, text = "Reload Selected Attributes", width = 23, background='blue', fg='white')
    
    '''Tree view'''
    tree = ttk.Treeview(root, show="headings")
    # Create the Treeview widget with the specified columns
    child_tree = ttk.Treeview(root, show="headings", height=5)  # columns=eda.df59.columns.to_list()
    '''Style of treeview'''
    style = ttk.Style(root)
    style.theme_use("alt")
    style.configure('Treeview',background="white",rowheight=30,foreground="black",font=("Arial", 10))
    style.map('Treeview',background=[('selected','blue')])
    style.configure('Treeview.Heading', font=("Arial", 10, "bold"))
    
    def __init__(self):
        self.root.geometry("1280x640")
        self.root.resizable(tk.FALSE, tk.FALSE)
        self.canvas = FigureCanvasTkAgg()
        self.fKetqua.place(x=20, y=150)
        self.fTTcol.place(x=1350, y =15)
        
        '''Button'''
        self.btnDlCol.grid(row=8, column=0, pady=10)
        self.btnDlCol.config(command=self.btndeleteAttr_clicked)
        self.btnRLCol.grid(row=9, column=0, pady=10)
        self.btnRLCol.config(command=self.show_selectedcol)
        
        '''Label'''
        self.lblChiSoK.grid(row=2, column=0)
        self.lblOutputAttr.grid(row=4, column=0)
        self.lblBoundzc.grid(row=0, column=0)
        self.lblSelectedCols.grid(row=6, column =0)
        
        '''Text'''
        self.txtChiSoK.grid(row=3, column=0)
        self.txtBoundzc.grid(row=1, column=0)
        self.txtSelectedCols.grid(row=7, column=0)
        
        '''Combobox'''
        self.cboOutput.grid(row=5, column=0)
        self.cboOutput.config(values=self.eda.df59.columns.to_list())
        
        '''Menu bar'''
        #Xử lý dữ liệu
        self.DPmenu = Menu(self.menubar, tearoff=0)
        self.DPmenu.add_command(label="Lay du lieu goc", command=self.ldg_clicked)
        self.DPmenu.add_command(label="Lay du lieu mau", command=self.ldlm_clicked)
        self.DPmenu.add_command(label="Kiem tra NULL", command=self.ktnull_clicked)
        self.DPmenu.add_command(label="Lay mo ta", command=self.lmt_clicked)
        self.DPmenu.add_command(label="Xu ly gia tri Null", command=self.btnremovenull_clicked)
        self.DPmenu.add_command(label="Ma tran zscore", command=self.btnmat_zscore_clicked)
        self.DPmenu.add_command(label="Loai du lieu theo zscore", command=self.btnfillter_zscore_clicked)
        self.DPmenu.add_command(label="Chon thuoc tinh", command=self.btnChonAttr_clicked)
        
        #Phân tích EDA
        self.DAmenu = Menu(self.menubar, tearoff=0)
        self.DAmenu.add_command(label="Chuẩn hóa rời rạc - MinMaxScaler", command=self.btnChrr_clicked)
        self.DAmenu.add_command(label="Xác định thuộc tính đặc trưng bằng chi2", command=self.btnfeatureselect_chi2_clicked)
        self.DAmenu.add_command(label="Xác định thuộc tính đặc trưng bằng Correlation", command=self.btnfeatureselect_corr_clicked)
        self.DAmenu.add_command(label="Xác định mô hình trích lọc", command=self.btnXdMh_TrichLoc_clicked)
        
        #Trợ lý ảo
        self.VAmenu = Menu(self.menubar, tearoff=0)
        self.VAmenu.add_command(label="Voice assistant", command=self.btnrecord_assit_clicked)
        self.VAmenu.add_command(label="Text assistant", command=self.btntext_assit_clicked)
        
        #Vẽ biểu đồ zscore
        self.DGmenu = Menu(self.menubar, tearoff=0)
        self.DGmenu.add_command(label="Biểu đồ z-score bằng scatter", command=self.draw_zscore_graph)
        self.DGmenu.add_command(label="Biểu đồ heatmap", command=self.draw_heatmap_graph)
        self.DGmenu.add_command(label="Biểu đồ biểu diễn độ biến thiên thuộc tính", command=self.draw_bienthien_graph)
        
        # Giải trí
        self.Game = Menu(self.menubar, tearoff=0)
        self.Game.add_command(label="Đua xe", command=self.btngame_clicked)
        
        #Them menu con vao menu cha
        self.menubar.add_cascade(label="Xử lý dữ liệu", menu=self.DPmenu)
        self.menubar.add_cascade(label="Phân tích dữ liệu", menu=self.DAmenu)
        self.menubar.add_cascade(label="Trợ lý ảo", menu=self.VAmenu)
        self.menubar.add_cascade(label="Vẽ biểu đồ", menu=self.DGmenu)
        self.menubar.add_cascade(label="Giải trí", menu=self.Game)
        
        '''Table of checking'''
        # self.show_check(self.eda.df59)
        
        '''Vòng lặp Form'''
        self.root.config(menu=self.menubar)
        self.root.mainloop()

    '''Hàm tiền xử lý'''
    def ldg_clicked(self):
        self.destroy_widgets()
        self.eda.load_data()
        self.cboOutput.config(values=self.eda.df59.columns.to_list())
    
    def ldlm_clicked(self):
        self.destroy_widgets()
        res = self.eda.get_sampled()
        self.load_data_to_treeview(res)
        self.show_check(self.eda.df59)
    
    def lmt_clicked(self):
        self.destroy_widgets()
        res = self.eda.get_statvl()
        self.load_data_to_treeview(res)
        self.show_check(self.eda.df59)
        
    def ktnull_clicked(self):
        self.destroy_widgets()
        res = self.eda.check_isnan()
        self.show_result(res)
        self.show_check(self.eda.df59)
    
    def btndeleteAttr_clicked(self):
        self.eda.remove_cols(tp.lst)
        messagebox.showinfo('info', 'Đã xóa thuộc tính')
        tp.lst = []
        self.destroy_widgets()
        self.cboOutput.config(values=self.eda.df59.columns.to_list())
        self.show_check(self.eda.df59)
        
    def btnChonAttr_clicked(self):
        fdelcol = SELECTCOL(self.eda.df59.columns)
        self.show_check(self.eda.df59)
        
    def btnmat_zscore_clicked(self):
        self.destroy_graph()
        self.destroy_txtKetqua()
        res = self.eda.mat_zscore()
        self.load_data_to_treeview(res)
        self.show_check(self.eda.df59)
    
    def btnremovenull_clicked(self):
        selection = simpledialog.askstring(title="Thông báo", prompt="Chọn kiểu xử lý giá trị Null\n1. Xóa các dòng có giá trị Null\n2. Thay thế giá trị Null bằng giá trị phổ biến\nNhập số: ")
        if selection:
            if selection == '1':
                self.eda.nanpros_dropna()
            elif selection == '2':
                self.eda.nanpros_dropna()
            else:
                messagebox.showerror('Error', 'Lựa chọn không hợp lệ')
    
    def btnfillter_zscore_clicked(self):
        self.destroy_widgets()
        res = self.eda.fillterdf_zscore(self.txtBoundzc.get(0.0, END).strip())
        if res:
           temp = f'Đã loại thành công\n{self.eda.get_shaped()}' 
        else:
            temp = f'Loại không thành công\n{self.eda.get_shaped()}'
        self.show_result(temp)
        self.show_check(self.eda.df59)
    
    '''Hàm lấy kết quả phân tích'''
    def btnChrr_clicked(self):
        self.destroy_graph()
        self.destroy_txtKetqua()
        res = self.eda.chrr_minmaxscaler()
        if res:
            self.load_data_to_treeview(self.eda.df59)
        else:
            self.show_result('Chuẩn hóa không thành công\n\n\n')
    
    def btnfeatureselect_chi2_clicked(self):
        self.destroy_widgets()
        res = self.eda.xd_attr_dactrungchi2(tp.lst, self.cboOutput.get().strip(), self.txtChiSoK.get(0.0, END).strip())
        self.show_result(res)
        tp.lst = []
    
    def btnfeatureselect_corr_clicked(self):
        self.destroy_widgets()
        res = self.eda.xd_attr_dactrungcor(self.cboOutput.get().strip(), self.txtChiSoK.get(0.0, END).strip())
        self.show_result(res)
    
    def btnXdMh_TrichLoc_clicked(self):
        tp.lst.append(self.cboOutput.get().strip())
        res = self.eda.xd_mohinh_trichloc(tp.lst)
        self.show_result(res)
    
    '''Trợ lý ảo'''
    def btnrecord_assit_clicked(self):
        self.destroy_widgets()
        res = self.bot.void_assist()
        self.show_result(res)
        self.show_check(self.eda.df59)
    
    def btntext_assit_clicked(self):
        self.destroy_widgets()
        text_assist = FCmdText(self.bot)
        self.show_check(self.eda.df59)  
    
    '''Hàm vẽ biểu đồ'''
    def draw_zscore_graph(self):
        self.destroy_widgets()
        self.canvas = self.eda.draw_zscore(self.fKetqua)
        if self.canvas == None:
            messagebox.showerror("Error", self.canvas)
        self.show_check(self.eda.df59)
            
    def draw_heatmap_graph(self):
        self.destroy_widgets()
        self.canvas = self.eda.daw_heatmap(self.fKetqua)
        if self.canvas == None:
            messagebox.showerror("Error", self.canvas)
        self.show_check(self.eda.df59)
    
    def draw_bienthien_graph(self):
        self.destroy_widgets()
        try:
            self.canvas = self.eda.draw_bienthien(self.fKetqua, tp.lst[0])
        except Exception as ex:
            messagebox.showerror("Error", str(ex))
        tp.lst = []
        self.show_check(self.eda.df59)
        
    '''Làm game'''
    def btngame_clicked(self):
        play_game()
            
    '''Show kết quả'''
    def show_result(self, res):
        self.show_txtKetqua()
        self.txtKetQua59.insert(END, f"{res}\n\n\n***********vvv***********\n\n")
    
    def show_selectedAttr(self):
        for col in tp.lst:
            self.txtCol.insert(END, f'{col}\n')
    
    def show_txtKetqua(self):
        self.txtKetQua59.grid(row=1, column=0, padx=1, pady=5)
        
    def show_selectedcol(self):
        self.txtSelectedCols.delete(0.0, END)
        for col in tp.lst:
            self.txtSelectedCols.insert(END, f'{col}\n')
    
    def load_data_to_treeview(self, df):
        columns = list(df.columns)
        # Set the headings for the columns
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
        # Set the width of each column
        for col in columns:
            self.tree.column(col, width=64)
        # Insert the data from the dataframe into the Treeview widget
        for index, row in df.iterrows():
            values = [row[col] for col in columns]
            self.tree.insert("", index, values=values, tags=(index,))
            self.tree.tag_configure(index, foreground="#0072c6")  # thiết lập màu cho tag
        # Place the Treeview widget in the GUI
        self.tree.place(x=20, y=150, height=600, width=1300, bordermode='outside')
        
    def show_check(self, df):
        # Set the style of the Treeview widget
        style = ttk.Style()
        style.theme_use("alt")
        # style.configure("Treeview", background="#f0f0f0")
        # style.configure("Treeview.Heading", foreground='#210F55')
        style.configure('child_tree',background="white",rowheight=25,foreground="black",font=("Arial", 9))
        style.map('child_tree',background=[('selected','blue')])
        style.configure('child_tree.Heading', font=("Arial", 9, "bold"))

        # Get the column names from the dataframe and create headings
        columns = df.columns.to_list()
        self.child_tree.config(columns=columns)
        
        # Set the headings for the columns
        for col in columns:
            self.child_tree.heading(col, text=col)

        # Set the width of each column
        for col in columns:
            self.child_tree.column(col, anchor="center", width=93)

       # Tạo một danh sách chứa các giá trị của dòng mới
        new_row = ["counts null"]

        # Lặp qua từng cột để tính toán số lượng dòng null và thêm vào danh sách new_row
        for col in df.columns.to_list():
            null_counts = df[col].isnull().sum()
            new_row.append(null_counts)
        # Chèn dòng mới vào cuối cùng
        self.child_tree.insert("", "end", values=new_row)
        
        new_row = ["Phổ biến"]
        for col in df.columns.to_list():
            phobien = df[col].mode()[0]
            new_row.append(phobien)
        self.child_tree.insert("", "end", values=new_row)
        
        new_row = ["duplicates_counts"]
        for col in df.columns.to_list():
            duplicates_counts = df.duplicated(subset=[col]).sum()
            new_row.append(duplicates_counts)
        self.child_tree.insert("", "end", values=new_row)
        
        new_row = ["Unique"]
        for col in df.columns.to_list():
            unique =df[col].nunique()
            new_row.append(unique)
        self.child_tree.insert("", "end", values=new_row)
        
        # Cấu hình lại màu sắc cho dòng mới thêm vào
        self.child_tree.tag_configure("new_row", background="lightblue")
        #place tree view
        self.child_tree.place(x=20, y=20, height=120, width=1300, bordermode='outside')
    
    '''Xóa Widget'''
    def destroy_txtKetqua(self):
        self.txtKetQua59.grid_forget()
        
    def destroy_graph(self):
        self.canvas.get_tk_widget().pack_forget()
        
    def destroy_treeview(self, tree):
        for col in tree['columns']:
            tree.heading(col, text="")
        for item in tree.get_children():
            tree.delete(item)
        tree.place_forget()
        
    def destroy_widgets(self):
        self.destroy_graph()
        self.destroy_txtKetqua()
        self.destroy_treeview(self.tree)
        self.destroy_treeview(self.child_tree)

class FCmdText(FGUI):
    def __init__(self, bot):
        self.bots = bot
        '''Form'''
        self.fcmdtext = customTK.CTk()
        self.cmd_frame = Frame(self.fcmdtext, bg="white")
                
        '''Label'''
        self.lbl_ready = Label(self.fcmdtext, text='Nhập lệnh', font=("Arial Bold",  15))
        self.lbl_ready.grid(row=0, column=0, padx=8, pady=5)

        '''Text Box'''
        self.txtcmd = customTK.CTkTextbox(self.fcmdtext, width=200, height=1, pady=0)
        self.txtcmd.grid(row=0, column=1, padx=8, pady=8)

        '''Button'''
        self.sendcmd_but59 = customTK.CTkButton(self.fcmdtext, text="Send", fg_color='red', command=self.btnsendcmd_clicked)
        self.sendcmd_but59.grid(row=0, column=2, padx=8, pady=8)
        
        self.fcmdtext.mainloop()
    
    def btnsendcmd_clicked(self):
        res = self.bots.text_assist(self.txtcmd.get(0.0, END).strip())
        self.show_result(res)
        

# Run
form = FGUI()
