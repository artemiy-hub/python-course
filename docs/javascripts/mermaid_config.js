// Enhanced Mermaid configuration with advanced controls like marmaid.html
let mermaidLoaded = false;
let mermaidInitialized = false;
let currentScale = 1;
let currentPanX = 0;
let currentPanY = 0;

// Функция для проверки загрузки Mermaid
function checkMermaidLoaded() {
    return typeof mermaid !== 'undefined' && mermaid !== null;
}

// Функция для ожидания загрузки Mermaid
function waitForMermaid(callback, maxAttempts = 50) {
    let attempts = 0;
    
    function check() {
        attempts++;
        if (checkMermaidLoaded()) {
            callback();
        } else if (attempts < maxAttempts) {
            setTimeout(check, 100);
        } else {
            console.error('Mermaid failed to load');
        }
    }
    
    check();
}

// Функция для инициализации Mermaid
function initializeMermaid() {
    if (mermaidInitialized) return;
    
    try {
        mermaid.initialize({
            startOnLoad: false,
            theme: 'default',
            flowchart: {
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            },
            themeVariables: {
                primaryColor: '#3498db',
                primaryTextColor: '#333',
                primaryBorderColor: '#2980b9',
                lineColor: '#333',
                secondaryColor: '#f39c12',
                tertiaryColor: '#9b59b6'
            }
        });
        
        mermaidInitialized = true;
        console.log('Mermaid initialized successfully');
        
        // Обработка диаграмм после инициализации
        processMermaidDiagrams();
        
    } catch (error) {
        console.error('Error initializing Mermaid:', error);
    }
}

// Функция для обработки диаграмм
function processMermaidDiagrams() {
    const diagrams = document.querySelectorAll('.mermaid');
    console.log(`Found ${diagrams.length} mermaid diagrams`);
    
    diagrams.forEach((diagram, index) => {
        // Добавляем кнопку для открытия в полноэкранном режиме
        addFullscreenButton(diagram);
        
        // Добавляем обработчик клика
        diagram.addEventListener('click', function(e) {
            if (e.target.closest('.mermaid-fullscreen-btn')) return;
            openMermaidFullscreen(this);
        });
    });
}

// Функция для добавления кнопки полноэкранного режима
function addFullscreenButton(diagram) {
    if (diagram.querySelector('.mermaid-fullscreen-btn')) return;
    
    const button = document.createElement('button');
    button.className = 'mermaid-fullscreen-btn';
    button.innerHTML = '��';
    button.title = 'Открыть в полноэкранном режиме';
    button.style.cssText = `
        position: absolute;
        top: 5px;
        right: 5px;
        background: rgba(52, 152, 219, 0.9);
        color: white;
        border: none;
        border-radius: 4px;
        width: 25px;
        height: 25px;
        font-size: 12px;
        cursor: pointer;
        z-index: 10;
        opacity: 0;
        transition: opacity 0.2s ease;
    `;
    
    diagram.style.position = 'relative';
    diagram.appendChild(button);
    
    diagram.addEventListener('mouseenter', () => {
        button.style.opacity = '1';
    });
    
    diagram.addEventListener('mouseleave', () => {
        button.style.opacity = '0';
    });
    
    button.addEventListener('click', (e) => {
        e.stopPropagation();
        openMermaidFullscreen(diagram);
    });
}

