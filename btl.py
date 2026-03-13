import tkinter as tk
from tkinter import messagebox
import random
import math

class TSPVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Mô phỏng TSP - Thuật toán tham ăn")
        
        self.canvas_width = 800
        self.canvas_height = 600
        self.points = []
        
        # UI Setup
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)
        
        self.lbl_num_points = tk.Label(self.frame, text="Số điểm:")
        self.lbl_num_points.grid(row=0, column=0, padx=5)
        
        self.entry_num_points = tk.Entry(self.frame, width=5)
        self.entry_num_points.insert(0, "20")
        self.entry_num_points.grid(row=0, column=1, padx=5)
        
        self.btn_generate = tk.Button(self.frame, text="Tạo điểm ngẫu nhiên", command=self.generate_points)
        self.btn_generate.grid(row=0, column=2, padx=5)
        
        self.btn_run = tk.Button(self.frame, text="Chạy thuật toán", command=self.run_algorithm)
        self.btn_run.grid(row=0, column=3, padx=5)
        
        self.lbl_info = tk.Label(self.frame, text="Chi phí: 0", font=("Arial", 12, "bold"), fg="blue")
        self.lbl_info.grid(row=0, column=4, padx=20)
        
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white", relief=tk.SUNKEN, borderwidth=2)
        self.canvas.pack(padx=10, pady=10)
        
        # Khởi tạo điểm lúc mới mở
        self.generate_points()

    def generate_points(self):
        try:
            num_points = int(self.entry_num_points.get())
            if num_points < 2:
                messagebox.showerror("Lỗi", "Số điểm phải lớn hơn 1")
                return
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")
            return
            
        self.points = []
        padding = 40
        self.canvas.delete("all")
        
        for i in range(num_points):
            x = random.randint(padding, self.canvas_width - padding)
            y = random.randint(padding, self.canvas_height - padding)
            self.points.append((x, y))
            
            # Vẽ các điểm
            r = 5
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="red", outline="black")
            # Hiển thị số thứ tự điểm
            self.canvas.create_text(x, y - 10, text=str(i), fill="darkred")
            
        self.lbl_info.config(text="Đã tạo điểm ngẫu nhiên.")

    def calc_distance_matrix(self):
        n = len(self.points)
        dist_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                dx = self.points[i][0] - self.points[j][0]
                dy = self.points[i][1] - self.points[j][1]
                dist_matrix[i][j] = math.sqrt(dx**2 + dy**2)
        return dist_matrix

    def nearest_neighbor(self, dist_matrix, start=0):
        n = len(dist_matrix)
        visited = [False] * n
        path = [start]
        visited[start] = True
        cost = 0

        current = start
        for _ in range(n-1):
            next_city = None
            min_dist = float('inf')
            for j in range(n):
                if not visited[j] and dist_matrix[current][j] < min_dist:
                    min_dist = dist_matrix[current][j]
                    next_city = j
            if next_city is not None:
                path.append(next_city)
                visited[next_city] = True
                cost += min_dist
                current = next_city

        cost += dist_matrix[current][start]
        path.append(start)
        return cost, path

    def run_algorithm(self):
        if not self.points:
            messagebox.showwarning("Cảnh báo", "Chưa có điểm nào để tính toán!")
            return
            
        dist_matrix = self.calc_distance_matrix()
        cost, path = self.nearest_neighbor(dist_matrix, start=0)
        
        # Cập nhật label chi phí (làm tròn 2 chữ số thập phân)
        self.lbl_info.config(text=f"Chi phí: {cost:.2f}")
        
        # Làm sạch các đường vẽ cũ, chỉ giữ lại điểm và text
        self.canvas.delete("line")
        
        # Vẽ lộ trình
        for i in range(len(path) - 1):
            p1 = self.points[path[i]]
            p2 = self.points[path[i+1]]
            # Vẽ đường thẳng có mũi tên chỉ hướng
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="blue", width=2, arrow=tk.LAST, tags="line")
            
        # Làm nổi bật điểm xuất phát (màu xanh lá)
        start_p = self.points[path[0]]
        self.canvas.create_oval(start_p[0] - 8, start_p[1] - 8, start_p[0] + 8, start_p[1] + 8, fill="green", tags="line")

if __name__ == "__main__":
    root = tk.Tk()
    app = TSPVisualizer(root)
    root.mainloop()
