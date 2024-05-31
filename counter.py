import tkinter as tk
from tkinter import ttk
import time

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer Application")
        self.root.configure(bg='#1E2A38')  # Darker blue-grey color

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # Countdown Timer Tab
        self.countdown_tab = tk.Frame(self.notebook, bg='#1E2A38')
        self.countdown_tab.pack(fill='both', expand=True)
        self.create_countdown_timer(self.countdown_tab)
        self.notebook.add(self.countdown_tab, text='Countdown Timer')

        # Stopwatch Tab
        self.stopwatch_tab = tk.Frame(self.notebook, bg='#1E2A38')
        self.stopwatch_tab.pack(fill='both', expand=True)
        self.create_stopwatch(self.stopwatch_tab)
        self.notebook.add(self.stopwatch_tab, text='Stopwatch')

        self.stopwatch_running = False
        self.stopwatch_start_time = 0

    def create_countdown_timer(self, parent):
        frame = tk.Frame(parent, bg='#1E2A38')
        frame.pack(expand=True)

        set_time_label = tk.Label(frame, text='Set Countdown Time (HH:MM:SS):',
                                   font=('Helvetica', 14, 'bold'), fg='white', bg='#1E2A38')
        set_time_label.pack(pady=10)

        self.countdown_time_var = tk.StringVar(value='00:00:00')
        self.time_entry = tk.Entry(frame, textvariable=self.countdown_time_var,
                                    font=('Helvetica', 48), justify='center')
        self.time_entry.pack(pady=20)

        self.countdown_label = tk.Label(frame, text='Time Left: 00:00:00',
                                         font=('Helvetica', 48, 'bold'), fg='white', bg='#1E2A38')
        self.countdown_label.pack(pady=20)

        self.start_countdown_button = tk.Button(frame, text='Start Countdown',
                                                 command=self.start_countdown, font=('Helvetica', 14, 'bold'),
                                                   fg='#1E2A38', bg='white', relief='flat')
        self.start_countdown_button.pack(pady=20)

    def start_countdown(self):
        time_str = self.countdown_time_var.get()
        try:
            h, m, s = map(int, time_str.split(':'))
            total_seconds = h * 3600 + m * 60 + s
            self.countdown(total_seconds)
        except ValueError:
            self.countdown_label.config(text="Invalid Time Format!")

    def countdown(self, remaining_seconds):
        if remaining_seconds > 0:
            mins, secs = divmod(remaining_seconds, 60)
            hours, mins = divmod(mins, 60)
            self.countdown_label.config(text=f'Time Left: {hours:02}:{mins:02}:{secs:02}')
            self.root.after(1000, self.countdown, remaining_seconds - 1)
        else:
            self.countdown_label.config(text='Time Left: 00:00:00')

    def create_stopwatch(self, parent):
        frame = tk.Frame(parent, bg='#1E2A38')
        frame.pack(expand=True)

        self.stopwatch_label = tk.Label(frame, text='00:00:00',
                                         font=('Helvetica', 48, 'bold'), fg='white', bg='#1E2A38')
        self.stopwatch_label.pack(pady=20)

        self.start_stopwatch_button = tk.Button(frame, text='Start', command=self.start_stopwatch,
                                                 font=('Helvetica', 14, 'bold'), fg='#1E2A38', bg='white', relief='flat')
        self.start_stopwatch_button.pack(side='left', padx=10, pady=20)

        self.stop_stopwatch_button = tk.Button(frame, text='Stop', command=self.stop_stopwatch,
                                                font=('Helvetica', 14, 'bold'), fg='#1E2A38', bg='white', relief='flat')
        self.stop_stopwatch_button.pack(side='left', padx=10, pady=20)

        self.reset_stopwatch_button = tk.Button(frame, text='Reset', command=self.reset_stopwatch, 
                                                font=('Helvetica', 14, 'bold'), fg='#1E2A38', bg='white', relief='flat')
        self.reset_stopwatch_button.pack(side='left', padx=10, pady=20)

    def start_stopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_start_time = time.time() - self.get_elapsed_time()
            self.update_stopwatch()
            self.stopwatch_running = True

    def stop_stopwatch(self):
        if self.stopwatch_running:
            self.root.after_cancel(self.stopwatch_update_job)
            self.stopwatch_running = False

    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_start_time = time.time()
        self.stopwatch_label.config(text='00:00:00')

    def update_stopwatch(self):
        elapsed_time = self.get_elapsed_time()
        mins, secs = divmod(int(elapsed_time), 60)
        hours, mins = divmod(mins, 60)
        self.stopwatch_label.config(text=f'{hours:02}:{mins:02}:{secs:02}')
        self.stopwatch_update_job = self.root.after(1000, self.update_stopwatch)

    def get_elapsed_time(self):
        return time.time() - self.stopwatch_start_time if self.stopwatch_running else 0

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
