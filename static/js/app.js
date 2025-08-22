// Optimized Image to Text Generator
document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.mode-tabs .tab');
    const modes = document.querySelectorAll('.input-mode');
    const fileInput = document.getElementById('image_file');
    const dropzone = document.getElementById('dropzone');
    const preview = document.getElementById('preview');
    const previewImg = document.getElementById('preview-img');
    const clearBtn = document.getElementById('clear-file');
    const imageUrl = document.getElementById('image_url');
    const localPath = document.getElementById('image_local_path');
    const form = document.getElementById('convert-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.getElementById('btn-text');

    // Simple background animation (reduced from complex math symbols)
    function createSimpleBackground() {
        const mathBackground = document.getElementById('math-background');
        const symbols = ['∑', 'π', '∞', '∂', '√', '∫', 'Δ', 'Ω', 'λ', 'μ'];
        
        for (let i = 0; i < 15; i++) {
            const symbol = document.createElement('div');
            symbol.className = 'math-symbol';
            symbol.textContent = symbols[Math.floor(Math.random() * symbols.length)];
            symbol.style.left = Math.random() * 100 + '%';
            symbol.style.top = Math.random() * 100 + '%';
            symbol.style.fontSize = (16 + Math.random() * 24) + 'px';
            symbol.style.animationDelay = Math.random() * 10 + 's';
            mathBackground.appendChild(symbol);
        }
    }

    createSimpleBackground();

    // Tab switching
    function setMode(mode) {
        tabs.forEach(t => {
            const active = t.dataset.mode === mode;
            t.classList.toggle('active', active);
            t.setAttribute('aria-selected', String(active));
        });
        
        modes.forEach(el => {
            const active = el.dataset.mode === mode;
            el.classList.toggle('hidden', !active);
            if (el.dataset.mode === 'url') imageUrl.disabled = !active;
            if (el.dataset.mode === 'local') localPath.disabled = !active;
        });
        
        // Clear inputs
        if (mode !== 'upload') {
            fileInput.value = '';
            preview.classList.add('hidden');
        }
        if (mode !== 'url') imageUrl.value = '';
        if (mode !== 'local') localPath.value = '';
    }

    tabs.forEach(tab => tab.addEventListener('click', () => setMode(tab.dataset.mode)));

    // Dropzone functionality
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(name =>
        dropzone.addEventListener(name, e => e.preventDefault())
    );
    
    ['dragenter', 'dragover'].forEach(name =>
        dropzone.addEventListener(name, () => dropzone.classList.add('dragover'))
    );
    
    ['dragleave', 'drop'].forEach(name =>
        dropzone.addEventListener(name, () => dropzone.classList.remove('dragover'))
    );
    
    dropzone.addEventListener('click', () => fileInput.click());
    
    dropzone.addEventListener('drop', e => {
        const files = e.dataTransfer.files;
        if (files && files[0]) {
            fileInput.files = files;
            showPreview(files[0]);
            setMode('upload');
        }
        
        const text = e.dataTransfer.getData('text/plain');
        if (text && /^https?:\/\//i.test(text)) {
            imageUrl.value = text;
            setMode('url');
        }
    });

    // File preview
    fileInput.addEventListener('change', () => {
        const file = fileInput.files && fileInput.files[0];
        if (file) showPreview(file);
    });

    function showPreview(file) {
        const reader = new FileReader();
        reader.onload = e => {
            previewImg.src = e.target.result;
            preview.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }

    clearBtn.addEventListener('click', () => {
        fileInput.value = '';
        preview.classList.add('hidden');
    });

    // Form submission
    form.addEventListener('submit', () => {
        submitBtn.disabled = true;
        btnText.textContent = 'Generating...';
        submitBtn.setAttribute('aria-busy', 'true');
        
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.style.display = 'flex';
            overlay.classList.remove('hidden');
        }
    });

    // Paste support
    document.addEventListener('paste', e => {
        const items = e.clipboardData?.items || [];
        
        for (const item of items) {
            if (item.type && item.type.startsWith('image/')) {
                const file = item.getAsFile();
                if (file) {
                    const dt = new DataTransfer();
                    dt.items.add(file);
                    fileInput.files = dt.files;
                    showPreview(file);
                    setMode('upload');
                    return;
                }
            }
        }
        
        const text = e.clipboardData?.getData('text');
        if (text && /^https?:\/\//i.test(text)) {
            imageUrl.value = text;
            setMode('url');
        }
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            form.requestSubmit();
        }
    });

    // Initialize
    setMode('upload');
    
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.add('hidden');
        overlay.style.display = 'none';
    }

    const hasDescription = !!document.getElementById('description-text');
    if (hasDescription) {
        submitBtn.disabled = false;
        btnText.textContent = 'Generated Successfully';
        submitBtn.setAttribute('aria-busy', 'false');
    } else {
        btnText.textContent = 'Generate Description';
    }
});


