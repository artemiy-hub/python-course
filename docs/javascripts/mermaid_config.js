// Enhanced Mermaid configuration with advanced controls like marmaid.html
let mermaidLoaded = false;
let mermaidInitialized = false;

// Функция для проверки загрузки Mermaid
function checkMermaidLoaded() {
    return typeof mermaid !== 'undefined' && mermaid !== null;
}

// Функция для получения исходного кода диаграммы
function getMermaidSourceCode(element) {
    // Проверяем атрибут data-diagram-source
    const sourceCode = element.getAttribute('data-diagram-source');
    if (sourceCode) {
        return sourceCode;
    }
    
    // Проверяем атрибут data-mermaid-source
    const mermaidSource = element.getAttribute('data-mermaid-source');
    if (mermaidSource) {
        return mermaidSource;
    }
    
    // Проверяем скрытый элемент с исходным кодом
    const sourceElement = element.querySelector('.mermaid-source');
    if (sourceElement) {
        return sourceElement.textContent || sourceElement.innerText;
    }
    
    // Проверяем содержимое элемента (если это еще не SVG)
    const textContent = element.textContent || element.innerText;
    if (textContent && !textContent.includes('<svg') && !textContent.includes('font-family:')) {
        return textContent;
    }
    
    // Если элемент уже содержит SVG, ищем исходный код в ближайших элементах
    const parent = element.parentElement;
    if (parent) {
        // Ищем комментарии с исходным кодом
        const comments = Array.from(parent.childNodes).filter(node => 
            node.nodeType === Node.COMMENT_NODE
        );
        
        for (const comment of comments) {
            const commentText = comment.textContent.trim();
            if (commentText.includes('graph') || 
                commentText.includes('flowchart') || 
                commentText.includes('sequenceDiagram') ||
                commentText.includes('stateDiagram') ||
                commentText.includes('classDiagram') ||
                commentText.includes('mindmap')) {
                return commentText;
            }
        }
        
        // Ищем в предыдущих элементах
        const prevElement = element.previousElementSibling;
        if (prevElement && prevElement.classList.contains('mermaid-source')) {
            return prevElement.textContent || prevElement.innerText;
        }
    }
    
    return null;
}

// Функция для проверки, является ли содержимое валидным кодом Mermaid
function isValidMermaidCode(text) {
    if (!text || typeof text !== 'string') return false;
    
    const trimmedText = text.trim();
    if (!trimmedText) return false;
    
    // Проверяем, не является ли это CSS кодом
    if (trimmedText.includes('font-family:') || 
        trimmedText.includes('fill:') || 
        trimmedText.includes('stroke:') ||
        trimmedText.includes('#mermaid-') ||
        trimmedText.includes('<svg')) {
        return false;
    }
    
    // Проверяем наличие ключевых слов Mermaid
    const mermaidKeywords = [
        'graph', 'flowchart', 'sequenceDiagram', 'classDiagram', 
        'stateDiagram', 'erDiagram', 'journey', 'gantt', 'pie', 
        'gitgraph', 'quadrantChart', 'timeline', 'zenuml', 'sankey', 'mindmap'
    ];
    
    const hasMermaidKeyword = mermaidKeywords.some(keyword => 
        trimmedText.toLowerCase().includes(keyword.toLowerCase())
    );
    
    // Проверяем наличие стрелок или связей
    const hasConnections = /-->|==>|\.\.\.>|-->|==>|\.\.\.>|--|==|\.\.\./.test(trimmedText);
    
    // Проверяем наличие узлов (квадратные скобки, круглые скобки и т.д.)
    const hasNodes = /\[.*\]|\(.*\)|{.*}|".*"|'.*'/.test(trimmedText);
    
    // Проверяем наличие участников в sequence diagram
    const hasParticipants = /participant\s+\w+/.test(trimmedText);
    
    // Проверяем наличие состояний в state diagram
    const hasStates = /\[\*\]|state\s+\w+/.test(trimmedText);
    
    return hasMermaidKeyword || hasConnections || hasNodes || hasParticipants || hasStates;
}

