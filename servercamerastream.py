if __name__ == '__main__':

    while True:
    
        try:

            import pickle
            import socket
            import struct
            import cv2
            from flask import Flask, Response

            app = Flask(__name__)

            @app.route('/')
            def index():
                return "Default Message"

            HOST = ''
            PORT = 8089

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Socket created')

            s.bind((HOST, PORT))
            print('Socket bind complete')
            s.listen(10)
            print('Socket now listening')

            conn, addr = s.accept()

            data = b'' ### CHANGED
            payload_size = struct.calcsize("L") ### CHANGED

            
            def gen():
                
                while True:
                
                # Retrieve message size
                    while len(data) < payload_size:
                        data += conn.recv(4096)

                    packed_msg_size = data[:payload_size]
                    data = data[payload_size:]
                    msg_size = struct.unpack("L", packed_msg_size)[0] ### CHANGED

                    # Retrieve all data based on message size
                    while len(data) < msg_size:
                        data += conn.recv(4096)

                    frame_data = data[:msg_size]
                    data = data[msg_size:]

                    # Extract frame
                    frame = pickle.loads(frame_data)
                    
                    ret, jpeg = cv2.imencode('.jpg', frame)
                    
                    frame = jpeg.tobytes()
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

            @app.route('/video_feed')
            def video_feed():
                return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

        except:
              print('Error Occured in running the script, Rerunning...')
