// Black and White Webapp - Clean Modern JavaScript with Mathematical Background
document.addEventListener('DOMContentLoaded', () => {
    const tabs = Array.from(document.querySelectorAll('.mode-tabs .tab'));
    const modes = Array.from(document.querySelectorAll('.input-mode'));
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

    // Mathematical Background Animation
    function createMathBackground() {
        const mathBackground = document.getElementById('math-background');
        const mathSymbols = [
            '∑', 'π', '∞', '∂', '√', '∫', 'Δ', 'Ω', 'λ', 'μ', 'σ', 'θ', 'φ', 'ψ', 'α', 'β', 'γ', 'δ', 'ε', 'ζ',
            'η', 'ι', 'κ', 'ν', 'ξ', 'ο', 'ρ', 'τ', 'υ', 'χ', 'ω', '∇', '∏', '∐', '⊕', '⊗', '⊖', '⊘', '⊙', '⊚',
            '⊛', '⊜', '⊝', '⊞', '⊟', '⊠', '⊡', '⊢', '⊣', '⊤', '⊥', '⊦', '⊧', '⊨', '⊩', '⊪', '⊫', '⊬', '⊭', '⊮',
            '±', '∓', '×', '÷', '⋅', '∘', '∙', '⋆', '⋄', '⋆', '⋇', '⋈', '⋉', '⋊', '⋋', '⋌', '⋍', '⋎', '⋏', '⋐', '⋑',
            '⋒', '⋓', '⋔', '⋕', '⋖', '⋗', '⋘', '⋙', '⋚', '⋛', '⋜', '⋝', '⋞', '⋟', '⋠', '⋡', '⋢', '⋣', '⋤', '⋥',
            '⋦', '⋧', '⋨', '⋩', '⋪', '⋫', '⋬', '⋭', '⋮', '⋯', '⋰', '⋱', '⋲', '⋳', '⋴', '⋵', '⋶', '⋷', '⋸', '⋹',
            '⋺', '⋻', '⋼', '⋽', '⋾', '⋿', '⌀', '⌁', '⌂', '⌃', '⌄', '⌅', '⌆', '⌇', '⌈', '⌉', '⌊', '⌋', '⌌', '⌍',
            '⌎', '⌏', '⌐', '⌑', '⌒', '⌓', '⌔', '⌕', '⌖', '⌗', '⌘', '⌙', '⌚', '⌛', '⌜', '⌝', '⌞', '⌟', '⌠', '⌡'
        ];
        
        const numSymbols = 35; // Increased number of symbols
        
        for (let i = 0; i < numSymbols; i++) {
            const symbol = document.createElement('div');
            symbol.className = 'math-symbol';
            symbol.textContent = mathSymbols[Math.floor(Math.random() * mathSymbols.length)];
            
            // Random positioning
            symbol.style.left = Math.random() * 100 + '%';
            symbol.style.top = Math.random() * 100 + '%';
            
            // Random size with more variation
            const size = 16 + Math.random() * 48;
            symbol.style.fontSize = size + 'px';
            
            // Random animation delay and duration
            const colorDelay = Math.random() * 15;
            const floatDelay = Math.random() * 20;
            symbol.style.animationDelay = colorDelay + 's, ' + floatDelay + 's';
            
            // Random z-index for layering
            symbol.style.zIndex = Math.floor(Math.random() * 15);
            
            // Add random rotation offset
            symbol.style.transform = `rotate(${Math.random() * 360}deg)`;
            
            // Add some symbols with different animation patterns
            if (i % 7 === 0) {
                symbol.style.animation = 'colorShift 6s ease-in-out infinite, float 15s linear infinite';
            } else if (i % 5 === 0) {
                symbol.style.animation = 'colorShift 10s ease-in-out infinite, float 25s linear infinite';
            } else if (i % 3 === 0) {
                symbol.style.animation = 'colorShift 12s ease-in-out infinite, float 30s linear infinite';
            }
            
            mathBackground.appendChild(symbol);
        }
        
        // Add some floating particles for extra glitter effect
        createGlitterParticles(mathBackground);
    }
    
    function createGlitterParticles(container) {
        const particleCount = 15;
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.style.position = 'absolute';
            particle.style.width = '4px';
            particle.style.height = '4px';
            particle.style.background = `hsl(${Math.random() * 360}, 70%, 60%)`;
            particle.style.borderRadius = '50%';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = Math.random() * 100 + '%';
            particle.style.zIndex = Math.floor(Math.random() * 10);
            particle.style.opacity = '0.6';
            particle.style.filter = 'blur(1px)';
            particle.style.animation = `glitterParticle ${8 + Math.random() * 12}s linear infinite`;
            particle.style.animationDelay = Math.random() * 10 + 's';
            
            container.appendChild(particle);
        }
    }

    // Initialize mathematical background
    createMathBackground();

    // Tab switching functionality
    function setMode(mode) {
        tabs.forEach(t => {
            const active = t.dataset.mode === mode;
            t.classList.toggle('active', active);
            t.setAttribute('aria-selected', String(active));
        });
        
        modes.forEach(el => {
            const active = el.dataset.mode === mode;
            el.classList.toggle('hidden', !active);
            
            // Enable/disable inputs based on mode
            if (el.dataset.mode === 'url') imageUrl.disabled = !active;
            if (el.dataset.mode === 'local') localPath.disabled = !active;
        });
        
        // Clear conflicting inputs
        if (mode !== 'upload') {
            fileInput.value = '';
            preview.classList.add('hidden');
        }
        if (mode !== 'url') imageUrl.value = '';
        if (mode !== 'local') localPath.value = '';
    }

    tabs.forEach(tab => tab.addEventListener('click', () => setMode(tab.dataset.mode)));

    // Dropzone interactions
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(name =>
        dropzone.addEventListener(name, preventDefaults, false)
    );
    
    ['dragenter', 'dragover'].forEach(name =>
        dropzone.addEventListener(name, () => dropzone.classList.add('dragover'))
    );
    
    ['dragleave', 'drop'].forEach(name =>
        dropzone.addEventListener(name, () => dropzone.classList.remove('dragover'))
    );
    
    dropzone.addEventListener('click', () => fileInput.click());
    
    dropzone.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            fileInput.click();
        }
    });
    
    dropzone.addEventListener('drop', e => {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files && files[0]) {
            fileInput.files = files;
            showPreview(files[0]);
            setMode('upload');
        }
        
        // Handle URL drops
        const text = dt.getData('text/plain');
        if (text && /^https?:\/\//i.test(text)) {
            imageUrl.value = text;
            setMode('url');
        }
    });

    // File input change handler
    fileInput.addEventListener('change', () => {
        const file = fileInput.files && fileInput.files[0];
        if (file) showPreview(file);
    });

    // Show image preview
    function showPreview(file) {
        const reader = new FileReader();
        reader.onload = e => {
            previewImg.src = e.target.result;
            preview.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }

    // Clear file button
    clearBtn.addEventListener('click', () => {
        fileInput.value = '';
        preview.classList.add('hidden');
    });

    // Form submission
    form.addEventListener('submit', () => {
        submitBtn.disabled = true;
        btnText.textContent = 'Generating...';
        
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.style.display = 'flex';
            overlay.classList.remove('hidden');
        }
        
        submitBtn.setAttribute('aria-busy', 'true');
    });

    // Default to upload mode
    setMode('upload');

    // Hide overlay on page load if result appears (server-rendered)
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.add('hidden');
        overlay.style.display = 'none';
    }

    // Show success state if description exists
    const hasDescription = !!document.getElementById('description-text');
    if (hasDescription) {
        submitBtn.disabled = false;
        btnText.textContent = 'Generated Successfully';
        submitBtn.setAttribute('aria-busy', 'false');
    } else {
        btnText.textContent = 'Generate Description';
    }

    // Ctrl+Enter shortcut
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            form.requestSubmit();
        }
    });

    // Paste support: paste image file or URL
    document.addEventListener('paste', e => {
        const items = e.clipboardData?.items || [];
        
        for (const item of items) {
            if (item.type && item.type.startsWith('image/')) {
                const file = item.getAsFile();
                if (file) {
                    fileInput.files = new DataTransfer().files; // reset
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

    // Typing reveal animation for description text
    const descEl = document.getElementById('description-text');
    if (descEl) {
        const full = descEl.textContent || '';
        let i = 0;
        descEl.textContent = '';
        
        const timer = setInterval(() => {
            descEl.textContent = full.slice(0, i += 2);
            if (i >= full.length) clearInterval(timer);
        }, 20);
    }

    // Add smooth hover effects
    submitBtn.addEventListener('mouseenter', () => {
        submitBtn.style.transform = 'translateY(-2px)';
    });
    
    submitBtn.addEventListener('mouseleave', () => {
        submitBtn.style.transform = 'translateY(0)';
    });

    // Enhanced accessibility
    dropzone.addEventListener('focus', () => {
        dropzone.style.borderColor = '#000000';
    });
    
    dropzone.addEventListener('blur', () => {
        if (!dropzone.classList.contains('dragover')) {
            dropzone.style.borderColor = '#d0d0d0';
        }
    });

    // Add some interactivity to math symbols on hover
    document.addEventListener('mouseover', (e) => {
        if (e.target.classList.contains('math-symbol')) {
            e.target.style.transform = 'scale(1.2) rotate(180deg)';
            e.target.style.filter = 'drop-shadow(0 0 20px currentColor) brightness(1.5)';
        }
    });

    document.addEventListener('mouseout', (e) => {
        if (e.target.classList.contains('math-symbol')) {
            e.target.style.transform = '';
            e.target.style.filter = 'drop-shadow(0 0 8px currentColor)';
        }
    });
});


