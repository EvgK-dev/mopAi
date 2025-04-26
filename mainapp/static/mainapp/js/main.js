
document.addEventListener("DOMContentLoaded", function () {
    initTypingEffect();
    initFileSizeCheck();
    initFormSubmitCheck();
    initCopyDownloadButtons();
    initResetButton();
    initTranscriptionStatusCheck();
    initRandomImage();
});


function initTypingEffect() {
    const page_title = document.querySelector(".page_title");
    if (page_title) {
        const text = "mopAi - Универсальное решение для обработки данных";
        let index = 0;

        function typeText() {
            if (index < text.length) {
                page_title.textContent += text.charAt(index);
                index++;
                setTimeout(typeText, 100);
            }
        }

        typeText();
    }
}

function updateSliderValue(slider) {
    const sliderValue = document.getElementById('accuracy-value');
    const value = parseInt(slider.value);
    switch (value) {
        case 1:
            sliderValue.textContent = 'Низкая, но быстрая';
            break;
        case 2:
            sliderValue.textContent = 'Оптимальная';
            break;
        case 3:
            sliderValue.textContent = 'Максимальная, но медленная';
            break;
    }
}

function initFileSizeCheck() {
    const fileInput = document.getElementById('file-upload');
    const fileNameDisplay = document.getElementById('file-name');
    const MAX_FILE_SIZE = 80 * 1024 * 1024; // 80 MB

    if (!fileInput || !fileNameDisplay) return;

    function showError(message) {
        showMessage(message, "error");
        fileInput.value = '';
        fileNameDisplay.textContent = 'Файл не выбран';
    }

    function generateErrorMessage() {
        return `
            <p class="error-message__help_title">Ошибка: Размер файла не должен превышать 80 МБ</p>
            <p class="error-message__help_title">Извлеките аудио из видео!</p>
            <p>С целью исключения перегрузки сервера <br> необходимо исключить загрузку больших видеофайлов.</p>
            <br>
            <ul>
                <li>Для этого необходимо:</li>
                <br>
                <li>1. Открыть на рабочем компьютере <img class="error-message__help_img" src="/static/mainapp/img/vlc.png" alt="VLC"> <span>VLC Media Player</span></li>
                <li>2. Перейти в меню "Медиа" и выбрать "Конвертировать/Сохранить"</li>
                <li>3. Нажать "Добавить" ⭢ выбрать видеофайл ⭢ нажать "Конвертировать/Сохранить"</li>
                <li>4. В разделе "Профиль" выбрать "Audio - MP3"</li>
                <li>5. В разделе "Конечный файл" нажать "Обзор"</li>
                <li>6. Ввести имя нового файла ⭢ "Сохранить" ⭢ "Начать"</li>
            </ul>
            <br>
            <p>В случае вопросов или при необходимости обработки больших видеофайлов <br> обращайтесь в отделы цифрового развития и криминалистические отделы УСК.</p>
            <br>
            <p>Вы можете также обратиться по телефону, указанному внизу страницы.</p>
            <p>Мы обязательно Вам поможем.</p>
        `;
    }

    function displayFileName(input) {
        const file = input.files[0];
        
        if (!file) {
            fileNameDisplay.textContent = 'Файл не выбран';
            return;
        }

        fileNameDisplay.textContent = `Выбран файл: ${file.name}`;

        if (file.size > MAX_FILE_SIZE) {
            showError(generateErrorMessage());
        }
    }

    fileInput.addEventListener('change', function () {
        displayFileName(fileInput);
    });
}


function initFormSubmitCheck() {
    const form = document.getElementById('uploadForm');
    const fileInput = document.getElementById('file-upload');

    if (form && fileInput) {
        form.addEventListener('submit', function (event) {
            if (!fileInput.value) {
                event.preventDefault();
                showMessage('Ошибка: Пожалуйста, выберите файл перед отправкой.', "error");
            }
        });
    }
}


