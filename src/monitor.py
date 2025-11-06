import cv2
import time
import threading
from detector import FaceDetector

# Configuration Constants - settings yaha adjust kar sakte ho
REQUIRED_SECONDS = 5  # Kitne seconds tak dekhna chahiye alert ke liye
FPS_EST = 20          # Target frame rate - performance ke liye

class Monitor:
    def __init__(self, webcam_index=0, required_seconds=REQUIRED_SECONDS):
        """Monitor initialize karo - webcam monitoring ke liye"""
        self.webcam_index = webcam_index
        self.required_seconds = required_seconds
        self.is_running = False
        self.thread = None
        self.callback = None  # Alert bhejne ke liye callback function
        
        # Face detector initialize karo
        self.detector = FaceDetector()
        self.cap = None  # Webcam capture object
        
        # State tracking variables - kon kab dekh raha hai track karne ke liye
        self.peeking_start_time = None  # Jab peeking start hui
        self.alert_active = False        # Alert abhi active hai ya nahi
        self.last_frame_time = time.time()
        
    def register_callback(self, callback):
        """
        Callback function register karo - alerts bhejne ke liye
        Jab bhi koi screen dekhega, yeh function call hoga
        """
        self.callback = callback
    
    def start(self):
        """Monitoring start karo - separate thread me chalega"""
        if self.is_running:
            return False  # Agar pehle se chal raha hai to dobara start mat karo
        
        self.is_running = True
        # Separate thread me run karo - UI block nahi hoga
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        return True
    
    def stop(self):
        """Monitoring band karo"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2.0)  # Thread ke end hone ka wait karo
        
        # Webcam release karo
        if self.cap:
            self.cap.release()
            self.cap = None
        
        # State reset karo
        self.peeking_start_time = None
        self.alert_active = False
    
    def _monitor_loop(self):
        """
        Main monitoring loop - yaha sabse important kaam hota hai
        Continuously frames capture karta hai aur analyze karta hai
        """
        # Webcam initialize karo
        self.cap = cv2.VideoCapture(self.webcam_index)
        
        if not self.cap.isOpened():
            print("❌ ERROR: Webcam nahi khula. Check karo camera connected hai.")
            self.is_running = False
            return
        
        # Camera properties set karo - better performance ke liye
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # Width
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Height
        self.cap.set(cv2.CAP_PROP_FPS, 30)            # Frame rate
        
        print("✓ Monitor start ho gaya - webcam active hai")
        
        # Infinite loop - jab tak monitoring on hai
        while self.is_running:
            # Frame capture karo
            ret, frame = self.cap.read()
            
            if not ret:
                print("⚠ Warning: Frame capture nahi hua")
                time.sleep(0.1)
                continue
            
            # Frame ko analyze karo - detector se
            result = self.detector.analyze_frame(frame)
            
            current_time = time.time()
            
            # PEEKING DETECTION LOGIC - yeh core logic hai!
            if result["peeking"]:
                # Koi dekh raha hai screen ko!
                
                if self.peeking_start_time is None:
                    # Pehli baar dekha - timer start karo
                    self.peeking_start_time = current_time
                    print(f"👀 Peeking shuru hui! ({result['face_count']} faces detected)")
                
                # Kitne der se dekh raha hai calculate karo
                peeking_duration = current_time - self.peeking_start_time
                
                # Agar required seconds se zyada time ho gaya
                if peeking_duration >= self.required_seconds and not self.alert_active:
                    # ALERT TRIGGER KARO!
                    self.alert_active = True
                    print(f"🚨 ALERT! Peeking {peeking_duration:.1f} seconds se ho rahi hai!")
                    
                    # Callback call karo - UI ko batao alert dikhane ke liye
                    if self.callback:
                        self.callback({"alert": True, "duration": peeking_duration})
            
            else:
                # Peeking nahi ho rahi - koi nahi dekh raha ya sirf ek face hai
                
                if self.peeking_start_time is not None:
                    # Peeking ruk gayi
                    peeking_duration = current_time - self.peeking_start_time
                    print(f"✓ Peeking band ho gayi ({peeking_duration:.1f}s ke baad)")
                
                # Timer reset karo
                self.peeking_start_time = None
                
                if self.alert_active:
                    # Alert deactivate karo
                    self.alert_active = False
                    print("✓ Alert deactivate - ab safe hai")
                    
                    # Callback call karo - UI ko batao alert band karne ke liye
                    if self.callback:
                        self.callback({"alert": False})
            
            # Frame rate control - CPU ko overload mat karo
            elapsed = time.time() - self.last_frame_time
            target_delay = 1.0 / FPS_EST
            
            if elapsed < target_delay:
                time.sleep(target_delay - elapsed)  # Thoda wait karo
            
            self.last_frame_time = time.time()
        
        # Loop end hone pe cleanup karo
        if self.cap:
            self.cap.release()
            self.cap = None
        
        print("✓ Monitor band ho gaya")
    
    def get_status(self):
        """Current monitoring status check karo"""
        return {
            "is_running": self.is_running,
            "alert_active": self.alert_active,
            "peeking_duration": (
                time.time() - self.peeking_start_time 
                if self.peeking_start_time else 0
            )
        }
    
    def cleanup(self):
        """Sab resources cleanup karo - memory leak avoid karne ke liye"""
        self.stop()
        self.detector.cleanup()