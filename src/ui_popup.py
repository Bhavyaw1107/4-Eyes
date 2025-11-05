#src/ui_popup.py
import tkinter as tk
from tkinter import font
import pyautogui
import platform

class AlertPopup:
    def __init__(self):
        self.popup_window = None
        self.is_visible = False
        
        # Modern color scheme
        self.bg_color = "#ff4757"
        self.dark_bg = "#ee5a6f"
        self.text_color = "#ffffff"
        self.button_primary = "#2ed573"
        self.button_secondary = "#1e90ff"
        self.button_tertiary = "#ffa502"
    
    def show_alert(self):
        """Show the alert popup"""
        if self.is_visible:
            return
        
        self.is_visible = True
        
        # Create popup window
        self.popup_window = tk.Toplevel()
        self.popup_window.title("Privacy Alert")
        
        # Window properties
        self.popup_window.attributes('-topmost', True)
        self.popup_window.overrideredirect(True)
        
        # Window dimensions
        window_width = 650
        window_height = 380
        
        # Center on screen
        screen_width = self.popup_window.winfo_screenwidth()
        screen_height = self.popup_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.popup_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.popup_window.configure(bg=self.bg_color)
        
        # Shadow/border effect
        border_frame = tk.Frame(
            self.popup_window,
            bg="#c23616",
            bd=0
        )
        border_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        
        # Main content frame
        content_frame = tk.Frame(border_frame, bg=self.bg_color, padx=30, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Warning icon container
        icon_container = tk.Frame(content_frame, bg=self.dark_bg, relief=tk.FLAT)
        icon_container.pack(pady=(0, 20))
        
        # Single eye icon in the middle
        icon_label = tk.Label(
            icon_container,
            text="👁️",
            font=("Arial", 48),
            bg=self.dark_bg,
            fg=self.text_color,
            padx=30,
            pady=15
        )
        icon_label.pack()
        
        # Alert title
        title_label = tk.Label(
            content_frame,
            text="⚠️ PRIVACY ALERT",
            font=("Segoe UI", 20, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title_label.pack(pady=(0, 15))
        
        # Main warning text
        main_text = "Dhyan se bhai! Piche koi dekh raha hai\nteri screen ki taraf!"
        main_label = tk.Label(
            content_frame,
            text=main_text,
            font=("Segoe UI", 15, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            justify=tk.CENTER
        )
        main_label.pack(pady=(0, 10))
        
        # Subtext
        subtext = "4 Eyes ne detect kiya — Choose your action wisely"
        sub_label = tk.Label(
            content_frame,
            text=subtext,
            font=("Segoe UI", 11),
            bg=self.bg_color,
            fg="#ffe5e5",
            justify=tk.CENTER
        )
        sub_label.pack(pady=(0, 25))
        
        # Button frame (3 buttons in a row)
        button_frame = tk.Frame(content_frame, bg=self.bg_color)
        button_frame.pack(pady=(0, 10))
        
        # Button styling function
        def create_button(parent, text, bg_color, hover_color, command):
            btn = tk.Button(
                parent,
                text=text,
                font=("Segoe UI", 11, "bold"),
                bg=bg_color,
                fg="white",
                activebackground=hover_color,
                activeforeground="white",
                relief=tk.FLAT,
                bd=0,
                padx=25,
                pady=12,
                cursor="hand2",
                command=command
            )
            
            # Hover effects
            btn.bind('<Enter>', lambda e: btn.config(bg=hover_color))
            btn.bind('<Leave>', lambda e: btn.config(bg=bg_color))
            
            return btn
        
        # Chalega button (dismiss)
        chalega_btn = create_button(
            button_frame,
            "Chalega",
            self.button_primary,
            "#26de81",
            self._on_chalega_click
        )
        chalega_btn.pack(side=tk.LEFT, padx=8)
        
        # Lock Screen button (middle)
        lock_btn = create_button(
            button_frame,
            "Lock Screen",
            self.button_tertiary,
            "#ff9234",
            self._on_lock_click
        )
        lock_btn.pack(side=tk.LEFT, padx=8)
        
        # Show Desktop button
        desktop_btn = create_button(
            button_frame,
            "Show Desktop",
            self.button_secondary,
            "#3742fa",
            self._on_back_click
        )
        desktop_btn.pack(side=tk.LEFT, padx=8)
        
        # Keyboard shortcuts info
        shortcut_label = tk.Label(
            content_frame,
            text="ESC to dismiss",
            font=("Segoe UI", 8),
            bg=self.bg_color,
            fg="#ffe5e5"
        )
        shortcut_label.pack(pady=(10, 0))
        
        # Bind escape key
        self.popup_window.bind('<Escape>', lambda e: self._on_chalega_click())
        
        # Focus window
        self.popup_window.focus_force()
    
    def _on_chalega_click(self):
        """Handle Chalega button - just dismiss popup"""
        self.hide_alert()
    
    def _on_lock_click(self):
        """Handle Lock Screen button - lock the computer"""
        self.hide_alert()
        
        system = platform.system()
        
        try:
            if system == "Windows":
                # Windows: Win+L to lock
                pyautogui.hotkey('win', 'l')
            elif system == "Darwin":  # macOS
                # macOS: Control+Command+Q to lock
                pyautogui.hotkey('ctrl', 'command', 'q')
            else:  # Linux
                # Linux: Ctrl+Alt+L to lock (common in many DEs)
                pyautogui.hotkey('ctrl', 'alt', 'l')
        except Exception as e:
            print(f"Error locking screen: {e}")
    
    def _on_back_click(self):
        """Handle Show Desktop button - minimize all windows"""
        self.hide_alert()
        
        system = platform.system()
        
        try:
            if system == "Windows":
                # Windows: Win+D to show desktop
                pyautogui.hotkey('win', 'd')
            elif system == "Darwin":  # macOS
                # macOS: F11 or Mission Control
                pyautogui.hotkey('fn', 'f11')
            else:  # Linux
                # Linux: Ctrl+Alt+D or Super+D
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