// Функция загрузки Mermaid
function loadMermaid() {
    return new Promise((resolve, reject) => {
        if (checkMermaidLoaded()) {
            resolve();
            return;
        }
        
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js';
        script.onload = () => {
            mermaidLoaded = true;
            resolve();
        };
        script.onerror = () => {
            reject(new Error('Failed to load Mermaid'));
        };
        document.head.appendChild(script);
    });
}

// Инициализация Mermaid
function initializeMermaid() {
    if (mermaidInitialized) return;
    
    try {
        mermaid.initialize({
            startOnLoad: false, // Отключаем автозагрузку
            theme: 'default',
            flowchart: {
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            },
            sequence: {
                useMaxWidth: true,
                diagramMarginX: 50,
                diagramMarginY: 10
            },
            gantt: {
                useMaxWidth: true
            },
            journey: {
                useMaxWidth: true
            },
            gitGraph: {
                useMaxWidth: true
            },
            pie: {
                useMaxWidth: true
            },
            quadrantChart: {
                useMaxWidth: true
            },
            timeline: {
                useMaxWidth: true
            },
            stateDiagram: {
                useMaxWidth: true
            },
            classDiagram: {
                useMaxWidth: true
            },
            erDiagram: {
                useMaxWidth: true
            },
            themeVariables: {
                darkMode: document.documentElement.getAttribute('data-md-color-scheme') === 'slate'
            }
        });
        
        mermaidInitialized = true;
        console.log('Mermaid initialized successfully');
        
        // Process all mermaid diagrams
        processMermaidDiagrams();
        
        // Create modal overlay
        createMermaidModal();
        
    } catch (error) {
        console.error('Error initializing Mermaid:', error);
    }
}

// Обработка всех диаграмм Mermaid
function processMermaidDiagrams() {
    var mermaidDivs = document.querySelectorAll('.mermaid');
    console.log('Found', mermaidDivs.length, 'mermaid diagrams');
    
    mermaidDivs.forEach(function(element, index) {
        try {
            // Проверяем, не был ли уже обработан элемент
            if (element.hasAttribute('data-mermaid-processed')) {
                return;
            }
            
            // Проверяем, содержит ли элемент уже SVG (уже обработан mermaid2)
            const hasSvg = element.querySelector('svg');
            
            if (hasSvg) {
                // Элемент уже содержит SVG, сохраняем исходный код и добавляем интерактивность
                saveSourceCodeForElement(element);
                setupMermaidInteractivity(element);
                element.setAttribute('data-mermaid-processed', 'true');
                console.log('Diagram', index, 'already rendered, adding interactivity');
                return;
            }
            
            // Получаем исходный код диаграммы
            const sourceCode = getMermaidSourceCode(element);
            
            if (!sourceCode) {
                console.warn('No valid Mermaid code found in element', index);
                element.innerHTML = `<div style="color: orange; padding: 20px; text-align: center;">⚠️ Не найден код диаграммы Mermaid</div>`;
                element.setAttribute('data-mermaid-processed', 'true');
                return;
            }
            
            console.log('Processing diagram', index, ':', sourceCode.substring(0, 100) + '...');
            
            // Сохраняем исходный код
            element.setAttribute('data-mermaid-source', sourceCode);
            
            // Очищаем элемент и добавляем исходный код
            element.innerHTML = '';
            element.textContent = sourceCode;
            
            // Рендерим диаграмму
            mermaid.init(undefined, element);
            
            // Настраиваем интерактивность
            setupMermaidInteractivity(element);
            
            // Отмечаем как обработанный
            element.setAttribute('data-mermaid-processed', 'true');
            
        } catch (error) {
            console.error('Error rendering mermaid diagram', index, ':', error);
            // Показываем ошибку в элементе
            element.innerHTML = `<div style="color: red; padding: 20px; text-align: center;">Ошибка рендеринга: ${error.message}</div>`;
            element.setAttribute('data-mermaid-processed', 'true');
        }
    });
}

