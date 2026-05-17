import cv2
import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl
from multiprocessing import Process, Queue
import time
import mediapipe as mp
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# --- 1. FUZZY SYSTEM SETUP ---
def get_fuzzy_system():
    distance = ctrl.Antecedent(np.arange(0, 201, 1), 'distance')
    speed = ctrl.Consequent(np.arange(0, 101, 1), 'speed')

    # Membership Functions
    distance['small'] = fuzzy.trimf(distance.universe, [0, 0, 100])
    distance['large'] = fuzzy.trimf(distance.universe, [80, 200, 200])

    speed['slow'] = fuzzy.trimf(speed.universe, [0, 0, 60])
    speed['fast'] = fuzzy.trimf(speed.universe, [40, 100, 100])

    # Rules
    rule1 = ctrl.Rule(distance['small'], speed['slow'])
    rule2 = ctrl.Rule(distance['large'], speed['fast'])

    speed_ctrl = ctrl.ControlSystem([rule1, rule2])
    return ctrl.ControlSystemSimulation(speed_ctrl)

# --- 2. PDC / DISTRIBUTED WORKER ---
def robot_worker(id, data_queue):
    print(f"Robot {id} is connected and waiting for Fuzzy commands...")
    while True:
        try:
            if not data_queue.empty():
                val = data_queue.get()
                print(f"[Robot {id}] Received Fuzzy Speed: {val:.2f}%")
        except EOFError:
            break
        time.sleep(0.1)

# --- 3. MAIN LOOP (Computer Vision) ---
if __name__ == "__main__":
    # Fuzzy initialize karein
    speed_sim = get_fuzzy_system()

    # PDC: Processes aur Queue setup
    q: Queue = Queue()
    p1 = Process(target=robot_worker, args=(1, q))
    p2 = Process(target=robot_worker, args=(2, q))
    p1.start()
    p2.start()

    # Mediapipe initialization (Inside main for Windows safety)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
    cap = cv2.VideoCapture(0)

    print("System Running. Show your hand to the camera!")

    try:
        while cap.isOpened():
            success, image = cap.read()
            if not success: break

            # Mirror effect aur RGB conversion
            image = cv2.flip(image, 1)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_image)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Thumb aur Index finger points
                    thumb = hand_landmarks.landmark[4]
                    index = hand_landmarks.landmark[8]
                    
                    # CV: Euclidean Distance calculation
                    dist_val = np.sqrt((thumb.x - index.x)**2 + (thumb.y - index.y)**2) * 500
                    dist_val = np.clip(dist_val, 0, 200)

                    # FUZZY: Decision making
                    speed_sim.input['distance'] = dist_val
                    speed_sim.compute()
                    calculated_speed = speed_sim.output['speed']

                    # PDC: Speed distribute 
                    q.put(calculated_speed)

                
                    cv2.putText(image, f"Fuzzy Speed: {calculated_speed:.1f}%", (10, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow('Gesture Control System', image)
            if cv2.waitKey(5) & 0xFF == 27: break # 'Esc' se band hoga
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        p1.terminate()
        p2.terminate()
