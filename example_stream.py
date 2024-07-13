import cv2
import os
from flask import Flask, Response
# import multiprocessing

HOME = os.getcwd()

# model = YOLO(HOME+'/best.pt')

# URL RTSP stream
rtsp_url = "http://192.168.4.1/stream"
app = Flask(__name__)


# Membuat objek video capture

# cv2.namedWindow('Gambar', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('Gambar',640,480)  # Ubah ukuran jendela sesuai keinginan
# frame_queue = multiprocessing.Queue()

# def read_frames(queue, video_path):
#     cap = cv2.VideoCapture(video_path)
#     cap.set(1, 320)
#     cap.set(2, 240)
#     cap.set(3,60)
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         queue.put(frame)
#     cap.release()

# if __name__ == '__main__':
#     video_path = rtsp_url
#     queue = multiprocessing.Queue()

#     # Start the process to read frames
#     process = multiprocessing.Process(target=read_frames, args=(queue, video_path))
#     process.start()

#     # Main process to retrieve frames from the queue
#     while process.is_alive():
#         if not queue.empty():
#             frame = queue.get()

#             # Process your frame here (e.g., display, save, etc.)
#             cv2.imshow('Frame', frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
    
#     cv2.destroyAllWindows()
#     process.join()



# cv2.namedWindow('Gambar', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('Gambar',400,300)  # Ubah ukuran jendela sesuai keinginan



#Periksa apakah video berhasil terbuka

def generate_frames():

    cap = cv2.VideoCapture(rtsp_url)
    cap.set(1, 160)
    cap.set(2, 120)
    cap.set(3,1)


    while True:
        # Baca frame dari video stream
        ret, frame = cap.read()
        if not ret:
            print("Error: Tidak dapat membaca frame.")
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'+b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return "Server streaming video menggunakan OpenCV dan Flask"

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
    
    # # Tampilkan frame
    # cv2.imshow('Gambar', frame)
    # # Periksa apakah pengguna menekan tombol 'q' untuk keluar
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
# Tutup video capture dan jendela tampilan
# cap.release()
# cv2.destroyAllWindows()