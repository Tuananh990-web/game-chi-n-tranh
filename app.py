import streamlit as st

st.set_page_config(page_title="Kingdom War - Ultimate RTS Edition", page_icon="⚔️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    iframe { border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.9); }
    </style>
""", unsafe_allow_html=True)

st.title("⚔️ Kingdom War: Đại Chiến Vương Quốc (RTS & Mana System)")
st.markdown("Chỉ huy quân đoàn Loài Người, điều phối chiến thuật và đại chiến với Cổng Quỷ!")

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Kingdom War RTS</title>
    <style>
        body { margin: 0; background: #111; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; overflow: hidden; }
        canvas { background: linear-gradient(to bottom, #1d3d1b, #2b5728); border: 4px solid #4a3319; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.9); cursor: crosshair; display: block; margin: 5px auto; }
        .ui-panel { display: flex; justify-content: center; flex-wrap: wrap; gap: 8px; margin-top: 5px; }
        .cmd-panel { display: flex; justify-content: center; gap: 10px; margin-top: 5px; }
        button { background: #b8860b; color: white; border: 2px solid #ffd700; padding: 7px 12px; font-weight: bold; font-size: 12px; border-radius: 6px; cursor: pointer; transition: 0.2s; }
        button:hover { background: #daa520; transform: scale(1.05); }
        .cmd-btn { background: #2980b9; border-color: #5adeff; }
        .cmd-btn:hover { background: #3498db; }
        .stats { font-size: 14px; font-weight: bold; color: #ffd700; margin-bottom: 2px; }
    </style>
</head>
<body>

    <div class="stats">
        🏰 Máu Thành: <span id="hpText">2000</span> | 🔮 Cổng Quỷ: <span id="portalHpText">2000</span> | 💰 Vàng: <span id="goldText">300</span> | ⚔️ Lệnh: <span id="cmdText" style="color:#2ecc71;">TẤN CÔNG</span>
    </div>

    <canvas id="gameCanvas" width="960" height="420"></canvas>

    <div class="cmd-panel">
        <button class="cmd-btn" onclick="setCommand('ATTACK')">⚔️ LỆNH: TẤN CÔNG</button>
        <button class="cmd-btn" onclick="setCommand('DEFEND')">🛡️ LỆNH: PHÒNG THỦ</button>
        <button class="cmd-btn" onclick="setCommand('RETREAT')">🚩 LỆNH: RÚT VỀ THÀNH (HỒI MÁU)</button>
        <button onclick="toggleAudio()">🔊 Bật/Tắt Âm Thanh</button>
    </div>

    <div class="ui-panel">
        <button onclick="spawnUnit('footman')">🛡️ Bộ Binh (40g)</button>
        <button onclick="spawnUnit('archer')">🏹 Cung Thủ (60g)</button>
        <button onclick="spawnUnit('lancer')">🗡️ Cầm Giáo (70g)</button>
        <button onclick="spawnUnit('mage')">🧙 Pháp Sư (100g)</button>
        <button onclick="spawnUnit('giant')">🗿 Khổng Lồ (180g)</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let castleHp = 2000, castleMaxHp = 2000;
        let portalHp = 2000, portalMaxHp = 2000;
        let gold = 300;
        let currentCommand = 'ATTACK'; // ATTACK, DEFEND, RETREAT

        let castleEnraged = false;
        let portalEnraged = false;

        let units = [];
        let enemies = [];
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
                osc.type = type;
                osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                gain.gain.setValueAtTime(0.05, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.start(); osc.stop(audioCtx.currentTime + duration);
            } catch(e) {}
        }

        function setCommand(cmd) {
            currentCommand = cmd;
            let txt = cmd === 'ATTACK' ? 'TẤN CÔNG' : (cmd === 'DEFEND' ? 'PHÒNG THỦ' : 'RÚT VỀ THÀNH');
            document.getElementById("cmdText").innerText = txt;
        }

        // Tự sinh quái định kỳ từ Cổng Quỷ
        setInterval(() => {
            if (portalHp > 0 && enemies.length < 35) {
                let types = ['goblin', 'orc', 'demon_mage', 'troll'];
                let t = types[Math.floor(Math.random() * types.length)];
                enemies.push(createEnemyObject(t));
            }
        }, 1800);

        // Hồi máu 6 HP/s khi quân đứng gần thành (Lệnh Rút về)
        setInterval(() => {
            if (currentCommand === 'RETREAT') {
                units.forEach(u => {
                    if (u.x < 220 && u.hp < u.maxHp) {
                        u.hp = Math.min(u.maxHp, u.hp + 6);
                        createParticles(u.x, u.y - 10, '#2ecc71', 2);
                    }
                });
            }
            gold += 12;
            updateUI();
        }, 1000);

        function updateUI() {
            document.getElementById("hpText").innerText = Math.max(0, Math.floor(castleHp));
            document.getElementById("portalHpText").innerText = Math.max(0, Math.floor(portalHp));
            document.getElementById("goldText").innerText = gold;
        }

        function createUnitObject(type) {
            let stats = {
                footman: { hp: 120, dmg: 12, range: 35, speed: 1.2, size: 1 },
                archer:  { hp: 80,  dmg: 16, range: 180, speed: 1.1, size: 1 },
                lancer:  { hp: 140, dmg: 18, range: 55, speed: 1.0, size: 1.1 },
                mage:    { hp: 90,  dmg: 28, range: 150, speed: 0.9, size: 1 },
                giant:   { hp: 450, dmg: 40, range: 45, speed: 0.6, size: 1.8 }
            }[type];

            return {
                x: 130 + Math.random() * 30,
                y: 140 + Math.random() * 200,
                type: type,
                hp: stats.hp, maxHp: stats.hp,
                dmg: stats.dmg, range: stats.range, speed: stats.speed, size: stats.size,
                mana: 0, maxMana: 100,
                attackCd: 0
            };
        }

        function createEnemyObject(type) {
            let stats = {
                goblin:     { hp: 80,  dmg: 8,  range: 30, speed: 1.4, size: 0.9 },
                orc:        { hp: 160, dmg: 16, range: 35, speed: 1.0, size: 1.2 },
                demon_mage: { hp: 100, dmg: 22, range: 140, speed: 0.8, size: 1 },
                troll:      { hp: 380, dmg: 35, range: 45, speed: 0.5, size: 1.7 }
            }[type];

            return {
                x: canvas.width - 120 - Math.random() * 30,
                y: 140 + Math.random() * 200,
                type: type,
                hp: stats.hp, maxHp: stats.hp,
                dmg: stats.dmg, range: stats.range, speed: stats.speed, size: stats.size,
                mana: 0, maxMana: 100,
                attackCd: 0
            };
        }

        function spawnUnit(type) {
            let costs = { footman: 40, archer: 60, lancer: 70, mage: 100, giant: 180 };
            if (gold >= costs[type]) {
                gold -= costs[type];
                units.push(createUnitObject(type));
                playSound(400, 'square', 0.1);
                updateUI();
            }
        }

        function createParticles(x, y, color, count) {
            for (let i = 0; i < count; i++) {
                particles.push({
                    x: x, y: y,
                    vx: (Math.random() - 0.5) * 6, vy: (Math.random() - 0.5) * 6,
                    life: 20, color: color
                });
            }
        }

        // --- VẼ ĐỒ HỌA CHI TIẾT ---
        function drawDetailedCastle() {
            // Nền móng đá
            ctx.fillStyle = "#2c3e50";
            ctx.fillRect(0, 50, 140, 330);

            // Tường gạch hoa văn
            ctx.fillStyle = "#34495e";
            for(let y = 60; y < 370; y += 25) {
                for(let x = 0; x < 130; x += 30) {
                    ctx.fillRect(x + (y%50==0?10:0), y, 26, 20);
                }
            }

            // Mái vòm & Cổng sắt
            ctx.fillStyle = "#1a252f";
            ctx.beginPath(); ctx.arc(70, 290, 30, Math.PI, 0, false); ctx.fill();
            ctx.fillRect(40, 290, 60, 90);

            // Tháp canh & Cờ rồng
            ctx.fillStyle = "#e74c3c";
            ctx.fillRect(20, 20, 25, 30); ctx.fillRect(95, 20, 25, 30);
            ctx.fillStyle = "#f1c40f";
            ctx.beginPath(); ctx.arc(32, 10, 6, 0, Math.PI*2); ctx.fill();

            // Hiệu ứng phẫn nộ (<50% Máu)
            if (castleHp / castleMaxHp < 0.5) {
                ctx.strokeStyle = "rgba(52, 152, 219, 0.8)";
                ctx.lineWidth = 4;
                ctx.strokeRect(2, 52, 136, 326);
            }
        }

        function drawDemonPortal() {
            let cx = canvas.width - 70, cy = 230;
            // Vòng xoáy ma thuật
            let grad = ctx.createRadialGradient(cx, cy, 10, cx, cy, 60);
            grad.addColorStop(0, "#e81cff");
            grad.addColorStop(0.5, "#4a154b");
            grad.addColorStop(1, "#11001c");

            ctx.fillStyle = grad;
            ctx.beginPath(); ctx.arc(cx, cy, 60, 0, Math.PI * 2); ctx.fill();

            // Đá cổ tự xung quanh
            ctx.fillStyle = "#2a0845";
            for(let a = 0; a < Math.PI*2; a += Math.PI/3) {
                let px = cx + Math.cos(a + animFrame*0.02) * 50;
                let py = cy + Math.sin(a + animFrame*0.02) * 50;
                ctx.fillRect(px - 6, py - 6, 12, 12);
            }

            // Hiệu ứng phẫn nộ (<50% Máu)
            if (portalHp / portalMaxHp < 0.5) {
                ctx.strokeStyle = "rgba(231, 76, 60, 0.8)";
                ctx.lineWidth = 4;
                ctx.beginPath(); ctx.arc(cx, cy, 65, 0, Math.PI*2); ctx.stroke();
            }
        }

        function drawCharacter(entity, isEnemy) {
            let x = entity.x, y = entity.y, s = entity.size;
            let color = isEnemy ? '#e74c3c' : '#3498db';
            if (entity.type === 'giant' || entity.type === 'troll') color = isEnemy ? '#8e44ad' : '#f39c12';
            if (entity.type === 'mage' || entity.type === 'demon_mage') color = isEnemy ? '#e67e22' : '#9b59b6';

            ctx.save();
            ctx.translate(x, y);

            // Thân
            ctx.fillStyle = color;
            ctx.beginPath(); ctx.arc(0, -12 * s, 8 * s, 0, Math.PI * 2); ctx.fill();
            ctx.strokeStyle = color; ctx.lineWidth = 3 * s;
            ctx.beginPath(); ctx.moveTo(0, -4 * s); ctx.lineTo(0, 10 * s); ctx.stroke();

            // Chân
            let swing = Math.sin(animFrame * 0.2) * 6;
            ctx.beginPath(); ctx.moveTo(0, 10 * s); ctx.lineTo(-6 * s, 20 * s + swing); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(0, 10 * s); ctx.lineTo(6 * s, 20 * s - swing); ctx.stroke();

            // Thanh Máu
            ctx.fillStyle = "#000"; ctx.fillRect(-15 * s, -28 * s, 30 * s, 4);
            ctx.fillStyle = "#2ecc71"; ctx.fillRect(-15 * s, -28 * s, (entity.hp / entity.maxHp) * 30 * s, 4);

            // Thanh MANA (Xanh dương)
            ctx.fillStyle = "#000"; ctx.fillRect(-15 * s, -23 * s, 30 * s, 3);
            ctx.fillStyle = "#00d2ff"; ctx.fillRect(-15 * s, -23 * s, (entity.mana / entity.maxMana) * 30 * s, 3);

            ctx.restore();
        }

        // --- VÒNG LẶP XỬ LÝ CHÍNH ---
        function gameLoop() {
            animFrame++;
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Chiến trường
            ctx.fillStyle = "#63472d"; ctx.fillRect(0, 110, canvas.width, 250);

            drawDetailedCastle();
            drawDemonPortal();

            // KIỂM TRA PHẪN NỘ (<50% MÁU & GIẢM 99% SÁT THƯƠNG)
            if (castleHp / castleMaxHp < 0.5 && !castleEnraged) {
                castleEnraged = true;
                for(let i = 0; i < 30; i++) {
                    let types = ['footman', 'archer', 'lancer'];
                    units.push(createUnitObject(types[i % 3]));
                }
                createParticles(100, 200, '#00d2ff', 50);
                playSound(200, 'sawtooth', 0.8);
            }

            if (portalHp / portalMaxHp < 0.5 && !portalEnraged) {
                portalEnraged = true;
                for(let i = 0; i < 40; i++) {
                    let types = ['goblin', 'orc', 'demon_mage'];
                    enemies.push(createEnemyObject(types[i % 3]));
                }
                createParticles(canvas.width - 100, 200, '#e74c3c', 50);
                playSound(150, 'sawtooth', 0.8);
            }

            // XỬ LÝ QUÂN PHE TA
            units.forEach((u, uIdx) => {
                let targetX = u.x;
                if (currentCommand === 'ATTACK') targetX = canvas.width - 130;
                else if (currentCommand === 'DEFEND') targetX = 300;
                else if (currentCommand === 'RETREAT') targetX = 180;

                // Tự di chuyển
                let enemyNear = enemies.find(e => Math.hypot(e.x - u.x, e.y - u.y) <= u.range);
                if (!enemyNear && Math.abs(u.x - targetX) > 10) {
                    u.x += u.x < targetX ? u.speed : -u.speed;
                }

                // Tấn công
                if (u.attackCd > 0) u.attackCd--;
                else {
                    let target = enemies.find(e => Math.hypot(e.x - u.x, e.y - u.y) <= u.range);
                    if (target) {
                        let dmg = u.dmg;
                        target.hp -= dmg;
                        u.mana = Math.min(u.maxMana, u.mana + 25); // Tích Mana
                        createParticles(target.x, target.y, '#fff', 4);
                        u.attackCd = 30;
                    } else if (u.x >= canvas.width - 140) {
                        // Tấn công Cổng Quỷ
                        let dmg = portalEnraged ? u.dmg * 0.01 : u.dmg; // Giảm 99% dame khi phẫn nộ
                        portalHp -= dmg;
                        u.mana = Math.min(u.maxMana, u.mana + 15);
                        u.attackCd = 35;
                        updateUI();
                    }
                }

                // KÍCH HOẠT FULL MANA
                if (u.mana >= u.maxMana) {
                    u.mana = 0;
                    u.hp = Math.min(u.maxHp, u.hp + 50); // Hồi 50 HP
                    enemies.forEach(e => {
                        if (Math.hypot(e.x - u.x, e.y - u.y) < 120) e.hp -= 45; // Tuyệt chiêu diện rộng
                    });
                    createParticles(u.x, u.y, '#00d2ff', 25);
                    playSound(600, 'sine', 0.3);
                }

                drawCharacter(u, false);

                if (u.hp <= 0) units.splice(uIdx, 1);
            });

            // XỬ LÝ QUÁI VẬT
            enemies.forEach((e, eIdx) => {
                let unitNear = units.find(u => Math.hypot(u.x - e.x, u.y - e.y) <= e.range);
                if (!unitNear && e.x > 140) {
                    e.x -= e.speed;
                }

                if (e.attackCd > 0) e.attackCd--;
                else {
                    let target = units.find(u => Math.hypot(u.x - e.x, u.y - e.y) <= e.range);
                    if (target) {
                        target.hp -= e.dmg;
                        e.mana = Math.min(e.maxMana, e.mana + 20);
                        createParticles(target.x, target.y, '#e74c3c', 4);
                        e.attackCd = 32;
                    } else if (e.x <= 140) {
                        // Tấn công Tòa Thành
                        let dmg = castleEnraged ? e.dmg * 0.01 : e.dmg; // Giảm 99% dame khi phẫn nộ
                        castleHp -= dmg;
                        e.mana = Math.min(e.maxMana, e.mana + 15);
                        e.attackCd = 35;
                        updateUI();
                    }
                }

                // Full Mana Quái
                if (e.mana >= e.maxMana) {
                    e.mana = 0;
                    units.forEach(u => {
                        if (Math.hypot(u.x - e.x, u.y - e.y) < 100) u.hp -= 35;
                    });
                    createParticles(e.x, e.y, '#e74c3c', 20);
                }

                drawCharacter(e, true);

                if (e.hp <= 0) {
                    enemies.splice(eIdx, 1);
                    gold += 20;
                    updateUI();
                }
            });

            // Hiệu ứng Hạt
            particles.forEach((p, idx) => {
                p.x += p.vx; p.y += p.vy; p.life--;
                ctx.fillStyle = p.color; ctx.fillRect(p.x, p.y, 3, 3);
                if (p.life <= 0) particles.splice(idx, 1);
            });

            // Kết thúc Game
            if (castleHp <= 0 || portalHp <= 0) {
                ctx.fillStyle = "rgba(0,0,0,0.85)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = castleHp > 0 ? "#2ecc71" : "#e74c3c";
                ctx.font = "bold 36px Arial";
                ctx.fillText(castleHp > 0 ? "🏆 VƯƠNG QUỐC CHIẾN THẮNG!" : "💀 TÒA THÀNH ĐÃ THẤT THỦ!", canvas.width / 2 - 220, canvas.height / 2);
                return;
            }

            requestAnimationFrame(gameLoop);
        }

        gameLoop();
    </script>
</body>
</html>
"""

st.components.v1.html(game_html, height=540, scrolling=False)
