import tkinter as tk
from tkinter import font
import pyautogui
import platform

class AlertPopup:
    def __init__(self):
        self.popup_window = None
        self.is_visible = False
    
    def show_alert(self):
        """Alert popup dikhao - jab koi screen dekh raha ho"""
        if self.is_visible:
            return  # Agar pehle se dikha hua hai to dobara mat dikhao
        
        self.is_visible = True
        
        # Popup window create karo
        self.popup_window = tk.Toplevel()
        self.popup_window.title("Alert!")
        
        # Window ko sabse upar rakho - kisi bhi window ke upar dikhe
        self.popup_window.attributes('-topmost', True)
        
        # Window decorations hata do - cleaner look ke liye
        self.popup_window.overrideredirect(True)
        
        # Window size set karo
        window_width = 700
        window_height = 280
        
        # Screen ke center me rakho
        screen_width = self.popup_window.winfo_screenwidth()
        screen_height = self.popup_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.popup_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Modern color scheme - Warning orange/red gradient
        bg_gradient_top = "#ff6b6b"    # Light red
        bg_gradient_bottom = "#ee5a6f"  # Deeper red
        border_color = "#c44569"        # Dark red border
        
        self.popup_window.configure(bg=bg_gradient_top)
        
        # Outer border frame - 3D effect ke liye
        border_frame = tk.Frame(
            self.popup_window,
            bg=border_color,
            bd=0
        )
        border_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        
        # Inner content frame
        content_frame = tk.Frame(border_frame, bg=bg_gradient_top, padx=25, pady=25)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Warning title - main heading
        title_label = tk.Label(
            content_frame,
            text="Dhyan se bhai koi tere PC ko\npiche se dekh raha hai!",
            font=("Segoe UI", 20, "bold"),
            bg=bg_gradient_top,
            fg="white",
            justify=tk.CENTER
        )
        title_label.pack(pady=(10, 20))
        
        # Subtext - additional info
        subtext = "KaunHaiBe ne pakad liya! Privacy chahiye to action lo."
        sub_label = tk.Label(
            content_frame,
            text=subtext,
            font=("Segoe UI", 12),
            bg=bg_gradient_top,
            fg="#fff9f9",
            justify=tk.CENTER
        )
        sub_label.pack(pady=(0, 25))
        
        # Button container - dono buttons yaha rahenge
        button_frame = tk.Frame(content_frame, bg=bg_gradient_top)
        button_frame.pack()
        
        # Button 1: Chalega - popup dismiss karne ke liye
        chalega_btn = tk.Button(
            button_frame,
            text="Chalega",
            font=("Segoe UI", 13, "bold"),
            bg="#00b894",  # Green
            fg="white",
            activebackground="#00a383",
            activeforeground="white",
            relief=tk.FLAT,
            padx=40,
            pady=12,
            cursor="hand2",
            borderwidth=0,
            command=self._on_chalega_click
        )
        chalega_btn.pack(side=tk.LEFT, padx=12)
        
        # Button 2: Minimize Page - window minimize karne ke liye
        minimize_btn = tk.Button(
            button_frame,
            text="Minimize Page",
            font=("Segoe UI", 13, "bold"),
            bg="#0984e3",  # Blue
            fg="white",
            activebackground="#0770c4",
            activeforeground="white",
            relief=tk.FLAT,
            padx=40,
            pady=12,
            cursor="hand2",
            borderwidth=0,
            command=self._on_minimize_click
        )
        minimize_btn.pack(side=tk.LEFT, padx=12)
        
        # Escape key se bhi popup band ho sake
        self.popup_window.bind('<Escape>', lambda e: self._on_chalega_click())
        
        # Window ko focus do
        self.popup_window.focus_force()
    
    def _on_chalega_click(self):
        """Chalega button click - popup band karo aur monitoring chalne do"""
        print("→ User ne 'Chalega' click kiya - popup band ho rahi hai")
        self.hide_alert()
    
    def _on_minimize_click(self):
        """Minimize Page button click - current window minimize karo"""
        print("→ User ne 'Minimize Page' click kiya - windows minimize ho rahi hain")
        self.hide_alert()  # Pehle popup band karo
        
        # OS ke according minimize karo
        system = platform.system()
        
        try:
            if system == "Windows":
                # Windows: Win+D se desktop dikha do
                pyautogui.hotkey('win', 'd')
                print("✓ Windows minimize ho gaye")
            elif system == "Darwin":  # macOS
                # macOS: Command+M ya Mission Control
                pyautogui.hotkey('command', 'm')
                print("✓ macOS window minimize ho gayi")
            else:  # Linux
                # Linux: desktop environment ke according
                try:
                    pyautogui.hotkey('super', 'd')  # Most Linux DEs
                except:
                    pyautogui.hotkey('ctrl', 'alt', 'd')  # Fallback
                print("✓ Linux windows minimize ho gayi")
        except Exception as e:
            print(f"⚠ Warning: Windows minimize nahi ho payi - {e}")
    
    def hide_alert(self):
        """Popup ko hide karo - jab zarurat na ho"""
        if not self.is_visible:
            return  # Agar pehle se hi band hai to kuch mat karo
        
        self.is_visible = False
        
        if self.popup_window:
            try:
                self.popup_window.destroy()
                print("✓ Popup successfully band ho gayi")
            except Exception as e:
                print(f"⚠ Popup destroy karne me issue: {e}")
            self.popup_window = None
    
    def is_showing(self):
        """Check karo ki popup dikha hua hai ya nahi"""
        return self.is_visible