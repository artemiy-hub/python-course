// Enhanced Mermaid configuration with advanced controls like marmaid.html
let mermaidLoaded = false;
let mermaidInitialized = false;

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
            console.error('Mermaid failed to load after', maxAttempts, 'attempts');
        }
    }
    
    check();
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
            
            // Рендерим диаграмму
            mermaid.init(undefined, element);
            
            // Настраиваем интерактивность
            setupMermaidInteractivity(element);
            
            // Отмечаем как обработанный
            element.setAttribute('data-mermaid-processed', 'true');
            
        } catch (error) {
            console.error('Error rendering mermaid diagram', index, ':', error);
        }
    });
}

function setupMermaidInteractivity(element) {
    // Add zoomable class
    element.classList.add('zoomable');
    
    // Add zoom controls
    const zoomControls = document.createElement('div');
    zoomControls.className = 'mermaid-zoom-controls-embedded';
    zoomControls.innerHTML = `
        <button class="mermaid-zoom-btn-small" onclick="zoomMermaid(this, 1.2)">+</button>
        <button class="mermaid-zoom-btn-small" onclick="zoomMermaid(this, 0.8)">-</button>
        <button class="mermaid-zoom-btn-small" onclick="openMermaidFullscreen(this)">⛶</button>
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
            <button class="mermaid-modal-close" onclick="closeMermaidModal()">×</button>
            <button class="mermaid-theme-toggle" onclick="toggleMermaidTheme()">🌙</button>
            <div class="mermaid-modal-diagram-container">
                <div id="mermaid-modal-diagram"></div>
            </div>
            <div class="mermaid-controls">
                <button class="up" onclick="panUp()">↑</button>
                <button class="reset" onclick="resetView()">⟲</button>
                <button class="down" onclick="panDown()">↓</button>
                <button class="left" onclick="panLeft()">←</button>
                <button class="zoom-in" onclick="zoomIn()">+</button>
                <button class="zoom-out" onclick="zoomOut()">−</button>
                <button class="right" onclick="panRight()">→</button>
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
    
    // Clone the diagram content
    const diagramContent = element.cloneNode(true);
    
    // Remove zoom controls from modal version
    const zoomControls = diagramContent.querySelector('.mermaid-zoom-controls-embedded');
    if (zoomControls) {
        zoomControls.remove();
    }
    
    // Add the diagram to modal
    modalDiagram.appendChild(diagramContent);
    
    // Show modal
    modal.classList.add('show');
    
    // Re-render mermaid in modal with error handling
    try {
        mermaid.init(undefined, modalDiagram).then(() => {
            resetView(); // Reset view when opening
        }).catch(error => {
            console.error('Error rendering mermaid diagram in modal:', error);
            modalDiagram.innerHTML = `<div style="color: red; padding: 20px;">Ошибка рендеринга: ${error.message}</div>`;
        });
    } catch (error) {
        console.error('Error initializing mermaid in modal:', error);
        modalDiagram.innerHTML = `<div style="color: red; padding: 20px;">Ошибка: ${error.message}</div>`;
    }
}

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
    } else {
        modal.classList.add('dark-theme');
        themeButton.textContent = '☀️';
    }
    
    // Re-render with new theme
    const modalDiagram = document.getElementById('mermaid-modal-diagram');
    if (modalDiagram) {
        const svg = modalDiagram.querySelector('svg');
        if (svg) {
            // Re-render the diagram with new theme
            const diagramCode = svg.getAttribute('data-diagram-code');
            if (diagramCode) {
                mermaid.render('temp-diagram', diagramCode).then(({ svg: newSvg }) => {
                    svg.outerHTML = newSvg;
                });
            }
        }
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
                                mermaid.init(undefined, element);
                                setupMermaidInteractivity(element);
                                element.setAttribute('data-mermaid-processed', 'true');
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
