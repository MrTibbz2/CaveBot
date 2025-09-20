import webview
import os



html_path = os.path.join(os.path.dirname(__file__), 'index.html')
webview.create_window('Desmos Calculator', html_path)
webview.start(debug=True)