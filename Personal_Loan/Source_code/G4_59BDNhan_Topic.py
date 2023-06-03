'''Thư viện cho EDA'''
# Numeric  Python: Thư viện về Đại số tuyến tính tính
import numpy as np
# Python  Analytic on Data System: Thư viện xử lý dữ liệu (for data processing) 
import pandas as pd
# Thư viện cung cấp các công cụ thống kê (statistics)
from scipy import stats
# Thư viện tiền xử lý DL (xử lý ngoại lệ: Isolated)
from sklearn import preprocessing
# Nạp hàm Thư viện phân tích dữ liệu thăm dò
from sklearn.feature_selection import SelectKBest, chi2
# Nạp thư viện Canvas và Figure, dùng để add matplotlib vào Form
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from tkinter import messagebox

'''EDA'''

#Tạo danh sách các cột cần xóa trong quá trình phân tích
global lst
lst = []

class EDA:
    def __init__(self):
        self.df59 = None
    
    '''Tiền xử lý dữ liệu'''
    def load_data(self):
        self.df59 = pd.read_csv('./G4_59BDNhan_UniversalBank.csv')    
    
    def get_shaped(self):
        # Lấy hình dạng của dataset
        return self.df59.shape
    
    def get_sampled(self):
        # Lấy mẫu của dataset
        return self.df59.head(10)
    
    def get_statvl(self):
        # Mô tả dữ liệu thống kê
        return self.df59.describe().reset_index()
    
    def remove_cols(self, lst):
        # Loại bỏ cột [ID] và [ZIP Code] vì không có giá trị trong chủ đề phân tích
        try:
            temp = self.df59.drop(columns=lst, axis=1)
            self.df59 = temp
        except: pass

    def check_isnan(self):
        # Kiểm tra giá trị NULL/NaN
        return self.df59.isna().sum()
    
    def nanpros_mode(self):
        # Thay thế giá trị rỗng bằng phương pháp phổ biến
        self.df59 = self.df59.replace(np.nan, self.df59.mode().iloc[0])
        return self.df59
    
    def nanpros_dropna(self):
        # Xử lý giá trị rỗng bằng phương pháp loại dòng NULL
        self.df59 = self.df59.dropna(how='any')
        return self.df59
    
    '''Xử lý Z-score'''
    # Lấy ma trận Z-score
    def mat_zscore(self): 
        z59 = np.abs(stats.zscore(self.df59._get_numeric_data()))  #  Dò  tìm  và  lấy  các  giá  trị  cá  biệt  trong  tập dữ  liệu  gốc  thông  qua  điểm  z  (z_score)
        return z59 #  in  ra  tập  (ma  trận)  các  giá  trị  z-score  từ  tập  dữ  liệu  gốc
    
    # Loại các điểm dữ liệu ngoại lệ
    def fillterdf_zscore(self, bound):
        try:
            z59 = self.mat_zscore()
            z_df59 = self.df59[(z59<float(bound)).all(axis=1)].reset_index().drop(columns=['index'])
        except:
            return False
        self.df59 = z_df59
        return True
    
    '''Chuẩn hóa rời rạc bằng thang đo MinMaxScaler'''
    def chrr_minmaxscaler(self):
        scaler = preprocessing.MinMaxScaler()
        df59_num = self.df59._get_numeric_data()
        scaler.fit(df59_num) # xác định thang đo MaxMin cho dataframe
        try:
            df59_chrr = pd.DataFrame(scaler.transform(df59_num),  index=df59_num.index,  columns=df59_num.columns) 
            self.df59 = df59_chrr
        except: return False
        return True
    
    '''Xác định các thuộc tính đặc trưng bằng PP chi2'''
    def xd_attr_dactrungchi2(self, input, output, num):
        try:
            output = output.split('\n')
            X = self.df59[input]
            y = self.df59[output]
            #Áp dụng mô hình vào tập dữ liệu
            selector = SelectKBest(chi2, k=int(num))
            selector.fit(X, y)
            attr_lst = X.columns[selector.get_support(indices=True)].to_list()
        except Exception as e:
            messagebox.showinfo('info', str(e))
            attr_lst = []
        return attr_lst
    
    def xd_attr_dactrungcor(self, output, bound):
        output = output.split('\n')
        cor = self.df59.corr()
        try: 
            # Chọn thuộc tính output cho mô hình
            cor_target = abs(cor[output[0]])
            # lọc chỉ số tương quan
            relevant_features = cor_target[(cor_target>float(bound)) & (cor_target < 1)].sort_values()
            num_of_feature = len(relevant_features)
        except Exception as ex:
            messagebox.showerror('Error', str(ex))
            relevant_features = 'Không thể xác định mức độ tương quan'
            num_of_feature = 0
            
        return f'Số thuộc tính ban đầu: {self.df59.shape[1]}\n' + f'Số thuộc tính tương quan đã lọc: {num_of_feature}\n\n' + f'{relevant_features}'
    
    '''Xác định mô hình trích lọc'''
    def xd_mohinh_trichloc(self, lst_attr):
        try:
            new_df59 = self.df59[lst_attr]
        except Exception as ex: 
            messagebox.showinfo('info', str(ex))
        return new_df59
    
    '''Xác định độ biến thiên dữ liệu'''
    def draw_bienthien(self, frame, col):
        try:
            indexrow = self.df59.reset_index()['index'].to_list()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))
            
        fig = Figure(figsize=(12.9, 6), dpi=100)
        ax = fig.add_subplot(111)
        ax.scatter(indexrow, self.df59[col].to_list())
        ax.legend()
        ax.set_title(col)
        ax.grid(True)
        ax.set_xlabel('Giá trị')
        ax.set_ylabel('Số lượng')
        
        # Add Biểu đồ vào Frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        return canvas
    
    def draw_zscore(self, frame):
        try:
            z_df = self.mat_zscore()
        except Exception as exc:
            return str(exc)
        cols = z_df.columns.to_list()
        # Create a figure and add a subplot to it
        fig = Figure(figsize=(12.9, 6), dpi=100)
        ax = fig.add_subplot(111)
        # Vẽ biểu đồ cho từng cột
        for col in cols:
            data = z_df[col].reset_index()
            ax.scatter(data['index'], data[col])
        ax.legend(cols)
        ax.grid(True)
        # Add Biểu đồ vào Frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        return canvas
    
    def daw_heatmap(self, frame):
        cols = self.df59.columns.to_list()
        # Create a figure and add a subplot to it
        fig = Figure(figsize=(12.9, 6), dpi=100)
        ax = fig.add_subplot(111)
        # Vẽ biểu đồ cho từng cột
        cor = self.df59.corr()
        heatmap = ax.imshow(cor, cmap='autumn', interpolation='nearest')
        for i in range(len(cols)):
            for j in range(len(cols)):
                ax.text(j, i, "{:.2f}".format(cor.iloc[i, j]), ha="center", va="center", color="white", fontsize=8)
        ax.set_xticks(range(len(cols)))
        ax.set_xticklabels(cols)
        ax.set_yticks(range(len(cols)))
        ax.set_yticklabels(cols)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        # Add colorbar
        cbar = fig.colorbar(heatmap, ax=ax)
        cbar.set_label('Correlation coefficient')
        # Add Biểu đồ vào Frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        return canvas