// Функция для сохранения исходного кода для уже обработанных элементов
function saveSourceCodeForElement(element) {
    // Ищем исходный код в ближайших элементах
    const parent = element.parentElement;
    if (parent) {
        // Ищем в предыдущих элементах
        let prevElement = element.previousElementSibling;
        while (prevElement) {
            if (prevElement.tagName === 'PRE' && prevElement.querySelector('code.language-mermaid')) {
                const sourceCode = prevElement.textContent.trim();
                if (isValidMermaidCode(sourceCode)) {
                    element.setAttribute('data-mermaid-source', sourceCode);
                    return;
                }
            }
            prevElement = prevElement.previousElementSibling;
        }
        
        // Ищем в следующих элементах
        let nextElement = element.nextElementSibling;
        while (nextElement) {
            if (nextElement.tagName === 'PRE' && nextElement.querySelector('code.language-mermaid')) {
                const sourceCode = nextElement.textContent.trim();
                if (isValidMermaidCode(sourceCode)) {
                    element.setAttribute('data-mermaid-source', sourceCode);
                    return;
                }
            }
            nextElement = nextElement.nextElementSibling;
        }
        
        // Ищем в комментариях
        const comments = Array.from(parent.childNodes).filter(node => 
            node.nodeType === Node.COMMENT_NODE
        );
        
        for (const comment of comments) {
            const commentText = comment.textContent.trim();
            if (isValidMermaidCode(commentText)) {
                element.setAttribute('data-mermaid-source', commentText);
                return;
            }
        }
    }
}

function setupMermaidInteractivity(element) {
    // Add zoomable class
    element.classList.add('zoomable');
    
    // Add zoom controls
    const zoomControls = document.createElement('div');
    zoomControls.className = 'mermaid-zoom-controls-embedded';
    zoomControls.innerHTML = `
        <button class="mermaid-zoom-btn-small" onclick="zoomMermaid(this, 1.2)" title="Увеличить">+</button>
        <button class="mermaid-zoom-btn-small" onclick="zoomMermaid(this, 0.8)" title="Уменьшить">-</button>
        <button class="mermaid-zoom-btn-small" onclick="openMermaidFullscreen(this)" title="Полноэкранный режим">⛶</button>
    `;
    element.appendChild(zoomControls);
    
    // Add click handler for fullscreen
    element.addEventListener('click', function(e) {
        if (!e.target.closest('.mermaid-zoom-controls-embedded')) {
            openMermaidFullscreen(element);
        }
    });
}

function createMermaidModal() {
    // Remove existing modal if any
    const existingModal = document.getElementById('mermaid-modal');
    if (existingModal) {
        existingModal.remove();
    }
    
    const modal = document.createElement('div');
    modal.className = 'mermaid-modal';
    modal.id = 'mermaid-modal';
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
    
    // Close modal on background click
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeMermaidModal();
        }
    });
    
    // Close modal on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('show')) {
            closeMermaidModal();
        }
    });
}

// Global variables for modal controls
let currentScale = 1;
let currentX = 0;
let currentY = 0;

function closeMermaidModal() {
    const modal = document.getElementById('mermaid-modal');
    if (modal) {
        modal.classList.remove('show');
        
        // Clear modal content
        const modalDiagram = document.getElementById('mermaid-modal-diagram');
        if (modalDiagram) {
            modalDiagram.innerHTML = '';
        }
    }
}

// Advanced control functions (like in marmaid.html)
function zoomIn() {
    currentScale *= 1.2;
    updateTransform();
}

function zoomOut() {
    currentScale /= 1.2;
    updateTransform();
}

function panUp() {
    currentY += 50;
    updateTransform();
}

function panDown() {
    currentY -= 50;
    updateTransform();
}

function panLeft() {
    currentX += 50;
    updateTransform();
}

function panRight() {
    currentX -= 50;
    updateTransform();
}

