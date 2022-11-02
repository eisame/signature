import socket, pickle
import svgutils as sv
import pickle

def sendsignature():
 
    HOST = ''
    PORT = 50007

    ## setup socket class

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Bind Socket

    s.bind((HOST, PORT))

    # Listen for Client Connection

    s.listen(1)

    conn, addr = s.accept()
    print ('Connected by', addr)

    # Received data from client
    data = conn.recv(4096)

    # Prepare Data to be sent to Client
         
    # Prepare files to send to client

    svgsignature = sv.compose.SVG(signaturepath)
    signaturewidth = svgsignature.width
    signatureheight = svgsignature.height
    signaturestring = svgsignature.tostr()

    # Group data to send into dictionary

    pickleditc = {'svgsignaturestring': signaturestring, 'signaturewidth': signaturewidth, 'signatureheight' : signatureheight}

    
    # Change data to pickle

    picklesig = pickle.dumps(pickleditc)

    # Send data to client via socket

    s.sendall(picklesig)

    conn.close()


# Capture Signature signed on web application
   
signaturepath = r'C:\Users\Eisa\Desktop\Projects\Axidraw\signatureapi\signature.svg'     # this path to point to signature just signed on web application

while (signaturepath != ''):
    sendsignature()


