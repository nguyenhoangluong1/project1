const API_URL = "http://127.0.0.1:5000/get-latest-data";

function fetchLatestData() {
  fetch(API_URL)
    .then(response => {
      if (response.ok) {
        return response.json();
      } else if (response.status === 204) {
        console.log("No new data.");
        return null;
      } else {
        throw new Error("Error fetching data.");
      }
    })
    .then(data => {
      if (data) {
        console.log("New data received:", data);
        // Cập nhật giao diện
        updateUI(data.data);
      }
    })
    .catch(error => console.error("Error:", error));
}

// Hàm cập nhật giao diện
function updateUI(data) {
  const [temperature, humidity, precipitation, windSpeed] = data;
  document.getElementById("temperature").textContent = `${temperature} °C`;
  document.getElementById("humidity").textContent = `${humidity} %`;
  document.getElementById("precipitation").textContent = `${precipitation} mm`;
  document.getElementById("windSpeed").textContent = `${windSpeed} km/h`;
}

// Gửi 1 request sau mỗi 30 giây
setInterval(fetchLatestData, 30000);


// Hiển thị ngày giờ
function updateClockAndDate() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');

    // Cập nhật giờ
    document.getElementById('hours').textContent = hours;
    document.getElementById('minutes').textContent = minutes;
    document.getElementById('seconds').textContent = seconds;

    // Cập nhật ngày
    const days = ['Chủ Nhật', 'Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy'];
    const dayName = days[now.getDay()];
    const day = now.getDate();
    const month = now.getMonth() + 1;
    const year = now.getFullYear();
    document.getElementById('date').textContent = `${dayName}, ${day} Tháng ${month}, ${year}`;
}

// Cập nhật mỗi giây
setInterval(updateClockAndDate, 1000);
updateClockAndDate(); // Gọi ngay lần đầu khi load trang

