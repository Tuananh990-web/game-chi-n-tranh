import streamlit as st

st.set_page_config(page_title="Stick War 2: Order Empire - Ultimate Edition", page_icon="⚔️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #020408; color: white; }
    iframe { border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.95); }
    </style>
""", unsafe_allow_html=True)

st.title("⚔️ Stick War 2: Order Empire (True Stickmen Graphics)")
st.markdown("Phiên bản làm lại hoàn toàn: Đồ họa người que chuẩn Stick War 2, 6 mỏ vàng nhỏ trước thành, hệ thống lính và kỹ năng chiến đấu độc lập.")

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Stick War 2 True Graphics</title>
    <style>
        body { margin: 0; background: #020408; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; overflow: hidden; }
        canvas { background: linear-gradient(to bottom, #0f2413, #18381c); border: 3px solid #2c3e50; border-radius: 8px; box-shadow: 0 12px 35px rgba(0,0,0,0.95); cursor: crosshair; display: block; margin: 4px auto; }
        .ui-panel { display: flex; justify-content: center; flex-wrap: wrap; gap: 5px; margin-top: 4px; }
        .cmd-panel { display: flex; justify-content: center; gap: 8px; margin-top: 4px; }
        button { background: #b7950b; color: #fff; border: 2px solid #f1c40f; padding: 6px 12px; font-weight: bold; font-size: 11px; border-radius: 5px; cursor: pointer; transition: 0.2s; }
        button:hover { background: #d4ac0d; transform: scale(1.05); }
        .cmd-btn { background: #1b4f72; border-color: #5dade2; }
        .skill-btn { background: #512e5f; border-color: #f39c12; }
        .stats { font-size: 13px; font-weight: bold; color: #f1c40f; margin-bottom: 2px; }
    </style>
</head>
<body>

    <div class="stats">
        🏰 Tượng Order: <span id="hpText">2500</span> | 👹 Tượng Địch: <span id="enemyHpText">2500</span> | 💰 Vàng: <span id="goldText">400</span> | 👥 Dân số: <span id="popText">0</span>/100 | ⚔️ Lệnh: <span id="cmdText" style="color:#2ecc71;">TẤN CÔNG</span>
    </div>

    <canvas id="gameCanvas" width="980" height="410"></canvas>

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
        <button onclick="spawnUnit('miner')">⛏️ Miner (30g - 1 Pop)</button>
        <button onclick="spawnUnit('swordwrath')">⚔️ Swordwrath (40g - 1 Pop)</button>
        <button onclick="spawnUnit('archidon')">🏹 Archidon (50g - 1 Pop)</button>
        <button onclick="spawnUnit('spearton')">🛡️ Spearton (70g - 3 Pop)</button>
        <button onclick="spawnUnit('magikill')">🧙 Magikill (100g - 5 Pop)</button>
        <button onclick="spawnUnit('giant')">🗿 Giant (160g - 4 Pop)</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let statueHp = 2500, statueMaxHp = 2500;
        let enemyStatueHp = 2500, enemyStatueMaxHp = 2500;
        let gold = 400;
        let currentCommand = 'ATTACK';

        // 6 Mỏ vàng nhỏ phân bổ ngay trước tượng chính của phe ta
        let goldMines = [
            { x: 160, y: 140, assignedMiner: null },
            { x: 210, y: 200, assignedMiner: null },
            { x: 260, y: 270, assignedMiner: null },
            { x: 180, y: 320, assignedMiner: null },
            { x: 230, y: 130, assignedMiner: null },
            { x: 280, y: 190, assignedMiner: null }
        ];

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
                gain.gain.setValueAtTime(0.03, audioCtx.currentTime);
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

        function addFloatingText(text, x, y, color = '#f1c40f') {
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
                addFloatingText("Mưa Tên!", 600, 80, '#f1c40f');
                playSound(750, 'sine', 0.3);
            } else if (type === 'earthquake') {
                units.filter(u => u.type === 'giant').forEach(u => {
                    enemies.forEach(e => {
                        if (Math.hypot(e.x - u.x, e.y - u.y) < 200) {
                            e.stunned = 100;
                            e.hp -= 50;
                            addFloatingText("-50 Choáng", e.x, e.y - 20, '#e74c3c');
                        }
                    });
                });
                playSound(100, 'sawtooth', 0.6);
            }
        }

        setInterval(() => {
            if (enemyStatueHp > 0 && enemies.length < 45) {
                let types = ['goblin', 'orc', 'shadow_mage', 'troll'];
                let t = types[Math.floor(Math.random() * types.length)];
                enemies.push(createEnemyObject(t));
            }
        }, 1600);

        function createUnitObject(type) {
            let stats = {
                miner:      { hp: 90,  dmg: 8,  range: 30, speed: 1.5, size: 0.9 },
                swordwrath: { hp: 150, dmg: 20, range: 35, speed: 1.3, size: 1 },
                archidon:   { hp: 100, dmg: 25, range: 190, speed: 1.1, size: 1 },
                spearton:   { hp: 220, dmg: 30, range: 60, speed: 0.9, size: 1.2 },
                magikill:   { hp: 110, dmg: 40, range: 170, speed: 0.8, size: 1 },
                giant:      { hp: 700, dmg: 65, range: 55, speed: 0.5, size: 1.9 }
            }[type];

            let unit = {
                x: 100, y: 150 + Math.random() * 200,
                type: type, hp: stats.hp, maxHp: stats.hp,
                dmg: stats.dmg, range: stats.range, speed: stats.speed, size: stats.size,
                attackCd: 0, state: 'going', goldBag: 0, isSpinning: 0, mineTarget: null
            };

            if (type === 'miner') {
                let freeMine = goldMines.find(m => !m.assignedMiner);
                if (freeMine) {
                    freeMine.assignedMiner = unit;
                    unit.mineTarget = freeMine;
                } else {
                    unit.mineTarget = goldMines[0];
                }
            }
            return unit;
        }

        function createEnemyObject(type) {
            let stats = {
                goblin:      { hp: 95,  dmg: 12, range: 30, speed: 1.4, size: 0.9 },
                orc:         { hp: 190, dmg: 22, range: 35, speed: 1.0, size: 1.2 },
                shadow_mage: { hp: 130, dmg: 32, range: 150, speed: 0.8, size: 1 },
                troll:       { hp: 500, dmg: 50, range: 50, speed: 0.5, size: 1.8 }
            }[type];

            return {
                x: canvas.width - 110 - Math.random() * 20, y: 150 + Math.random() * 200,
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

        function updateUI() {
            document.getElementById("hpText").innerText = Math.max(0, Math.floor(statueHp));
            document.getElementById("enemyHpText").innerText = Math.max(0, Math.floor(enemyStatueHp));
            document.getElementById("goldText").innerText = gold;
            document.getElementById("popText").innerText = getCurrentPopulation();
        }

        // --- HỆ THỐNG VẼ ĐỒ HỌA THỰC TẾ CHUẨN STICK WAR 2 ---
        function drawEnvironment() {
            // Tượng chính Order Empire (Bên trái)
            ctx.fillStyle = "#d4ac0d"; ctx.fillRect(25, 80, 60, 260);
            ctx.fillStyle = "#f1c40f"; ctx.beginPath(); ctx.arc(55, 80, 30, Math.PI, 0, false); ctx.fill();
            ctx.fillStyle = "#1b4f72"; ctx.font = "bold 9px Arial"; ctx.fillText("ORDER", 36, 215);

            // 6 Mỏ vàng nhỏ trước thành
            goldMines.forEach((m, idx) => {
                ctx.fillStyle = "#f39c12";
                ctx.beginPath(); ctx.arc(m.x, m.y, 15, 0, Math.PI*2); ctx.fill();
                ctx.strokeStyle = "#b9770e"; ctx.lineWidth = 2; ctx.stroke();
                ctx.fillStyle = "#000"; ctx.font = "bold 8px Arial";
                ctx.fillText("M" + (idx+1), m.x - 5, m.y + 3);
            });

            // Tượng Cổng Địch (Bên phải)
            ctx.fillStyle = "#641e16"; ctx.fillRect(canvas.width - 85, 80, 60, 260);
            ctx.fillStyle = "#922b21"; ctx.beginPath(); ctx.arc(canvas.width - 55, 80, 30, Math.PI, 0, false); ctx.fill();
            ctx.fillStyle = "#f1c40f"; ctx.font = "bold 9px Arial"; ctx.fillText("EMPIRE", canvas.width - 77, 215);
        }

        function drawStickWarCharacter(entity, isEnemy) {
            let x = entity.x, y = entity.y, s = entity.size;
            let teamColor = isEnemy ? '#e74c3c' : '#3498db';
            if (entity.type === 'giant' || entity.type === 'troll') teamColor = isEnemy ? '#8e44ad' : '#d35400';
            if (entity.type === 'magikill' || entity.type === 'shadow_mage') teamColor = isEnemy ? '#9b59b6' : '#8e44ad';
            if (entity.type === 'miner') teamColor = '#f39c12';
            if (entity.type === 'spearton') teamColor = '#2980b9';

            ctx.save();
            ctx.translate(x, y);
            if (entity.isSpinning > 0) ctx.rotate((50 - entity.isSpinning) * 0.4);

            // Đầu người que đặc trưng
            ctx.strokeStyle = teamColor; ctx.lineWidth = 2.2 * s;
            ctx.beginPath(); ctx.arc(0, -14 * s, 5.5 * s, 0, Math.PI * 2); ctx.stroke();
            ctx.fillStyle = teamColor; ctx.fill();

            // Mũ giáp chiến binh Stick War 2
            if (entity.type === 'swordwrath') {
                ctx.fillStyle = '#95a5a6'; ctx.fillRect(-5*s, -18*s, 10*s, 3*s);
            } else if (entity.type === 'spearton') {
                ctx.fillStyle = '#2c3e50'; ctx.fillRect(-6*s, -19*s, 12*s, 5*s);
            } else if (entity.type === 'magikill' || entity.type === 'shadow_mage') {
                ctx.fillStyle = '#512e5f'; ctx.beginPath(); ctx.moveTo(0, -24*s); ctx.lineTo(-6*s, -14*s); ctx.lineTo(6*s, -14*s); ctx.fill();
            }

            // Thân người que
            ctx.beginPath(); ctx.moveTo(0, -8.5 * s); ctx.lineTo(0, 7 * s); ctx.stroke();

            // Trang bị vũ khí chi tiết
            if (entity.type === 'archidon') {
                ctx.strokeStyle = '#d4af37'; ctx.beginPath(); ctx.arc(6*s, -4*s, 6*s, -Math.PI/2, Math.PI/2); ctx.stroke();
            } else if (entity.type === 'spearton') {
                ctx.strokeStyle = '#fff'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(7*s, -12*s); ctx.lineTo(13*s, 12*s); ctx.stroke();
                ctx.fillStyle = '#1b4f72'; ctx.fillRect(-10*s, -7*s, 5*s, 12*s); // Khiên xanh
            } else if (entity.type === 'magikill') {
                ctx.strokeStyle = '#e74c3c'; ctx.beginPath(); ctx.moveTo(8*s, -12*s); ctx.lineTo(8*s, 12*s); ctx.stroke();
                ctx.fillStyle = '#00ffff'; ctx.beginPath(); ctx.arc(8*s, -13*s, 3.5*s, 0, Math.PI*2); ctx.fill();
            } else if (entity.type === 'giant') {
                ctx.strokeStyle = '#4e342e'; ctx.lineWidth = 4.5 * s;
                ctx.beginPath(); ctx.moveTo(9*s, -16*s); ctx.lineTo(14*s, 16*s); ctx.stroke();
            } else if (entity.type === 'miner') {
                ctx.strokeStyle = '#95a5a6'; ctx.beginPath(); ctx.moveTo(6*s, -7*s); ctx.lineTo(11*s, -2*s); ctx.stroke();
                if (entity.goldBag > 0) {
                    ctx.fillStyle = "#f1c40f"; ctx.beginPath(); ctx.arc(-7*s, 0, 4.5*s, 0, Math.PI*2); ctx.fill();
                }
            } else if (entity.type === 'swordwrath') {
                ctx.strokeStyle = '#95a5a6'; ctx.beginPath(); ctx.moveTo(7*s, -4*s); ctx.lineTo(11*s, 8*s); ctx.stroke();
            }

            // Chân bước đi
            let swing = Math.sin(animFrame * 0.3) * 5;
            ctx.strokeStyle = teamColor; ctx.lineWidth = 2.2 * s;
            ctx.beginPath(); ctx.moveTo(0, 7 * s); ctx.lineTo(-4 * s, 15 * s + swing); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(0, 7 * s); ctx.lineTo(4 * s, 15 * s - swing); ctx.stroke();

            // Thanh Máu
            ctx.fillStyle = "#000"; ctx.fillRect(-12 * s, -24 * s, 24 * s, 3.5);
            ctx.fillStyle = "#2ecc71"; ctx.fillRect(-12 * s, -24 * s, (entity.hp / entity.maxHp) * 24 * s, 3.5);

            ctx.restore();
        }

        function gameLoop() {
            animFrame++;
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Nền chiến trường
            ctx.fillStyle = "#1a2e1d"; ctx.fillRect(0, 100, canvas.width, 290);

            drawEnvironment();

            // XỬ LÝ THỢ MỎ ĐI KHAI THÁC TẠI 6 MỎ VÀNG NHỎ
            units.filter(u => u.type === 'miner').forEach((u) => {
                if (u.mineTarget) {
                    if (u.state === 'going') {
                        let dx = u.mineTarget.x - u.x;
                        let dy = u.mineTarget.y - u.y;
                        let dist = Math.hypot(dx, dy);
                        if (dist > 3) {
                            u.x += (dx / dist) * u.speed;
                            u.y += (dy / dist) * u.speed;
                        } else {
                            u.state = 'mining';
                        }
                    } else if (u.state === 'mining') {
                        u.goldBag = 12;
                        u.state = 'returning';
                    } else if (u.state === 'returning') {
                        let dx = 85 - u.x;
                        let dy = 200 - u.y;
                        let dist = Math.hypot(dx, dy);
                        if (dist > 3) {
                            u.x += (dx / dist) * u.speed;
                            u.y += (dy / dist) * u.speed;
                        } else {
                            gold += u.goldBag || 12;
                            u.goldBag = 0;
                            u.state = 'going';
                            addFloatingText("+12 Vàng", 85, 200, '#f1c40f');
                        }
                    }
                }
                drawStickWarCharacter(u, false);
            });

            // XỬ LÝ QUÂN LÍNH CHIẾN ĐẤU
            units.filter(u => u.type !== 'miner').forEach((u, uIdx) => {
                if (u.isSpinning > 0) {
                    u.isSpinning--;
                    enemies.forEach(e => {
                        if (Math.hypot(e.x - u.x, e.y - u.y) < 60) e.hp -= 4;
                    });
                }

                let targetX = u.x;
                if (currentCommand === 'ATTACK') targetX = canvas.width - 100;
                else if (currentCommand === 'DEFEND') targetX = 320;
                else if (currentCommand === 'HOLD') targetX = u.x;

                let enemyNear = enemies.find(e => Math.hypot(e.x - u.x, e.y - u.y) <= u.range);
                if (!enemyNear && Math.abs(u.x - targetX) > 6) {
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
                        u.attackCd = 30;
                    } else if (u.x >= canvas.width - 110) {
                        enemyStatueHp -= u.dmg;
                        addFloatingText("-" + u.dmg, canvas.width - 90, 180, '#f1c40f');
                        u.attackCd = 35;
                        updateUI();
                    }
                }

                drawStickWarCharacter(u, false);
                if (u.hp <= 0) units.splice(uIdx, 1);
            });

            // XỬ LÝ KẺ ĐỊCH
            enemies.forEach((e, eIdx) => {
                if (e.stunned > 0) {
                    e.stunned--;
                    drawStickWarCharacter(e, true);
                    return;
                }

                let unitNear = units.find(u => Math.hypot(u.x - e.x, u.y - e.y) <= e.range);
                if (!unitNear && e.x > 100) { e.x -= e.speed; }

                if (e.attackCd > 0) e.attackCd--;
                else {
                    let target = units.find(u => Math.hypot(u.x - e.x, u.y - e.y) <= e.range);
                    if (target) {
                        target.hp -= e.dmg;
                        addFloatingText("-" + e.dmg, target.x, target.y - 15, '#e74c3c');
                        e.attackCd = 32;
                    } else if (e.x <= 100) {
                        statueHp -= e.dmg;
                        addFloatingText("-" + e.dmg, 90, 180, '#e74c3c');
                        e.attackCd = 35;
                        updateUI();
                    }
                }

                drawStickWarCharacter(e, true);
                if (e.hp <= 0) { enemies.splice(eIdx, 1); gold += 25; addFloatingText("+25 Vàng", e.x, e.y, '#f1c40f'); updateUI(); }
            });

            projectiles.forEach((p, pIdx) => {
                p.x += p.vx; p.y += p.vy;
                ctx.fillStyle = "#f1c40f"; ctx.fillRect(p.x, p.y, 6, 2);
                if (p.y >= (p.targetY || 300)) {
                    enemies.forEach(e => { if (Math.hypot(e.x - p.x, e.y - p.y) < 35) { e.hp -= p.damage; addFloatingText("-" + p.damage, e.x, e.y, '#e74c3c'); } });
                    projectiles.splice(pIdx, 1);
                }
            });

            floatingTexts.forEach((ft, idx) => {
                ft.y -= 0.8; ft.alpha -= 0.02;
                ctx.fillStyle = ft.color;
                ctx.globalAlpha = Math.max(0, ft.alpha);
                ctx.font = "bold 11px Arial";
                ctx.fillText(ft.text, ft.x, ft.y);
                ctx.globalAlpha = 1.0;
                if (ft.alpha <= 0) floatingTexts.splice(idx, 1);
            });

            if (statueHp <= 0 || enemyStatueHp <= 0) {
                ctx.fillStyle = "rgba(0,0,0,0.85)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = statueHp > 0 ? "#2ecc71" : "#e74c3c";
                ctx.font = "bold 34px Arial";
                ctx.fillText(statueHp > 0 ? "🏆 ORDER EMPIRE CHIẾN THẮNG!" : "💀 TƯỢNG CHÍNH ĐÃ SỤP ĐỔ!", canvas.width / 2 - 220, canvas.height / 2);
                return;
            }

            requestAnimationFrame(gameLoop);
        }

        gameLoop();
    </script>
</body>
</html>
"""

st.components.v1.html(game_html, height=550, scrolling=False)
