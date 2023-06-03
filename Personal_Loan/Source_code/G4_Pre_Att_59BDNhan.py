import tkinter as tk59
from tkinter import messagebox
import G4_59BDNhan_Topic as tp

class SELECTCOL:
    weight = {1: 'PersonalLoan', 2: 'Income', 3: 'Education', 4: 'Experience', 5: 'CCAvg', 6: 'Age', 7: 'CDAccount', 8: 'SecuritiesAccount', 9: 'CreditCard', 10: 'Online ', 11: 'ID', 12: 'ZIP Code'}
    
    def __init__(self, cols):
        #Khởi tạo thiết lập đối tượng win59FORM
        self.win59 = tk59.Tk()
        self.win59.title("BƯỚC 3: XỬ LÝ CỘT NULL = NẠP & CHỌN CÁC CỘT NULL CẦN XỬ LÝ")
        self.win59.geometry("955x610")
        self.win59.resizable(tk59.FALSE, tk59.FALSE)

        #######################################
        #Listbox1 
        self.listbox1 = tk59.Listbox(self.win59, height = 25, width = 40, font = "Consolas 12", selectmode = tk59.EXTENDED, border=3)
        self.listbox1.bind("<Button-3>", self.ShowPopupMenulb1) #<Button-3> : đăng ký sự kiện cho chuột phải của listbox = e: vị trí 
        self.listbox1.place(x = 15, y = 50)
        #Thiết lập listbox2
        self.listbox2 = tk59.Listbox(self.win59, height = 25, width = 40, font = "Consolas 12", selectmode = tk59.EXTENDED, border=3)
        self.listbox2.bind("<Button-3>", self.ShowPopupMenulb2)
        self.listbox2.place(x = 550, y = 50)
        #Thiết lập lblSoLuong
        tk59.Label(self.win59, text = "Số lượng").place(x = 15, y = 573)
        self.lblSoLuong = tk59.Label(self.win59, relief = tk59.SUNKEN ,font = "Times 8", borderwidth = 3, width = 15, height = 1)
        self.lblSoLuong.place(x = 100, y = 575)

        #Move all Leff
        self.btnallL = tk59.Button(self.win59, text = "Move All Left", width = 15, command = self.move_all_left) 
        self.btnallL.place(x = 400, y = 160) 
        #Move all right
        self.btnallR = tk59.Button(self.win59, text = "Move All Right", width = 15, command = self.move_all_right) 
        self.btnallR.place(x = 400, y = 210)
        #delete
        self.btnDlL = tk59.Button(self.win59, text = "Delete All Left", width = 15, command = self.delete_all_left) 
        self.btnDlL.place(x = 400, y = 270)

        self.btnDlR = tk59.Button(self.win59, text = "Delete All Right", width = 15, command = self.delete_all_right) 
        self.btnDlR.place(x = 400, y = 330)
        
        self.btnXoa = tk59.Button(self.win59, text = "Select Attributes", width = 15, command = self.btnChon_clicked) 
        self.btnXoa.place(x = 400, y = 100)
        
        self.load_data(self.weight, cols)
        
        self.win59.mainloop()

    #Hàm xử lý btnAdd
    def load_data(self, weight, cols): 
        for col in weight:
            if weight[col] in cols: 
                self.listbox1.insert(tk59.END, weight[col])

    #Copy
    def copy_to(self, lbm, lbd):
        i = 0
        while i < lbd.size(): # duyệt listbox1 -> đến từng vị trí chọn
            if(lbd.select_includes(i) == 1): 
                # sự kiện xác định 1 pt tại vị trí i trong listbox1 đang chọn or not
                check, j = False, 0
                while j < lbm.size():
                    if lbm.get(j) == lbd.get(i):                   
                        messagebox.showwarning("Cảnh báo", "Đã tồn tại")
                        check = True
                        break
                    j += 1
                if check == False or lbm.size() == 0:
                    lbm.insert(tk59.END, lbd.get(i))
                
            i = i + 1
        #Clear selectitem listbox1 
        lbd.select_clear(0,tk59.END) # bỏ chế độ chọn các pt đã chọn

    def CopyToRight(self): 
        self.copy_to(self.listbox2, self.listbox1)

    def CopyToLeft(self): 
        self.copy_to(self.listbox1, self.listbox2)

    #Hàm MoveTo: di chuyên các thuộc tính từ listbox1 sang listbox2 (xóa các thuộc tính đã chuyển listbox1->)
    def move_to(self, lbm, lbd):
        i = 0
        while i < lbd.size(): # duyệt listbox1 -> đến từng vị trí chọn
            if lbd.select_includes(i) == 1: 
                lbm.insert(tk59.END, lbd.get(i))
                lbd.delete(i)
                i -= 1
            i += 1
        #Đếm lại số dòng trong listbox1
        dem = lbd.size() 
        #Cập nhật vào label
        self.lblSoLuong.configure(text = dem)
        # không cần bỏ chế độ = vì đã xóa all pt chọn

    def MoveToRight(self): 
        self.move_to(self.listbox2, self.listbox1)

    def MoveToLeft(self): 
        self.move_to(self.listbox1, self.listbox2)

    #Move all to
    def move_all_right(self):
        i = 0
        while i < self.listbox1.size(): # duyệt listbox1 -> đến từng vị trí chọn
            self.listbox2.insert(tk59.END, self.listbox1.get(i))
            self.listbox1.delete(i)  
            
    def move_all_left(self):
        i = 0
        while i < self.listbox2.size(): # duyệt listbox1 -> đến từng vị trí chọn
            self.listbox1.insert(tk59.END, self.listbox2.get(i))
            self.listbox2.delete(i)  

    #Hàm Delete thuộc tính
    def delete_left(self): 
        i = 0
        while i < self.listbox1.size(): # duyệt listbox1 -> đến từng vị trí chọn
            if self.listbox1.select_includes(i) == 1: 
                self.listbox1.delete(i)
                break
            i += 1
        #Đếm lại dòng trong listbox1
        dem = self.listbox1.size() 
        #Cập nhật vào label
        self.lblSoLuong.configure(text = dem)
        #Clear selectitem listbox1 
        self.listbox1.select_clear(0,tk59.END)
        
    def delete_right(self):
        i = 0
        while i < self.listbox2.size(): # duyệt listbox1 -> đến từng vị trí chọn
            if self.listbox2.select_includes(i): 
                self.listbox2.delete(i)
                break
            i += 1
        #Đếm lại dòng trong listbox1
        dem = self.listbox2.size() 
        #Cập nhật vào label
        self.lblSoLuong.configure(text = dem)
        #Clear selectitem listbox1 
        self.listbox2.select_clear(0,tk59.END)

    # Delete all
    def delete_all_right(self):
        i = 0
        while i < self.listbox2.size(): # duyệt listbox1 -> đến từng vị trí chọn 
            self.listbox2.delete(i)
                
    def delete_all_left(self):
        i = 0
        while i < self.listbox1.size(): # duyệt listbox1 -> đến từng vị trí chọn
            self.listbox1.delete(i)

    #Lập Menu cho Listbox1:
    def ShowPopupMenulb1(self, e): 
        if self.listbox1.size() > 0 : 
            popMenulb1 = tk59.Menu(self.listbox1, tearoff = tk59.FALSE)
            popMenulb1.add_command(label = "Copy To Right", command = self.CopyToRight)
            popMenulb1.add_command(label = "Move To Right", command = self.MoveToRight)
            popMenulb1.add_command(label = "Delete", command = self.delete_left)
            popMenulb1.tk_popup(e.x_root, e.y_root)#phải thiết lập x_root, y_root để showpopup
            
    def ShowPopupMenulb2(self, e): 
        if self.listbox2.size() > 0 : 
            popMenulb2 = tk59.Menu(self.listbox2, tearoff = tk59.FALSE)
            popMenulb2.add_command(label = "Copy To Left", command = self.CopyToLeft)
            popMenulb2.add_command(label = "Move To Left", command = self.MoveToLeft)
            popMenulb2.add_command(label = "Delete", command = self.delete_right)
            popMenulb2.tk_popup(e.x_root, e.y_root)#phải thiết lập x_root, y_root để showpopup
    
    def btnChon_clicked(self):
        self.GetAttr(self.listbox2)
        messagebox.showinfo('info', 'Đã thêm thuộc tính cần thiết')
    
    def GetAttr(self, listbox):
        i = 0
        while i < listbox.size():
            tp.lst.append(listbox.get(i).strip())
            i += 1
        