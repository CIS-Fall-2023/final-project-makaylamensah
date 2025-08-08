const BASE_URL = 'http://127.0.0.1:5000';

function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  fetch(`${BASE_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, password })
  })
  .then(res => res.json().then(data => ({ status: res.status, body: data })))
  .then(({ status, body }) => {
    document.getElementById("login-message").textContent = body.message;
    document.getElementById("login-message").style.color = status === 200 ? "green" : "red";
  })
  .catch(err => console.error("Login error:", err));
}

function fetchFloors() {
  fetch(`${BASE_URL}/floors`)
    .then(response => response.json())
    .then(data => {
      const list = document.getElementById("floors-list");
      list.innerHTML = "";
      data.forEach(floor => {
        const li = document.createElement("li");
        li.textContent = `${floor.name} (ID: ${floor.id})`;
        list.appendChild(li);
      });
    });
}

function fetchRooms() {
  fetch(`${BASE_URL}/rooms`)
    .then(response => response.json())
    .then(data => {
      const list = document.getElementById("rooms-list");
      list.innerHTML = "";
      data.forEach(room => {
        const li = document.createElement("li");
        li.textContent = `${room.name} (ID: ${room.id}, Floor ID: ${room.floor_id})`;
        list.appendChild(li);
      });
    });
}

function fetchResidents() {
  fetch(`${BASE_URL}/residents`)
    .then(response => response.json())
    .then(data => {
      const list = document.getElementById("residents-list");
      list.innerHTML = "";
      data.forEach(resident => {
        const li = document.createElement("li");
        li.textContent = `${resident.name} (ID: ${resident.id}, Room ID: ${resident.room_id})`;
        list.appendChild(li);
      });
    });
}