function showMessage(text, status) {
    let messageElement = document.getElementById("status-message");
    const container = document.querySelector(".app-form-container");

    if (!container) {
        console.error('Элемент с классом "app-form-container" не найден.');
        return;
    }

    if (!messageElement) {
        messageElement = document.createElement("div");
        messageElement.id = "status-message";
        messageElement.style.padding = "15px 30px";
        messageElement.style.borderRadius = "5px";
        messageElement.style.position = "absolute";
        messageElement.style.left = "50%";
        messageElement.style.transform = "translateX(-50%)";
        messageElement.style.top = "-20px";
        messageElement.style.transition = "top 0.8s ease, opacity 0.8s ease";
        messageElement.style.opacity = "0";
        messageElement.style.zIndex = "1000";
        messageElement.style.border = "1px solid";
        messageElement.style.fontWeight = "bold";

        container.appendChild(messageElement);
    }

    if (status === "error") {
        messageElement.style.backgroundColor = "#f8d7da";
        messageElement.style.color = "#721c24";
        messageElement.style.borderColor = "red";
    } else if (status === "success") {
        messageElement.style.backgroundColor = "#d4edda";
        messageElement.style.color = "#155724";
        messageElement.style.borderColor = "green";
    }

    messageElement.innerHTML = `<div>${text}</div>
        <button type="button" id="close-message" style="position: absolute; top: 5px; right: 5px; background: none; border: none; font-size: 20px; cursor: pointer;">❌</button>`;

    setTimeout(() => {
        messageElement.style.top = "50px";
        messageElement.style.opacity = "1";
    }, 10);

    const closeButton = messageElement.querySelector("#close-message");
    closeButton.addEventListener("click", function () {
        messageElement.style.opacity = "0";
        messageElement.style.top = "-20px";
        setTimeout(() => {
            messageElement.remove();
        }, 500);
    });
}



function initCopyDownloadButtons() {
    const copyButton = document.querySelector(".app_buttons__copy");
    const downloadButton = document.querySelector(".app_buttons__download");
    const textContainer = document.querySelector(".app_status__result");

    if (copyButton) {
        copyButton.addEventListener("click", function () {
            if (textContainer) {
                const text = textContainer.innerText.trim();
                if (text) {
                    navigator.clipboard.writeText(text).then(() => {
                        showMessage("Скопировано в буфер обмена. Можете вставить в файл Ctrl+V", "success");
                    }).catch(err => {
                        console.error("Ошибка при копировании: ", err);
                        showMessage("Ошибка при копировании!", "error");
                    });
                } else {
                    showMessage("Нет текста для копирования!", "error");
                }
            }
        });
    }

    if (downloadButton) {
        downloadButton.addEventListener("click", function () {
            if (textContainer) {
                const text = textContainer.innerText.trim();
                if (text) {
                    const blob = new Blob([text], { type: "text/plain" });
                    const link = document.createElement("a");
                    link.href = URL.createObjectURL(blob);
                    link.download = "transcription.txt";
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    showMessage("Файл успешно скачан!", "success");
                } else {
                    showMessage("Нет текста для скачивания!", "error");
                }
            }
        });
    }
}


function initResetButton() {
    const resetButton = document.querySelector(".app_buttons__reset");

    if (!resetButton) {
        return;
    }

    function resetFormData() {
        const form = document.querySelector('#uploadForm');
        if (form) {
            form.reset(); 
        }
    }

    resetButton.addEventListener("click", function () {
        fetch("/delete_ip_record/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(), 
                "Content-Type": "application/json"
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            showMessage(data.message, "success");
            resetFormData();
            setTimeout(function() {
                window.location.replace(window.location.href); 
            }, 1000);
        })
        .catch(error => {
            console.error("Ошибка при удалении записи:", error);
            showMessage("Ошибка при удалении записи!", "error");
            resetFormData();
            setTimeout(function() {
                window.location.replace(window.location.href);
            }, 1000);
        });
    });


    function getCSRFToken() {
        const cookieValue = document.cookie
            .split("; ")
            .find(row => row.startsWith("csrftoken="))
            ?.split("=")[1];
        return cookieValue || "";
    }
}


