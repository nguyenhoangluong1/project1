from flask import Flask, jsonify
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from flask_cors import CORS
from dotenv import load_dotenv
import os

# tải các biến môi trường từ file .env
load_dotenv()

# Tạo API bằng Flask
app = Flask(__name__)
CORS(app)

# Các cài đặt cho Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
SPREADSHEET_ID = os.getenv('SHEET_ID')
RANGE_NAME = 'Sheet1!B2:E2'

# Tải thông tin xác thực từ file json
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Khởi tạo các dịch vụ Google Sheets
def get_sheets_service():
    return build("sheets", "v4", credentials=creds)

# Lưu trữ dữ liệu cuối cùng để so sánh
last_data = None

@app.route("/get-latest-data", methods=["GET"])
def get_latest_data():
    global last_data
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        values = result.get("values", [])

        current_data = values[0] if values else []

        if current_data != last_data:
            # Cập nhật dữ liệu mới nhất
            last_data = current_data
            return jsonify({"data": current_data})
        else:
            # Trả về mã 204 No Content nếu không có dữ liệu mới
            return jsonify({"data": "No new data"}), 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     app.run(debug=True, port=5000)