# -*- coding: utf-8 -*-
"""
Generate complete modern single-page web app histology_quiz_app.html
"""

html_template = '''<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Histology Master Quiz: 3 Interactive Modes</title>
    <style>
        :root {
            --primary: #1e40af;
            --primary-light: #3b82f6;
            --primary-bg: #eff6ff;
            --success: #15803d;
            --success-bg: #f0fdf4;
            --danger: #b91c1c;
            --danger-bg: #fef2f2;
            --warning: #b45309;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #cbd5e1;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg);
            color: var(--text-main);
            padding: 20px;
            line-height: 1.5;
        }
        .app-container {
            max-width: 1100px;
            margin: 0 auto;
        }
        header {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
            color: white;
            padding: 24px 28px;
            border-radius: 16px;
            margin-bottom: 20px;
            box-shadow: var(--shadow);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }
        header h1 { font-size: 22px; font-weight: 700; }
        header p { font-size: 14px; opacity: 0.9; margin-top: 4px; }
        .score-pill {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(8px);
            padding: 10px 18px;
            border-radius: 12px;
            display: flex;
            gap: 16px;
            font-weight: 600;
            font-size: 14px;
        }
        .mode-nav {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 20px;
        }
        .mode-btn {
            background: white;
            border: 2px solid var(--border);
            padding: 14px 18px;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            color: var(--text-main);
        }
        .mode-btn:hover {
            border-color: var(--primary-light);
            background: var(--primary-bg);
        }
        .mode-btn.active {
            background: var(--primary);
            border-color: var(--primary);
            color: white;
            box-shadow: 0 4px 12px rgba(30, 64, 175, 0.25);
        }
        .filter-bar {
            background: white;
            padding: 14px 20px;
            border-radius: 12px;
            border: 1px solid var(--border);
            margin-bottom: 20px;
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
        }
        .select-group {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }
        select, input[type="text"] {
            padding: 9px 14px;
            border-radius: 8px;
            border: 1px solid var(--border);
            font-size: 14px;
            background: white;
            color: var(--text-main);
            outline: none;
        }
        select:focus, input[type="text"]:focus {
            border-color: var(--primary-light);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
        }
        .main-card {
            background: white;
            border-radius: 16px;
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            margin-bottom: 24px;
        }
        .card-header-info {
            padding: 16px 24px;
            background: #f8fafc;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }
        .badge {
            display: inline-flex;
            align-items: center;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .badge-system { background: #dbeafe; color: #1e40af; }
        .badge-source { background: #fef3c7; color: #92400e; margin-left: 6px; }
        .badge-stain { background: #f3e8ff; color: #6b21a8; margin-left: 6px; }

        .viewer-container {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            min-height: 480px;
        }
        @media (max-width: 860px) {
            .viewer-container { grid-template-columns: 1fr; }
            .mode-nav { grid-template-columns: 1fr; }
        }
        .image-viewport {
            background: #0f172a;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
            padding: 12px;
            user-select: none;
        }
        .image-wrapper {
            position: relative;
            display: inline-block;
            max-width: 100%;
            max-height: 520px;
        }
        .slide-img {
            max-width: 100%;
            max-height: 500px;
            object-fit: contain;
            border-radius: 8px;
            display: block;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
            cursor: default;
        }
        .image-viewport.pointing-active .slide-img {
            cursor: crosshair;
        }
        .click-marker {
            position: absolute;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: 10;
        }
        .target-circle {
            position: absolute;
            border-radius: 50%;
            border: 3px solid #eab308;
            background: rgba(234, 179, 8, 0.25);
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: 9;
            animation: pulseCircle 1.6s infinite ease-in-out;
        }
        @keyframes pulseCircle {
            0% { transform: translate(-50%, -50%) scale(0.95); opacity: 0.8; }
            50% { transform: translate(-50%, -50%) scale(1.05); opacity: 0.4; }
            100% { transform: translate(-50%, -50%) scale(0.95); opacity: 0.8; }
        }
        .interaction-panel {
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background: #ffffff;
            border-left: 1px solid var(--border);
            overflow-y: auto;
            max-height: 600px;
        }
        .task-title {
            font-size: 17px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 14px;
        }
        .task-subtitle {
            font-size: 14px;
            color: var(--text-muted);
            margin-bottom: 18px;
        }

        /* Mode 1: Multiple choice */
        .options-grid {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 20px;
        }
        .option-btn {
            background: #f8fafc;
            border: 1.5px solid var(--border);
            padding: 13px 16px;
            border-radius: 10px;
            font-size: 14.5px;
            font-weight: 500;
            cursor: pointer;
            text-align: left;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .option-btn:hover:not(.disabled) {
            border-color: var(--primary-light);
            background: var(--primary-bg);
        }
        .option-btn.correct {
            border-color: var(--success) !important;
            background: var(--success-bg) !important;
            color: var(--success);
            font-weight: 700;
        }
        .option-btn.incorrect {
            border-color: var(--danger) !important;
            background: var(--danger-bg) !important;
            color: var(--danger);
        }
        .opt-char {
            width: 26px;
            height: 26px;
            border-radius: 50%;
            background: #e2e8f0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 13px;
            font-weight: 700;
            flex-shrink: 0;
        }

        /* Mode 2: Autocomplete */
        .autocomplete-wrapper {
            position: relative;
            margin-bottom: 16px;
        }
        .search-input {
            width: 100%;
            padding: 12px 16px;
            font-size: 15px;
            border-radius: 10px;
            border: 2px solid var(--border);
        }
        .autocomplete-list {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            max-height: 240px;
            overflow-y: auto;
            background: white;
            border: 1px solid var(--border);
            border-radius: 8px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            z-index: 50;
            margin-top: 4px;
            display: none;
        }
        .autocomplete-item {
            padding: 10px 14px;
            font-size: 14px;
            cursor: pointer;
            border-bottom: 1px solid #f1f5f9;
        }
        .autocomplete-item:hover {
            background: var(--primary-bg);
            color: var(--primary);
        }
        .submit-btn {
            background: var(--primary);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 10px;
            font-weight: 600;
            font-size: 15px;
            cursor: pointer;
            width: 100%;
            margin-bottom: 16px;
            transition: background 0.2s;
        }
        .submit-btn:hover { background: #1e3a8a; }

        /* Mode 3: Pointing instructions */
        .pointing-instructions {
            background: #f0fdf4;
            border: 1.5px solid #86efac;
            padding: 14px 18px;
            border-radius: 10px;
            margin-bottom: 18px;
            font-size: 14.5px;
        }
        .hint-btn {
            background: none;
            border: none;
            color: var(--primary);
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            text-decoration: underline;
            margin-top: 6px;
            display: inline-block;
        }

        /* Result & Explanation Box */
        .result-box {
            display: none;
            padding: 16px;
            border-radius: 12px;
            margin-top: 14px;
            animation: fadeIn 0.3s ease;
        }
        .result-box.correct {
            background: var(--success-bg);
            border: 1.5px solid #86efac;
        }
        .result-box.incorrect {
            background: var(--danger-bg);
            border: 1.5px solid #fca5a5;
        }
        .result-box h4 { font-size: 15px; margin-bottom: 6px; }
        .result-box p { font-size: 14px; line-height: 1.5; color: #334155; }
        .distractors-wrap {
            margin-top: 12px;
            padding-top: 10px;
            border-top: 1px dashed var(--border);
            font-size: 13px;
            color: #475569;
        }
        .distractors-wrap ul { padding-left: 18px; margin-top: 6px; }

        .nav-controls {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            margin-top: 20px;
            padding-top: 16px;
            border-top: 1px solid var(--border);
        }
        .btn-secondary {
            background: #f1f5f9;
            color: #334155;
            border: 1px solid var(--border);
            padding: 10px 18px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
        }
        .btn-secondary:hover { background: #e2e8f0; }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-4px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <header>
            <div>
                <h1>🔬 Histology Master Quiz</h1>
                <p>Навчальні та екзаменаційні мікропрепарати кафедр проф. О.М. Грабового та проф. С.І. Савосько</p>
            </div>
            <div class="score-pill">
                <div>Пройдено: <span id="statAnswered">0</span></div>
                <div>Правильно: <span id="statCorrect" style="color: #4ade80;">0</span></div>
                <div>Точність: <span id="statAccuracy">0%</span></div>
            </div>
        </header>

        <!-- 3 Modes Navigation -->
        <div class="mode-nav">
            <button class="mode-btn active" id="btnMode1" onclick="switchMode(1)">
                📋 1. Тест на вибір (Multiple Choice)
            </button>
            <button class="mode-btn" id="btnMode2" onclick="switchMode(2)">
                🔍 2. Пошук назви (Autocomplete)
            </button>
            <button class="mode-btn" id="btnMode3" onclick="switchMode(3)">
                🎯 3. Локалізація структури (Image Pointing)
            </button>
        </div>

        <!-- Filter bar -->
        <div class="filter-bar">
            <div class="select-group">
                <select id="selectSystem" onchange="applyFilters()">
                    <option value="all">Усі гістологічні системи (All Systems)</option>
                    <option value="digestive">Травна система та зуби</option>
                    <option value="nervous">Нервова система та аналізатори</option>
                    <option value="connective">Сполучні, хрящові та кісткові</option>
                    <option value="muscle">М'язові тканини</option>
                    <option value="hematology">Кров та органи кровотворення</option>
                    <option value="cardiovascular">Серцево-судинна система</option>
                    <option value="epithelium">Епітелії та шкіра</option>
                    <option value="urinary">Сечовидільна система</option>
                    <option value="endocrine">Ендокринна система</option>
                    <option value="reproductive">Статева система</option>
                </select>

                <select id="selectSource" onchange="applyFilters()">
                    <option value="all">Усі колекції (All Folders)</option>
                    <option value="grabovyi">Препарати О.М. Грабового</option>
                    <option value="savosko">Препарати С.І. Савосько</option>
                </select>
            </div>

            <div>
                <span style="font-size: 13px; color: var(--text-muted); font-weight: 500;">Препарат <span id="slideIndex">1</span> з <span id="totalSlides">0</span></span>
            </div>
        </div>

        <!-- Main Card -->
        <div class="main-card">
            <div class="card-header-info">
                <div>
                    <span class="badge badge-system" id="badgeSystem">Система</span>
                    <span class="badge badge-source" id="badgeSource">Викладач</span>
                    <span class="badge badge-stain" id="badgeStain">Забарвлення</span>
                </div>
                <div style="font-size: 12px; color: var(--text-muted);" id="slideFileName"></div>
            </div>

            <div class="viewer-container">
                <!-- Image Viewport -->
                <div class="image-viewport" id="viewport">
                    <div class="image-wrapper" id="imgWrapper">
                        <img id="currentImage" class="slide-img" src="" alt="Мікропрепарат" onclick="handleImageClick(event)">
                        <div id="clickMarker" class="click-marker" style="display: none;"></div>
                        <div id="targetCircle" class="target-circle" style="display: none;"></div>
                    </div>
                </div>

                <!-- Interaction Panel -->
                <div class="interaction-panel">
                    <div id="panelContent">
                        <!-- Dynamic mode content injected here -->
                    </div>

                    <!-- Result / Explanation Box -->
                    <div id="resultBox" class="result-box">
                        <h4 id="resultTitle">Результат</h4>
                        <p id="resultText"></p>
                        <div id="distractorSection" class="distractors-wrap" style="display: none;">
                            <b>Розбір альтернативних варіантів:</b>
                            <ul id="distractorList"></ul>
                        </div>
                    </div>

                    <!-- Bottom Nav -->
                    <div class="nav-controls">
                        <button class="btn-secondary" onclick="prevSlide()">◀ Попередній</button>
                        <button class="btn-secondary" onclick="shuffleSlide()">🎲 Випадковий</button>
                        <button class="btn-secondary" style="background: var(--primary); color: white; border: none;" onclick="nextSlide()">Наступний ▶</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Load Data -->
    <script src="slides_db.js"></script>
    <script>
        let currentMode = 1;
        let currentSlideIdx = 0;
        let filteredSlides = [];
        let score = { answered: 0, correct: 0 };
        let answeredSlides = {};

        function initApp() {
            filteredSlides = [...SLIDES_DB];
            document.getElementById('totalSlides').innerText = filteredSlides.length;
            loadSlide(0);
        }

        function switchMode(modeNum) {
            currentMode = modeNum;
            document.querySelectorAll('.mode-btn').forEach((btn, idx) => {
                btn.classList.toggle('active', idx + 1 === modeNum);
            });
            const viewport = document.getElementById('viewport');
            viewport.classList.toggle('pointing-active', modeNum === 3);
            clearMarkers();
            renderModeUI();
        }

        function applyFilters() {
            const sys = document.getElementById('selectSystem').value;
            const src = document.getElementById('selectSource').value;

            filteredSlides = SLIDES_DB.filter(s => {
                const matchSys = (sys === 'all' || s.system === sys);
                const matchSrc = (src === 'all' || s.source === src);
                return matchSys && matchSrc;
            });

            document.getElementById('totalSlides').innerText = filteredSlides.length;
            if (filteredSlides.length === 0) {
                alert('Не знайдено препаратів за обраними фільтрами.');
                return;
            }
            currentSlideIdx = 0;
            loadSlide(0);
        }

        function loadSlide(idx) {
            if (idx < 0 || idx >= filteredSlides.length) return;
            currentSlideIdx = idx;
            document.getElementById('slideIndex').innerText = idx + 1;

            const slide = filteredSlides[idx];
            document.getElementById('currentImage').src = encodeURI(slide.file);
            document.getElementById('badgeSystem').innerText = slide.system_ua;
            document.getElementById('badgeSource').innerText = slide.source_label;
            document.getElementById('badgeStain').innerText = slide.stain;
            document.getElementById('slideFileName').innerText = slide.file.split('/').pop();

            clearMarkers();
            document.getElementById('resultBox').style.display = 'none';

            renderModeUI();
        }

        function clearMarkers() {
            document.getElementById('clickMarker').style.display = 'none';
            document.getElementById('targetCircle').style.display = 'none';
        }

        function renderModeUI() {
            const container = document.getElementById('panelContent');
            const slide = filteredSlides[currentSlideIdx];
            if (!slide) return;

            if (currentMode === 1) {
                // Mode 1: Multiple choice
                let optionsHtml = '';
                slide.options.forEach((opt, oIdx) => {
                    const char = String.fromCharCode(65 + oIdx);
                    optionsHtml += `
                        <button class="option-btn" id="optBtn-${oIdx}" onclick="handleMCSelect(${oIdx})">
                            <span class="opt-char">${char}</span>
                            <span>${opt}</span>
                        </button>
                    `;
                });
                container.innerHTML = `
                    <div class="task-title">📋 Режим 1: Ідентифікація препарату / структури</div>
                    <div class="task-subtitle">${slide.mc_question}</div>
                    <div class="options-grid">${optionsHtml}</div>
                `;
            } else if (currentMode === 2) {
                // Mode 2: Autocomplete Text Search
                container.innerHTML = `
                    <div class="task-title">🔍 Режим 2: Введіть назву препарату</div>
                    <div class="task-subtitle">Почніть вводити назву тканини, органа чи патології українською або латиною:</div>
                    <div class="autocomplete-wrapper">
                        <input type="text" id="slideSearchInput" class="search-input" placeholder="Наприклад: Дно шлунку, Гіаліновий хрящ..." oninput="handleSearchInput(event)" autocomplete="off">
                        <div id="autocompleteList" class="autocomplete-list"></div>
                    </div>
                    <button class="submit-btn" onclick="submitSearchName()">Перевірити відповідь</button>
                    <div style="font-size: 13px; color: var(--text-muted);">
                        💡 <i>Підказка: Працює автодоповнення назв у списку за синонімами та українською / латинською термінологією.</i>
                    </div>
                `;
            } else if (currentMode === 3) {
                // Mode 3: Image Pointing
                container.innerHTML = `
                    <div class="task-title">🎯 Режим 3: Вказівка на структуру</div>
                    <div class="pointing-instructions">
                        <b>Завдання:</b> ${slide.pointing_task.prompt}<br>
                        <span style="font-size: 13px; color: #166534;">Клацніть курсором безпосередньо на мікропрепарат ліворуч у місці розташування цієї структури.</span>
                        <div>
                            <button class="hint-btn" onclick="toggleHint()">💡 Показати гістологічну підказку</button>
                            <div id="hintText" style="display: none; margin-top: 6px; font-size: 13px; color: #1e40af;">
                                ${slide.pointing_task.hint}
                            </div>
                        </div>
                    </div>
                `;
            }
        }

        // --- MODE 1 HANDLER ---
        function handleMCSelect(selectedIdx) {
            const slide = filteredSlides[currentSlideIdx];
            const isCorrect = (selectedIdx === slide.correct_idx);

            for (let i = 0; i < slide.options.length; i++) {
                const btn = document.getElementById(`optBtn-${i}`);
                if (btn) {
                    btn.classList.add('disabled');
                    if (i === slide.correct_idx) btn.classList.add('correct');
                    else if (i === selectedIdx && !isCorrect) btn.classList.add('incorrect');
                }
            }

            updateScore(isCorrect);
            showResult(isCorrect, isCorrect ? "Вірно! Відмінна ідентифікація." : "Невірно. Ознайомтеся з обґрунтуванням:", slide.explanation, slide.distractors_explanations);
        }

        // --- MODE 2 HANDLERS ---
        function handleSearchInput(e) {
            const val = e.target.value.trim().toLowerCase();
            const list = document.getElementById('autocompleteList');
            if (val.length < 1) { list.style.display = 'none'; return; }

            // Find all matching slide names from the entire database
            const matches = [];
            SLIDES_DB.forEach(s => {
                const namesToSearch = [s.name_ua, s.name_lat, ...(s.synonyms || [])];
                const isMatch = namesToSearch.some(n => n.toLowerCase().includes(val));
                if (isMatch && !matches.some(m => m.name === s.name_ua)) {
                    matches.push({ name: s.name_ua, id: s.id, sys: s.system_ua });
                }
            });

            if (matches.length === 0) { list.style.display = 'none'; return; }

            list.innerHTML = matches.slice(0, 7).map(m => `
                <div class="autocomplete-item" onclick="selectAutocomplete('${m.name.replace(/'/g, "\\'")}')">
                    <b>${m.name}</b> <span style="font-size: 11px; color: var(--text-muted);">(${m.sys})</span>
                </div>
            `).join('');
            list.style.display = 'block';
        }

        function selectAutocomplete(name) {
            const input = document.getElementById('slideSearchInput');
            if (input) input.value = name;
            document.getElementById('autocompleteList').style.display = 'none';
        }

        function submitSearchName() {
            const input = document.getElementById('slideSearchInput');
            if (!input) return;
            const userVal = input.value.trim().toLowerCase();
            const slide = filteredSlides[currentSlideIdx];

            const accepted = [slide.name_ua, slide.name_lat, ...(slide.synonyms || [])].map(s => s.toLowerCase());
            const isCorrect = accepted.some(acc => userVal.includes(acc) || acc.includes(userVal) && userVal.length > 3);

            updateScore(isCorrect);
            showResult(
                isCorrect,
                isCorrect ? `🎉 Абсолютно точно! Це: ${slide.name_ua}` : `Помилка. Правильна назва: ${slide.name_ua}`,
                `<b>Препарат:</b> ${slide.name_ua} (<i>${slide.name_lat}</i>).<br><b>Забарвлення:</b> ${slide.stain}.<br>${slide.explanation}`,
                slide.distractors_explanations
            );
        }

        // --- MODE 3 HANDLER ---
        function handleImageClick(e) {
            if (currentMode !== 3) return;
            const img = document.getElementById('currentImage');
            const rect = img.getBoundingClientRect();

            // Calculate percentage coordinates
            const clickX = ((e.clientX - rect.left) / rect.width) * 100;
            const clickY = ((e.clientY - rect.top) / rect.height) * 100;

            const slide = filteredSlides[currentSlideIdx];
            const pt = slide.pointing_task;

            // Distance calculation
            const dx = clickX - pt.target_x;
            const dy = clickY - pt.target_y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            const isCorrect = (dist <= pt.radius);

            // Display click marker
            const marker = document.getElementById('clickMarker');
            marker.style.left = `${clickX}%`;
            marker.style.top = `${clickY}%`;
            marker.style.background = isCorrect ? '#22c55e' : '#ef4444';
            marker.style.boxShadow = isCorrect ? '0 0 10px #22c55e' : '0 0 10px #ef4444';
            marker.style.display = 'block';

            // Reveal target circle
            const circle = document.getElementById('targetCircle');
            circle.style.left = `${pt.target_x}%`;
            circle.style.top = `${pt.target_y}%`;
            circle.style.width = `${pt.radius * 2 * (rect.width / 100)}px`;
            circle.style.height = `${pt.radius * 2 * (rect.height / 100)}px`;
            circle.style.borderColor = isCorrect ? '#22c55e' : '#eab308';
            circle.style.display = 'block';

            updateScore(isCorrect);
            showResult(
                isCorrect,
                isCorrect ? "🎯 Точне попадання! Структуру знайдено вірно." : "Майже! Зверніть увагу на підсвічену золотим колом ділянку:",
                `<b>${pt.prompt.replace('Клацніть на: ', '')}:</b> ${pt.structure_desc}`,
                null
            );
        }

        function toggleHint() {
            const h = document.getElementById('hintText');
            if (h) h.style.display = (h.style.display === 'none' ? 'block' : 'none');
        }

        function showResult(isCorrect, title, desc, distractors) {
            const box = document.getElementById('resultBox');
            box.className = `result-box ${isCorrect ? 'correct' : 'incorrect'}`;
            document.getElementById('resultTitle').innerHTML = title;
            document.getElementById('resultText').innerHTML = desc;

            const distSec = document.getElementById('distractorSection');
            const distList = document.getElementById('distractorList');
            if (distractors && distractors.length > 0) {
                distList.innerHTML = distractors.map(d => `<li>${d}</li>`).join('');
                distSec.style.display = 'block';
            } else {
                distSec.style.display = 'none';
            }
            box.style.display = 'block';
        }

        function updateScore(isCorrect) {
            score.answered++;
            if (isCorrect) score.correct++;
            document.getElementById('statAnswered').innerText = score.answered;
            document.getElementById('statCorrect').innerText = score.correct;
            const pct = Math.round((score.correct / score.answered) * 100);
            document.getElementById('statAccuracy').innerText = `${pct}%`;
        }

        function nextSlide() {
            const next = (currentSlideIdx + 1) % filteredSlides.length;
            loadSlide(next);
        }

        function prevSlide() {
            const prev = (currentSlideIdx - 1 + filteredSlides.length) % filteredSlides.length;
            loadSlide(prev);
        }

        function shuffleSlide() {
            const rand = Math.floor(Math.random() * filteredSlides.length);
            loadSlide(rand);
        }

        window.onload = initApp;
    </script>
</body>
</html>
'''

with open('histology_quiz_app.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print('histology_quiz_app.html created successfully!')
