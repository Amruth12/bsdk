import cv2
import csv
import mediapipe as mp
import time
import os

# Define absolute path to your CSV file
path = "C:\Users\Admin\Desktop\A-virtual-Quiz-Based-On-Artificial-Intelligence-OpenCv2-Mediapipe-And-CvZone--main\quiz.csv"

class Question:
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])
        self.userAnswer = None

    def update(self, cursor, bboxs):
        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAnswer = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)

# Initialize MediaPipe Hands and DrawingUtils
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 1024)

# Import CSV file
if not os.path.isfile(path):
    raise FileNotFoundError(f"The file at path {path} does not exist.")
    
with open(path, newline="\n") as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]

questionList = []
for q in dataAll:
    questionList.append(Question(q))
print("___ " + str(len(questionList)))

questNumber = 0
totalQuest = len(dataAll)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Assuming first detected hand for simplicity
        lmList = results.multi_hand_landmarks[0].landmark
        cursor = (int(lmList[8].x * img.shape[1]), int(lmList[8].y * img.shape[0]))
        length = cv2.norm(np.array(cursor) - np.array((int(lmList[12].x * img.shape[1]), int(lmList[12].y * img.shape[0]))), cv2.NORM_L2)

        if length < 60:
            Qesut.update(cursor, [bbox1, bbox2, bbox3, bbox4])
            if Qesut.userAnswer is not None:
                time.sleep(0.4)
                questNumber += 1

    Qesut = questionList[0] if questNumber < totalQuest else None

    if Qesut:
        img, bbox = cvzone.putTextRect(img, Qesut.question, [20, 20], 1, 2, offset=20, border=2)
        img, bbox1 = cvzone.putTextRect(img, Qesut.choice1, [150, 100], 1, 2, offset=20, border=2)
        img, bbox2 = cvzone.putTextRect(img, Qesut.choice2, [400, 100], 1, 2, offset=20, border=2)
        img, bbox3 = cvzone.putTextRect(img, Qesut.choice3, [150, 300], 1, 2, offset=20, border=2)
        img, bbox4 = cvzone.putTextRect(img, Qesut.choice4, [400, 300], 1, 2, offset=20, border=2)
    else:
        score = sum(1 for mcq in questionList if mcq.userAnswer == mcq.answer)
        score = round((score / totalQuest) * 100, 2)
        img, _ = cvzone.putTextRect(img, "Quiz completed ", [150, 200], 1, 2, offset=15)
        img, _ = cvzone.putTextRect(img, "your score " + str(score) + "%", [150, 300], 1, 2, offset=15)

    # Draw progress bar
    barValue = 120 + (330 // totalQuest) * questNumber
    cv2.rectangle(img, (120, 400), (barValue, 450), (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (120, 400), (450, 450), (255, 0, 255), 2)
    img, _ = cvzone.putTextRect(img, f'{round((questNumber / totalQuest) * 100)}%', [500, 430], 1, 2, offset=15)

    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
