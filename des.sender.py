import tkinter as tk
from tkinter import filedialog
import numpy as np
import time
import os
import socket
from PIL import Image, ImageTk  # Import thư viện xử lý ảnh

# Bảng để thực hiện hoán vị IP cho bảng dữ liệu ban đầu
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# Bảng IP^-1: để thực hiện hoán vị cuối cùng 
FP = [40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25]

#Bảng để thực hiện phép mở rộng E
EBox = [32,1,2,3,4,5,
        4,5,6,7,8,9,
        8,9,10,11,12,13,
        12,13,14,15,16,17,
        16,17,18,19,20,21,
        20,21,22,23,24,25,
        24,25,26,27,28,29,
        28,29,30,31,32,1]

# Vì có 56 bit cần mã hóa -> 8 phần mỗi phần 6 bit, 2 bit đầu cuối là hàng, 4 bit giữa là cột
SBox =[
		# S1
		[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
		 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
		 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
		 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

		# S2
		[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
		 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
		 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
		 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

		# S3
		[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
		 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
		 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
		 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

		# S4
		[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
		 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
		 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
		 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

		# S5
		[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
		 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
		 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
		 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

		# S6
		[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
		 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
		 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
		 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

		# S7
		[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
		 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
		 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
		 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

		# S8
		[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
		 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
		 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
		 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
	]


# Bảng để thực hiện hoán vị P trong Hàm Feistel
F_PBox = [16, 7, 20, 21, 29, 12, 28, 17,
              1, 15, 23, 26, 5, 18, 31, 10,
              2, 8, 24, 14, 32, 27, 3, 9,
              19, 13, 30, 6, 22, 11, 4, 25 ]

# Bảng mã để thực hiện hoán vị PC2 trước khi XOR khóa K với dữ liệu
key_PBox = [14,    17,   11,    24,     1,    5,
                  3,    28,   15,     6,    21,   10,
                 23,    19,   12,     4,    26,    8,
                 16,     7,   27,    20,    13,    2,
                 41,    52,   31,    37,    47,   55,
                 30,    40,   51,    45,    33,   48,
                 44,    49,   39,    56,    34,  53,
                 46,    42,   50,    36,    29,   32]

# Thực hiện phép xor 2 mảng và trả về 1 mảng bit
def xor(left,xorstream):
    xorresult = np.logical_xor(left,xorstream)

    xorresult  = xorresult.astype(int) # Ép kiểu sang int (ban đầu là boolean)

    return xorresult

# Mở rộng mảng từ 32 -> 48 bit
def E_box(right):
    expanded = np.empty(48) # Khởi tạo mảng rỗng có kdl float
    j = 0
    for i in EBox:
        expanded[j] = right[i - 1]
        j += 1
    expanded = list(map(int,expanded)) # chuyển sang int
    expanded = np.array(expanded)
    return expanded


def sboxloopup(sinput,x):
    tableno = x - 1
    row = int((np.array2string(sinput[0]) + np.array2string(sinput[5])),2)

    column = sinput[1:5]
    column = np.array2string(column)
    column = column[1:8].replace(" ", "")
    column = int(column,2)

    elementno = (16 * row) + column
    soutput = SBox[tableno][elementno]
    soutput = list(np.binary_repr(soutput, width=4))
    soutput= np.array(list(map(int, soutput)))
    return soutput

def sbox(sboxin):
    sboxin1 = sboxin[0:6]
    sboxout1 = sboxloopup(sboxin1,1)
    sboxin2 = sboxin[6:12]
    sboxout2 = sboxloopup(sboxin2,2)
    sboxin3 = sboxin[12:18]
    sboxout3 = sboxloopup(sboxin3, 3)
    sboxin4 = sboxin[18:24]
    sboxout4 = sboxloopup(sboxin4, 4)
    sboxin5 = sboxin[24:30]
    sboxout5 = sboxloopup(sboxin5, 5)
    sboxin6 = sboxin[30:36]
    sboxout6 = sboxloopup(sboxin6, 6)
    sboxin7 = sboxin[36:42]
    sboxout7 = sboxloopup(sboxin7, 7)
    sboxin8 = sboxin[42:48]
    sboxout8 = sboxloopup(sboxin8, 8)
    sboxout = np.concatenate([sboxout1,sboxout2,sboxout3,sboxout4,sboxout5,sboxout6,sboxout7,sboxout8])
    return sboxout

def f_permute(topermute):
    permuted= np.empty(32)
    j = 0
    for i in F_PBox:
        permuted[j] = topermute[i - 1]
        j += 1
    return permuted

def f_function(right,rkey):
    expanded = E_box(right)
    xored = xor(expanded,rkey)
    sboxed = sbox(xored)
    xorstream = f_permute(sboxed)
    return xorstream

def round(data,rkey):
    l0 = data[0:32]
    r0 = data[32:64]
    xorstream = f_function(r0,rkey)
    r1 = xor(l0,xorstream)
    l1 = r0
    returndata = np.empty_like(data)
    returndata[0:32] = l1
    returndata[32:64] = r1
    return(returndata)

def permutation(data,x):
    permute1 = np.empty_like(IP)
    if x == 0:
        j = 0
        for i in IP:
            permute1[j] = data[i-1]
            j += 1
        return(permute1)
    else:
        permute2 = np.empty_like(FP)
        k = 0
        for l in FP:
            permute2[k] = data[l-1]
            k += 1
        return(permute2)


def keyshift(toshift,n):
    if (n == 1) or (n == 2) or (n == 9) or (n == 16):
        toshift= np.roll(toshift,-1)
        return toshift
    else:
        toshift = np.roll(toshift, -2)
        return toshift

def keypermute(key16):
    keypermuted = np.empty([16,48])
    l = 0
    for k in key16:
        j = 0
        for i in key_PBox:
            keypermuted[l][j] = k[i - 1]
            j += 1
        l += 1
    return keypermuted

#
def keyschedule(key):
    left = key[0:28]
    right = key[28:56]
    shifted = np.zeros(56)
    key16 = np.zeros([16,56])
    for i in range(1,17):
        shifted[0:28] = keyshift(left,i)
        shifted[28:56] = keyshift(right,i)
        left = shifted[0:28]
        right = shifted[28:56]
#Cộng vế trái và vế phải trả ra khóa
        key16[i - 1] = shifted
#hoán vị khóa
    key16 = keypermute(key16)
    key16 = [list(map(int, x)) for x in key16]
    key16 = np.array(key16)
    return key16

def split_binary_string(binary_string):
    smaller_strings = []

    full_chunks = len(binary_string) // 64

    for i in range(full_chunks):
        chunk = binary_string[i*64:(i+1)*64]
        smaller_strings.append(chunk)

    remaining_bits = len(binary_string) % 64
    if remaining_bits > 0:
        remaining_chunk = binary_string[full_chunks*64:]
        smaller_strings.append(remaining_chunk)

    return smaller_strings

def binary_to_char(binary_str):
    # Chia chuỗi bit thành các nhóm có độ dài 8 bit (1 byte)
    bytes_list = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]

    # Chuyển đổi từ nhóm 8 bit thành ký tự ASCII
    chars = ''.join([chr(int(byte, 2)) for byte in bytes_list])

    return chars

def browse_file():
    filename = filedialog.askopenfilename()
    if filename:
        entry_file.delete(0, tk.END)  # Xóa nội dung hiện tại của ô input
        entry_file.insert(0, filename)   # Gán giá trị mới vào ô input


def send_file():
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = entry_host.get()
    port = entry_port.get()
    try:
        client.connect((host, int(port)))
        print("Connected to the server successfully!")
        label_status.config(text = label_status.cget("text") + "Connected to the server successfully!" + "\n")

            # BufferedReader reader = new BufferedReader(new InputStreamReader(client.getInputStream()))

    except ConnectionRefusedError:
        print("Connection failed. Server is not running or refused the connection.")
        label_status.config(text = label_status.cget("text") + "Connection failed. Server is not running or refused the connection." + "\n")

    key = entry_key.get()
    key = format(int(key, 16), '056b')
    key = list(key)
    key16 = keyschedule(key)

    file = open(entry_file.get(),"rb")
    data = file.read()
    data = data.decode()
    binary_data = ''.join(format(ord(char), '08b') for char in data)
    print(binary_data)

    lenofdata = 64

    smaller_strings = []

    if len(binary_data) == lenofdata:
        print("data entry accepted, data loaded succesfully")
        smaller_strings.append(binary_data)
    elif len(binary_data) > lenofdata:
        smaller_strings = split_binary_string(binary_data)
        print("length of file: ", len(binary_data))
        for i in range(0, (64-len(smaller_strings[-1]))//8, 1):
            smaller_strings[-1] += '00100000'
            # print(len(smaller_strings[-1]))
    else:
        for i in range(0, (64-len(binary_data))//8, 1):
            binary_data += '00100000'
        smaller_strings.append(binary_data)

    for i in range(0, len(smaller_strings), 1):
        smaller_strings[i] = (permutation(smaller_strings[i], 0))
        starttime = time.time()

        for j in range(16):
            smaller_strings[i] = round(smaller_strings[i],key16[j])

        smaller_strings[i] = np.roll(smaller_strings[i],32)
        smaller_strings[i] = (permutation(smaller_strings[i], 1))

        
    print("Time taken to encrypt the data with DES is", time.time() - starttime)
    print("Encrypted data is")
    data_str = ''
    for string in smaller_strings:
            # print(string)
        data_str += ''.join(map(str, string))
        # Convert string to bytes
    print(data_str)
        # data_string = binary_to_char(data_str)
    bytes_data = bytes(int(data_str[i:i+8], 2) for i in range(0, len(data_str), 8))
        # print(data_string)
    client.sendall(bytes_data)
    label_status.config(text = label_status.cget("text") + "Client: " + "Send file success!!!" + "\n")
    file.close()

    received_message = client.recv(1024).decode('utf-8')
    if received_message: 
        label_status.config(text = label_status.cget("text") + "Server: " + received_message + "\n")


# Tạo cửa sổ chính
root = tk.Tk()
root.title("SENDER PAGE")
root.geometry("600x300")
root.resizable(False, False)  # Không cho thay đổi kích thước

# Tạo frame chính (chia 2 cột)
frame_main = tk.Frame(root)
frame_main.pack(fill="both", expand=True)

# Frame trái (Nhập liệu)
frame_left = tk.Frame(frame_main, bg="#ffffff", bd=2)
frame_left.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# Frame phải (Hiển thị ảnh + trạng thái)
frame_right = tk.Frame(frame_main, bg="#ffffff", bd=2)
frame_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Font chữ chung
font = ("Helvetica", 12)

# ------------------- BÊN TRÁI: NHẬP THÔNG TIN -------------------
tk.Label(frame_left, text="Host:", font=font, bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_host = tk.Entry(frame_left, width=20, font=font)
entry_host.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_left, text="Port:", font=font, bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_port = tk.Entry(frame_left, width=20, font=font)
entry_port.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_left, text="File:", font=font, bg="white").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_file = tk.Entry(frame_left, width=20, font=font)
entry_file.grid(row=2, column=1, padx=5, pady=5)
button_browse = tk.Button(frame_left, text="Chọn file", font=font, command=browse_file)
button_browse.grid(row=2, column=2, padx=5, pady=5)

tk.Label(frame_left, text="Key:", font=font, bg="white").grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_key = tk.Entry(frame_left, width=20, font=font)
entry_key.grid(row=3, column=1, padx=5, pady=5)

button_send = tk.Button(frame_left, text="Gửi", font=font, command=send_file, width=15, bg="green", fg="white")
button_send.grid(row=4, column=1, pady=10, columnspan=2)

# ------------------- BÊN PHẢI: HIỂN THỊ ẢNH + TRẠNG THÁI -------------------

# Load hình ảnh background
try:
    bg_image = Image.open("Des.jpg")  # Đổi thành đường dẫn ảnh của bạn
    bg_image = bg_image.resize((250, 150))  # Resize ảnh để vừa với phần hiển thị
    bg_photo = ImageTk.PhotoImage(bg_image)

    label_image = tk.Label(frame_right, image=bg_photo, bg="white")
    label_image.pack(pady=5)
except Exception as e:
    label_image = tk.Label(frame_right, text="Không thể tải ảnh", bg="white", font=font, fg="red")
    label_image.pack(pady=5)

# Label trạng thái
# label_status = tk.Label(frame_right, text="Trạng thái: Chờ gửi...", font=font, fg="gray", relief="sunken", anchor="w", height=2, bg="white")
# label_status.pack(fill="x", padx=5, pady=5)

label_status = tk.Label(
    frame_right,
    text="Trạng thái: Chờ gửi...",
    font=font,
    fg="gray",
    relief="flat",
    anchor="w",
    height=2,
    bg="white",
    wraplength=200,   # Tự động xuống dòng khi quá 200px
    justify="left"     # Căn lề trái văn bản
)
label_status.pack(fill="x", padx=5, pady=5)


# Khởi chạy giao diện
root.mainloop()

