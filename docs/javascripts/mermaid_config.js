// Enhanced Mermaid configuration with advanced controls like marmaid.html
let mermaidInitialized = false;
let currentScale = 1;
let currentPanX = 0;
let currentPanY = 0;

// Функция для сброса переменных управления
function resetControlVariables() {
    currentScale = 1;
    currentPanX = 0;
    currentPanY = 0;
    console.log('Control variables reset');
}

// Функция для ожидания загрузки библиотеки Mermaid
function waitForMermaid() {
    if (typeof mermaid !== 'undefined') {
        console.log('Mermaid library found, initializing controls...');
        initializeMermaidControls();
    } else {
        console.log('Waiting for Mermaid library to load...');
        setTimeout(waitForMermaid, 100);
    }
}

// Функция для инициализации после загрузки DOM
function initializeMermaidControls() {
    if (mermaidInitialized) return;
    
    console.log('Initializing Mermaid controls...');
    
    // Инициализируем Mermaid принудительно
    if (typeof mermaid !== 'undefined') {
        mermaid.initialize({
            startOnLoad: true,
            theme: 'default',
            flowchart: {
                useMaxWidth: true,
                htmlLabels: true
            },
            sequence: {
                useMaxWidth: true
            },
            gantt: {
                useMaxWidth: true
            }
        });
        
        // Принудительно обрабатываем все элементы с классом mermaid
        mermaid.run();
        console.log('Mermaid initialized and run completed');
    }
    
    // Ждем немного и обрабатываем диаграммы
    setTimeout(() => {
        processMermaidDiagrams();
    }, 500);
    
    mermaidInitialized = true;
    console.log('Mermaid controls initialized successfully');
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
    button.innerHTML = '⛶';
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
    console.log('Opening fullscreen for diagram:', diagram);
    
    // Закрываем существующее модальное окно, если оно есть
    const existingModal = document.querySelector('.mermaid-modal-overlay');
    if (existingModal) {
        existingModal.remove();
        document.removeEventListener('keydown', handleKeyDown);
    }
    
    // Создаем модальное окно
    const modal = document.createElement('div');
    modal.className = 'mermaid-modal-overlay active';
    modal.innerHTML = `
        <div class="mermaid-modal-content">
            <button class="mermaid-modal-close" data-action="close" title="Закрыть">×</button>
            <button class="mermaid-theme-toggle" data-action="toggleTheme" title="Переключить тему">🌙</button>
            <div class="mermaid-modal-diagram-container">
                <div id="mermaid-modal-diagram"></div>
            </div>
            <div class="mermaid-controls">
                <button class="zoom-in" data-action="zoomIn" title="Увеличить">+</button>
                <button class="up" data-action="panUp" title="Вверх">↑</button>
                <button class="zoom-out" data-action="zoomOut" title="Уменьшить">−</button>
                <button class="left" data-action="panLeft" title="Влево">←</button>
                <button class="reset" data-action="resetView" title="Сброс">⟲</button>
                <button class="right" data-action="panRight" title="Вправо">→</button>
                <button class="spacer"></button>
                <button class="down" data-action="panDown" title="Вниз">↓</button>
                <button class="spacer"></button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Копируем содержимое диаграммы в модальное окно
    const modalDiagram = document.getElementById('mermaid-modal-diagram');
    
    // Ищем SVG или другой элемент диаграммы
    const originalSvg = diagram.querySelector('svg');
    const originalContent = diagram.innerHTML;
    
    console.log('Original SVG found:', !!originalSvg);
    console.log('Original content length:', originalContent ? originalContent.length : 0);
    
    if (originalSvg) {
        // Копируем SVG полностью
        const svgHTML = originalSvg.outerHTML;
        console.log('Original SVG HTML length:', svgHTML.length);
        modalDiagram.innerHTML = svgHTML;
        const clonedSvg = modalDiagram.querySelector('svg');
        
        // Применяем правильные стили к SVG
        if (clonedSvg) {
            applySvgStyles(clonedSvg);
            console.log('SVG fully copied and added to modal');
            
            // Проверяем, что SVG действительно добавлен
            console.log('SVG in modal after adding:', !!clonedSvg);
            console.log('SVG dimensions:', clonedSvg.getBoundingClientRect());
            console.log('SVG outerHTML length:', clonedSvg.outerHTML.length);
            
            // Проверяем размеры контейнера
            const containerRect = modalDiagram.getBoundingClientRect();
            console.log('Modal container dimensions:', containerRect);
            
            // Принудительно устанавливаем размеры SVG
            clonedSvg.style.width = '100%';
            clonedSvg.style.height = '100%';
            clonedSvg.style.minWidth = '400px';
            clonedSvg.style.minHeight = '400px';
            clonedSvg.style.visibility = 'visible';
            clonedSvg.style.opacity = '1';
            console.log('Forced SVG dimensions set');
            
            // Проверяем видимость через небольшую задержку
            setTimeout(() => {
                const rect = clonedSvg.getBoundingClientRect();
                console.log('SVG dimensions after timeout:', rect);
                console.log('SVG computed styles:', window.getComputedStyle(clonedSvg));
            }, 100);
        } else {
            console.log('Failed to find cloned SVG in modal');
        }
    } else if (originalContent) {
        // Если нет SVG, копируем все содержимое
        modalDiagram.innerHTML = originalContent;
        
        // Применяем стили к первому SVG, если он есть
        const svg = modalDiagram.querySelector('svg');
        if (svg) {
            applySvgStyles(svg);
            console.log('Content copied and SVG styled');
        } else {
            console.log('No SVG found in copied content');
        }
    } else {
        console.log('No content found in diagram');
    }
    
    // Сброс переменных управления при открытии
    resetControlVariables();
    
    // Обработчик закрытия по клику вне диаграммы
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeMermaidModal();
        }
    });
    
    // Обработчик клавиш
    document.addEventListener('keydown', handleKeyDown);
    
    // Добавляем обработчики для кнопок управления
    setupControlButtons();
}

// Функция для применения стилей к SVG
function applySvgStyles(svg) {
    console.log('Applying styles to SVG:', svg);
    console.log('SVG before styling:', svg.outerHTML.substring(0, 200) + '...');
    
    svg.style.maxWidth = '100%';
    svg.style.maxHeight = '100%';
    svg.style.width = 'auto';
    svg.style.height = 'auto';
    svg.style.transformOrigin = 'center center';
    svg.style.objectFit = 'contain';
    svg.style.display = 'block';
    svg.style.margin = 'auto';
    
    console.log('SVG after styling:', svg.outerHTML.substring(0, 200) + '...');
}

// Функция для настройки обработчиков кнопок управления
function setupControlButtons() {
    const modal = document.querySelector('.mermaid-modal-overlay');
    if (!modal) return;
    
    // Обрабатываем все кнопки с data-action
    const buttons = modal.querySelectorAll('button[data-action]');
    console.log(`Setting up ${buttons.length} control buttons`);
    
    buttons.forEach(button => {
        const action = button.getAttribute('data-action');
        if (!action || button.classList.contains('spacer')) return;
        
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log(`Control button clicked: ${action}`);
            
            switch(action) {
                case 'panUp': panUp(); break;
                case 'panDown': panDown(); break;
                case 'panLeft': panLeft(); break;
                case 'panRight': panRight(); break;
                case 'zoomIn': zoomIn(); break;
                case 'zoomOut': zoomOut(); break;
                case 'resetView': resetView(); break;
                case 'close': closeMermaidModal(); break;
                case 'toggleTheme': toggleMermaidTheme(); break;
                default: console.log(`Unknown action: ${action}`);
            }
        });
    });
}

// Функция для закрытия модального окна
function closeMermaidModal() {
    const modal = document.querySelector('.mermaid-modal-overlay');
    if (modal) {
        modal.remove();
        document.removeEventListener('keydown', handleKeyDown);
        console.log('Modal closed');
    }
}

// Функции управления масштабом и панорамированием
function zoomIn() {
    console.log('zoomIn function called');
    currentScale = Math.min(currentScale * 1.2, 5);
    console.log('Zoom in:', currentScale);
    updateSvgTransform();
}

function zoomOut() {
    currentScale = Math.max(currentScale / 1.2, 0.1);
    console.log('Zoom out:', currentScale);
    updateSvgTransform();
}

function panUp() {
    console.log('panUp function called');
    currentPanY += 50;
    console.log('Pan up:', currentPanY);
    updateSvgTransform();
}

function panDown() {
    currentPanY -= 50;
    console.log('Pan down:', currentPanY);
    updateSvgTransform();
}

function panLeft() {
    currentPanX += 50;
    console.log('Pan left:', currentPanX);
    updateSvgTransform();
}

function panRight() {
    currentPanX -= 50;
    console.log('Pan right:', currentPanX);
    updateSvgTransform();
}

function resetView() {
    currentScale = 1;
    currentPanX = 0;
    currentPanY = 0;
    console.log('Reset view');
    updateSvgTransform();
}

function updateSvgTransform() {
    const svg = document.querySelector('#mermaid-modal-diagram svg');
    if (svg) {
        // Проверяем, что SVG имеет видимые размеры
        const rect = svg.getBoundingClientRect();
        if (rect.width === 0 || rect.height === 0) {
            console.log('SVG has zero dimensions, retrying in 100ms...');
            setTimeout(updateSvgTransform, 100);
            return;
        }
        
        const transform = `translate(${currentPanX}px, ${currentPanY}px) scale(${currentScale})`;
        svg.style.transform = transform;
        svg.style.transformOrigin = 'center center';
        console.log('Applied transform:', transform);
        console.log('SVG rect:', rect);
    } else {
        console.log('No SVG found for transform');
        console.log('Available elements in modal:', document.querySelector('#mermaid-modal-diagram')?.innerHTML);
    }
}

// Функция для переключения темы
function toggleMermaidTheme() {
    const button = document.querySelector('.mermaid-theme-toggle');
    const svg = document.querySelector('#mermaid-modal-diagram svg');
    
    console.log('Toggle theme clicked');
    console.log('Button text:', button.textContent);
    console.log('SVG found:', !!svg);
    
    // Проверяем текущее состояние по наличию фильтра
    const currentFilter = svg ? svg.style.filter : '';
    const isDarkTheme = currentFilter.includes('invert');
    
    if (!isDarkTheme) {
        button.textContent = '☀️';
        if (svg) {
            svg.style.filter = 'invert(1) hue-rotate(180deg)';
            console.log('Applied dark theme filter');
        }
    } else {
        button.textContent = '🌙';
        if (svg) {
            svg.style.filter = 'none';
            console.log('Removed theme filter');
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
    console.log('DOM loaded, initializing Mermaid controls...');
    
    // Ждем немного, чтобы MkDocs и плагин mermaid2 обработали диаграммы
    setTimeout(() => {
        waitForMermaid();
    }, 2000);
});

// Дополнительная инициализация при полной загрузке страницы
window.addEventListener('load', function() {
    console.log('Window loaded, trying to initialize Mermaid again...');
    setTimeout(() => {
        if (!mermaidInitialized) {
            waitForMermaid();
        }
    }, 1000);
});

// Дополнительная инициализация при изменении содержимого страницы
let observer = null;

function setupObserver() {
    if (observer) {
        observer.disconnect();
    }
    
    observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                const diagrams = document.querySelectorAll('.mermaid:not([data-controls-added])');
                if (diagrams.length > 0) {
                    diagrams.forEach(diagram => {
                        diagram.setAttribute('data-controls-added', 'true');
                        addFullscreenButton(diagram);
                        diagram.addEventListener('click', function(e) {
                            if (e.target.closest('.mermaid-fullscreen-btn')) return;
                            openMermaidFullscreen(this);
                        });
                    });
                }
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

// Запускаем observer после инициализации
setTimeout(() => {
    setupObserver();
}, 3000);

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