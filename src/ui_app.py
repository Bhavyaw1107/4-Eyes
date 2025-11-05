import tkinter as tk
from tkinter import font, messagebox
from monitor import Monitor
from ui_popup import AlertPopup
import sys

class FourEyesApp:
    def _init_(self):
        self.root = tk.Tk()
        self.root.title("4 Eyes 👁👁")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Set background color
        bg_color = "#2C3E50"
        self.root.configure(bg=bg_color)
        
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
        # Main frame
        main_frame = tk.Frame(self.root, bg="#2C3E50")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Title with emoji
        title_label = tk.Label(
            main_frame,
            text="4 Eyes 👁👁",
            font=("Arial", 28, "bold"),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        title_label.pack(pady=(20, 10))
        
        # Tagline
        tagline_label = tk.Label(
            main_frame,
            text="Integrate 2 Eyes at Your Back",
            font=("Arial", 14, "italic"),
            bg="#2C3E50",
            fg="#BDC3C7"
        )
        tagline_label.pack(pady=(0, 30))
        
        # Status indicator
        self.status_frame = tk.Frame(main_frame, bg="#2C3E50")
        self.status_frame.pack(pady=(0, 20))
        
        self.status_indicator = tk.Label(
            self.status_frame,
            text="●",
            font=("Arial", 20),
            bg="#2C3E50",
            fg="#95A5A6"  # Gray when inactive
        )
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 10))
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Inactive",
            font=("Arial", 12),
            bg="#2C3E50",
            fg="#95A5A6"
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Activate/Deactivate button
        self.toggle_button = tk.Button(
            main_frame,
            text="Activate",
            font=("Arial", 14, "bold"),
            bg="#27AE60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            relief=tk.FLAT,
            padx=40,
            pady=15,
            cursor="hand2",
            command=self._toggle_monitoring
        )
        self.toggle_button.pack(pady=10)
        
        # Info label
        info_label = tk.Label(
            main_frame,
            text="Press 'q' to quit",
            font=("Arial", 9),
            bg="#2C3E50",
            fg="#7F8C8D"
        )
        info_label.pack(side=tk.BOTTOM, pady=(20, 0))
    
    def _toggle_monitoring(self):
        """Toggle monitoring on/off"""
        if not self.is_active:
            # Activate monitoring
            success = self.monitor.start()
            if success:
                self.is_active = True
                self.toggle_button.config(
                    text="Deactivate",
                    bg="#E74C3C",
                    activebackground="#C0392B"
                )
                self.status_indicator.config(fg="#27AE60")  # Green
                self.status_label.config(
                    text="Active - Monitoring...",
                    fg="#27AE60"
                )
                print("Monitoring activated")
            else:
                messagebox.showerror(
                    "Error",
                    "Failed to start monitoring. Check your webcam."
                )
        else:
            # Deactivate monitoring
            self.monitor.stop()
            self.popup.hide_alert()  # Hide any active popup
            self.is_active = False
            self.toggle_button.config(
                text="Activate",
                bg="#27AE60",
                activebackground="#229954"
            )
            self.status_indicator.config(fg="#95A5A6")  # Gray
            self.status_label.config(
                text="Inactive",
                fg="#95A5A6"
            )
            print("Monitoring deactivated")
    
    def _on_alert_event(self, event):
        """Handle alert events from monitor"""
        if event.get("alert"):
            # Show popup
            print("Alert triggered - showing popup")
            self.popup.show_alert()
        else:
            # Hide popup
            print("Alert cleared - hiding popup")
            self.popup.hide_alert()
    
    def _on_close(self):
        """Handle application close"""
        print("Closing application...")
        
        # Stop monitoring
        if self.is_active:
            self.monitor.stop()
        
        # Hide popup
        self.popup.hide_alert()
        
        # Cleanup
        self.monitor.cleanup()
        
        # Destroy window
        self.root.quit()
        self.root.destroy()
        sys.exit(0)
    
    def run(self):
        """Start the application"""
        print("4 Eyes application started")
        print("Press 'Activate' to start monitoring")
        print("Press 'q' to quit")
        self.root.mainloop()

if _name_ == "_main_":
    app = FourEyesApp()
    app.run()