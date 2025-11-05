import tkinter as tk
from tkinter import font
import pyautogui
import platform

class AlertPopup:
    def __init__(self):
        self.popup_window = None
        self.is_visible = False
    
    def show_alert(self):
        """Show the alert popup"""
        if self.is_visible:
            return
        
        self.is_visible = True
        
        # Create popup window
        self.popup_window = tk.Toplevel()
        self.popup_window.title("4 Eyes Alert")
        
        # Make window stay on top
        self.popup_window.attributes('-topmost', True)
        
        # Remove window decorations for cleaner look
        self.popup_window.overrideredirect(True)
        
        # Set window size
        window_width = 600
        window_height = 250
        
        # Center on screen
        screen_width = self.popup_window.winfo_screenwidth()
        screen_height = self.popup_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.popup_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Set background color (warning orange/red)
        bg_color = "#FF6B6B"
        self.popup_window.configure(bg=bg_color)
        
        # Add border
        border_frame = tk.Frame(
            self.popup_window, 
            bg="#D63031", 
            bd=0, 
            highlightthickness=3,
            highlightbackground="#D63031"
        )
        border_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Main content frame
        content_frame = tk.Frame(border_frame, bg=bg_color, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Alert icon/emoji
        icon_label = tk.Label(
            content_frame,
            text="👁️👁️ ⚠️",
            font=("Arial", 32),
            bg=bg_color,
            fg="white"
        )
        icon_label.pack(pady=(0, 10))
        
        # Main warning text (Hindi)
        main_text = "Dhyan se bhai piche koi dekh raha hai\nteri screen ki taraf!"
        main_label = tk.Label(
            content_frame,
            text=main_text,
            font=("Arial", 16, "bold"),
            bg=bg_color,
            fg="white",
            justify=tk.CENTER
        )
        main_label.pack(pady=(0, 15))
        
        # Subtext
        subtext = "4 Eyes ne detect kiya — agar tu kaam chahte hai\ntoh 'Back' dabao."
        sub_label = tk.Label(
            content_frame,
            text=subtext,
            font=("Arial", 11),
            bg=bg_color,
            fg="white",
            justify=tk.CENTER
        )
        sub_label.pack(pady=(0, 20))
        
        # Button frame
        button_frame = tk.Frame(content_frame, bg=bg_color)
        button_frame.pack()
        
        # Chalega button
        chalega_btn = tk.Button(
            button_frame,
            text="Chalega",
            font=("Arial", 12, "bold"),
            bg="#00B894",
            fg="white",
            activebackground="#00A383",
            activeforeground="white",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2",
            command=self._on_chalega_click
        )
        chalega_btn.pack(side=tk.LEFT, padx=10)
        
        # Back button
        back_btn = tk.Button(
            button_frame,
            text="Back",
            font=("Arial", 12, "bold"),
            bg="#0984E3",
            fg="white",
            activebackground="#0770C4",
            activeforeground="white",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2",
            command=self._on_back_click
        )
        back_btn.pack(side=tk.LEFT, padx=10)
        
        # Bind escape key to close
        self.popup_window.bind('<Escape>', lambda e: self._on_chalega_click())
        
        # Focus the window
        self.popup_window.focus_force()
    
    def _on_chalega_click(self):
        """Handle Chalega button click - just dismiss popup"""
        self.hide_alert()
    
    def _on_back_click(self):
        """Handle Back button click - minimize all windows"""
        self.hide_alert()
        
        # Show desktop based on OS
        system = platform.system()
        
        try:
            if system == "Windows":
                # Windows: Win+D to show desktop
                pyautogui.hotkey('win', 'd')
            elif system == "Darwin":  # macOS
                # macOS: F11 or Mission Control
                pyautogui.hotkey('fn', 'f11')
            else:  # Linux
                # Linux: Ctrl+Alt+D or Super+D depending on desktop environment
                try:
                    pyautogui.hotkey('ctrl', 'alt', 'd')
                except:
                    pyautogui.hotkey('super', 'd')
        except Exception as e:
            print(f"Error minimizing windows: {e}")
    
    def hide_alert(self):
        """Hide the alert popup"""
        if not self.is_visible:
            return
        
        self.is_visible = False
        
        if self.popup_window:
            try:
                self.popup_window.destroy()
            except:
                pass
            self.popup_window = None
    
    def is_showing(self):
        """Check if popup is currently visible"""
        return self.is_visible