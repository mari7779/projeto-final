import cv2

# Caminho para o vídeo de origem
input_video_path = "C:\\Users\\Pichau\\Desktop\\mari\\sistema_final\\WhatsApp Video 2024-03-27 at 09.22.09.mp4"

# Caminho para o vídeo de saída
output_video_path = "video_invertido_horizontal_vertical.mp4"

# Carrega o vídeo
cap = cv2.VideoCapture(input_video_path)

# Verifica se o vídeo foi carregado corretamente
if not cap.isOpened():
    print("Erro ao carregar o vídeo.")
    exit()

# Obtém as informações do vídeo
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Define o codec e cria um objeto VideoWriter para salvar o vídeo de saída
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # codec para formato mp4
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# Loop para processar cada frame do vídeo
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Inverte verticalmente o frame
    frame_invertido_vertical = cv2.flip(frame, 0)
    # Inverte horizontalmente o frame
    frame_invertido_horizontal_vertical = cv2.flip(frame_invertido_vertical, 1)

    # Escreve o frame invertido no vídeo de saída
    out.write(frame_invertido_horizontal_vertical)

    # Exibe o frame invertido
    cv2.imshow('Frame invertido horizontal e vertical', frame_invertido_horizontal_vertical)
    
    # Verifica se o usuário pressionou a tecla 'q' para sair do loop
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Libera os objetos VideoCapture e VideoWriter
cap.release()
out.release()

# Fecha todas as janelas abertas
cv2.destroyAllWindows()
