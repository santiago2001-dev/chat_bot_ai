const socket = new WebSocket("ws://localhost:8000/ws/products/");

// Inicializar el estado del chat si no existe
const CHAT_STEP_KEY = "chatStep";
if (!localStorage.getItem(CHAT_STEP_KEY)) {
  localStorage.setItem(CHAT_STEP_KEY, "get_options");
}

document.addEventListener("DOMContentLoaded", () => {
  initializeSocket();
});

function initializeSocket() {
  socket.onopen = () => {
    console.log("Conectado al WebSocket");
    requestOptions();
  };

  socket.onmessage = (event) => handleIncomingMessage(event);
}

function requestOptions() {
  sendSocketMessage("get_options");
}

function handleIncomingMessage(event) {
  const chatBox = document.getElementById("chat-box");
  const messageContainer = createMessageContainer();

  try {
    const data = JSON.parse(event.data);
    console.log(data);

    if (data.options && isStep("get_options")) {
      renderOptions(messageContainer, data.message, data.options);
    } else if (data.products) {
      updateStep("view_products");
      renderProductList(messageContainer, data);
    } else if (isStep("get_assistance")) {
      renderAssistanceOptions(messageContainer, data);
    } else if (isStep("3")) {
      messageContainer.innerHTML = `<p>${data.message}</p>`;
    } else if (data.chart && isStep("2")) {
      renderChart(messageContainer, data.chart);
    } else {
      messageContainer.textContent = data.message || event.data;
    }
  } catch (error) {
    messageContainer.textContent = event.data;
  }

  chatBox.appendChild(messageContainer);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage(action, content = "") {
  const messageInput = document.getElementById("message");
  const step = getChatStep();

  if (step === "3" && messageInput.value.trim()) {
    sendSocketMessage(step, messageInput.value.trim());
    messageInput.value = "";
  } else if (step !== "3") {
    sendSocketMessage(action, content);
  }
}

function sendSocketMessage(action, content = "") {
  const data = { action, content };
  socket.send(JSON.stringify(data));
}

function renderOptions(container, message, options) {
  container.innerHTML = `<strong>${message}</strong><br><br>`;
  const optionsDiv = createOptionsContainer(options, handleOptionClick);
  container.appendChild(optionsDiv);
}

function renderProductList(container, data) {
  let productList = `<strong>Lista de Productos:</strong><br>
  <table>
      <tr><th>ID</th><th>Nombre</th><th>Precio</th></tr>
      ${data.products
        .map(
          (product) =>
            `<tr><td>${product.id}</td><td>${product.name}</td><td>$${product.price}</td></tr>`
        )
        .join("")}
  </table>
  <p>${data.message}</p>`;

  const optionsDiv = createOptionsContainer(data.options, () => {
    sendMessage("get_assistance");
    updateStep("get_assistance");
  });

  container.innerHTML = productList;
  container.appendChild(optionsDiv);
}

function renderAssistanceOptions(container, data) {
  container.innerHTML = `<p>${data.message}</p>`;
  const optionsDiv = createOptionsContainer(data.options, () =>
    updateStep("3")
  );
  container.appendChild(optionsDiv);
}

function renderChart(container, chartData) {
  container.innerHTML = `
  <strong>Gráfico de Ventas:</strong><br>
  <div style="display: flex; justify-content: center; margin-top: 10px;">
      <img src="data:image/png;base64,${chartData}" alt="Gráfico de Ventas" 
          style="max-width: 90%; height: auto; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);">
  </div>
`;
}

function createMessageContainer() {
  const div = document.createElement("div");
  div.classList.add("message-container");
  return div;
}

function createOptionsContainer(options, callback) {
  const div = document.createElement("div");
  div.classList.add("options-container");

  options.forEach((option) => {
    const button = document.createElement("button");
    button.classList.add("option-button");
    button.textContent = option.name;
    button.onclick = () => callback(option);
    div.appendChild(button);
  });

  return div;
}

function handleOptionClick(option) {
  sendMessage(option.id);
  updateStep(option.id);
}

function updateStep(step) {
  localStorage.setItem(CHAT_STEP_KEY, step);
}

function getChatStep() {
  return localStorage.getItem(CHAT_STEP_KEY);
}

function isStep(step) {
  return getChatStep() === step;
}