function resetView() {
    currentScale = 1;
    currentX = 0;
    currentY = 0;
    updateTransform();
}

function updateTransform() {
    const modalDiagram = document.getElementById('mermaid-modal-diagram');
    if (modalDiagram) {
        const svg = modalDiagram.querySelector('svg');
        if (svg) {
            svg.style.transform = `translate(${currentX}px, ${currentY}px) scale(${currentScale})`;
        }
    }
}

function zoomMermaid(button, factor) {
    const mermaidDiv = button.closest('.mermaid');
    const svg = mermaidDiv.querySelector('svg');
    if (svg) {
        const currentScale = svg.style.transform ? 
            parseFloat(svg.style.transform.match(/scale\(([^)]+)\)/)?.[1] || 1) : 1;
        const newScale = Math.max(0.5, Math.min(3, currentScale * factor));
        svg.style.transform = `scale(${newScale})`;
        svg.style.transformOrigin = 'center center';
    }
}

function toggleMermaidTheme() {
    const modal = document.getElementById('mermaid-modal');
    const themeButton = modal.querySelector('.mermaid-theme-toggle');
    
    // Toggle theme
    const isDark = modal.classList.contains('dark-theme');
    if (isDark) {
        modal.classList.remove('dark-theme');
        themeButton.textContent = '🌙';
        themeButton.title = 'Переключить на темную тему';
    } else {
        modal.classList.add('dark-theme');
        themeButton.textContent = '☀️';
        themeButton.title = 'Переключить на светлую тему';
    }
}

function openMermaidFullscreen(element) {
    if (!checkMermaidLoaded()) {
        console.error('Mermaid not loaded');
        return;
    }
    
    const modal = document.getElementById('mermaid-modal');
    const modalDiagram = document.getElementById('mermaid-modal-diagram');
    
    if (!modal || !modalDiagram) {
        console.error('Modal elements not found');
        return;
    }
    
    // Clear previous content
    modalDiagram.innerHTML = '';
    
    // Проверяем, содержит ли элемент уже SVG
    const svg = element.querySelector('svg');
    if (svg) {
        // Клонируем SVG для модального окна
        const clonedSvg = svg.cloneNode(true);
        
        // Создаем новый контейнер для SVG
        const svgContainer = document.createElement('div');
        svgContainer.className = 'mermaid';
        svgContainer.appendChild(clonedSvg);
        
        // Сбрасываем все трансформации и устанавливаем правильные размеры
        clonedSvg.style.transform = 'none';
        clonedSvg.style.maxWidth = '100%';
        clonedSvg.style.maxHeight = '100%';
        clonedSvg.style.width = 'auto';
        clonedSvg.style.height = 'auto';
        
        // Автоматическое масштабирование для очень широких диаграмм
        const viewBox = clonedSvg.getAttribute('viewBox');
        if (viewBox) {
            const parts = viewBox.split(' ');
            const width = parseFloat(parts[2]);
            const height = parseFloat(parts[3]);
            
            if (width > 2000) {
                const scale = Math.min(0.3, 1200 / width);
                clonedSvg.style.transform = `scale(${scale})`;
                clonedSvg.style.transformOrigin = 'center center';
            } else if (width > 1500) {
                const scale = Math.min(0.5, 1000 / width);
                clonedSvg.style.transform = `scale(${scale})`;
                clonedSvg.style.transformOrigin = 'center center';
            }
        }
        
        modalDiagram.appendChild(svgContainer);
        modal.classList.add('show');
        resetView();
        return;
    }
    
    // Получаем исходный код диаграммы
    const sourceCode = getMermaidSourceCode(element);
    
    if (!sourceCode) {
        modalDiagram.innerHTML = `<div style="color: orange; padding: 20px; text-align: center;">⚠️ Не найден код диаграммы Mermaid</div>`;
        modal.classList.add('show');
        return;
    }
    
    // Create a new mermaid div for the modal
    const newMermaidDiv = document.createElement('div');
    newMermaidDiv.className = 'mermaid';
    newMermaidDiv.textContent = sourceCode;
    
    // Add the diagram to modal
    modalDiagram.appendChild(newMermaidDiv);
    
    // Show modal
    modal.classList.add('show');
    
    // Re-render mermaid in modal with error handling
    try {
        mermaid.init(undefined, newMermaidDiv).then(() => {
            resetView(); // Reset view when opening
            
            // Сбрасываем трансформации после рендеринга
            const newSvg = newMermaidDiv.querySelector('svg');
            if (newSvg) {
                newSvg.style.transform = 'none';
                newSvg.style.maxWidth = '100%';
                newSvg.style.maxHeight = '100%';
                newSvg.style.width = 'auto';
                newSvg.style.height = 'auto';
                
                // Автоматическое масштабирование для очень широких диаграмм
                const viewBox = newSvg.getAttribute('viewBox');
                if (viewBox) {
                    const parts = viewBox.split(' ');
                    const width = parseFloat(parts[2]);
                    const height = parseFloat(parts[3]);
                    
                    if (width > 2000) {
                        const scale = Math.min(0.3, 1200 / width);
                        newSvg.style.transform = `scale(${scale})`;
                        newSvg.style.transformOrigin = 'center center';
                    } else if (width > 1500) {
                        const scale = Math.min(0.5, 1000 / width);
                        newSvg.style.transform = `scale(${scale})`;
                        newSvg.style.transformOrigin = 'center center';
                    }
                }
            }
        }).catch(error => {
            console.error('Error rendering mermaid diagram in modal:', error);
            modalDiagram.innerHTML = `<div style="color: red; padding: 20px; text-align: center;">Ошибка рендеринга: ${error.message}</div>`;
        });
    } catch (error) {
        console.error('Error initializing mermaid in modal:', error);
        modalDiagram.innerHTML = `<div style="color: red; padding: 20px; text-align: center;">Ошибка: ${error.message}</div>`;
    }
}


