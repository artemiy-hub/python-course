// Enhanced Mermaid configuration with zoom and fullscreen support
document.addEventListener('DOMContentLoaded', function() {
    // Wait for Mermaid to be loaded
    if (typeof mermaid !== 'undefined') {
        initializeMermaid();
    } else {
        // Load Mermaid if not already loaded
        var script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js';
        script.onload = initializeMermaid;
        document.head.appendChild(script);
    }
});

function initializeMermaid() {
    mermaid.initialize({
        startOnLoad: true,
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
        }
    });
    
    // Process all mermaid diagrams
    var mermaidDivs = document.querySelectorAll('.mermaid');
    mermaidDivs.forEach(function(element) {
        try {
            mermaid.init(undefined, element);
            setupMermaidInteractivity(element);
        } catch (error) {
            console.error('Error rendering mermaid diagram:', error);
        }
    });
    
    // Create modal overlay
    createMermaidModal();
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
            <div class="mermaid-modal-diagram-container">
                <div id="mermaid-modal-diagram"></div>
            </div>
            <div class="mermaid-modal-zoom-controls">
                <button class="mermaid-zoom-btn" onclick="zoomModalMermaid(1.2)">Увеличить</button>
                <button class="mermaid-zoom-btn" onclick="zoomModalMermaid(0.8)">Уменьшить</button>
                <button class="mermaid-zoom-btn" onclick="resetModalMermaidZoom()">Сброс</button>
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

function openMermaidFullscreen(element) {
    const modal = document.getElementById('mermaid-modal');
    const modalDiagram = document.getElementById('mermaid-modal-diagram');
    
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
    
    // Re-render mermaid in modal
    try {
        mermaid.init(undefined, modalDiagram);
    } catch (error) {
        console.error('Error rendering mermaid diagram in modal:', error);
    }
}

function closeMermaidModal() {
    const modal = document.getElementById('mermaid-modal');
    modal.classList.remove('show');
    
    // Clear modal content
    const modalDiagram = document.getElementById('mermaid-modal-diagram');
    if (modalDiagram) {
        modalDiagram.innerHTML = '';
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

function zoomModalMermaid(factor) {
    const modalDiagram = document.getElementById('mermaid-modal-diagram');
    const svg = modalDiagram.querySelector('svg');
    if (svg) {
        const currentScale = svg.style.transform ? 
            parseFloat(svg.style.transform.match(/scale\(([^)]+)\)/)?.[1] || 1) : 1;
        const newScale = Math.max(0.5, Math.min(3, currentScale * factor));
        svg.style.transform = `scale(${newScale})`;
        svg.style.transformOrigin = 'center center';
    }
}

function resetModalMermaidZoom() {
    const modalDiagram = document.getElementById('mermaid-modal-diagram');
    const svg = modalDiagram.querySelector('svg');
    if (svg) {
        svg.style.transform = 'scale(1)';
    }
}