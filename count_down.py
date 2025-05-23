import tkinter
import datetime
import time
import threading

# メインウィンドウ生成
root = tkinter.Tk()
root.title('Countdown & Countup Timer')
root.geometry('1920x1080')
root.attributes('-fullscreen', True)

# ------ カウントダウン時間を保持する変数 ------
countdown_duration = None  # datetime.timedelta を入れる
timer_thread = None         # スレッドオブジェクトを格納しておく

# ------ キャンバス生成 ------
canvas = tkinter.Canvas(root, width=1920, height=1080, background='black',highlightthickness=0)
canvas.pack()

# タイマーのテキストを初期化
timer_text = canvas.create_text(
    960, 540,  # キャンバス中央に表示
    text="",    # 初期値は空
    font=('Arial Black', 300),
    fill='white'
)

# ------ エントリー入力欄 (時・分・秒) とラベル ------
label_h = tkinter.Label(root, text="Hours:", font=("Arial", 14), bg='black', fg='white')
label_h.place(x=50, y=50)
entry_h = tkinter.Entry(root, width=5, font=("Arial", 14))
entry_h.place(x=110, y=50)

label_m = tkinter.Label(root, text="Minutes:", font=("Arial", 14), bg='black', fg='white')
label_m.place(x=200, y=50)
entry_m = tkinter.Entry(root, width=5, font=("Arial", 14))
entry_m.place(x=280, y=50)

label_s = tkinter.Label(root, text="Seconds:", font=("Arial", 14), bg='black', fg='white')
label_s.place(x=370, y=50)
entry_s = tkinter.Entry(root, width=5, font=("Arial", 14))
entry_s.place(x=450, y=50)

# ------ [Start] ボタン ------
btn_start = tkinter.Button(
    root, text="Start", font=("Arial", 14), command=lambda: set_time_and_start()
)
btn_start.place(x=550, y=45)

def countdown_and_countup():
    """
    カウントダウン → 00:00:00 → カウントアップ
    00:00:00 を超えたら文字色を黄色に。
    """
    global countdown_duration
    
    # カウントダウン終了時刻
    end_time = datetime.datetime.now() + countdown_duration

    while True:
        now = datetime.datetime.now()
        
        if now < end_time:
            # ---- カウントダウン中 ----
            remaining = end_time - now
            total_seconds = int(remaining.total_seconds())
            color = 'white'
        else:
            # ---- カウントアップ中 ----
            elapsed = now - end_time
            total_seconds = int(elapsed.total_seconds())
            color = 'yellow'
        
        # 時・分・秒を計算
        hours = total_seconds // 3600
        remainder = total_seconds % 3600
        minutes = remainder // 60
        seconds = remainder % 60
        
        # 表示用文字列
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        
        # テキストを更新（ちらつき防止）
        canvas.itemconfig(timer_text, text=time_str, fill=color)
        
        # 次のフレーム更新まで待機
        time.sleep(0.1)

def hide_input_widgets():
    """
    入力欄やラベル、スタートボタンなどを非表示 (place_forget) にする
    """
    label_h.place_forget()
    entry_h.place_forget()
    label_m.place_forget()
    entry_m.place_forget()
    label_s.place_forget()
    entry_s.place_forget()
    btn_start.place_forget()

def set_time_and_start():
    """
    入力された 時・分・秒 を取得して datetime.timedelta に変換し、
    タイマースレッドを起動する。
    同時に、入力画面を消して時計のみ表示。
    """
    global countdown_duration, timer_thread

    try:
        # 入力値を取得し、数値へ変換
        hours = int(entry_h.get().strip()) if entry_h.get().strip().isdigit() else 0
        minutes = int(entry_m.get().strip()) if entry_m.get().strip().isdigit() else 0
        seconds = int(entry_s.get().strip()) if entry_s.get().strip().isdigit() else 0
    except ValueError:
        # 不正な入力値の場合はタイマースタートしない
        return
    
    # 指定された時間を timedelta で保持
    countdown_duration = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
    
    # タイマーの初期時間が 0 の場合は開始しない
    if countdown_duration.total_seconds() <= 0:
        return

    # ----- 入力画面を消す -----
    hide_input_widgets()
    
    # ----- タイマースレッド開始 -----
    timer_thread = threading.Thread(target=countdown_and_countup, daemon=True)
    timer_thread.start()

# ------ Escape キーでアプリを終了 ------
def exit_app(event):
    root.destroy()

root.bind("<Escape>", exit_app)

# ------ メインループ開始 ------
root.mainloop()