// Функция для открытия диаграммы в полноэкранном режиме
function openMermaidFullscreen(diagram) {
    // Создаем модальное окно
    const modal = document.createElement('div');
    modal.className = 'mermaid-modal-overlay active';
    modal.innerHTML = `
        <div class="mermaid-modal-content">
            <button class="mermaid-modal-close" onclick="closeMermaidModal()" title="Закрыть">×</button>
            <button class="mermaid-theme-toggle" onclick="toggleMermaidTheme()" title="Переключить тему">🌙</button>
            <div class="mermaid-modal-diagram-container">
                <div id="mermaid-modal-diagram"></div>
            </div>
            <div class="mermaid-controls">
                <button class="up" onclick="panUp()" title="Вверх">↑</button>
                <button class="reset" onclick="resetView()" title="Сброс">⟲</button>
                <button class="down" onclick="panDown()" title="Вниз">↓</button>
                <button class="left" onclick="panLeft()" title="Влево">←</button>
                <button class="zoom-in" onclick="zoomIn()" title="Увеличить">+</button>
                <button class="zoom-out" onclick="zoomOut()" title="Уменьшить">−</button>
                <button class="right" onclick="panRight()" title="Вправо">→</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Копируем SVG в модальное окно
    const modalDiagram = document.getElementById('mermaid-modal-diagram');
    const originalSvg = diagram.querySelector('svg');
    
    if (originalSvg) {
        const clonedSvg = originalSvg.cloneNode(true);
        modalDiagram.appendChild(clonedSvg);
        
        // Применяем правильные стили к SVG
        applySvgStyles(clonedSvg);
    }
    
    // Сброс масштаба и панорамирования
    resetView();
    
    // Обработчик закрытия по клику вне диаграммы
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeMermaidModal();
        }
    });
    
    // Обработчик клавиш
    document.addEventListener('keydown', handleKeyDown);
}

// Функция для применения стилей к SVG
function applySvgStyles(svg) {
    svg.style.maxWidth = '100%';
    svg.style.maxHeight = '100%';
    svg.style.width = 'auto';
    svg.style.height = 'auto';
    svg.style.transform = 'scale(1)';
    svg.style.transformOrigin = 'center center';
    svg.style.objectFit = 'contain';
}

// Функция для закрытия модального окна
function closeMermaidModal() {
    const modal = document.querySelector('.mermaid-modal-overlay');
    if (modal) {
        modal.remove();
        document.removeEventListener('keydown', handleKeyDown);
    }
}

// Функции управления масштабом и панорамированием
function zoomIn() {
    currentScale = Math.min(currentScale * 1.2, 5);
    updateSvgTransform();
}

function zoomOut() {
    currentScale = Math.max(currentScale / 1.2, 0.1);
    updateSvgTransform();
}

function panUp() {
    currentPanY += 50;
    updateSvgTransform();
}

function panDown() {
    currentPanY -= 50;
    updateSvgTransform();
}

function panLeft() {
    currentPanX += 50;
    updateSvgTransform();
}

function panRight() {
    currentPanX -= 50;
    updateSvgTransform();
}

function resetView() {
    currentScale = 1;
    currentPanX = 0;
    currentPanY = 0;
    updateSvgTransform();
}

function updateSvgTransform() {
    const svg = document.querySelector('#mermaid-modal-diagram svg');
    if (svg) {
        svg.style.transform = `translate(${currentPanX}px, ${currentPanY}px) scale(${currentScale})`;
    }
}

// Функция для переключения темы
function toggleMermaidTheme() {
    const button = document.querySelector('.mermaid-theme-toggle');
    const svg = document.querySelector('#mermaid-modal-diagram svg');
    
    if (button.textContent === '��') {
        button.textContent = '☀️';
        if (svg) {
            svg.style.filter = 'invert(1) hue-rotate(180deg)';
        }
    } else {
        button.textContent = '��';
        if (svg) {
            svg.style.filter = 'none';
        }
    }
}

// Обработчик клавиш
function handleKeyDown(e) {
    switch(e.key) {
        case 'Escape':
            closeMermaidModal();
            break;
        case '+':
        case '=':
            zoomIn();
            break;
        case '-':
            zoomOut();
            break;
        case 'ArrowUp':
            panUp();
            break;
        case 'ArrowDown':
            panDown();
            break;
        case 'ArrowLeft':
            panLeft();
            break;
        case 'ArrowRight':
            panRight();
            break;
        case '0':
            resetView();
            break;
    }
}

// Инициализация при загрузке DOM
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, checking for Mermaid...');
    waitForMermaid(function() {
        console.log('Loading Mermaid...');
        mermaid.load().then(() => {
            console.log('Mermaid loaded successfully');
            initializeMermaid();
        }).catch(error => {
            console.error('Error loading Mermaid:', error);
        });
    });
});

// Глобальные функции для кнопок
window.closeMermaidModal = closeMermaidModal;
window.toggleMermaidTheme = toggleMermaidTheme;
window.zoomIn = zoomIn;
window.zoomOut = zoomOut;
window.panUp = panUp;
window.panDown = panDown;
window.panLeft = panLeft;
window.panRight = panRight;
window.resetView = resetView;