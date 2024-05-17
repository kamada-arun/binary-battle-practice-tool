import tkinter as tk
from tkinter import ttk
import os
import random as rand
import time
from PIL import Image, ImageTk

class BinaryBattlePracticeTool(tk.Tk):
    def __init__(self):
        self.OPTIONS_FILE = "options"
        self.RESULTS_FILE = "results"
        self.results = []
        self.read_options()

        super().__init__()
        self.title("Binary Battle Practice Tool")
        self.geometry("1024x640")
        self.minsize(1024, 640)
        self.create_main_frame()
        self.create_menu_screen()
        self.question_number = 1  # 初期問題番号
        self.start_time = None  # 開始時間を記録する変数
        self.elapsed_time_label = None  # 経過時間ラベルの参照を保持

    def read_options(self):
        self.options_value = {"idx": 1, "number_range_min": 0, "number_range_max": 255}  # 初期値

        if not os.path.isfile(self.OPTIONS_FILE):
            self.set_options()  # ファイル生成
        
        with open(self.OPTIONS_FILE, "r") as file:
            content = file.read()
        
        for i in content.split():
            self.options_value[i.split(":")[0]] = int(i.split(":")[1])
    
    def set_options(self):
        options_text = ""

        for key, value in self.options_value.items():
            options_text += f"{key}:{value}\n"

        with open(self.OPTIONS_FILE, "w") as file:
            file.write(options_text)

    def create_main_frame(self):
        self.main_frame = tk.Frame(self, bg="black")
        self.main_frame.pack(fill="both", expand=True)

    def create_menu_screen(self):
        self.clear_frame(self.main_frame)

        title_label = tk.Label(self.main_frame, text="Binary Battle Practice Tool", font=("Helvetica", 50, "bold"), fg="white", bg="black")
        title_label.pack(pady=60)

        idx_label = tk.Label(self.main_frame, text="あなたの番号 :", font=("Helvetica", 24), fg="white", bg="black")
        idx_label.pack(pady=(20, 5))

        self.menu_selected_idx = tk.StringVar()
        idx_dropdown = ttk.Combobox(self.main_frame, textvariable=self.menu_selected_idx, values=[str(i) for i in range(1, 9)], font=("Helvetica", 24))
        idx_dropdown.pack(pady=(5, 20))
        self.menu_selected_idx.set(str(self.options_value["idx"]))

        start_button = tk.Button(self.main_frame, text="START", font=("Helvetica", 70, "bold"), fg="lime", bg="black", command=self.start_questions)
        start_button.pack(pady=(40, 10))

    def start_questions(self):
        self.options_value["idx"] = int(self.menu_selected_idx.get())
        self.set_options()  # 設定の保存
        self.question_number = 1
        self.start_time = time.time()
        self.create_question_screen()

    def create_question_screen(self):
        self.clear_frame(self.main_frame)

        # ランダムな3桁の数字を生成
        random_number = rand.randint(self.options_value["number_range_min"], self.options_value["number_range_max"])

        # 問題番号のラベル
        question_label = tk.Label(self.main_frame, text=f"{self.question_number}問目", font=("Helvetica", 24), fg="white", bg="black")
        question_label.pack(anchor="nw", padx=20, pady=(10, 0))

        # 経過秒数のラベル（更新される）
        self.elapsed_time_label = tk.Label(self.main_frame, font=("Helvetica", 24), fg="yellow", bg="black")
        self.elapsed_time_label.pack(anchor="ne", padx=20, pady=(0, 10))

        # ランダムな数字のラベル
        number_label = tk.Label(self.main_frame, text=f"{random_number}", font=("Helvetica", 100, "bold"), fg="white", bg="black")
        number_label.pack(pady=20)

        # ボタンフレーム
        button_frame = tk.Frame(self.main_frame, bg="black")
        button_frame.pack(pady=20)

        def show_result_one():
            self.get_result(random_number, "one")

        def show_result_zero():
            self.get_result(random_number, "zero")

        def show_result_pass():
            self.get_result(random_number, "pass")

        one_button = tk.Button(button_frame, text='  １  ', font=("Helvetica", 36, "bold"), fg="lime", bg="black", command=show_result_one)
        one_button.pack(side="left", padx=20)

        zero_button = tk.Button(button_frame, text='  ０  ', font=("Helvetica", 36, "bold"), fg="red", bg="black", command=show_result_zero)
        zero_button.pack(side="left", padx=20)

        pass_button = tk.Button(self.main_frame, text="パス", font=("Helvetica", 24, "bold"), fg="white", bg="black", command=show_result_pass)
        pass_button.pack(pady=20)

        self.update_timer()

    def get_result(self, random_number,  player_select):
        raw_answer = str(bin(random_number))[2:].zfill(8)
        answer = raw_answer[:4] + " " + raw_answer[4:]

        if (raw_answer[-self.options_value["idx"]] == "1" and player_select == "one") or (raw_answer[-self.options_value["idx"]] == "0" and player_select == "zero"):
            result = "correct"
        else:
            result = "incorrect"
        
        self.add_result(self.options_value["idx"], random_number, player_select, time.time() - self.start_time)
        if self.question_number % 10 == 0:
            self.save_result()
        self.create_result_screen(random_number, answer, result)

    def update_timer(self):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            self.elapsed_time_label.config(text=f"{elapsed_time:.1f}秒")
            self.after(100, self.update_timer)  # 100ミリ秒ごとに更新

    def create_result_screen(self, number, answer, result):
        self.clear_frame(self.main_frame)

        # 問題番号のラベル
        problem_label = tk.Label(self.main_frame, text=f"{self.question_number}問目", font=("Helvetica", 24), fg="white", bg="black")
        problem_label.pack(anchor="nw", padx=20, pady=(10, 0))

        # 経過秒数のラベル（停止して色変更）
        elapsed_time = time.time() - self.start_time
        self.start_time = None
        self.elapsed_time_label = tk.Label(self.main_frame, text=f"{elapsed_time:.1f}秒", font=("Helvetica", 24), fg="yellow", bg="black")
        self.elapsed_time_label.pack(anchor="ne", padx=20, pady=(0, 10))

        # マルバツ画像のラベル
        if result == "correct":
            answer_image = Image.open("data/maru.png")
        else:
            answer_image = Image.open("data/batu.png")
        
        answer_image = answer_image.resize((180, 180), Image.ANTIALIAS)
        self.answer_image_tk = ImageTk.PhotoImage(answer_image)
        canvas = tk.Canvas(self.main_frame, width=1024, height=200, bg="black", highlightthickness=0)
        canvas.pack()
        number_label = canvas.create_text(512, 100, text=f"{number}", font=("Helvetica", 100, "bold"), fill="white")
        canvas.create_image(512, 100, image=self.answer_image_tk)

        # 答えのラベル
        answer_label = tk.Label(self.main_frame, text=f"答え : {answer}", font=("Helvetica", 24), fg="white", bg="black")
        answer_label.pack(pady=20)

        # ボタンフレーム
        button_frame = tk.Frame(self.main_frame, bg="black")
        button_frame.pack(pady=20)

        def next_question():
            self.question_number += 1
            self.start_time = time.time()
            self.create_question_screen()

        next_button = tk.Button(button_frame, text="次の問題", font=("Helvetica", 50, "bold"), fg="lime", bg="black", command=next_question)
        next_button.pack(padx=20)

        quit_frame = tk.Frame(self.main_frame, bg="black")
        quit_frame.pack(side="bottom", anchor="se", padx=20, pady=(0, 20))

        def quit_sys():
            self.save_result()
            self.quit()


        quit_button = tk.Button(quit_frame, text="QUIT", font=("Helvetica", 24, "bold"), fg="white", bg="black", command=quit_sys)
        quit_button.pack(side="right")

    def clear_frame(self, screen):
        for widget in screen.winfo_children():
            widget.destroy()

    def add_result(self, idx, num, ans, time):
        self.results.append(f"idx:{idx}, num:{num}, ans:{ans}, time:{time}")

    def save_result(self):
        with open(self.RESULTS_FILE, "a") as file:
            [file.write(f"{res}\n") for res in self.results]
        self.results = []

if __name__ == "__main__":
    app = BinaryBattlePracticeTool()
    app.mainloop()
