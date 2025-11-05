#src/ui_app.py
import tkinter as tk
from tkinter import font, messagebox
from monitor import Monitor
from ui_popup import AlertPopup
import sys

class FourEyesApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("4 Eyes - Privacy Monitor")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        
        # Modern color scheme
        self.bg_color = "#1a1a2e"
        self.accent_color = "#16213e"
        self.primary_color = "#0f3460"
        self.success_color = "#00d9ff"
        self.danger_color = "#e94560"
        self.text_color = "#eaeaea"
        self.secondary_text = "#94a1b2"
        
        self.root.configure(bg=self.bg_color)
        
        # Initialize monitor and popup
        self.monitor = Monitor()
        self.monitor.register_callback(self._on_alert_event)
        self.popup = AlertPopup()
        
        self.is_active = False
        
        # Create UI elements
        self._create_ui()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Bind keyboard shortcuts
        self.root.bind('q', lambda e: self._on_close())
        self.root.bind('Q', lambda e: self._on_close())
    
    def _create_ui(self):
        """Create the main UI elements"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        # Header frame with gradient effect simulation
        header_frame = tk.Frame(main_frame, bg=self.accent_color, relief=tk.FLAT)
        header_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="4 EYES",
            font=("Segoe UI", 32, "bold"),
            bg=self.accent_color,
            fg=self.success_color,
            pady=15
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Privacy Monitor System",
            font=("Segoe UI", 11),
            bg=self.accent_color,
            fg=self.secondary_text,
            pady=(0, 10)
        )
        subtitle_label.pack()
        
        # Status card
        status_card = tk.Frame(
            main_frame, 
            bg=self.primary_color, 
            relief=tk.FLAT,
            bd=0
        )
        status_card.pack(fill=tk.X, pady=(0, 25), ipady=15)
        
        # Status content frame
        status_content = tk.Frame(status_card, bg=self.primary_color)
        status_content.pack()
        
        # Status indicator
        self.status_indicator = tk.Label(
            status_content,
            text="●",
            font=("Arial", 24),
            bg=self.primary_color,
            fg=self.secondary_text
        )
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 12))
        
        # Status text frame
        status_text_frame = tk.Frame(status_content, bg=self.primary_color)
        status_text_frame.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(
            status_text_frame,
            text="INACTIVE",
            font=("Segoe UI", 14, "bold"),
            bg=self.primary_color,
            fg=self.text_color
        )
        self.status_label.pack(anchor=tk.W)
        
        self.status_sublabel = tk.Label(
            status_text_frame,
            text="Click activate to start monitoring",
            font=("Segoe UI", 9),
            bg=self.primary_color,
            fg=self.secondary_text
        )
        self.status_sublabel.pack(anchor=tk.W)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(pady=10)
        
        # Activate/Deactivate button with modern styling
        self.toggle_button = tk.Button(
            button_frame,
            text="ACTIVATE MONITORING",
            font=("Segoe UI", 13, "bold"),
            bg=self.success_color,
            fg=self.bg_color,
            activebackground="#00b8d4",
            activeforeground=self.bg_color,
            relief=tk.FLAT,
            bd=0,
            padx=50,
            pady=18,
            cursor="hand2",
            command=self._toggle_monitoring
        )
        self.toggle_button.pack()
        
        # Add hover effect
        self.toggle_button.bind('<Enter>', self._on_button_hover)
        self.toggle_button.bind('<Leave>', self._on_button_leave)
        
        # Info section
        info_frame = tk.Frame(main_frame, bg=self.bg_color)
        info_frame.pack(side=tk.BOTTOM, pady=(25, 0))
        
        info_label = tk.Label(
            info_frame,
            text="Press 'Q' to quit application",
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg=self.secondary_text
        )
        info_label.pack()
    
    def _on_button_hover(self, event):
        """Button hover effect"""
        if not self.is_active:
            self.toggle_button.config(bg="#00b8d4")
        else:
            self.toggle_button.config(bg="#d63447")
    
    def _on_button_leave(self, event):
        """Button leave effect"""
        if not self.is_active:
            self.toggle_button.config(bg=self.success_color)
        else:
            self.toggle_button.config(bg=self.danger_color)
    
    def _toggle_monitoring(self):
        """Toggle monitoring on/off"""
        if not self.is_active:
            # Activate monitoring
            success = self.monitor.start()
            if success:
                self.is_active = True
                self.toggle_button.config(
                    text="DEACTIVATE MONITORING",
                    bg=self.danger_color,
                    activebackground="#d63447"
                )
                self.status_indicator.config(fg=self.success_color)
                self.status_label.config(
                    text="ACTIVE",
                    fg=self.success_color
                )
                self.status_sublabel.config(
                    text="System is monitoring for privacy threats"
                )
                print("Monitoring activated")
            else:
                messagebox.showerror(
                    "Error",
                    "Failed to start monitoring. Please check your webcam."
                )
        else:
            # Deactivate monitoring
            self.monitor.stop()
            self.popup.hide_alert()
            self.is_active = False
            self.toggle_button.config(
                text="ACTIVATE MONITORING",
                bg=self.success_color,
                activebackground="#00b8d4"
            )
            self.status_indicator.config(fg=self.secondary_text)
            self.status_label.config(
                text="INACTIVE",
                fg=self.text_color
            )
            self.status_sublabel.config(
                text="Click activate to start monitoring"
            )
            print("Monitoring deactivated")
    
    def _on_alert_event(self, event):
        """Handle alert events from monitor"""
        if event.get("alert"):
            print("Alert triggered - showing popup")
            self.popup.show_alert()
        else:
            print("Alert cleared - hiding popup")
            self.popup.hide_alert()
    
    def _on_close(self):
        """Handle application close"""
        print("Closing application...")
        
        if self.is_active:
            self.monitor.stop()
        
        self.popup.hide_alert()
        self.monitor.cleanup()
        
        self.root.quit()
        self.root.destroy()
        sys.exit(0)
    
    def run(self):
        """Start the application"""
        print("=" * 50)
        print("4 Eyes Privacy Monitor Started")
        print("=" * 50)
        print("Press 'ACTIVATE' to start monitoring")
        print("Press 'Q' to quit")
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = FourEyesApp()
        app.run()
    except Exception as e:
        print(f"\nERROR: Application failed to start!")
        print(f"Error details: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)