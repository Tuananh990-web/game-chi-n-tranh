import streamlit as st

st.set_page_config(
    page_title="Stick War 2: Order Empire - Official 2D Vector Edition",
    page_icon="⚔️",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #030508; color: #e0e0e0; font-family: 'Segoe UI', Tahoma, sans-serif; }
    iframe { border-radius: 12px; box-shadow: 0 12px 40px rgba(0,0,0,0.95); }
    .title-text { text-align: center; color: #ffcc00; text-transform: uppercase; font-weight: 800; margin-bottom: 0px; }
    .sub-text { text-align: center; color: #aaaaaa; font-size: 14px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-text'>⚔️ STICK WAR 2: ORDER EMPIRE ⚔️</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>2D Side-Scrolling Vector Engine | Authentic Flash Art Style & Mechanics</p>", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Stick War 2 Order Empire</title>
    <style>
        body { margin: 0; background: #020305; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; overflow: hidden; }
        canvas { background: #111a14; border: 3px solid #3a2c1d; border-radius: 8px; box-shadow: 0 12px 35px rgba(0,0,0,0.95); cursor: crosshair; display: block; margin: 4px auto; }
        .ui-panel { display: flex; justify-content: center; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
        .cmd-panel { display: flex; justify-content: center; gap: 10px; margin-top: 6px; }
        button { background: #8a641b; color: #fff; border: 2px solid #ffcc00; padding: 7px 14px; font-weight: bold; font-size: 11px; border-radius: 4px; cursor: pointer; transition: 0.2s; text-transform: uppercase; }
        button:hover { background: #b38324; transform: scale(1.05); }
        .cmd-btn { background: #1b4f72; border-color: #5dade2; }
        .skill-btn { background: #512e5f; border-color: #f39c12; }
        .stats { font-size: 14px; font-weight: bold; color: #ffcc00; margin-bottom: 4px; }
    </style>
</head>
<body>

    <div class="stats">
        🏰 TƯỢNG ORDER: <span id="hpText">2500</span> | 👹 TƯỢNG EMPIRE: <span id="enemyHpText">2500</span> | 💰 VÀNG: <span id="goldText">400</span> | 👥 DÂN SỐ: <span id="popText">0</span>/100 | ⚔️ CHỈ THỊ: <span id="cmdText" style="color:#2ecc71;">ATTACK</span>
    </div>

    <canvas id="gameCanvas" width="980" height="420"></canvas>

    <div class="cmd-panel">
        <button class="cmd-btn" onclick="setCommand('ATTACK')">⚔️ ATTACK (TẤN CÔNG)</button>
        <button class="cmd-btn" onclick="setCommand('DEFEND')">🛡️ DEFEND (PHÒNG THỦ)</button>
        <button class="cmd-btn" onclick="setCommand('HOLD')">🛑 HOLD (GIỮ VỊ TRÍ)</button>
        <button class="skill-btn" onclick="triggerSkill('spin')">🌀 SPIN ATTACK</button>
        <button class="skill-btn" onclick="triggerSkill('arrowRain')">🏹 ARROW RAIN</button>
        <button class="skill-btn" onclick="triggerSkill('earthquake')">💥 EARTHQUAKE</button>
        <button onclick="toggleAudio()">🔊 ÂM THANH</button>
    </div>

    <div class="ui-panel">
        <button onclick="spawnUnit('miner')">⛏️ MINER (30g - 1 Pop)</button>
        <button onclick="spawnUnit('swordwrath')">⚔️ SWORDWRATH (40g - 1 Pop)</button>
        <button onclick="spawnUnit('archidon')">🏹 ARCHIDON (50g - 1 Pop)</button>
        <button onclick="spawnUnit('spearton')">🛡️ SPEARTON (70g - 3 Pop)</button>
        <button onclick="spawnUnit('magikill')">🧙 MAGIKILL (100g - 5 Pop)</button>
        <button onclick="spawnUnit('giant')">🗿 GIANT (160g - 4 Pop)</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let statueHp = 2500, statueMaxHp = 2500;
        let enemyStatueHp = 2500, enemyStatueMaxHp = 2500;
        let gold = 400;
        let currentCommand = 'ATTACK';

        // 6 mỏ vàng vị trí chuẩn ngay trước tượng phe ta
        let goldMines = [
            { x: 150, y: 140, miner: null },
            { x: 195, y: 195, miner: null },
            { x: 240, y: 260, miner: null },
            { x: 170, y: 315, miner: null },
            { x: 220, y: 130, miner: null },
            { x: 260, y: 185, miner: null }
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
            document.getElementById("cmdText").innerText = cmd;
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

        function addFloatingText(text, x, y, color = '#ffcc00') {
            floatingTexts.push({ text, x, y, alpha: 1.0, color });
        }

        function triggerSkill(type) {
            if (type === 'spin') {
                units.filter(u => u.type === 'swordwrath').forEach(u => {
                    u.isSpinning = 50;
                    addFloatingText("SPIN ATTACK!", u.x, u.y - 30, '#5dade2');
                });
                playSound(450, 'sawtooth', 0.4);
            } else if (type === 'arrowRain') {
                for(let i=0; i<20; i++) {
                    projectiles.push({
                        x: 450 + Math.random()*300, y: 0,
                        targetY: 200 + Math.random()*160,
                        vx: 0, vy: 14, type: 'arrow', damage: 30
                    });
                }
                addFloatingText("ARROW RAIN!", 600, 70, '#f1c40f');
                playSound(750, 'sine', 0.3);
            } else if (type === 'earthquake') {
                units.filter(u => u.type === 'giant').forEach(u => {
                    enemies.forEach(e => {
                        if (Math.hypot(e.x - u.x, e.y - u.y) < 220) {
                            e.stunned = 100;
                            e.hp -= 60;
                            addFloatingText("-60 STUN", e.x, e.y - 20, '#e74c3c');
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
                miner:      { hp: 100, dmg: 8,  range: 30, speed: 1.5, size: 0.95 },
                swordwrath: { hp: 160, dmg: 22, range: 35, speed: 1.35, size: 1.0 },
                archidon:   { hp: 110, dmg: 26, range: 190, speed: 1.15, size: 1.0 },
                spearton:   { hp: 240, dmg: 32, range: 60, speed: 0.95, size: 1.2 },
                magikill:   { hp: 120, dmg: 42, range: 170, speed: 0.85, size: 1.05 },
                giant:      { hp: 750, dmg: 70, range: 55, speed: 0.55, size: 1.95 }
            }[type];

            let unit = {
                x: 90, y: 150 + Math.random() * 200,
                type: type, hp: stats.hp, maxHp: stats.hp,
                dmg: stats.dmg, range: stats.range, speed: stats.speed, size: stats.size,
                attackCd: 0, state: 'going', goldBag: 0, isSpinning: 0, mineTarget: null
            };

            if (type === 'miner') {
                let freeMine = goldMines.find(m => !m.miner);
                if (freeMine) {
                    freeMine.miner = unit;
                    unit.mineTarget = freeMine;
                } else {
                    unit.mineTarget = goldMines[0];
                }
            }
            return unit;
        }

        function createEnemyObject(type) {
            let stats = {
                goblin:      { hp: 100, dmg: 12, range: 30, speed: 1.4, size: 0.95 },
                orc:         { hp: 200, dmg: 24, range: 35, speed: 1.0, size: 1.2 },
                shadow_mage: { hp: 140, dmg: 34, range: 150, speed: 0.8, size: 1.05 },
                troll:       { hp: 550, dmg: 55, range: 50, speed: 0.5, size: 1.85 }
            }[type];

            return {
                x: canvas.width - 100 - Math.random() * 20, y: 150 + Math.random() * 200,
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

        // --- BẮT ĐẦU ĐỒ HỌA CHUẨN STICK WAR 2 ORDER EMPIRE ---
        function drawBackgroundAndStatues() {
            // Núi non nền xa
            ctx.fillStyle = "#0d1712";
            ctx.beginPath(); ctx.moveTo(0, 120); ctx.lineTo(180, 40); ctx.lineTo(380, 120); ctx.fill();
            ctx.beginPath(); ctx.moveTo(320, 120); ctx.lineTo(550, 30); ctx.lineTo(780, 120); ctx.fill();
            ctx.beginPath(); ctx.moveTo(700, 120); ctx.lineTo(880, 50); ctx.lineTo(980, 120); ctx.fill();

            // Mặt đất
            ctx.fillStyle = "#1e2c20";
            ctx.fillRect(0, 120, canvas.width, 270);
            ctx.fillStyle = "#2c3e2e";
            ctx.fillRect(0, 120, canvas.width, 6);

            // Tượng Order Empire (Tay cầm gươm lớn giơ cao)
            ctx.fillStyle = "#c59b27";
            ctx.fillRect(20, 70, 50, 270); // Bệ đá
            ctx.fillStyle = "#e5c158";
            ctx.beginPath(); ctx.arc(45, 65, 22, 0, Math.PI*2); ctx.fill(); // Đầu tượng
            ctx.strokeStyle = "#e5c158"; ctx.lineWidth = 6;
            ctx.beginPath(); ctx.moveTo(45, 87); ctx.lineTo(45, 160); ctx.stroke(); // Thân
            ctx.beginPath(); ctx.moveTo(45, 100); ctx.lineTo(75, 45); ctx.stroke(); // Tay cầm kiếm
            ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 4;
            ctx.beginPath(); ctx.moveTo(75, 45); ctx.lineTo(75, 10); ctx.stroke(); // Lưỡi kiếm Order
            ctx.fillStyle = "#154360"; ctx.font = "bold 10px Arial"; ctx.fillText("ORDER", 28, 200);

            // 6 Mỏ Vàng Nhỏ Trước Thành
            goldMines.forEach((m, idx) => {
                ctx.fillStyle = "#f39c12";
                ctx.beginPath(); ctx.arc(m.x, m.y, 14, 0, Math.PI*2); ctx.fill();
                ctx.strokeStyle = "#9a7d0a"; ctx.lineWidth = 2.5; ctx.stroke();
                ctx.fillStyle = "#111"; ctx.font = "bold 9px Arial";
                ctx.fillText("M" + (idx+1), m.x - 5, m.y + 3);
            });

            // Tượng Ác Quỷ/Empire Địch
            ctx.fillStyle = "#5c1d18";
            ctx.fillRect(canvas.width - 70, 70, 50, 270);
            ctx.fillStyle = "#922b21";
            ctx.beginPath(); ctx.arc(canvas.width - 45, 65, 22, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "#f39c12"; ctx.font = "bold 10px Arial"; ctx.fillText("EMPIRE", canvas.width - 63, 200);
        }

        // HỆ THỐNG MÔ PHỎNG CHIẾN BINH NGƯỜI QUE ĐEN (STICKMAN VECTOR)
        function drawOfficialStickman(entity, isEnemy) {
            let x = entity.x, y = entity.y, s = entity.size;

            ctx.save();
            ctx.translate(x, y);
            if (entity.isSpinning > 0) ctx.rotate((50 - entity.isSpinning) * 0.4);

            // 1. Thân & Đầu người que đen tuyền (Khuôn mặt đen tròn không nét)
            ctx.strokeStyle = "#000000";
            ctx.lineWidth = 3.5 * s;
            ctx.fillStyle = "#000000";

            // Head (Black Circle - Stick War Signature)
            ctx.beginPath(); ctx.arc(0, -16 * s, 6 * s, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

            // Spine (Cột sống)
            ctx.beginPath(); ctx.moveTo(0, -10 * s); ctx.lineTo(0, 8 * s); ctx.stroke();

            // Arms & Weapons
            let armSwing = Math.sin(animFrame * 0.25) * 4;
            ctx.beginPath(); ctx.moveTo(0, -7 * s); ctx.lineTo(-6 * s, 2 * s + armSwing); ctx.stroke(); // Tay trái
            ctx.beginPath(); ctx.moveTo(0, -7 * s); ctx.lineTo(8 * s, 0 * s - armSwing); ctx.stroke(); // Tay phải cầm vũ khí

            // Vũ khí & Trang bị chi tiết theo đúng thiết kế Stick War 2
            if (entity.type === 'swordwrath') {
                // Swordwrath: Mũ giáp sắt + Kiếm sắc bén
                ctx.fillStyle = '#b2bec3'; ctx.fillRect(-5*s, -21*s, 10*s, 4*s); // Helmet
                ctx.strokeStyle = '#dfe6e9'; ctx.lineWidth = 3 * s;
                ctx.beginPath(); ctx.moveTo(8*s, 0); ctx.lineTo(18*s, -12*s); ctx.stroke(); // Gươm
            } else if (entity.type === 'spearton') {
                // Spearton: Mũ giáp Hoplite + Giáo dài + Khiên đồng tròn to
                ctx.fillStyle = '#636e72'; ctx.fillRect(-6*s, -23*s, 12*s, 6*s); // Mũ
                ctx.strokeStyle = '#fff'; ctx.lineWidth = 2.5 * s;
                ctx.beginPath(); ctx.moveTo(8*s, -16*s); ctx.lineTo(18*s, 16*s); ctx.stroke(); // Giáo
                // Khiên tròn to màu xanh đậm / đồng
                ctx.fillStyle = isEnemy ? '#a29bfe' : '#0984e3';
                ctx.beginPath(); ctx.arc(-8*s, 0, 9*s, 0, Math.PI*2); ctx.fill();
                ctx.strokeStyle = '#d63031'; ctx.lineWidth = 2; ctx.stroke();
            } else if (entity.type === 'archidon') {
                // Archidon: Cung gỗ + Bao tên trên lưng
                ctx.strokeStyle = '#e17055'; ctx.lineWidth = 2 * s;
                ctx.beginPath(); ctx.arc(9*s, -2*s, 8*s, -Math.PI/2, Math.PI/2); ctx.stroke(); // Cung
                ctx.fillStyle = '#d63031'; ctx.fillRect(-7*s, -12*s, 4*s, 10*s); // Quiver bao tên
            } else if (entity.type === 'magikill') {
                // Magikill: Mũ phù thủy nhọn + Gậy phép sáng
                ctx.fillStyle = '#6c5ce7';
                ctx.beginPath(); ctx.moveTo(0, -28*s); ctx.lineTo(-7*s, -16*s); ctx.lineTo(7*s, -16*s); ctx.fill();
                ctx.strokeStyle = '#fdcb6e'; ctx.lineWidth = 3 * s;
                ctx.beginPath(); ctx.moveTo(9*s, -16*s); ctx.lineTo(9*s, 14*s); ctx.stroke();
                ctx.fillStyle = '#00cec9'; ctx.beginPath(); ctx.arc(9*s, -17*s, 4.5*s, 0, Math.PI*2); ctx.fill(); // Orb
            } else if (entity.type === 'giant') {
                // Giant: Thân to trâu bò + Chùy gỗ bọc đinh
                ctx.strokeStyle = '#2d3436'; ctx.lineWidth = 9 * s;
                ctx.beginPath(); ctx.moveTo(10*s, -20*s); ctx.lineTo(16*s, 18*s); ctx.stroke();
            } else if (entity.type === 'miner') {
                // Miner: Cuốc chim + Bao tải vàng sau lưng
                ctx.strokeStyle = '#b2bec3'; ctx.lineWidth = 2.5 * s;
                ctx.beginPath(); ctx.moveTo(7*s, -10*s); ctx.lineTo(14*s, -4*s); ctx.stroke(); // Cuốc
                if (entity.goldBag > 0) {
                    ctx.fillStyle = "#f1c40f"; ctx.beginPath(); ctx.arc(-8*s, 0, 5*s, 0, Math.PI*2); ctx.fill();
                }
            }

            // Legs (Chân bước di chuyển mượt)
            let legSwing = Math.sin(animFrame * 0.3) * 6;
            ctx.strokeStyle = "#000000"; ctx.lineWidth = 3.5 * s;
            ctx.beginPath(); ctx.moveTo(0, 8 * s); ctx.lineTo(-5 * s, 18 * s + legSwing); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(0, 8 * s); ctx.lineTo(5 * s, 18 * s - legSwing); ctx.stroke();

            // Health Bar
            ctx.fillStyle = "#000"; ctx.fillRect(-12 * s, -28 * s, 24 * s, 3.5);
            ctx.fillStyle = isEnemy ? "#e74c3c" : "#2ecc71";
            ctx.fillRect(-12 * s, -28 * s, (entity.hp / entity.maxHp) * 24 * s, 3.5);

            ctx.restore();
        }

        // --- LOOP CHÍNH ---
        function gameLoop() {
            animFrame++;
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            drawBackgroundAndStatues();

            // THỢ MỎ TẢI VÀNG VỀ TẠI 6 MỎ
            units.filter(u => u.type === 'miner').forEach((u) => {
                if (u.mineTarget) {
                    if (u.state === 'going') {
                        let dx = u.mineTarget.x - u.x;
                        let dy = u.mineTarget.y - u.y;
                        let dist = Math.hypot(dx, dy);
                        if (dist > 3) { u.x += (dx / dist) * u.speed; u.y += (dy / dist) * u.speed; }
                        else { u.state = 'mining'; }
                    } else if (u.state === 'mining') {
                        u.goldBag = 12; u.state = 'returning';
                    } else if (u.state === 'returning') {
                        let dx = 70 - u.x; let dy = 200 - u.y;
                        let dist = Math.hypot(dx, dy);
                        if (dist > 3) { u.x += (dx / dist) * u.speed; u.y += (dy / dist) * u.speed; }
                        else {
                            gold += u.goldBag || 12; u.goldBag = 0; u.state = 'going';
                            addFloatingText("+12 Gold", 70, 200, '#ffcc00');
                        }
                    }
                }
                drawOfficialStickman(u, false);
            });

            // LÍNH BỘ BINH PHE TA
            units.filter(u => u.type !== 'miner').forEach((u, uIdx) => {
                if (u.isSpinning > 0) {
                    u.isSpinning--;
                    enemies.forEach(e => {
                        if (Math.hypot(e.x - u.x, e.y - u.y) < 65) e.hp -= 4;
                    });
                }

                let targetX = u.x;
                if (currentCommand === 'ATTACK') targetX = canvas.width - 90;
                else if (currentCommand === 'DEFEND') targetX = 300;
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
                    } else if (u.x >= canvas.width - 90) {
                        enemyStatueHp -= u.dmg;
                        addFloatingText("-" + u.dmg, canvas.width - 70, 180, '#ffcc00');
                        u.attackCd = 35;
                        updateUI();
                    }
                }

                drawOfficialStickman(u, false);
                if (u.hp <= 0) units.splice(uIdx, 1);
            });

            // QUÁI VẬT PHE ĐỊCH
            enemies.forEach((e, eIdx) => {
                if (e.stunned > 0) {
                    e.stunned--;
                    drawOfficialStickman(e, true);
                    return;
                }

                let unitNear = units.find(u => Math.hypot(u.x - e.x, u.y - e.y) <= e.range);
                if (!unitNear && e.x > 80) { e.x -= e.speed; }

                if (e.attackCd > 0) e.attackCd--;
                else {
                    let target = units.find(u => Math.hypot(u.x - e.x, u.y - e.y) <= e.range);
                    if (target) {
                        target.hp -= e.dmg;
                        addFloatingText("-" + e.dmg, target.x, target.y - 15, '#e74c3c');
                        e.attackCd = 32;
                    } else if (e.x <= 80) {
                        statueHp -= e.dmg;
                        addFloatingText("-" + e.dmg, 70, 180, '#e74c3c');
                        e.attackCd = 35;
                        updateUI();
                    }
                }

                drawOfficialStickman(e, true);
                if (e.hp <= 0) { enemies.splice(eIdx, 1); gold += 25; addFloatingText("+25 Gold", e.x, e.y, '#ffcc00'); updateUI(); }
            });

            // TÊN BAY & EFFECT
            projectiles.forEach((p, pIdx) => {
                p.x += p.vx; p.y += p.vy;
                ctx.fillStyle = "#ffcc00"; ctx.fillRect(p.x, p.y, 6, 2);
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
                ctx.fillStyle = "rgba(0,0,0,0.88)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = statueHp > 0 ? "#2ecc71" : "#e74c3c";
                ctx.font = "bold 34px Arial";
                ctx.fillText(statueHp > 0 ? "🏆 ORDER EMPIRE VICTORY!" : "💀 DEFEAT!", canvas.width / 2 - 200, canvas.height / 2);
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
