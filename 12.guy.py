
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ไฟล์สำหรับบันทึกข้อมูลคงทน (Persistence File)
DATA_FILE = "grade_data.json"

DEFAULT_DATA = {
    "settings": {
        "lang": "TH",
        "noti_enable": True,
        "noti_weekly": True,
        "noti_sound": False,
        "freq": "รายสัปดาห์ (Weekly)",
        "day": "อาทิตย์",
        "time": "20:00 น."
    },
    "subjects": [
        {"cat": "STEM", "name": "Mathematics", "grade": "A", "score": 84, "target_score": 92, "credits": 4},
        {"cat": "HUMANITIES", "name": "English", "grade": "A", "score": 94, "target_score": 90, "credits": 3},
        {"cat": "STEM", "name": "Physics", "grade": "B+", "score": 78, "target_score": 88, "credits": 4},
        {"cat": "SOCIAL SCIENCE", "name": "History", "grade": "A-", "score": 89, "target_score": 90, "credits": 3}
    ]
}

GRADE_WEIGHTS = {
    "A": 4.0, "A-": 3.7, "B+": 3.5, "B": 3.0, 
    "B-": 2.7, "C+": 2.5, "C": 2.0, "D": 1.0, "F": 0.0
}

class GradeAlertApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("GradeAlert App - Complete System")
        self.geometry("420x800")
        self.resizable(False, False)
        self.configure(bg="#0D0714")

        # โหลดข้อมูลจากไฟล์ JSON
        self.data = self.load_data()
        
        self.current_lang = self.data["settings"]["lang"]
        self.current_page = "dashboard"

        # ตัวแปรระบบตั้งค่า
        s = self.data["settings"]
        self.var_noti_enable = tk.BooleanVar(value=s["noti_enable"])
        self.var_noti_weekly = tk.BooleanVar(value=s["noti_weekly"])
        self.var_noti_sound = tk.BooleanVar(value=s["noti_sound"])
        self.var_day = tk.StringVar(value=s["day"])
        self.var_time = tk.StringVar(value=s["time"])

        # พจนานุกรม 2 ภาษา
        self.translations = {
            "TH": {
                "title_dashboard": "เกรดของฉัน",
                "title_settings": "การตั้งค่า",
                "gpa_summary": "สรุปเกรดเฉลี่ย",
                "target_gpa": "เกรดเป้าหมาย",
                "current_gpa": "เกรดปัจจุบัน",
                "missing_points": "คะแนนที่ขาด",
                "target_badge": "เป้าหมาย 3.6",
                "track_grades": "ติดตามเกรด",
                "btn_add_sub": "➕ เพิ่มวิชาใหม่",
                "btn_test_noti": "🔔 ทดสอบยิงแจ้งเตือน Windows",
                "btn_save_sett": "💾 บันทึกการตั้งค่า",
                "nav_dashboard": "แดชบอร์ด",
                "nav_settings": "ตั้งค่า",
                "lang_section": "ภาษา / Language",
                "noti_section": "ระบบการแจ้งเตือน",
                "noti_enable": "เปิดการแจ้งเตือนระบบ",
                "noti_weekly": "รายงานผลรายสัปดาห์",
                "noti_sound": "เปิดเสียงกระดิ่งเตือน",
                "schedule_section": "ตั้งเวลาแจ้งเตือน",
                "day_label": "เลือกวัน:",
                "time_label": "เลือกเวลา:",
                "theme_section": "ธีมระบบ: ม่วงเข้ม (Dark Purple)"
            },
            "EN": {
                "title_dashboard": "My Grades",
                "title_settings": "Settings",
                "gpa_summary": "GPA Summary",
                "target_gpa": "Target GPA",
                "current_gpa": "Current GPA",
                "missing_points": "Points Needed",
                "target_badge": "Target 3.6",
                "track_grades": "Track Grades",
                "btn_add_sub": "➕ Add New Subject",
                "btn_test_noti": "🔔 Test Windows Notification",
                "btn_save_sett": "💾 Save Settings",
                "nav_dashboard": "Dashboard",
                "nav_settings": "Settings",
                "lang_section": "Language",
                "noti_section": "Notifications System",
                "noti_enable": "Enable System Alerts",
                "noti_weekly": "Weekly Alert Report",
                "noti_sound": "Enable Alert Sound",
                "schedule_section": "Alert Schedule",
                "day_label": "Select Day:",
                "time_label": "Select Time:",
                "theme_section": "System Theme: Dark Purple"
            }
        }

        # Layout Frames
        self.header_frame = tk.Frame(self, bg="#0D0714")
        self.header_frame.pack(fill="x", padx=20, pady=(15, 10))

        self.content_frame = tk.Frame(self, bg="#0D0714")
        self.content_frame.pack(fill="both", expand=True, padx=15)

        self.build_bottom_nav()
        self.render_header()
        self.render_dashboard()

    # --- ระบบ JSON Persistence ---
    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return DEFAULT_DATA
        return DEFAULT_DATA

    def save_data(self):
        self.data["settings"]["lang"] = self.current_lang
        self.data["settings"]["noti_enable"] = self.var_noti_enable.get()
        self.data["settings"]["noti_weekly"] = self.var_noti_weekly.get()
        self.data["settings"]["noti_sound"] = self.var_noti_sound.get()
        self.data["settings"]["day"] = self.var_day.get()
        self.data["settings"]["time"] = self.var_time.get()

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    # --- คำนวณ GPA & คะแนนส่วนขาด ---
    def calculate_stats(self):
        total_credits = sum(sub["credits"] for sub in self.data["subjects"])
        if total_credits == 0:
            return "0.00", 0

        weighted_grade = sum(GRADE_WEIGHTS.get(sub["grade"], 0.0) * sub["credits"] for sub in self.data["subjects"])
        current_gpa = weighted_grade / total_credits

        total_missing = sum(max(0, sub["target_score"] - sub["score"]) for sub in self.data["subjects"])
        return f"{current_gpa:.2f}", int(total_missing)

    # --- UI Rendering ---
    def toggle_language(self, lang=None):
        if lang:
            self.current_lang = lang
        else:
            self.current_lang = "EN" if self.current_lang == "TH" else "TH"
        self.save_data()
        self.render_header()
        if self.current_page == "dashboard":
            self.render_dashboard()
        else:
            self.render_settings()

    def render_header(self):
        for widget in self.header_frame.winfo_children():
            widget.destroy()

        t = self.translations[self.current_lang]
        title_text = t["title_dashboard"] if self.current_page == "dashboard" else t["title_settings"]

        lbl_title = tk.Label(self.header_frame, text=title_text, font=("Tahoma", 18, "bold"), fg="white", bg="#0D0714")
        lbl_title.pack(side="left")

        btn_lang = tk.Button(
            self.header_frame, 
            text=f"🌐 {self.current_lang}", 
            font=("Tahoma", 10, "bold"),
            fg="white", bg="#1E142B", activebackground="#2D1F40", activeforeground="white",
            bd=0, relief="flat", padx=10, pady=4,
            command=self.toggle_language
        )
        btn_lang.pack(side="right")

    def render_dashboard(self):
        self.current_page = "dashboard"
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        t = self.translations[self.current_lang]
        gpa_val, missing_val = self.calculate_stats()

        # Card สรุปเกรด
        card_summary = tk.Frame(self.content_frame, bg="#1A102A", bd=1, relief="solid")
        card_summary.pack(fill="x", pady=8)

        f_sum_head = tk.Frame(card_summary, bg="#1A102A")
        f_sum_head.pack(fill="x", padx=12, pady=(10, 0))
        tk.Label(f_sum_head, text=t["gpa_summary"], font=("Tahoma", 10), fg="#A199B8", bg="#1A102A").pack(side="left")
        
        badge_target = tk.Label(f_sum_head, text=t["target_badge"], font=("Tahoma", 9, "bold"), fg="white", bg="#5B21B6", padx=8, pady=2)
        badge_target.pack(side="right")

        f_stats = tk.Frame(card_summary, bg="#1A102A")
        f_stats.pack(fill="x", padx=12, pady=12)

        # Target GPA
        f_s1 = tk.Frame(f_stats, bg="#1A102A")
        f_s1.pack(side="left", expand=True)
        tk.Label(f_s1, text=t["target_gpa"], font=("Tahoma", 9), fg="#A199B8", bg="#1A102A").pack(anchor="w")
        tk.Label(f_s1, text="3.60", font=("Tahoma", 16, "bold"), fg="white", bg="#1A102A").pack(anchor="w")

        # Current GPA
        f_s2 = tk.Frame(f_stats, bg="#1A102A")
        f_s2.pack(side="left", expand=True)
        tk.Label(f_s2, text=t["current_gpa"], font=("Tahoma", 9), fg="#A199B8", bg="#1A102A").pack(anchor="w")
        tk.Label(f_s2, text=gpa_val, font=("Tahoma", 16, "bold"), fg="#10B981" if float(gpa_val)>=3.6 else "white", bg="#1A102A").pack(anchor="w")

        # Missing Points
        f_s3 = tk.Frame(f_stats, bg="#1A102A")
        f_s3.pack(side="left", expand=True)
        tk.Label(f_s3, text=t["missing_points"], font=("Tahoma", 9), fg="#A199B8", bg="#1A102A").pack(anchor="w")
        tk.Label(f_s3, text=str(missing_val), font=("Tahoma", 16, "bold"), fg="#F43F5E", bg="#1A102A").pack(anchor="w")

        # ปุ่มเพิ่มวิชาใหม่
        btn_add = tk.Button(
            self.content_frame, text=t["btn_add_sub"], font=("Tahoma", 10, "bold"),
            fg="white", bg="#8B5CF6", activebackground="#7C3AED", activeforeground="white",
            bd=0, pady=6, command=self.open_add_subject_dialog
        )
        btn_add.pack(fill="x", pady=(0, 6))

        # รายการวิชา
        f_track = tk.Frame(self.content_frame, bg="#0D0714")
        f_track.pack(fill="x", pady=(2, 6))
        tk.Label(f_track, text=t["track_grades"], font=("Tahoma", 13, "bold"), fg="white", bg="#0D0714").pack(side="left")
        tk.Label(f_track, text=f"{len(self.data['subjects'])} วิชา", font=("Tahoma", 9), fg="#8B7AA8", bg="#0D0714").pack(side="right")

        # Container แบบเลื่อนได้ (Scrollable Window)
        canvas = tk.Canvas(self.content_frame, bg="#0D0714", highlightthickness=0)
        scroll = tk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        sub_list_frame = tk.Frame(canvas, bg="#0D0714")

        sub_list_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sub_list_frame, anchor="nw", width=380)
        canvas.configure(yscrollcommand=scroll.set)

        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        for idx, sub in enumerate(self.data["subjects"]):
            card = tk.Frame(sub_list_frame, bg="#140D21", bd=1, relief="groove")
            card.pack(fill="x", pady=4, padx=2)

            f_r1 = tk.Frame(card, bg="#140D21")
            f_r1.pack(fill="x", padx=10, pady=(6, 2))
            tk.Label(f_r1, text=sub["cat"], font=("Tahoma", 8, "bold"), fg="#7C6A96", bg="#140D21").pack(side="left")
            
            # ปุ่มลบวิชา
            btn_del = tk.Button(f_r1, text="✕", font=("Tahoma", 8, "bold"), fg="#F43F5E", bg="#140D21", bd=0, command=lambda i=idx: self.delete_subject(i))
            btn_del.pack(side="right", padx=(5, 0))

            tk.Label(f_r1, text=f"Grade: {sub['grade']}", font=("Tahoma", 8, "bold"), fg="white", bg="#3B1566", padx=6).pack(side="right")

            f_r2 = tk.Frame(card, bg="#140D21")
            f_r2.pack(fill="x", padx=10, pady=2)
            tk.Label(f_r2, text=sub["name"], font=("Tahoma", 11, "bold"), fg="white", bg="#140D21").pack(side="left")
            tk.Label(f_r2, text=f"{sub['score']}/{sub['target_score']}", font=("Tahoma", 9), fg="#9CA3AF", bg="#140D21").pack(side="right")

            f_r3 = tk.Frame(card, bg="#140D21")
            f_r3.pack(fill="x", padx=10, pady=(2, 6))
            short = max(0, sub["target_score"] - sub["score"])
            st_text = f"ขาด {short} คะแนน" if short > 0 else "ผ่านเกณฑ์แล้ว"
            st_color = "#F43F5E" if short > 0 else "#10B981"
            
            tk.Label(f_r3, text=st_text, font=("Tahoma", 8, "bold"), fg=st_color, bg="#140D21").pack(side="left")
            tk.Label(f_r3, text=f"{sub['credits']} หน่วยกิต", font=("Tahoma", 8), fg="#7C6A96", bg="#140D21").pack(side="right")

    def render_settings(self):
        self.current_page = "settings"
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        t = self.translations[self.current_lang]

        # 1. ภาษา
        card_lang = tk.Frame(self.content_frame, bg="#140D21", bd=1, relief="groove")
        card_lang.pack(fill="x", pady=6, ipady=5)
        
        tk.Label(card_lang, text=t["lang_section"], font=("Tahoma", 11, "bold"), fg="white", bg="#140D21").pack(anchor="w", padx=12, pady=(6, 4))
        
        f_btns = tk.Frame(card_lang, bg="#140D21")
        f_btns.pack(anchor="w", padx=12)
        
        btn_th = tk.Button(f_btns, text="ภาษาไทย", font=("Tahoma", 9), fg="white", bg="#8B5CF6" if self.current_lang == "TH" else "#2D1F40", bd=0, padx=12, command=lambda: self.toggle_language("TH"))
        btn_th.pack(side="left", padx=(0, 5))

        btn_en = tk.Button(f_btns, text="English", font=("Tahoma", 9), fg="white", bg="#8B5CF6" if self.current_lang == "EN" else "#2D1F40", bd=0, padx=12, command=lambda: self.toggle_language("EN"))
        btn_en.pack(side="left")

        # 2. การแจ้งเตือน
        card_noti = tk.Frame(self.content_frame, bg="#140D21", bd=1, relief="groove")
        card_noti.pack(fill="x", pady=6, ipady=5)
        
        tk.Label(card_noti, text=t["noti_section"], font=("Tahoma", 11, "bold"), fg="white", bg="#140D21").pack(anchor="w", padx=12, pady=(6, 4))
        
        chk1 = tk.Checkbutton(card_noti, text=t["noti_enable"], variable=self.var_noti_enable, font=("Tahoma", 9), fg="white", bg="#140D21", selectcolor="#140D21", activebackground="#140D21", activeforeground="white")
        chk1.pack(anchor="w", padx=12, pady=2)

        chk2 = tk.Checkbutton(card_noti, text=t["noti_weekly"], variable=self.var_noti_weekly, font=("Tahoma", 9), fg="white", bg="#140D21", selectcolor="#140D21", activebackground="#140D21", activeforeground="white")
        chk2.pack(anchor="w", padx=12, pady=2)

        chk3 = tk.Checkbutton(card_noti, text=t["noti_sound"], variable=self.var_noti_sound, font=("Tahoma", 9), fg="white", bg="#140D21", selectcolor="#140D21", activebackground="#140D21", activeforeground="white")
        chk3.pack(anchor="w", padx=12, pady=2)

        # 3. กำหนดเวลา
        card_sch = tk.Frame(self.content_frame, bg="#140D21", bd=1, relief="groove")
        card_sch.pack(fill="x", pady=6, ipady=5)
        
        tk.Label(card_sch, text=t["schedule_section"], font=("Tahoma", 11, "bold"), fg="white", bg="#140D21").pack(anchor="w", padx=12, pady=(6, 4))
        
        f_day = tk.Frame(card_sch, bg="#140D21")
        f_day.pack(fill="x", padx=12, pady=2)
        tk.Label(f_day, text=t["day_label"], font=("Tahoma", 9), fg="#A199B8", bg="#140D21").pack(side="left")
        om_day = ttk.OptionMenu(f_day, self.var_day, self.var_day.get(), "จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์")
        om_day.pack(side="right")

        f_time = tk.Frame(card_sch, bg="#140D21")
        f_time.pack(fill="x", padx=12, pady=2)
        tk.Label(f_time, text=t["time_label"], font=("Tahoma", 9), fg="#A199B8", bg="#140D21").pack(side="left")
        om_time = ttk.OptionMenu(f_time, self.var_time, self.var_time.get(), "18:00 น.", "19:00 น.", "20:00 น.", "21:00 น.")
        om_time.pack(side="right")

        # ปุ่มบันทึกและปุ่มยิงแจ้งเตือน Windows
        btn_save = tk.Button(self.content_frame, text=t["btn_save_sett"], font=("Tahoma", 10, "bold"), fg="white", bg="#10B981", bd=0, pady=6, command=self.save_settings_action)
        btn_save.pack(fill="x", pady=(10, 4))

        btn_test = tk.Button(self.content_frame, text=t["btn_test_noti"], font=("Tahoma", 9, "bold"), fg="white", bg="#8B5CF6", bd=0, pady=6, command=self.send_windows_notification)
        btn_test.pack(fill="x")

    # --- ฟังก์ชันจัดการข้อมูลวิชา (CRUD) ---
    def open_add_subject_dialog(self):
        win = tk.Toplevel(self)
        win.title("เพิ่มวิชาใหม่")
        win.geometry("320x340")
        win.configure(bg="#1A102A")

        fields = [
            ("หมวดหมู่ (เช่น STEM):", "cat"),
            ("ชื่อวิชา:", "name"),
            ("เกรด (เช่น A, B+):", "grade"),
            ("คะแนนที่ได้:", "score"),
            ("คะแนนเป้าหมาย:", "target_score"),
            ("หน่วยกิต:", "credits")
        ]
        entries = {}

        for lbl_text, key in fields:
            f = tk.Frame(win, bg="#1A102A")
            f.pack(fill="x", padx=15, pady=3)
            tk.Label(f, text=lbl_text, font=("Tahoma", 9), fg="#A199B8", bg="#1A102A").pack(side="left")
            e = tk.Entry(f, width=15)
            e.pack(side="right")
            entries[key] = e

        def add_action():
            try:
                new_sub = {
                    "cat": entries["cat"].get().upper() or "GENERAL",
                    "name": entries["name"].get() or "วิชาใหม่",
                    "grade": entries["grade"].get().upper() or "A",
                    "score": float(entries["score"].get() or 0),
                    "target_score": float(entries["target_score"].get() or 100),
                    "credits": int(entries["credits"].get() or 3)
                }
                self.data["subjects"].append(new_sub)
                self.save_data()
                self.render_dashboard()
                win.destroy()
                messagebox.showinfo("สำเร็จ", "เพิ่มวิชาเรียบร้อยแล้ว!")
            except ValueError:
                messagebox.showerror("ผิดพลาด", "กรุณากรอกคะแนนและหน่วยกิตเป็นตัวเลข")

        tk.Button(win, text="บันทึกวิชา", font=("Tahoma", 10, "bold"), fg="white", bg="#8B5CF6", bd=0, pady=6, command=add_action).pack(pady=15)

    def delete_subject(self, index):
        if messagebox.askyesno("ยืนยัน", "คุณต้องการลบวิชานี้ใช่หรือไม่?"):
            del self.data["subjects"][index]
            self.save_data()
            self.render_dashboard()

    def save_settings_action(self):
        self.save_data()
        messagebox.showinfo("การตั้งค่า", "บันทึกข้อมูลเรียบร้อยแล้ว!")

    # --- ส่งแจ้งเตือน Native บน Windows ---
    def send_windows_notification(self):
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            gpa_val, missing_val = self.calculate_stats()
            toaster.show_toast(
                "GradeAlert Notification",
                f"เกรดปัจจุบัน: {gpa_val} | คะแนนที่ขาด: {missing_val} คะแนน",
                duration=5,
                threaded=True
            )
        except ImportError:
            # Fallback หากยังไม่ได้ลง win10toast
            gpa_val, missing_val = self.calculate_stats()
            messagebox.showinfo("GradeAlert Notification", f"🔔 แจ้งเตือนระบบ:\nGPA ปัจจุบัน: {gpa_val}\nคะแนนที่ต้องทำเพิ่ม: {missing_val} คะแนน")

    def build_bottom_nav(self):
        nav_frame = tk.Frame(self, bg="#180F26", bd=1, relief="raised")
        nav_frame.pack(side="bottom", fill="x", ipady=5)

        t = self.translations[self.current_lang]

        self.btn_nav_dash = tk.Button(
            nav_frame, text=f"📱 {t['nav_dashboard']}", font=("Tahoma", 10, "bold"),
            fg="#8B5CF6", bg="#180F26", bd=0, command=self.show_dashboard
        )
        self.btn_nav_dash.pack(side="left", expand=True)

        self.btn_nav_sett = tk.Button(
            nav_frame, text=f"⚙️ {t['nav_settings']}", font=("Tahoma", 10, "bold"),
            fg="#6B7280", bg="#180F26", bd=0, command=self.show_settings
        )
        self.btn_nav_sett.pack(side="right", expand=True)

    def show_dashboard(self):
        t = self.translations[self.current_lang]
        self.btn_nav_dash.config(fg="#8B5CF6", text=f"📱 {t['nav_dashboard']}")
        self.btn_nav_sett.config(fg="#6B7280", text=f"⚙️ {t['nav_settings']}")
        self.render_header()
        self.render_dashboard()

    def show_settings(self):
        t = self.translations[self.current_lang]
        self.btn_nav_sett.config(fg="#8B5CF6", text=f"⚙️ {t['nav_settings']}")
        self.btn_nav_dash.config(fg="#6B7280", text=f"📱 {t['nav_dashboard']}")
        self.render_header()
        self.render_settings()

if __name__ == "__main__":
    app = GradeAlertApp()
    app.mainloop()