// Основная инициализация
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, checking for Mermaid...');
    
    // Проверяем, загружен ли уже Mermaid
    if (checkMermaidLoaded()) {
        console.log('Mermaid already loaded');
        initializeMermaid();
    } else {
        console.log('Loading Mermaid...');
        loadMermaid().then(() => {
            console.log('Mermaid loaded successfully');
            initializeMermaid();
        }).catch(error => {
            console.error('Failed to load Mermaid:', error);
        });
    }
});

// Дополнительная проверка для случаев, когда Mermaid загружается после DOM
window.addEventListener('load', function() {
    if (!mermaidInitialized && checkMermaidLoaded()) {
        console.log('Mermaid loaded after window load');
        initializeMermaid();
    }
});



// Обработка динамически добавленных диаграмм
function observeMermaidDiagrams() {
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1) { // Element node
                    const mermaidDivs = node.querySelectorAll ? node.querySelectorAll('.mermaid') : [];
                    mermaidDivs.forEach(function(element) {
                        if (!element.hasAttribute('data-mermaid-processed')) {
                            try {
                                const hasSvg = element.querySelector('svg');
                                if (hasSvg) {
                                    saveSourceCodeForElement(element);
                                    setupMermaidInteractivity(element);
                                    element.setAttribute('data-mermaid-processed', 'true');
                                } else {
                                    const sourceCode = getMermaidSourceCode(element);
                                    if (sourceCode) {
                                        element.setAttribute('data-mermaid-source', sourceCode);
                                        element.innerHTML = '';
                                        element.textContent = sourceCode;
                                        mermaid.init(undefined, element);
                                        setupMermaidInteractivity(element);
                                        element.setAttribute('data-mermaid-processed', 'true');
                                    }
                                }
                            } catch (error) {
                                console.error('Error processing new mermaid diagram:', error);
                            }
                        }
                    });
                }
            });
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

// Запускаем наблюдение после инициализации
setTimeout(observeMermaidDiagrams, 1000);