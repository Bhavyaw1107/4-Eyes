#src/monitor.py
import cv2
import time
import threading
from detector import FaceDetector

# Configuration Constants
REQUIRED_SECONDS = 5
FPS_EST = 20

class Monitor:
    def __init__(self, webcam_index=0, required_seconds=REQUIRED_SECONDS):
        self.webcam_index = webcam_index
        self.required_seconds = required_seconds
        self.is_running = False
        self.thread = None
        self.callback = None
        
        self.detector = FaceDetector()
        self.cap = None
        
        # State tracking
        self.peeking_start_time = None
        self.alert_active = False
        self.last_frame_time = time.time()
        
    def register_callback(self, callback):
        """Register callback function for alerts"""
        self.callback = callback
    
    def start(self):
        """Start monitoring in a separate thread"""
        if self.is_running:
            return False
        
        self.is_running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        return True
    
    def stop(self):
        """Stop monitoring"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        # Reset state
        self.peeking_start_time = None
        self.alert_active = False
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        # Initialize webcam
        self.cap = cv2.VideoCapture(self.webcam_index)
        
        if not self.cap.isOpened():
            print("Error: Could not open webcam")
            self.is_running = False
            return
        
        # Set camera properties for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        print("Monitor started...")
        
        while self.is_running:
            ret, frame = self.cap.read()
            
            if not ret:
                print("Error: Failed to grab frame")
                time.sleep(0.1)
                continue
            
            # Analyze frame
            result = self.detector.analyze_frame(frame)
            
            current_time = time.time()
            
            # Handle peeking detection
            if result["peeking"]:
                # Someone is peeking
                if self.peeking_start_time is None:
                    # Start tracking peeking duration
                    self.peeking_start_time = current_time
                    print(f"Peeking detected! ({result['face_count']} faces)")
                
                # Check if peeking duration exceeds threshold
                peeking_duration = current_time - self.peeking_start_time
                
                if peeking_duration >= self.required_seconds and not self.alert_active:
                    # Trigger alert
                    self.alert_active = True
                    print(f"ALERT! Peeking sustained for {peeking_duration:.1f}s")
                    if self.callback:
                        self.callback({"alert": True, "duration": peeking_duration})
            
            else:
                # No peeking detected
                if self.peeking_start_time is not None:
                    peeking_duration = current_time - self.peeking_start_time
                    print(f"Peeking stopped after {peeking_duration:.1f}s")
                
                # Reset tracking
                self.peeking_start_time = None
                
                if self.alert_active:
                    # Deactivate alert
                    self.alert_active = False
                    print("Alert deactivated")
                    if self.callback:
                        self.callback({"alert": False})
            
            # Control frame rate
            elapsed = time.time() - self.last_frame_time
            target_delay = 1.0 / FPS_EST
            
            if elapsed < target_delay:
                time.sleep(target_delay - elapsed)
            
            self.last_frame_time = time.time()
        
        # Cleanup
        if self.cap:
            self.cap.release()
            self.cap = None
        
        print("Monitor stopped")
    
    def get_status(self):
        """Get current monitoring status"""
        return {
            "is_running": self.is_running,
            "alert_active": self.alert_active,
            "peeking_duration": (
                time.time() - self.peeking_start_time 
                if self.peeking_start_time else 0
            )
        }
    
    def cleanup(self):
        """Cleanup resources"""
        self.stop()
        self.detector.cleanup()