function initTranscriptionStatusCheck() {
    const ipStatusCheckInterval = 10000; 

    function checkUploadStatus() {
        fetch('/check_upload_status/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (typeof data === 'string') {
                data = JSON.parse(data); 
            }
            if (data.status === 'not_found') {
                console.log('Данных нет, прекращение работы.');
                return;
            }
            if (data.status === 'found') {
                handleUploadStatus(data.client_data);
                console.log('Данные имеются.');
            }
        })
        .catch(error => {
            console.error('Ошибка при запросе статуса:', error);
        });
    }

    function updateInterface() {
        const appStatusContainer = document.querySelector('.app_status__container');
        if (appStatusContainer) {
            appStatusContainer.classList.remove('none');
        }
    }

    function handleUploadStatus(client_data) {
        if (typeof client_data === 'string') {
            client_data = JSON.parse(client_data); 
        }
    
        updateInterface();

        processUploadStatus(client_data);

        processTranscribeStatus(client_data);

        setTimeout(checkUploadStatus, ipStatusCheckInterval);
    }

    function processUploadStatus(client_data) {
        const uploadElement = document.querySelector('.app_status_upload');
    
        if (client_data && client_data.hasOwnProperty('upload_status')) {
            if (client_data.upload_status === 'in_progress') {
                uploadElement.classList.remove('app_status_compled');
                uploadElement.classList.add('app_status_loading');
                uploadElement.textContent = 'Идет загрузка файла на сервер...';
            } else if (client_data.upload_status === 'completed') {
                uploadElement.classList.remove('app_status_loading');
                uploadElement.classList.add('app_status_compled');
                uploadElement.textContent = 'Файл загружен';
    
                const fileElement = document.querySelector('.app_status__item_file');
                if (fileElement) {
                    fileElement.classList.remove('none');
                }
            }
        } else {
            console.error('client_data не содержит нужных данных:', client_data);
        }
    }

    function processTranscribeStatus(client_data) {
        const processElement = document.querySelector('.app_status_process');
        const resultElement = document.querySelector('.app_status__result');
        const buttonsElement = document.querySelector('.app_buttons');

        if (client_data && client_data.hasOwnProperty('transcribe_status')) {
            if (client_data.transcribe_status === 'pending') {
                if (processElement) {
                    processElement.textContent = 'Расшифровка';
                    processElement.classList.add('app_status_loading');
                    processElement.classList.remove('app_status_compled');
                }
            } else if (client_data.transcribe_status === 'completed') {
                if (processElement) {
                    processElement.textContent = 'Завершена';
                    processElement.classList.add('app_status_compled');
                    processElement.classList.remove('app_status_loading');
                }

                if (resultElement) {
                    resultElement.classList.remove('none');
                    
                    resultElement.textContent = client_data.transcribed_text;
                }

                if (buttonsElement) {
                    buttonsElement.classList.remove('none');
                }
            } else if (client_data.transcribe_status !== 'pending' && client_data.transcribe_status !== 'completed') {
                processElement.textContent = client_data.transcribe_status;
                processElement.classList.add('app_status_loading');
                processElement.classList.remove('app_status_compled');
            }
        } else {
            console.error('client_data не содержит нужных данных по расшифровке:', client_data);
        }
    }

    checkUploadStatus();
}

function initRandomImage() {
    function showRandomImage() {
        let images = document.querySelectorAll(".penalty");
        if (images.length === 0) return;

        let randomIndex = Math.floor(Math.random() * images.length);
        let selectedImage = images[randomIndex];

        selectedImage.classList.remove("none");

        setTimeout(() => {
            selectedImage.classList.add("none");
        }, 15000);
    }

    setTimeout(() => {
        showRandomImage();

        setInterval(showRandomImage, 60000);
    }, 10000);
}
