import cv2
import mediapipe as mp
import numpy as np

GAZE_THRESHOLD_CENTER = 0.35  # Kitna center me dekhna chahiye 
MIN_EYE_VISIBILITY = 0.4       # Minimum eye visibility required

class FaceDetector:
    def __init__(self):
        """Face detector initialize karo - MediaPipe use karenge"""
        # MediaPipe face mesh setup karo
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=5,              # Maximum 5 faces detect kar sakte hain
            refine_landmarks=True,        # Iris landmarks bhi chahiye
            min_detection_confidence=0.5, # Detection confidence threshold
            min_tracking_confidence=0.5   # Tracking confidence threshold
        )
        
        # Iris landmark indices - left aur right eye ke centers
        self.LEFT_IRIS = [469, 470, 471, 472]   # Left iris ke 4 points
        self.RIGHT_IRIS = [474, 475, 476, 477]  # Right iris ke 4 points
        
        # Eye region landmarks - puri eye ka boundary
        self.LEFT_EYE = [33, 133, 160, 159, 158, 144, 145, 153]
        self.RIGHT_EYE = [362, 263, 387, 386, 385, 373, 374, 380]
    
    def get_face_center(self, landmarks, frame_shape):
        """Face ka center point nikalo - coordinates me"""
        h, w = frame_shape[:2]
        # Sabhi landmarks ke x aur y coordinates nikalo
        xs = [lm.x * w for lm in landmarks]
        ys = [lm.y * h for lm in landmarks]
        # Average nikalo - yahi center hoga
        return (np.mean(xs), np.mean(ys))
    
    def get_iris_position(self, landmarks, iris_indices, eye_indices, frame_shape):
        """Iris ki position nikalo eye ke andar - normalized (0 to 1)"""
        h, w = frame_shape[:2]
        
        # Iris ka center calculate karo
        iris_x = np.mean([landmarks[i].x for i in iris_indices])
        iris_y = np.mean([landmarks[i].y for i in iris_indices])
        
        # Eye ki boundaries nikalo - left, right, top, bottom
        eye_xs = [landmarks[i].x for i in eye_indices]
        eye_ys = [landmarks[i].y for i in eye_indices]
        
        eye_left = min(eye_xs)
        eye_right = max(eye_xs)
        eye_top = min(eye_ys)
        eye_bottom = max(eye_ys)
        
        # Iris position ko normalize karo (0 to 1, jaha 0.5 = center)
        if eye_right - eye_left > 0:
            norm_x = (iris_x - eye_left) / (eye_right - eye_left)
        else:
            norm_x = 0.5  # Default center
            
        if eye_bottom - eye_top > 0:
            norm_y = (iris_y - eye_top) / (eye_bottom - eye_top)
        else:
            norm_y = 0.5  # Default center
        # Ye batata hai Iris kitna centre me dekh rha hai
        return norm_x, norm_y
    
    def is_looking_at_camera(self, left_iris_pos, right_iris_pos):
        """
        Check karo ki koi camera/screen ki taraf dekh raha hai ya nahi
        Iris ka position center ke paas hona chahiye
        """
        left_x, left_y = left_iris_pos
        right_x, right_y = right_iris_pos
        
        # Dono eyes ke horizontal position ka average nikalo
        avg_x = (left_x + right_x) / 2
        
        # Check karo iris center ke paas hai ya nahi
        # 0.5 = perfect center, GAZE_THRESHOLD_CENTER = allowed deviation
        is_centered = abs(avg_x - 0.5) < GAZE_THRESHOLD_CENTER
        
        return is_centered
    
    def get_face_size(self, landmarks, frame_shape):
        """Face ka size calculate karo - area me"""
        h, w = frame_shape[:2]
        xs = [lm.x * w for lm in landmarks]
        ys = [lm.y * h for lm in landmarks]
        
        # Width aur height nikalo
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)
        
        # Area return karo
        return width * height
    
    def analyze_frame(self, frame):
        """
        Frame ko analyze karo - faces aur gaze direction detect karo
        Ye function multiple faces ko detect karta hai 
        """
        if frame is None:
            return {
                "face_count": 0,
                "peeking": False,
                "confidence": 0.0,
                "reason": "no_frame"
            }
        
        # BGR se RGB me convert karo - MediaPipe ko RGB chahiye
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        # Agar koi face nahi mila
        if not results.multi_face_landmarks:
            return {
                "face_count": 0,
                "peeking": False,
                "confidence": 0.0,
                "reason": "no_faces"
            }
        
        # Kitne faces detect hue
        face_count = len(results.multi_face_landmarks)
        
        # Agar sirf ek face hai (user khud), to peeking possible nahi
        if face_count == 1:
            return {
                "face_count": 1,
                "peeking": False,
                "confidence": 0.0,
                "reason": "single_face"
            }
        
        # MULTI-FACE DETECTION - YEH SABSE IMPORTANT PART HAI!
        # Sabse bada face primary user hoga, baaki sab ko check karenge
        
        face_data = []
        for face_landmarks in results.multi_face_landmarks:
            size = self.get_face_size(face_landmarks.landmark, frame.shape)
            center = self.get_face_center(face_landmarks.landmark, frame.shape)
            face_data.append({
                'landmarks': face_landmarks.landmark,
                'size': size,
                'center': center
            })
        
        # Size ke basis pe sort karo - sabse bada pehle
        # Assumption: Sabse bada face = primary user (jo kaam kar raha hai)
        face_data.sort(key=lambda x: x['size'], reverse=True)
        
        # Ab baaki ke faces check karo (index 1 se start - 0 to user hai)
        peeking_detected = False
        max_confidence = 0.0
        reason = None
        
        # Har secondary face ko check karo
        for i in range(1, len(face_data)):
            landmarks = face_data[i]['landmarks']
            
            # Is face ke iris positions nikalo
            left_iris_pos = self.get_iris_position(
                landmarks, self.LEFT_IRIS, self.LEFT_EYE, frame.shape
            )
            right_iris_pos = self.get_iris_position(
                landmarks, self.RIGHT_IRIS, self.RIGHT_EYE, frame.shape
            )
            
            # Check karo - kya yeh banda camera/screen ki taraf dekh raha hai?
            if self.is_looking_at_camera(left_iris_pos, right_iris_pos):
                # HA! Koi dekh raha hai!
                peeking_detected = True
                
                # Confidence calculate karo - kitna centered hai gaze
                avg_x = (left_iris_pos[0] + right_iris_pos[0]) / 2
                confidence = 1.0 - (abs(avg_x - 0.5) / GAZE_THRESHOLD_CENTER)
                confidence = max(0.0, min(1.0, confidence))  # 0 se 1 ke beech me rakho
                
                # Sabse zyada confident detection save karo
                if confidence > max_confidence:
                    max_confidence = confidence
                    reason = "gaze_at_screen"
                
                print(f"  → Face #{i+1}: DEKH RAHA HAI! Confidence: {confidence:.2f}")
        
        # Agar koi nahi dekh raha
        if not peeking_detected:
            reason = "multiple_faces_not_looking"
        
        # Final result return karo
        return {
            "face_count": face_count,
            "peeking": peeking_detected,
            "confidence": max_confidence,
            "reason": reason
        }
    
    def cleanup(self):
        self.face_mesh.close()