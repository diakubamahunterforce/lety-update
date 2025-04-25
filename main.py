import cv2
import mediapipe as mp
import threading
import time

# Inicializa o MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

# Inicializa a captura de vídeo
cap = cv2.VideoCapture(0)

# Função para ação quando a mão está aberta
def acao_mao_aberta():
  
        print("Ação: Mão Aberta")
        time.sleep(1)  # Ação a cada 1 segundo

# Função para ação quando a mão está fechada
def acao_mao_fechada():
    
        print("Ação: Mão Fechada")
        time.sleep(1)  # Ação a cada 1 segundo

# Variáveis para controle de threads
maos_abertas = False
maos_fechadas = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Converte a imagem para RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Desenha os pontos da mão
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Verifica o estado da palma
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            # Lógica para determinar se a mão está aberta ou fechada
            if (index_tip.y < thumb_tip.y) and (middle_tip.y < thumb_tip.y) and (ring_tip.y < thumb_tip.y) and (pinky_tip.y < thumb_tip.y):
                cv2.putText(frame, "Mão Aberta", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Inicia a thread para ação da mão aberta se não estiver em execução
                if not maos_abertas:
                    maos_abertas = True
                    maos_fechadas = False
                    threading.Thread(target=acao_mao_aberta, daemon=True).start()

            else:
                cv2.putText(frame, "Mão Fechada", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                # Inicia a thread para ação da mão fechada se não estiver em execução
                if not maos_fechadas:
                    maos_fechadas = True
                    maos_abertas = False
                    threading.Thread(target=acao_mao_fechada, daemon=True).start()

    # Exibe o resultado
    cv2.imshow('Detecção da Palma da Mão', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a captura e fecha as janelas
cap.release()
cv2.destroyAllWindows()
