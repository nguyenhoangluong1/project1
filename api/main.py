from flask import Flask, jsonify
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime

# tải các biến môi trường từ file .env
load_dotenv()

# Tạo API bằng Flask
app = Flask(__name__)
CORS(app)

# Các cài đặt cho Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_API_KEY')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID1')
RANGE_NAME = 'Sheet1!C2:F2'
HISTORY_RANGE = 'Sheet1!A1:F'

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

"""
@app.route("/get-history", methods=["GET"])
def get_history():
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()
        # Lấy dữ liệu từ Google Sheets
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Sheet1!A2:F").execute()
        values = result.get("values", [])

        # Giới hạn số lượng kết quả trả về là 20
        history = []
        for row in values[:20]:
            # Phân tích datetime từ cột A
            try:
                datetime_obj = datetime.strptime(row[0], "%d/%m/%Y %H:%M:%S")
                date = datetime_obj.strftime("%Y/%m/%d")
                time = datetime_obj.strftime("%H:%M:%S")
            except:
                date = "Invalid date"
                time = "Invalid time"

            history.append({
                "date": date,
                "time": time,
                "temperature": row[1],
                "humidity": row[2],
                "precipitation": row[3],
                "wind_speed": row[4]
            })

        return jsonify({"history": history})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
"""

@app.route("/get-history", methods=["GET"])
def get_history():
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()
        # Lấy dữ liệu từ Google Sheets
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Sheet1!A2:F").execute()
        values = result.get("values", [])

        # Giới hạn số lượng kết quả trả về là 20
        history = [{"date": row[0], 
                    "time": row[1], 
                    "temperature": row[2], 
                    "humidity": row[3], 
                    "precipitation": row[4], 
                    "wind_speed": row[5]} for row in values[:20]]

        return jsonify({"history": history})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
