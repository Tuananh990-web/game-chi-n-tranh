import streamlit as st

st.set_page_config(
    page_title="Stick War 2: Order Empire - Advanced RTS Engine",
    page_icon="⚔️",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #030508; color: #ffffff; font-family: 'Segoe UI', Tahoma, sans-serif; }
    iframe { border-radius: 12px; box-shadow: 0 15px 45px rgba(0,0,0,0.95); }
    .title-text { text-align: center; color: #ffcc00; text-transform: uppercase; font-weight: 800; margin-bottom: 0px; }
    .sub-text { text-align: center; color: #aaaaaa; font-size: 14px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-text'>⚔️ STICK WAR 2: ORDER EMPIRE - ADVANCED RTS ⚔️</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Full-featured RTS Engine: Tech Tree, Advanced Pathfinding, AI Skirmish & Flash 2D Art System</p>", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Stick War 2 Advanced RTS</title>
    <style>
        body { margin: 0; background: #030508; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; overflow: hidden; }
        canvas { background: linear-gradient(to bottom, #4ca64c 0%, #388e3c 70%, #2e7d32 100%); border: 4px solid #3e2723; border-radius: 10px; box-shadow: 0 15px 40px rgba(0,0,0,0.95); display: block; margin: 4px auto; }
        .ui-panel { display: flex; justify-content: center; flex-wrap: wrap; gap: 5px; margin-top: 4px; }
        .cmd-panel { display: flex; justify-content: center; gap: 6px; margin-top: 4px; }
        button { background: #795548; color: #fff; border: 2px solid #ffcc00; padding: 6px 11px; font-weight: bold; font-size: 11px; border-radius: 4px; cursor: pointer; transition: 0.2s; text-transform: uppercase; }
        button:hover { background: #8d6e63; transform: scale(1.05); }
        .cmd-btn { background: #01579b; border-color: #4fc3f7; }
        .skill-btn { background: #4a148c; border-color: #ffb74d; }
        .tech-btn { background: #1b5e20; border-color: #81c784; }
        .stats { font-size: 13px; font-weight: bold; color: #ffcc00; margin-bottom: 3px; }
    </style>
</head>
<body>

    <div class="stats">
        🏰 ORDER HP: <span id="hpText">3000</span> | 👹 EMPIRE HP: <span id="enemyHpText">3000</span> | 💰 GOLD: <span id="goldText">450</span> | 👥 POP: <span id="popText">0</span>/100 | 💎 TECH LVL: <span id="techText">1</span>
    </div>

    <canvas id="gameCanvas" width="980" height="400"></canvas>

    <div class="cmd-panel">
        <button class="cmd-btn" onclick="setCommand('ATTACK')">⚔️ TẤN CÔNG</button>
        <button class="cmd-btn" onclick="setCommand('DEFEND')">🛡️ PHÒNG THỦ</button>
        <button class="cmd-btn" onclick="setCommand('HOLD')">🛑 GIỮ VỊ TRÍ</button>
        <button class="tech-btn" onclick="upgradeTech()">⬆️ NÂNG CẤP CÔNG NGHỆ (150G)</button>
        <button class="skill-btn" onclick="triggerSkill('spin')">🌀 BÃO KIẾM</button>
        <button class="skill-btn" onclick="triggerSkill('earthquake')">💥 ĐỘNG ĐẤT</button>
    </div>

    <div class="ui-panel">
        <button onclick="spawnUnit('miner')">⛏️ Miner (30g)</button>
        <button onclick="spawnUnit('swordwrath')">⚔️ Swordwrath (40g)</button>
        <button onclick="spawnUnit('archidon')">🏹 Archidon (50g)</button>
        <button onclick="spawnUnit('spearton')">🛡️ Spearton (70g)</button>
        <button onclick="spawnUnit('magikill')">🧙 Magikill (100g)</button>
        <button onclick="spawnUnit('giant')">🗿 Giant (160g)</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let statueHp = 3000, enemyStatueHp = 3000;
        let gold = 450;
        let techLevel = 1;
        let currentCommand = 'ATTACK';
        let gameOver = false;
        let showBriefing = true;

        // 6 Mỏ vàng nhỏ chiến thuật ngay trước thành Order
        let goldMines = [
            { x: 150, y: 140, miner: null }, { x: 200, y: 200, miner: null }, { x: 250, y: 270, miner: null },
            { x: 170, y: 320, miner: null }, { x: 220, y: 120, miner: null }, { x: 270, y: 180, miner: null }
        ];

        let units = [];
        let enemies = [];
        let floatingTexts = [];
        let projectiles = [];
        let animFrame = 0;

        function setCommand(cmd) { currentCommand = cmd; }

        function getCurrentPopulation() {
            let count = 0;
            units.forEach(u => {
                if (u.type === 'spearton') count += 3;
                else if (u.type === 'magikill') count += 5;
                else if (u.type === 'giant') count += 4;
                else count += 1;
            });
            return count;
        }

        function addFloatingText(text, x, y, color = '#ffcc00') {
            floatingTexts.push({ text, x, y, alpha: 1.0, color });
        }

        function upgradeTech() {
            if (showBriefing || gameOver) return;
            if (gold >= 150 && techLevel < 3) {
                gold -= 150;
                techLevel++;
                document.getElementById("techText").innerText = techLevel;
                units.forEach(u => { u.dmg = Math.floor(u.dmg * 1.25); u.maxHp = Math.floor(u.maxHp * 1.2); u.hp = u.maxHp; });
                addFloatingText("⬆️ CÔNG NGHỆ ĐÃ ĐƯỢC NÂNG CẤP!", canvas.width / 2, 100, '#81c784');
                updateUI();
            }
        }

        function triggerSkill(type) {
            if (showBriefing || gameOver) return;
            if (type === 'spin') {
                units.filter(u => u.type === 'swordwrath').forEach(u => {
                    u.isSpinning = 45;
                    addFloatingText("Bão Kiếm!", u.x, u.y - 25, '#4fc3f7');
                });
            } else if (type === 'earthquake') {
                enemies.forEach(e => {
                    e.hp -= (80 * techLevel);
                    addFloatingText("-" + (80 * techLevel) + " Động Đất", e.x, e.y, '#e53935');
                });
            }
        }

        canvas.addEventListener('click', function(event) {
            if (showBriefing) {
                const rect = canvas.getBoundingClientRect();
                const mouseX = event.clientX - rect.left;
                const mouseY = event.clientY - rect.top;
                if (mouseX >= canvas.width/2 - 55 && mouseX <= canvas.width/2 + 55 && mouseY >= 270 && mouseY <= 315) {
                    showBriefing = false;
                }
            }
        });

        // AI thông minh điều phối quân địch
        setInterval(() => {
            if (!showBriefing && !gameOver && enemyStatueHp > 0 && enemies.length < 30) {
                let types = ['goblin', 'orc', 'shadow_mage', 'troll'];
                let t = types[Math.floor(Math.random() * types.length)];
                let stats = {
                    goblin: { hp: 110, dmg: 14, range: 30, speed: 1.4, size: 0.95 },
                    orc: { hp: 230, dmg: 26, range: 35, speed: 1.0, size: 1.2 },
                    shadow_mage: { hp: 160, dmg: 38, range: 150, speed: 0.8, size: 1.05 },
                    troll: { hp: 650, dmg: 60, range: 50, speed: 0.5, size: 1.85 }
                }[t];

                enemies.push({
                    x: canvas.width - 80, y: 140 + Math.random() * 200,
                    type: t, hp: stats.hp, maxHp: stats.hp, dmg: stats.dmg,
                    range: stats.range, speed: stats.speed, size: stats.size, attackCd: 0
                });
            }
        }, 3200);

        function spawnUnit(type) {
            if (showBriefing || gameOver) return;
            let costs = { miner: 30, swordwrath: 40, archidon: 50, spearton: 70, magikill: 100, giant: 160 };
            let pops = { miner: 1, swordwrath: 1, archidon: 1, spearton: 3, magikill: 5, giant: 4 };
            let stats = {
                miner:      { hp: 100, dmg: 8,  range: 30, speed: 1.5, size: 0.95 },
                swordwrath: { hp: 170, dmg: 22, range: 35, speed: 1.35, size: 1.0 },
                archidon:   { hp: 120, dmg: 28, range: 190, speed: 1.15, size: 1.0 },
                spearton:   { hp: 260, dmg: 34, range: 60, speed: 0.95, size: 1.2 },
                magikill:   { hp: 130, dmg: 45, range: 170, speed: 0.85, size: 1.05 },
                giant:      { hp: 800, dmg: 75, range: 55, speed: 0.55, size: 1.95 }
            }[type];

            if (gold >= costs[type] && getCurrentPopulation() + pops[type] <= 100) {
                gold -= costs[type];
                let unit = {
                    x: 80, y: 140 + Math.random() * 200,
                    type: type, hp: stats.hp * techLevel, maxHp: stats.hp * techLevel,
                    dmg: stats.dmg * techLevel, range: stats.range, speed: stats.speed,
                    size: stats.size, attackCd: 0, goldBag: 0, state: 'going', mineTarget: null
                };

                if (type === 'miner') {
                    let freeMine = goldMines.find(m => !m.miner);
                    if (freeMine) { freeMine.miner = unit; unit.mineTarget = freeMine; }
                    else { unit.mineTarget = goldMines[0]; }
                }
                units.push(unit);
                updateUI();
            }
        }

        function updateUI() {
            document.getElementById("hpText").innerText = Math.max(0, Math.floor(statueHp));
            document.getElementById("enemyHpText").innerText = Math.max(0, Math.floor(enemyStatueHp));
            document.getElementById("goldText").innerText = gold;
            document.getElementById("popText").innerText = getCurrentPopulation();
        }

        function drawScene() {
            ctx.fillStyle = "#388e3c"; ctx.fillRect(0, 100, canvas.width, 300);
            ctx.fillStyle = "#2e7d32"; ctx.fillRect(0, 100, canvas.width, 6);

            // Tượng Order (Trái)
            ctx.fillStyle = "#ffb300"; ctx.fillRect(15, 60, 45, 260);
            ctx.fillStyle = "#ffe082"; ctx.beginPath(); ctx.arc(37, 55, 18, 0, Math.PI*2); ctx.fill();

            // 6 Mỏ vàng nhỏ
            goldMines.forEach((m, idx) => {
                ctx.fillStyle = "#ffb300";
                ctx.beginPath(); ctx.arc(m.x, m.y, 14, 0, Math.PI*2); ctx.fill();
                ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 1.5; ctx.stroke();
                ctx.fillStyle = "#000"; ctx.font = "bold 9px 'Segoe UI'";
                ctx.fillText("M" + (idx+1), m.x - 5, m.y + 3);
            });

            // Tượng Empire (Phải)
            ctx.fillStyle = "#b71c1c"; ctx.fillRect(canvas.width - 60, 60, 45, 260);
            ctx.fillStyle = "#e53935"; ctx.beginPath(); ctx.arc(canvas.width - 37, 55, 18, 0, Math.PI*2); ctx.fill();
        }

        function drawBriefingScroll() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.85)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#f5f5dc"; ctx.fillRect(140, 50, canvas.width - 280, 300);
            ctx.fillStyle = "#5d4037"; ctx.fillRect(125, 40, 25, 320); ctx.fillRect(canvas.width - 150, 40, 25, 320);
            ctx.strokeStyle = "#d7ccc8"; ctx.lineWidth = 3; ctx.strokeRect(140, 50, canvas.width - 280, 300);

            ctx.fillStyle = "#111"; ctx.font = "bold 26px 'Segoe UI'"; ctx.textAlign = "center";
            ctx.fillText("Chiến Dịch Order Empire", canvas.width / 2, 100);
            ctx.font = "14px 'Segoe UI'";
            ctx.fillText("Thế lực Hắc Ám Empire đang dồn toàn lực tấn công căn cứ của bạn.", canvas.width / 2, 145);
            ctx.fillText("Hãy khai thác vàng, nâng cấp công nghệ và bảo vệ tượng chính!", canvas.width / 2, 170);
            ctx.fillStyle = "#b71c1c"; ctx.font = "bold 15px 'Segoe UI'";
            ctx.fillText("Bảo vệ vương quốc và tiêu diệt Cổng Quỷ!", canvas.width / 2, 220);

            ctx.fillStyle = "#01579b"; ctx.fillRect(canvas.width / 2 - 55, 270, 110, 40);
            ctx.strokeStyle = "#4fc3f7"; ctx.lineWidth = 2; ctx.strokeRect(canvas.width / 2 - 55, 270, 110, 40);
            ctx.fillStyle = "#fff"; ctx.font = "bold 16px 'Segoe UI'";
            ctx.fillText("BẮT ĐẦU", canvas.width / 2, 296);
            ctx.textAlign = "left";
        }

        function drawCharacter(entity, isEnemy) {
            ctx.save();
            ctx.translate(entity.x, entity.y);
            let color = isEnemy ? '#e53935' : '#0288d1';
            if (entity.type === 'miner') color = '#fb8c00';
            if (entity.type === 'spearton') color = '#1565c0';
            if (entity.type === 'giant') color = '#6d4c41';

            // Đầu đen hoàn toàn phẳng không có mặt chuẩn Stick War
            ctx.fillStyle = "#000"; ctx.beginPath(); ctx.arc(0, -14 * entity.size, 6 * entity.size, 0, Math.PI*2); ctx.fill();
            if (entity.type === 'spearton') {
                ctx.fillStyle = "#b71c1c"; ctx.fillRect(-7*entity.size, -23*entity.size, 14*entity.size, 5*entity.size);
            }

            ctx.strokeStyle = color; ctx.lineWidth = 3.5 * entity.size;
            ctx.beginPath(); ctx.moveTo(0, -8 * entity.size); ctx.lineTo(0, 8 * entity.size); ctx.stroke();
            let swing = Math.sin(animFrame * 0.3) * 5;
            ctx.beginPath(); ctx.moveTo(0, 8 * entity.size); ctx.lineTo(-5 * entity.size, 18 * entity.size + swing); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(0, 8 * entity.size); ctx.lineTo(5 * entity.size, 18 * entity.size - swing); ctx.stroke();

            ctx.fillStyle = "#000"; ctx.fillRect(-12 * entity.size, -28 * entity.size, 24 * entity.size, 3.5);
            ctx.fillStyle = isEnemy ? "#e53935" : "#4caf50";
            ctx.fillRect(-12 * entity.size, -28 * entity.size, (entity.hp / entity.maxHp) * 24 * entity.size, 3.5);
            ctx.restore();
        }

        function gameLoop() {
            if (statueHp <= 0 || enemyStatueHp <= 0) {
                gameOver = true;
                ctx.fillStyle = "rgba(0,0,0,0.9)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = statueHp > 0 ? "#4caf50" : "#e53935";
                ctx.font = "bold 36px 'Segoe UI'"; ctx.textAlign = "center";
                ctx.fillText(statueHp > 0 ? "🏆 ORDER EMPIRE CHIẾN THẮNG!" : "💀 TÒA THÀNH ĐÃ THẤT THỦ!", canvas.width / 2, canvas.height / 2);
                return;
            }

            animFrame++;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawScene();

            if (showBriefing) {
                drawBriefingScroll();
                requestAnimationFrame(gameLoop);
                return;
            }

            // Xử lý thợ mỏ tại 6 mỏ vàng nhỏ
            units.forEach((u, idx) => {
                if (u.type === 'miner') {
                    if (u.mineTarget) {
                        if (u.state === 'going') {
                            let dx = u.mineTarget.x - u.x; let dy = u.mineTarget.y - u.y;
                            let dist = Math.hypot(dx, dy);
                            if (dist > 3) { u.x += (dx / dist) * u.speed; u.y += (dy / dist) * u.speed; }
                            else { u.state = 'mining'; }
                        } else if (u.state === 'mining') {
                            u.goldBag = 15 * techLevel; u.state = 'returning';
                        } else if (u.state === 'returning') {
                            let dx = 70 - u.x; let dy = 200 - u.y;
                            let dist = Math.hypot(dx, dy);
                            if (dist > 3) { u.x += (dx / dist) * u.speed; u.y += (dy / dist) * u.speed; }
                            else {
                                gold += u.goldBag || 15; u.goldBag = 0; u.state = 'going';
                                addFloatingText("+" + (15 * techLevel) + " Gold", 70, 200, '#ffcc00');
                                updateUI();
                            }
                        }
                    }
                } else {
                    let nearestEnemy = enemies.find(e => Math.hypot(e.x - u.x, e.y - u.y) <= u.range);
                    if (nearestEnemy) {
                        if (u.attackCd > 0) u.attackCd--;
                        else {
                            nearestEnemy.hp -= u.dmg;
                            addFloatingText("-" + u.dmg, nearestEnemy.x, nearestEnemy.y - 15, '#e53935');
                            u.attackCd = 28;
                        }
                    } else {
                        let targetX = currentCommand === 'ATTACK' ? canvas.width - 70 : 280;
                        if (u.x < targetX) { u.x += u.speed; }
                        else if (currentCommand === 'ATTACK' && u.x >= canvas.width - 80) {
                            if (u.attackCd > 0) u.attackCd--;
                            else {
                                enemyStatueHp -= u.dmg;
                                addFloatingText("-" + u.dmg, canvas.width - 60, 180, '#ffcc00');
                                u.attackCd = 35;
                                updateUI();
                            }
                        }
                    }
                }
                drawCharacter(u, false);
                if (u.hp <= 0) units.splice(idx, 1);
            });

            // Xử lý quái vật
            enemies.forEach((e, idx) => {
                let nearestUnit = units.find(u => u.type !== 'miner' && Math.hypot(u.x - e.x, u.y - e.y) <= e.range);
                if (nearestUnit) {
                    if (e.attackCd > 0) e.attackCd--;
                    else {
                        nearestUnit.hp -= e.dmg;
                        addFloatingText("-" + e.dmg, nearestUnit.x, nearestUnit.y - 15, '#ffcc00');
                        e.attackCd = 32;
                    }
                } else {
                    e.x -= e.speed;
                    if (e.x <= 70) {
                        if (e.attackCd > 0) e.attackCd--;
                        else {
                            statueHp -= e.dmg;
                            addFloatingText("-" + e.dmg, 50, 180, '#e53935');
                            e.attackCd = 38;
                            updateUI();
                        }
                    }
                }
                drawCharacter(e, true);
                if (e.hp <= 0) { enemies.splice(idx, 1); gold += 35; updateUI(); }
            });

            floatingTexts.forEach((ft, idx) => {
                ft.y -= 0.6; ft.alpha -= 0.02;
                ctx.fillStyle = ft.color; ctx.globalAlpha = Math.max(0, ft.alpha);
                ctx.font = "bold 12px 'Segoe UI'"; ctx.fillText(ft.text, ft.x, ft.y);
                ctx.globalAlpha = 1.0;
                if (ft.alpha <= 0) floatingTexts.splice(idx, 1);
            });

            requestAnimationFrame(gameLoop);
        }

        gameLoop();
    </script>
</body>
</html>
"""

st.components.v1.html(game_html, height=540, scrolling=False)
