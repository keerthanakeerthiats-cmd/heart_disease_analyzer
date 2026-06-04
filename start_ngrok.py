from pyngrok import ngrok
import time

# Start an ngrok tunnel to port 5001
print('Starting ngrok tunnel to port 5001...')
tunnel = ngrok.connect(5001)
print('ngrok tunnel started:', tunnel.public_url)
print('Press Ctrl+C in this terminal to stop the tunnel.')

try:
    while True:
        time.sleep(3600)
except KeyboardInterrupt:
    print('Shutting down ngrok tunnel...')
    ngrok.disconnect(tunnel.public_url)
    print('Tunnel stopped.')
