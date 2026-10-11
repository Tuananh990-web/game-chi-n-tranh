import streamlit as st

st.set_page_config(page_title="Stick War 2: Order Empire Deluxe", page_icon="⚔️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: white; }
    iframe { border-radius: 14px; box-shadow: 0 10px 40px rgba(0,0,0,0.95); }
    </style>
""", unsafe_allow_html=True)

st.title("⚔️ Stick War 2: Order Empire - Deluxe Edition")
st.markdown("Chỉ huy quân đoàn Order Empire, khai thác vàng, nâng cấp binh chủng chiến đấu hoành tráng chống lại thế lực hắc ám!")

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Stick War 2 Deluxe</title>
    <style>
        body { margin: 0; background: #060913; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; overflow: hidden; }
        canvas { background: linear-gradient(to bottom, #14281a, #1f3b25); border: 4px solid #4a3b2c; border-radius: 10px; box-shadow: 0 12px 35px rgba(0,0,0,0.9); cursor: crosshair; display: block; margin: 6px auto; }
        .ui-panel { display: flex; justify-content: center; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
        .cmd-panel { display: flex; justify-content: center; gap: 8px; margin-top: 6px; }
        button { background: #8c672e; color: #fff; border: 2px solid #ffd700; padding: 7px 13px; font-weight: bold; font-size: 11px; border-radius: 6px; cursor: pointer; transition: 0.2s; }
        button:hover { background: #b0853b; transform: scale(1.05); }
        .cmd-btn { background: #1b4f72; border-color: #5dade2; }
        .skill-btn { background: #7d3c98; border-color: #f39c12; }
        .stats { font-size: 13px; font-weight: bold; color: #ffd700; margin-bottom: 3px; }
    </style>
</head>
<body>

    <div class="stats">
        🏰 Tượng Chính: <span id="hpText">2500</span> | 👹 Tượng Địch: <span id="enemyHpText">2500</span> | 💰 Vàng: <span id="goldText">400</span> | 👥 Dân số: <span id="popText">0</span>/100 | ⚔️ Lệnh: <span id="cmdText" style="color:#2ecc71;">TẤN CÔNG</span>
    </div>

    <canvas id="gameCanvas" width="980" height="420"></canvas>

    <div class="cmd-panel">
        <button class="cmd-btn" onclick="setCommand('ATTACK')">⚔️ TẤN CÔNG</button>
        <button class="cmd-btn" onclick="setCommand('DEFEND')">🛡️ PHÒNG THỦ</button>
        <button class="cmd-btn" onclick="setCommand('HOLD')">🛑 GIỮ VỊ TRÍ</button>
        <button class="skill-btn" onclick="triggerSkill('spin')">🌀 BÃO KIẾM</button>
        <button class="skill-btn" onclick="triggerSkill('arrowRain')">🏹 MƯA TÊN</button>
        <button class="skill-btn" onclick="triggerSkill('earthquake')">💥 ĐỘNG ĐẤT</button>
        <button onclick="toggleAudio()">🔊 Âm Thanh</button>
    </div>

    <div class="ui-panel">
        <button onclick="spawnUnit('miner')">⛏️ Thợ Mỏ (30g - 1 Pop)</button>
        <button onclick="spawnUnit('swordwrath')">⚔️ Kiếm Sĩ (40g - 1 Pop)</button>
        <button onclick="spawnUnit('archidon')">🏹 Cung Thủ (50g - 1 Pop)</button>
        <button onclick="spawnUnit('spearton')">🛡️ Giáo Binh (70g - 3 Pop)</button>
        <button onclick="spawnUnit('magikill')">🧙 Pháp Sư (100g - 5 Pop)</button>
        <button onclick="spawnUnit('giant')">🗿 Khổng Lồ (160g - 4 Pop)</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let statueHp = 2500, statueMaxHp = 2500;
        let enemyStatueHp = 2500, enemyStatueMaxHp = 2500;
        let gold = 400;
        let currentCommand = 'ATTACK';

        let units = [];
        let enemies = [];
        let projectiles = [];
        let floatingTexts = [];
        let particles = [];
        let animFrame = 0;
        let audioEnabled = false, audioCtx = null;

        function toggleAudio() {
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            audioEnabled = !audioEnabled;
        }

        function playSound(freq, type, duration) {
            if (!audioEnabled || !audioCtx) return;
            try {
                let osc = audioCtx.createOscillator();
                let gain = audioCtx.createGain();
                osc.type = type; osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                gain.gain.setValueAtTime(0.04, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.start(); osc.stop(audioCtx.currentTime + duration);
            } catch(e) {}
        }

        function setCommand(cmd) {
            currentCommand = cmd;
            let txt = cmd === 'ATTACK' ? 'TẤN CÔNG' : (cmd === 'DEFEND' ? 'PHÒNG THỦ' : 'GIỮ VỊ TRÍ');
            document.getElementById("cmdText").innerText = txt;
        }

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

        function addFloatingText(text, x, y, color = '#ffd700') {
            floatingTexts.push({ text, x, y, alpha: 1.0, color });
        }

        function triggerSkill(type) {
            if (type === 'spin') {
                units.filter(u => u.type === 'swordwrath').forEach(u => {
                    u.isSpinning = 50;
                    addFloatingText("Bão Kiếm!", u.x, u.y - 30, '#3498db');
                });
                playSound(450, 'sawtooth', 0.4);
            } else if (type === 'arrowRain') {
                for(let i=0; i<18; i++) {
                    projectiles.push({
                        x: 450 + Math.random()*300, y: 0,
                        targetY: 200 + Math.random()*160,
                        vx: 0, vy: 14, type: 'arrow', damage: 25
                    });
                }
                addFloatingText("Mưa Tên Hủy Diệt!", 600, 80, '#f1c40f');
                playSound(750, 'sine', 0.3);
            } else if (type === 'earthquake') {
                units.filter(u => u.type === 'giant').forEach(u => {
                    enemies.forEach(e => {
                        if (Math.hypot(e.x - u.x, e.y - u.y) < 200) {
                            e.stunned = 100;
                            e.hp -= 50;
                            addFloatingText("-50 Động Đất", e.x, e.y - 20, '#e74c3c');
                        }
                    });
                });
                playSound(100, 'sawtooth', 0.6);
            }
        }

        // Tự sinh kẻ địch
        setInterval(() => {
            if (enemyStatueHp > 0 && enemies.length < 45) {
                let types = ['goblin', 'orc', 'shadow_mage', 'troll'];
                let t = types[Math.floor(Math.random() * types.length)];
                enemies.push(createEnemyObject(t));
            }
        }, 1600);

        // Khai thác vàng định kỳ
        setInterval(() => {
            units.forEach(u => {
                if (u.type === 'miner') {
                    if (u.state === 'going') {
                        u.x += u.speed;
                        if (u.x >= 480) u.state = 'mining';
                    } else if (u.state === 'returning') {
                        u.x -= u.speed;
                        if (u.x <= 140) {
                            gold += u.goldBag || 15;
                            u.goldBag = 0;
                            u.state = 'going';
                            addFloatingText("+15 Vàng", 140, 200, '#ffd700');
                        }
                    } else if (u.state === 'mining') {
                        u.goldBag = 15;
                        u.state = 'returning';
                    }
                }
            });
            gold += 10;
            updateUI();
        }, 1000);

        function updateUI() {
            document.getElementById("hpText").innerText = Math.max(0, Math.floor(statueHp));
            document.getElementById("enemyHpText").innerText = Math.max(0, Math.floor(enemyStatueHp));
            document.getElementById("goldText").innerText = gold;
            document.getElementById("popText").innerText = getCurrentPopulation();
        }

        function createUnitObject(type) {
            let stats = {
                miner:      { hp: 90,  dmg: 8,  range: 30, speed: 1.5, size: 0.9 },
                swordwrath: { hp: 150, dmg: 20, range: 35, speed: 1.3, size: 1 },
                archidon:   { hp: 100, dmg: 25, range: 190, speed: 1.1, size: 1 },
                spearton:   { hp: 220, dmg: 30, range: 60, speed: 0.9, size: 1.2 },
                magikill:   { hp: 110, dmg: 40, range: 170, speed: 0.8, size: 1 },
                giant:      { hp: 700, dmg: 65, range: 55, speed: 0.5, size: 1.9 }
            }[type];

            return {
                x: 140 + Math.random() * 20, y: 150 + Math.random() * 200,
                type: type, hp: stats.hp, maxHp: stats.hp,
                dmg: stats.dmg, range: stats.range, speed: stats.speed, size: stats.size,
                attackCd: 0, state: 'going', goldBag: 0, isSpinning: 0
            };
        }

        function createEnemyObject(type) {
            let stats = {
                goblin:      { hp: 95,  dmg: 12, range: 30, speed: 1.4, size: 0.9 },
                orc:         { hp: 190, dmg: 22, range: 35, speed: 1.0, size: 1.2 },
                shadow_mage: { hp: 130, dmg: 32, range: 150, speed: 0.8, size: 1 },
                troll:       { hp: 500, dmg: 50, range: 50, speed: 0.5, size: 1.8 }
            }[type];

            return {
                x: canvas.width - 130 - Math.random() * 20, y: 150 + Math.random() * 200,
                type: type, hp: stats.hp, maxHp: stats.hp,
                dmg: stats.dmg, range: stats.range, speed: stats.speed, size: stats.size,
                attackCd: 0, stunned: 0
            };
        }

        function spawnUnit(type) {
            let costs = { miner: 30, swordwrath: 40, archidon: 50, spearton: 70, magikill: 100, giant: 160 };
            let pops = { miner: 1, swordwrath: 1, archidon: 1, spearton: 3, magikill: 5, giant: 4 };
            if (gold >= costs[type] && getCurrentPopulation() + pops[type] <= 100) {
                gold -= costs[type];
                units.push(createUnitObject(type));
                playSound(440, 'square', 0.1);
                updateUI();
            }
        }

        // --- VẼ ĐỒ HỌA CAO CẤP (ARTISTIC RENDERER) ---
        function drawStatuesAndEnvironment() {
            // Tượng chính Order Empire (Bên trái)
            ctx.fillStyle = "#d4af37";
            ctx.fillRect(40, 100, 70, 240);
            ctx.fillStyle = "#b8860b";
            ctx.beginPath(); ctx.arc(75, 100, 35, Math.PI, 0, false); ctx.fill();
            ctx.fillStyle = "#fff"; ctx.font = "bold 11px Arial"; ctx.fillText("ORDER", 56, 215);

            // Mỏ vàng trung tâm
            ctx.fillStyle = "#27ae60"; ctx.beginPath(); ctx.arc(490, 230, 48, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "#f1c40f"; ctx.beginPath(); ctx.arc(490, 230, 26, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "#000"; ctx.font = "bold 11px Arial"; ctx.fillText("MỎ VÀNG", 456, 234);

            // Tượng Thần Đen / Cổng Địch (Bên phải)
            ctx.fillStyle = "#512e5f";
            ctx.fillRect(canvas.width - 110, 100, 70, 240);
            ctx.fillStyle = "#4a235a";
            ctx.beginPath(); ctx.arc(canvas.width - 75, 100, 35, Math.PI, 0, false); ctx.fill();
            ctx.fillStyle = "#e74c3c"; ctx.font = "bold 11px Arial"; ctx.fillText("EMPIRE", canvas.width - 102, 215);
        }

        function drawCharacterModel(entity, isEnemy) {
            let x = entity.x, y = entity.y, s = entity.size;
            let primaryColor = isEnemy ? '#c0392b' : '#2980b9';
            if (entity.type === 'giant' || entity.type === 'troll') primaryColor = isEnemy ? '#6c3483' : '#d35400';
            if (entity.type === 'magikill' || entity.type === 'shadow_mage') primaryColor = isEnemy ? '#884ea0' : '#8e44ad';
            if (entity.type === 'miner') primaryColor = '#d35400';
            if (entity.type === 'spearton') primaryColor = '#1f618d';

            ctx.save();
            ctx.translate(x, y);
            if (entity.isSpinning > 0) ctx.rotate((50 - entity.isSpinning) * 0.4);

            // Đầu & Mũ giáp chiến binh tinh xảo
            ctx.fillStyle = primaryColor; ctx.beginPath(); ctx.arc(0, -14 * s, 9 * s, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#ecf0f1';
            if (entity.type === 'swordwrath' || entity.type === 'spearton') {
                ctx.fillRect(-7*s, -21*s, 14*s, 5*s); // Mũ giáp sắt
            } else if (entity.type === 'magikill' || entity.type === 'shadow_mage') {
                ctx.beginPath(); ctx.moveTo(0, -28*s); ctx.lineTo(-9*s, -15*s); ctx.lineTo(9*s, -15*s); ctx.fill(); // Mũ chóp phép
            }

            // Áo giáp thân
            ctx.strokeStyle = primaryColor; ctx.lineWidth = 4 * s;
            ctx.beginPath(); ctx.moveTo(0, -5 * s); ctx.lineTo(0, 12 * s); ctx.stroke();

            // Vũ khí chi tiết
            if (entity.type === 'archidon') {
                ctx.strokeStyle = '#d4af37'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(8*s, -4*s, 9*s, -Math.PI/2, Math.PI/2); ctx.stroke();
            } else if (entity.type === 'spearton') {
                ctx.strokeStyle = '#fff'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(10*s, -18*s); ctx.lineTo(16*s, 18*s); ctx.stroke();
                ctx.fillStyle = '#34495e'; ctx.fillRect(-14*s, -10*s, 7*s, 16*s); // Khiên lớn
            } else if (entity.type === 'magikill') {
                ctx.strokeStyle = '#e74c3c'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(12*s, -18*s); ctx.lineTo(12*s, 18*s); ctx.stroke();
                ctx.fillStyle = '#00ffff'; ctx.beginPath(); ctx.arc(12*s, -19*s, 5*s, 0, Math.PI*2); ctx.fill(); // Ngọc gậy phép
            } else if (entity.type === 'giant') {
                ctx.strokeStyle = '#4e342e'; ctx.lineWidth = 7*s; ctx.beginPath(); ctx.moveTo(14*s, -22*s); ctx.lineTo(20*s, 22*s); ctx.stroke();
            } else if (entity.type === 'miner') {
                ctx.strokeStyle = '#bdc3c7'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(8*s, -10*s); ctx.lineTo(16*s, -4*s); ctx.stroke();
                if (entity.goldBag > 0) {
                    ctx.fillStyle = "#f1c40f"; ctx.beginPath(); ctx.arc(-9*s, 2, 6*s, 0, Math.PI*2); ctx.fill();
                }
            } else if (entity.type === 'swordwrath') {
                ctx.strokeStyle = '#bdc3c7'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(10*s, -6*s); ctx.lineTo(16*s, 12*s); ctx.stroke();
            }

            // Chân bước đi linh hoạt
            let legSwing = Math.sin(animFrame * 0.25) * 7;
            ctx.strokeStyle = primaryColor; ctx.lineWidth = 3.5 * s;
            ctx.beginPath(); ctx.moveTo(0, 12 * s); ctx.lineTo(-7 * s, 22 * s + legSwing); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(0, 12 * s); ctx.lineTo(7 * s, 22 * s - legSwing); ctx.stroke();

            // Thanh HP trên đầu
            ctx.fillStyle = "#000"; ctx.fillRect(-16 * s, -33 * s, 32 * s, 5);
            ctx.fillStyle = "#2ecc71"; ctx.fillRect(-16 * s, -33 * s, (entity.hp / entity.maxHp) * 32 * s, 5);

            ctx.restore();
        }

        // --- GAME LOOP CHÍNH ---
        function gameLoop() {
            animFrame++;
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Nền chiến trường sắc nét
            ctx.fillStyle = "#4a3c2e"; ctx.fillRect(0, 120, canvas.width, 260);

            drawStatuesAndEnvironment();

            // XỬ LÝ THỢ MỎ
            units.filter(u => u.type === 'miner').forEach(u => {
                if (u.state === 'going') {
                    u.x += u.speed;
                    if (u.x >= 475) u.state = 'mining';
                } else if (u.state === 'returning') {
                    u.x -= u.speed;
                    if (u.x <= 130) {
                        gold += u.goldBag || 15;
                        u.goldBag = 0;
                        u.state = 'going';
                        addFloatingText("+15 Vàng", 130, 200, '#ffd700');
                    }
                } else if (u.state === 'mining') {
                    u.goldBag = 15;
                    u.state = 'returning';
                }
                drawCharacterModel(u, false);
            });

            // XỬ LÝ QUÂN LÍNH CHIẾN ĐẤU
            units.filter(u => u.type !== 'miner').forEach((u, uIdx) => {
                if (u.isSpinning > 0) {
                    u.isSpinning--;
                    enemies.forEach(e => {
                        if (Math.hypot(e.x - u.x, e.y - u.y) < 70) e.hp -= 4;
                    });
                }

                let targetX = u.x;
                if (currentCommand === 'ATTACK') targetX = canvas.width - 140;
                else if (currentCommand === 'DEFEND') targetX = 350;
                else if (currentCommand === 'HOLD') targetX = u.x;

                let enemyNear = enemies.find(e => Math.hypot(e.x - u.x, e.y - u.y) <= u.range);
                if (!enemyNear && Math.abs(u.x - targetX) > 10) {
                    u.x += u.x < targetX ? u.speed : -u.speed;
                }

                if (u.type === 'archidon' && enemyNear && u.attackCd === 0) {
                    projectiles.push({ x: u.x, y: u.y - 10, targetX: enemyNear.x, targetY: enemyNear.y, vx: 7, vy: -2, type: 'arrow', damage: u.dmg });
                    u.attackCd = 40;
                }

                if (u.attackCd > 0) u.attackCd--;
                else {
                    let target = enemies.find(e => Math.hypot(e.x - u.x, e.y - u.y) <= u.range);
                    if (target) {
                        target.hp -= u.dmg;
                        addFloatingText("-" + u.dmg, target.x, target.y - 15, '#e74c3c');
                        u.attackCd = 32;
                    } else if (u.x >= canvas.width - 150) {
                        enemyStatueHp -= u.dmg;
                        addFloatingText("-" + u.dmg, canvas.width - 130, 180, '#f1c40f');
                        u.attackCd = 35;
                        updateUI();
                    }
                }

                drawCharacterModel(u, false);
                if (u.hp <= 0) units.splice(uIdx, 1);
            });

            // XỬ LÝ KẺ ĐỊCH
            enemies.forEach((e, eIdx) => {
                if (e.stunned > 0) {
                    e.stunned--;
                    drawCharacterModel(e, true);
                    return;
                }

                let unitNear = units.find(u => Math.hypot(u.x - e.x, u.y - e.y) <= e.range);
                if (!unitNear && e.x > 140) { e.x -= e.speed; }

                if (e.attackCd > 0) e.attackCd--;
                else {
                    let target = units.find(u => Math.hypot(u.x - e.x, u.y - e.y) <= e.range);
                    if (target) {
                        target.hp -= e.dmg;
                        addFloatingText("-" + e.dmg, target.x, target.y - 15, '#e74c3c');
                        e.attackCd = 35;
                    } else if (e.x <= 140) {
                        statueHp -= e.dmg;
                        addFloatingText("-" + e.dmg, 130, 180, '#e74c3c');
                        e.attackCd = 35;
                        updateUI();
                    }
                }

                drawCharacterModel(e, true);
                if (e.hp <= 0) { enemies.splice(eIdx, 1); gold += 25; addFloatingText("+25 Vàng", e.x, e.y, '#ffd700'); updateUI(); }
            });

            // ĐẠN & HIỆU ỨNG TÊN BAY
            projectiles.forEach((p, pIdx) => {
                p.x += p.vx; p.y += p.vy;
                ctx.fillStyle = "#f1c40f"; ctx.fillRect(p.x, p.y, 8, 2);
                if (p.y >= (p.targetY || 300)) {
                    enemies.forEach(e => { if (Math.hypot(e.x - p.x, e.y - p.y) < 45) { e.hp -= p.damage; addFloatingText("-" + p.damage, e.x, e.y, '#e74c3c'); } });
                    projectiles.splice(pIdx, 1);
                }
            });

            // CHỮ SỐ BAY (FLOATING TEXTS)
            floatingTexts.forEach((ft, idx) => {
                ft.y -= 0.8; ft.alpha -= 0.02;
                ctx.fillStyle = ft.color;
                ctx.globalAlpha = Math.max(0, ft.alpha);
                ctx.font = "bold 13px Arial";
                ctx.fillText(ft.text, ft.x, ft.y);
                ctx.globalAlpha = 1.0;
                if (ft.alpha <= 0) floatingTexts.splice(idx, 1);
            });

            // KIỂM TRA THẮNG THUA
            if (statueHp <= 0 || enemyStatueHp <= 0) {
                ctx.fillStyle = "rgba(0,0,0,0.85)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = statueHp > 0 ? "#2ecc71" : "#e74c3c";
                ctx.font = "bold 36px Arial";
                ctx.fillText(statueHp > 0 ? "🏆 ORDER EMPIRE CHIẾN THẮNG!" : "💀 TƯỢNG CHÍNH ĐÃ SỤP ĐỔ!", canvas.width / 2 - 230, canvas.height / 2);
                return;
            }

            requestAnimationFrame(gameLoop);
        }

        gameLoop();
    </script>
</body>
</html>
"""

st.components.v1.html(game_html, height=560, scrolling=False)
