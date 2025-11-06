import tkinter as tk
from tkinter import font, messagebox
from monitor import Monitor
from ui_popup import AlertPopup
import sys

class FourEyesApp:
    def __init__(self):
        # Main window banao
        self.root = tk.Tk()
        self.root.title("KaunHaiBe!")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        
        # Modern gradient-style colors - Dark purple se light purple
        self.bg_primary = "#1a1a2e"      # Deep dark blue-purple
        self.bg_secondary = "#16213e"    # Slightly lighter
        self.accent_color = "#0f3460"    # Blue accent
        self.text_primary = "#eaeaea"    # Light text
        self.text_secondary = "#94a1b2"  # Muted text
        self.active_green = "#00d9ff"    # Cyan blue for active state
        self.button_color = "#e94560"    # Red-pink for button
        
        self.root.configure(bg=self.bg_primary)
        
        # Monitor aur popup initialize karo
        self.monitor = Monitor()
        self.monitor.register_callback(self._on_alert_event)
        self.popup = AlertPopup()
        
        self.is_active = False
        
        # UI elements banao
        self._create_ui()
        
        # Window close pe cleanup karo
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Keyboard shortcuts bind karo
        self.root.bind('q', lambda e: self._on_close())
        self.root.bind('Q', lambda e: self._on_close())
    
    def _create_ui(self):
        """Main UI elements create karo - sab kuch yaha design hoga"""
        # Main container frame
        main_frame = tk.Frame(self.root, bg=self.bg_primary)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        # Top section - Title area
        title_frame = tk.Frame(main_frame, bg=self.bg_primary)
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Main title - "KaunHaiBe!"
        title_label = tk.Label(
            title_frame,
            text="KaunHaiBe!",
            font=("Segoe UI", 36, "bold"),
            bg=self.bg_primary,
            fg=self.text_primary
        )
        title_label.pack(pady=(10, 5))
        
        # Subtitle - description
        subtitle_label = tk.Label(
            title_frame,
            text="Ab har nazar pe nazar hai",
            font=("Segoe UI", 12),
            bg=self.bg_primary,
            fg=self.text_secondary
        )
        subtitle_label.pack()
        
        # Middle section - Status display
        status_container = tk.Frame(main_frame, bg=self.bg_secondary, height=80)
        status_container.pack(fill=tk.X, pady=(0, 25))
        status_container.pack_propagate(False)
        
        # Status indicator aur text
        status_inner = tk.Frame(status_container, bg=self.bg_secondary)
        status_inner.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.status_dot = tk.Label(
            status_inner,
            text="●",
            font=("Arial", 24),
            bg=self.bg_secondary,
            fg="#5a5a5a"  # Gray jab inactive ho
        )
        self.status_dot.pack(side=tk.LEFT, padx=(0, 15))
        
        self.status_label = tk.Label(
            status_inner,
            text="Abhi Band Hai",
            font=("Segoe UI", 14, "bold"),
            bg=self.bg_secondary,
            fg=self.text_secondary
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Bottom section - Activate button (main action)
        button_frame = tk.Frame(main_frame, bg=self.bg_primary)
        button_frame.pack(pady=20)
        
        self.toggle_button = tk.Button(
            button_frame,
            text="Activate",
            font=("Segoe UI", 16, "bold"),
            bg=self.button_color,
            fg="white",
            activebackground="#d63447",
            activeforeground="white",
            relief=tk.FLAT,
            padx=60,
            pady=18,
            cursor="hand2",
            borderwidth=0,
            command=self._toggle_monitoring
        )
        self.toggle_button.pack()
    
    def _toggle_monitoring(self):
        """Monitoring ko on/off karo - button click pe"""
        if not self.is_active:
            # Monitoring shuru karo
            success = self.monitor.start()
            if success:
                self.is_active = True
                # Button ka text aur color change karo
                self.toggle_button.config(
                    text="Deactivate",
                    bg="#2d3436"  # Dark gray jab active
                )
                # Status indicator ko green karo
                self.status_dot.config(fg=self.active_green)
                self.status_label.config(
                    text="Chal Raha Hai...",
                    fg=self.active_green
                )
                print("✓ Monitoring activate ho gayi")
            else:
                # Agar webcam nahi mila
                messagebox.showerror(
                    "Error",
                    "Webcam start nahi hua. Check karo camera connected hai ya nahi."
                )
        else:
            # Monitoring band karo
            self.monitor.stop()
            self.popup.hide_alert()  # Agar popup khula hai to band karo
            self.is_active = False
            # Button ko wapas original state me lao
            self.toggle_button.config(
                text="Activate",
                bg=self.button_color
            )
            # Status indicator ko gray karo
            self.status_dot.config(fg="#5a5a5a")
            self.status_label.config(
                text="Abhi Band Hai",
                fg=self.text_secondary
            )
            print("✗ Monitoring deactivate ho gayi")
    
    def _on_alert_event(self, event):
        """Alert events handle karo - jab koi dekh raha ho"""
        if event.get("alert"):
            # Popup dikhao - koi dekh raha hai!
            print("⚠ ALERT! Koi dekh raha hai - popup dikha rahe hain")
            self.popup.show_alert()
        else:
            # Popup hide karo - ab koi nahi dekh raha
            print("✓ Safe hai - popup band kar rahe hain")
            self.popup.hide_alert()
    
    def _on_close(self):
        """Application band karne pe cleanup karo"""
        print("\n=== Application band ho rahi hai ===")
        
        # Monitoring band karo agar chal rahi hai
        if self.is_active:
            self.monitor.stop()
        
        # Popup hide karo
        self.popup.hide_alert()
        
        # Resources cleanup karo
        self.monitor.cleanup()
        
        # Window destroy karo aur exit karo
        self.root.quit()
        self.root.destroy()
        sys.exit(0)
    
    def run(self):
        """Application ko start karo"""
        print("\n" + "="*50)
        print("🔷 KaunHaiBe! Application Start Ho Gayi")
        print("="*50)
        print("➤ 'Activate' button dabao monitoring shuru karne ke liye")
        print("="*50 + "\n")
        self.root.mainloop()

# Main entry point - yaha se program start hota hai
if __name__ == "__main__":
    try:
        print("=" * 50)
        print("Starting KaunHaiBe Application...")
        print("=" * 50)
        app = FourEyesApp()
        app.run()
    except Exception as e:
        print(f"\n❌ ERROR: Application fail ho gayi!")
        print(f"Error details: {e}")
        import traceback
        traceback.print_exc()
        input("\nEnter dabao exit karne ke liye...")
        sys.exit(1)