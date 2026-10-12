import streamlit as st

st.set_page_config(
    page_title="Stick War 2: Order Empire - Complete Masterpiece Edition",
    page_icon="⚔️",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #06090f; color: #ffffff; font-family: 'Segoe UI', Tahoma, sans-serif; }
    iframe { border-radius: 12px; box-shadow: 0 12px 40px rgba(0,0,0,0.95); }
    .title-text { text-align: center; color: #ffcc00; text-transform: uppercase; font-weight: 800; margin-bottom: 0px; }
    .sub-text { text-align: center; color: #aaaaaa; font-size: 14px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-text'>⚔️ STICK WAR 2: ORDER EMPIRE - MASTER EDITION ⚔️</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Complete RTS Strategy Engine | 6 Gold Mines, Flash 2D Art Style, Mission Briefing & Balanced Combat</p>", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Stick War 2 Master Edition</title>
    <style>
        body { margin: 0; background: #06090f; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; overflow: hidden; }
        canvas { background: linear-gradient(to bottom, #5cb85c 0%, #4cae4c 70%, #398439 100%); border: 4px solid #2e6b2e; border-radius: 8px; box-shadow: 0 12px 35px rgba(0,0,0,0.95); display: block; margin: 4px auto; }
        .ui-panel { display: flex; justify-content: center; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
        .cmd-panel { display: flex; justify-content: center; gap: 8px; margin-top: 6px; }
        button { background: #8a641b; color: #fff; border: 2px solid #ffcc00; padding: 7px 12px; font-weight: bold; font-size: 11px; border-radius: 4px; cursor: pointer; transition: 0.2s; text-transform: uppercase; }
        button:hover { background: #b38324; transform: scale(1.05); }
        .cmd-btn { background: #1b4f72; border-color: #5dade2; }
        .skill-btn { background: #512e5f; border-color: #f39c12; }
        .stats { font-size: 13px; font-weight: bold; color: #ffcc00; margin-bottom: 4px; }
    </style>
</head>
<body>

    <div class="stats">
        🏰 TƯỢNG ORDER: <span id="hpText">2500</span> | 👹 TƯỢNG EMPIRE: <span id="enemyHpText">2500</span> | 💰 VÀNG: <span id="goldText">400</span> | 👥 DÂN SỐ: <span id="popText">0</span>/100
    </div>

    <canvas id="gameCanvas" width="980" height="400"></canvas>

    <div class="cmd-panel">
        <button class="cmd-btn" onclick="setCommand('ATTACK')">⚔️ TẤN CÔNG</button>
        <button class="cmd-btn" onclick="setCommand('DEFEND')">🛡️ PHÒNG THỦ</button>
        <button class="cmd-btn" onclick="setCommand('HOLD')">🛑 GIỮ VỊ TRÍ</button>
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

        let statueHp = 2500, enemyStatueHp = 2500;
        let gold = 400;
        let currentCommand = 'ATTACK';
        let gameOver = false;
        let showBriefing = true; // Bảng cuộn giấy cốt truyện ban đầu

        // 6 mỏ vàng nhỏ phân bổ ngay trước thành Order Empire
        let goldMines = [
            { x: 140, y: 150 }, { x: 190, y: 210 }, { x: 240, y: 280 },
            { x: 160, y: 330 }, { x: 210, y: 120 }, { x: 260, y: 180 }
        ];

        let units = [];
        let enemies = [];
        let floatingTexts = [];
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

        function triggerSkill(type) {
            if (showBriefing || gameOver) return;
            if (type === 'spin') {
                units.filter(u => u.type === 'swordwrath').forEach(u => {
                    u.isSpinning = 40;
                    addFloatingText("Bão Kiếm!", u.x, u.y - 25, '#5dade2');
                });
            } else if (type === 'earthquake') {
                enemies.forEach(e => {
                    e.hp -= 70;
                    addFloatingText("-70 Động Đất", e.x, e.y, '#e74c3c');
                });
            }
        }

        // Click để đóng cuộn giấy cốt truyện (Bấm nút OK)
        canvas.addEventListener('click', function(event) {
            if (showBriefing) {
                const rect = canvas.getBoundingClientRect();
                const mouseX = event.clientX - rect.left;
                const mouseY = event.clientY - rect.top;
                if (mouseX >= canvas.width/2 - 50 && mouseX <= canvas.width/2 + 50 && mouseY >= 270 && mouseY <= 310) {
                    showBriefing = false;
                }
            }
        });

        // Tự sinh quái địch theo đợt
        setInterval(() => {
            if (!showBriefing && !gameOver && enemyStatueHp > 0 && enemies.length < 25) {
                enemies.push({
                    x: canvas.width - 80, y: 150 + Math.random() * 200,
                    type: Math.random() > 0.5 ? 'orc' : 'goblin',
                    hp: 120, maxHp: 120, dmg: 15, range: 35, speed: 1.0, size: 1.1, attackCd: 0
                });
            }
        }, 3500);

        function spawnUnit(type) {
            if (showBriefing || gameOver) return;
            let costs = { miner: 30, swordwrath: 40, archidon: 50, spearton: 70, magikill: 100, giant: 160 };
            let pops = { miner: 1, swordwrath: 1, archidon: 1, spearton: 3, magikill: 5, giant: 4 };

            if (gold >= costs[type] && getCurrentPopulation() + pops[type] <= 100) {
                gold -= costs[type];
                units.push({
                    x: 80, y: 150 + Math.random() * 200,
                    type: type, hp: 150, maxHp: 150, dmg: 20, range: 40,
                    speed: 1.2, size: 1.0, attackCd: 0, goldBag: 0, state: 'going'
                });
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
            ctx.fillStyle = "#5cb85c"; ctx.fillRect(0, 100, canvas.width, 300);
            ctx.fillStyle = "#4cae4c"; ctx.fillRect(0, 100, canvas.width, 6);

            // Tượng Order (Trái)
            ctx.fillStyle = "#d4af37"; ctx.fillRect(15, 60, 45, 260);
            ctx.fillStyle = "#f1c40f"; ctx.beginPath(); ctx.arc(37, 55, 18, 0, Math.PI*2); ctx.fill();

            // 6 Mỏ vàng nhỏ
            goldMines.forEach((m, idx) => {
                ctx.fillStyle = "#f1c40f";
                ctx.beginPath(); ctx.arc(m.x, m.y, 14, 0, Math.PI*2); ctx.fill();
                ctx.strokeStyle = "#fff"; ctx.lineWidth = 1.5; ctx.stroke();
                ctx.fillStyle = "#000"; ctx.font = "bold 9px Arial";
                ctx.fillText("M" + (idx+1), m.x - 5, m.y + 3);
            });

            // Tượng Empire (Phải)
            ctx.fillStyle = "#78281f"; ctx.fillRect(canvas.width - 60, 60, 45, 260);
            ctx.fillStyle = "#922b21"; ctx.beginPath(); ctx.arc(canvas.width - 37, 55, 18, 0, Math.PI*2); ctx.fill();
        }

        function drawBriefingScroll() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = "#f4e8c1";
            ctx.fillRect(150, 60, canvas.width - 300, 280);

            ctx.fillStyle = "#8b5a2b";
            ctx.fillRect(135, 50, 25, 300);
            ctx.fillRect(canvas.width - 160, 50, 25, 300);

            ctx.strokeStyle = "#b59e67"; ctx.lineWidth = 3;
            ctx.strokeRect(150, 60, canvas.width - 300, 280);

            ctx.fillStyle = "#111"; ctx.font = "bold 26px 'Segoe UI'";
            ctx.textAlign = "center";
            ctx.fillText("Kiếm sĩ Phản công", canvas.width / 2, 115);

            ctx.font = "14px 'Segoe UI'";
            ctx.fillText("Trong nỗ lực giành lại đất đai, lượng Kiếm sĩ còn lại đang dồn toàn", canvas.width / 2, 160);
            ctx.fillText("lực còn lại để tấn công bạn!", canvas.width / 2, 185);

            ctx.fillStyle = "#c0392b"; ctx.font = "bold 15px 'Segoe UI'";
            ctx.fillText("Hãy vượt qua cuộc phản công của Kiếm sĩ", canvas.width / 2, 235);

            ctx.fillStyle = "#1b4f72";
            ctx.fillRect(canvas.width / 2 - 50, 275, 100, 36);
            ctx.strokeStyle = "#5dade2"; ctx.lineWidth = 2;
            ctx.strokeRect(canvas.width / 2 - 50, 275, 100, 36);

            ctx.fillStyle = "#fff"; ctx.font = "bold 16px 'Segoe UI'";
            ctx.fillText("OK", canvas.width / 2, 298);
            ctx.textAlign = "left";
        }

        function drawCharacter(entity, isEnemy) {
            ctx.save();
            ctx.translate(entity.x, entity.y);
            let color = isEnemy ? '#e74c3c' : '#3498db';
            if (entity.type === 'miner') color = '#f39c12';
            if (entity.type === 'spearton') color = '#2980b9';

            // Đầu đen tròn hoàn toàn chuẩn phong cách Flash Stick War
            ctx.fillStyle = "#000"; ctx.beginPath(); ctx.arc(0, -14, 6, 0, Math.PI*2); ctx.fill();
            if (entity.type === 'spearton') {
                ctx.fillStyle = "#c0392b"; ctx.fillRect(-7, -23, 14, 5); // Mũ lông đỏ
            }

            ctx.strokeStyle = color; ctx.lineWidth = 3.5;
            ctx.beginPath(); ctx.moveTo(0, -8); ctx.lineTo(0, 8); ctx.stroke();
            let swing = Math.sin(animFrame * 0.3) * 5;
            ctx.beginPath(); ctx.moveTo(0, 8); ctx.lineTo(-4, 18 + swing); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(0, 8); ctx.lineTo(4, 18 - swing); ctx.stroke();

            ctx.fillStyle = "#000"; ctx.fillRect(-12, -28, 24, 3);
            ctx.fillStyle = isEnemy ? "#e74c3c" : "#2ecc71";
            ctx.fillRect(-12, -28, (entity.hp / entity.maxHp) * 24, 3);
            ctx.restore();
        }

        function gameLoop() {
            if (statueHp <= 0 || enemyStatueHp <= 0) {
                gameOver = true;
                ctx.fillStyle = "rgba(0,0,0,0.88)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = statueHp > 0 ? "#2ecc71" : "#e74c3c";
                ctx.font = "bold 34px 'Segoe UI'";
                ctx.fillText(statueHp > 0 ? "🏆 ORDER EMPIRE CHIẾN THẮNG!" : "💀 TÒA THÀNH ĐÃ THẤT THỦ!", canvas.width / 2 - 220, canvas.height / 2);
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
                    if (u.state === 'going') {
                        u.x += 1.5;
                        if (u.x >= 200) u.state = 'returning';
                    } else {
                        u.x -= 1.5;
                        if (u.x <= 70) {
                            gold += 12;
                            u.state = 'going';
                            updateUI();
                        }
                    }
                } else {
                    let nearestEnemy = enemies.find(e => Math.abs(e.x - u.x) <= u.range);
                    if (nearestEnemy) {
                        if (u.attackCd > 0) u.attackCd--;
                        else {
                            nearestEnemy.hp -= u.dmg;
                            addFloatingText("-" + u.dmg, nearestEnemy.x, nearestEnemy.y - 15, '#e74c3c');
                            u.attackCd = 30;
                        }
                    } else {
                        let targetX = currentCommand === 'ATTACK' ? canvas.width - 70 : 250;
                        if (u.x < targetX) {
                            u.x += u.speed;
                        } else if (currentCommand === 'ATTACK' && u.x >= canvas.width - 80) {
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
                let nearestUnit = units.find(u => u.type !== 'miner' && Math.abs(u.x - e.x) <= e.range);
                if (nearestUnit) {
                    if (e.attackCd > 0) e.attackCd--;
                    else {
                        nearestUnit.hp -= e.dmg;
                        addFloatingText("-" + e.dmg, nearestUnit.x, nearestUnit.y - 15, '#e74c3c');
                        e.attackCd = 35;
                    }
                } else {
                    e.x -= e.speed;
                    if (e.x <= 70) {
                        if (e.attackCd > 0) e.attackCd--;
                        else {
                            statueHp -= e.dmg;
                            addFloatingText("-" + e.dmg, 50, 180, '#e74c3c');
                            e.attackCd = 40;
                            updateUI();
                        }
                    }
                }
                drawCharacter(e, true);
                if (e.hp <= 0) enemies.splice(idx, 1);
            });

            floatingTexts.forEach((ft, idx) => {
                ft.y -= 0.6; ft.alpha -= 0.02;
                ctx.fillStyle = ft.color;
                ctx.globalAlpha = Math.max(0, ft.alpha);
                ctx.font = "bold 11px 'Segoe UI'";
                ctx.fillText(ft.text, ft.x, ft.y);
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

st.components.v1.html(game_html, height=530, scrolling=False)
