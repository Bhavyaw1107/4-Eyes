#src/detector.py
import cv2
import mediapipe as mp
import numpy as np

# Configuration Constants
GAZE_THRESHOLD_CENTER = 0.35
PERIPHERAL_MARGIN = 0.25
MIN_EYE_VISIBILITY = 0.4

class FaceDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=5,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Iris landmark indices (left and right eye centers)
        self.LEFT_IRIS = [469, 470, 471, 472]
        self.RIGHT_IRIS = [474, 475, 476, 477]
        
        # Eye region landmarks
        self.LEFT_EYE = [33, 133, 160, 159, 158, 144, 145, 153]
        self.RIGHT_EYE = [362, 263, 387, 386, 385, 373, 374, 380]
    
    def get_face_center(self, landmarks, frame_shape):
        """Calculate the center of a face"""
        h, w = frame_shape[:2]
        xs = [lm.x * w for lm in landmarks]
        ys = [lm.y * h for lm in landmarks]
        return (np.mean(xs), np.mean(ys))
    
    def get_iris_position(self, landmarks, iris_indices, eye_indices, frame_shape):
        """Get normalized iris position within the eye"""
        h, w = frame_shape[:2]
        
        # Get iris center
        iris_x = np.mean([landmarks[i].x for i in iris_indices])
        iris_y = np.mean([landmarks[i].y for i in iris_indices])
        
        # Get eye boundaries
        eye_xs = [landmarks[i].x for i in eye_indices]
        eye_ys = [landmarks[i].y for i in eye_indices]
        
        eye_left = min(eye_xs)
        eye_right = max(eye_xs)
        eye_top = min(eye_ys)
        eye_bottom = max(eye_ys)
        
        # Normalize iris position (0 to 1 where 0.5 is center)
        if eye_right - eye_left > 0:
            norm_x = (iris_x - eye_left) / (eye_right - eye_left)
        else:
            norm_x = 0.5
            
        if eye_bottom - eye_top > 0:
            norm_y = (iris_y - eye_top) / (eye_bottom - eye_top)
        else:
            norm_y = 0.5
        
        return norm_x, norm_y
    
    def is_looking_at_camera(self, left_iris_pos, right_iris_pos):
        """Determine if someone is looking at the camera/screen"""
        left_x, left_y = left_iris_pos
        right_x, right_y = right_iris_pos
        
        # Average horizontal position (0.5 is center, looking straight)
        avg_x = (left_x + right_x) / 2
        
        # Check if iris is near center (looking at camera)
        # Center range: 0.5 ± GAZE_THRESHOLD_CENTER
        is_centered = abs(avg_x - 0.5) < GAZE_THRESHOLD_CENTER
        
        return is_centered
    
    def get_face_size(self, landmarks, frame_shape):
        """Calculate approximate face size"""
        h, w = frame_shape[:2]
        xs = [lm.x * w for lm in landmarks]
        ys = [lm.y * h for lm in landmarks]
        
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)
        
        return width * height
    
    def analyze_frame(self, frame):
        """
        Analyze frame for face and gaze detection
        
        Returns:
            dict: {
                "face_count": int,
                "peeking": bool,
                "confidence": float,
                "reason": str | None,
            }
        """
        if frame is None:
            return {
                "face_count": 0,
                "peeking": False,
                "confidence": 0.0,
                "reason": "no_frame"
            }
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if not results.multi_face_landmarks:
            return {
                "face_count": 0,
                "peeking": False,
                "confidence": 0.0,
                "reason": "no_faces"
            }
        
        face_count = len(results.multi_face_landmarks)
        
        # If only one face, no peeking possible
        if face_count == 1:
            return {
                "face_count": 1,
                "peeking": False,
                "confidence": 0.0,
                "reason": "single_face"
            }
        
        # Find primary face (largest, assumed to be the user)
        face_data = []
        for face_landmarks in results.multi_face_landmarks:
            size = self.get_face_size(face_landmarks.landmark, frame.shape)
            center = self.get_face_center(face_landmarks.landmark, frame.shape)
            face_data.append({
                'landmarks': face_landmarks.landmark,
                'size': size,
                'center': center
            })
        
        # Sort by size (largest first - primary user)
        face_data.sort(key=lambda x: x['size'], reverse=True)
        
        # Check secondary faces (all except the largest)
        peeking_detected = False
        max_confidence = 0.0
        reason = None
        
        for i in range(1, len(face_data)):
            landmarks = face_data[i]['landmarks']
            
            # Get iris positions
            left_iris_pos = self.get_iris_position(
                landmarks, self.LEFT_IRIS, self.LEFT_EYE, frame.shape
            )
            right_iris_pos = self.get_iris_position(
                landmarks, self.RIGHT_IRIS, self.RIGHT_EYE, frame.shape
            )
            
            # Check if looking at camera
            if self.is_looking_at_camera(left_iris_pos, right_iris_pos):
                peeking_detected = True
                
                # Calculate confidence based on how centered the gaze is
                avg_x = (left_iris_pos[0] + right_iris_pos[0]) / 2
                confidence = 1.0 - (abs(avg_x - 0.5) / GAZE_THRESHOLD_CENTER)
                confidence = max(0.0, min(1.0, confidence))
                
                if confidence > max_confidence:
                    max_confidence = confidence
                    reason = "gaze_at_screen"
        
        if not peeking_detected:
            reason = "multiple_faces_not_looking"
        
        return {
            "face_count": face_count,
            "peeking": peeking_detected,
            "confidence": max_confidence,
            "reason": reason
        }
    
    def cleanup(self):
        """Release resources"""
        self.face_mesh.close()