import streamlit as st

st.set_page_config(page_title="Kingdom War - Ultimate Tactical RTS", page_icon="⚔️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    iframe { border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.9); }
    </style>
""", unsafe_allow_html=True)

st.title("⚔️ Kingdom War: Đế Chế Người Que & Mỏ Vàng Chiến Thuật")
st.markdown("Khai thác vàng, quản lý giới hạn dân số 100 quân, điều phối binh chủng chi tiết và chiến đấu với Cổng Quỷ!")

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Kingdom War Ultimate RTS</title>
    <style>
        body { margin: 0; background: #111; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; overflow: hidden; }
        canvas { background: linear-gradient(to bottom, #1d3d1b, #2b5728); border: 4px solid #4a3319; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.9); cursor: crosshair; display: block; margin: 5px auto; }
        .ui-panel { display: flex; justify-content: center; flex-wrap: wrap; gap: 6px; margin-top: 5px; }
        .cmd-panel { display: flex; justify-content: center; gap: 10px; margin-top: 5px; }
        button { background: #b8860b; color: white; border: 2px solid #ffd700; padding: 7px 12px; font-weight: bold; font-size: 11px; border-radius: 6px; cursor: pointer; transition: 0.2s; }
        button:hover { background: #daa520; transform: scale(1.05); }
        .cmd-btn { background: #2980b9; border-color: #5adeff; }
        .stats { font-size: 13px; font-weight: bold; color: #ffd700; margin-bottom: 2px; }
    </style>
</head>
<body>

    <div class="stats">
        🏰 Máu Thành: <span id="hpText">2000</span> | 🔮 Cổng Quỷ: <span id="portalHpText">2000</span> | 💰 Vàng: <span id="goldText">250</span> | 👥 Dân số: <span id="popText">0</span>/100 | ⚔️ Lệnh: <span id="cmdText" style="color:#2ecc71;">TẤN CÔNG</span>
    </div>

    <canvas id="gameCanvas" width="960" height="420"></canvas>

    <div class="cmd-panel">
        <button class="cmd-btn" onclick="setCommand('ATTACK')">⚔️ TẤN CÔNG</button>
        <button class="cmd-btn" onclick="setCommand('DEFEND')">🛡️ PHÒNG THỦ</button>
        <button class="cmd-btn" onclick="setCommand('RETREAT')">🚩 RÚT VỀ THÀNH (HỒI MÁU)</button>
        <button onclick="toggleAudio()">🔊 Bật/Tắt Âm Thanh</button>
    </div>

    <div class="ui-panel">
        <button onclick="spawnUnit('miner')">⛏️ Thợ Mỏ (30g - 1 Slot)</button>
        <button onclick="spawnUnit('footman')">🛡️ Kiếm Sĩ (40g - 1 Slot)</button>
        <button onclick="spawnUnit('archer')">🏹 Cung Thủ (50g - 1 Slot)</button>
        <button onclick="spawnUnit('lancer')">🗡️ Giáo Sĩ (70g - 3 Slot)</button>
        <button onclick="spawnUnit('mage')">🧙 Pháp Sư (100g - 5 Slot)</button>
        <button onclick="spawnUnit('giant')">🗿 Khổng Lồ (160g - 4 Slot)</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let castleHp = 2000, castleMaxHp = 2000;
        let portalHp = 2000, portalMaxHp = 2000;
        let gold = 250;
        let currentCommand = 'ATTACK';

        let castleEnragedTimer = 0; // 15 giây (900 frame)
        let portalEnragedTimer = 0;

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
                osc.type = type; osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                gain.gain.setValueAtTime(0.04, audioCtx.currentTime);
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

        function getCurrentPopulation() {
            let count = 0;
            units.forEach(u => {
                if (u.type === 'lancer') count += 3;
                else if (u.type === 'mage') count += 5;
                else if (u.type === 'giant') count += 4;
                else count += 1; // miner, footman, archer, summon
            });
            return count;
        }

        // Tự sinh quái từ Cổng Quỷ
        setInterval(() => {
            if (portalHp > 0 && enemies.length < 40) {
                let types = ['goblin', 'orc', 'demon_mage', 'troll'];
                let t = types[Math.floor(Math.random() * types.length)];
                enemies.push(createEnemyObject(t));
            }
        }, 1600);

        // Hồi máu 6 HP/s khi quân đứng gần thành (Lệnh Rút về) & Thợ mỏ kiếm vàng
        setInterval(() => {
            units.forEach(u => {
                if (u.type === 'miner') {
                    // Thợ mỏ đi tới mỏ vàng ở giữa (x: 450) khai thác
                    if (Math.abs(u.x - 450) > 20) {
                        u.x += u.x < 450 ? 1 : -1;
                    } else {
                        gold += 5; // Khai thác mỏ vàng
                    }
                } else if (currentCommand === 'RETREAT' && u.x < 220 && u.hp < u.maxHp) {
                    u.hp = Math.min(u.maxHp, u.hp + 6);
                    createParticles(u.x, u.y - 10, '#2ecc71', 2);
                }
            });
            gold += 10; // Thuế thành định kỳ
            updateUI();
        }, 1000);

        function updateUI() {
            document.getElementById("hpText").innerText = Math.max(0, Math.floor(castleHp));
            document.getElementById("portalHpText").innerText = Math.max(0, Math.floor(portalHp));
            document.getElementById("goldText").innerText = gold;
            document.getElementById("popText").innerText = getCurrentPopulation();
        }

        function getUnitCostAndPop(type) {
            if (type === 'miner') return { gold: 30, pop: 1 };
            if (type === 'footman') return { gold: 40, pop: 1 };
            if (type === 'archer') return { gold: 50, pop: 1 };
            if (type === 'lancer') return { gold: 70, pop: 3 };
            if (type === 'mage') return { gold: 100, pop: 5 };
            if (type === 'giant') return { gold: 160, pop: 4 };
            return { gold: 0, pop: 1 };
        }

        function createUnitObject(type) {
            let stats = {
                miner:   { hp: 60,  dmg: 5,  range: 25, speed: 1.3, size: 0.8 },
                footman: { hp: 120, dmg: 14, range: 35, speed: 1.2, size: 1 },
                archer:  { hp: 80,  dmg: 18, range: 170, speed: 1.1, size: 1 },
                lancer:  { hp: 150, dmg: 22, range: 60, speed: 1.0, size: 1.1 },
                mage:    { hp: 90,  dmg: 30, range: 150, speed: 0.9, size: 1, summonCd: 0 },
                giant:   { hp: 500, dmg: 45, range: 45, speed: 0.6, size: 1.8 }
            }[type];

            return {
                x: 130 + Math.random() * 30, y: 140 + Math.random() * 200,
                type: type, hp: stats.hp, maxHp: stats.hp,
                dmg: stats.dmg, range: stats.range, speed: stats.speed, size: stats.size,
                mana: 0, maxMana: 100, attackCd: 0, summonCd: stats.summonCd || 0
            };
        }

        function createEnemyObject(type) {
            let stats = {
                goblin:     { hp: 80,  dmg: 8,  range: 30, speed: 1.4, size: 0.9 },
                orc:        { hp: 160, dmg: 16, range: 35, speed: 1.0, size: 1.2 },
                demon_mage: { hp: 100, dmg: 24, range: 140, speed: 0.8, size: 1 },
                troll:      { hp: 400, dmg: 38, range: 45, speed: 0.5, size: 1.7 }
            }[type];

            return {
                x: canvas.width - 120 - Math.random() * 30, y: 140 + Math.random() * 200,
                type: type, hp: stats.hp, maxHp: stats.hp,
                dmg: stats.dmg, range: stats.range, speed: stats.speed, size: stats.size,
                mana: 0, maxMana: 100, attackCd: 0
            };
        }

        function spawnUnit(type) {
            let info = getUnitCostAndPop(type);
            if (gold >= info.gold && getCurrentPopulation() + info.pop <= 100) {
                gold -= info.gold;
                units.push(createUnitObject(type));
                playSound(420, 'square', 0.1);
                updateUI();
            }
        }

        function createParticles(x, y, color, count) {
            for (let i = 0; i < count; i++) {
                particles.push({
                    x: x, y: y, vx: (Math.random() - 0.5) * 6, vy: (Math.random() - 0.5) * 6,
                    life: 20, color: color
                });
            }
        }

        // --- HỌA TIẾT VẼ CHI TIẾT ---
        function drawCastle() {
            ctx.fillStyle = "#2c3e50"; ctx.fillRect(0, 50, 140, 330);
            ctx.fillStyle = "#34495e";
            for(let y = 60; y < 370; y += 25) {
                for(let x = 0; x < 130; x += 30) { ctx.fillRect(x + (y%50==0?10:0), y, 26, 20); }
            }
            ctx.fillStyle = "#1a252f";
            ctx.beginPath(); ctx.arc(70, 290, 30, Math.PI, 0, false); ctx.fill();
            ctx.fillRect(40, 290, 60, 90);
            ctx.fillStyle = "#e74c3c";
            ctx.fillRect(20, 20, 25, 30); ctx.fillRect(95, 20, 25, 30);

            if (castleEnragedTimer > 0) {
                ctx.strokeStyle = "rgba(0, 210, 255, 0.9)"; ctx.lineWidth = 4;
                ctx.strokeRect(2, 52, 136, 326);
            }
        }

        function drawGoldMine() {
            // Vẽ Mỏ Vàng & Thợ Mỏ ở giữa sân
            ctx.fillStyle = "#b5832a";
            ctx.beginPath(); ctx.arc(480, 230, 45, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "#ffd700";
            ctx.beginPath(); ctx.arc(480, 230, 25, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "#fff"; ctx.font = "bold 12px Arial";
            ctx.fillText("💰 MỎ VÀNG", 440, 225);
        }

        function drawDemonPortal() {
            let cx = canvas.width - 70, cy = 230;
            ctx.fillStyle = "#4a154b"; ctx.beginPath(); ctx.arc(cx, cy, 60, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = "#e81cff"; ctx.beginPath(); ctx.arc(cx, cy, 30, 0, Math.PI*2); ctx.fill();

            if (portalEnragedTimer > 0) {
                ctx.strokeStyle = "rgba(231, 76, 60, 0.9)"; ctx.lineWidth = 4;
                ctx.beginPath(); ctx.arc(cx, cy, 65, 0, Math.PI*2); ctx.stroke();
            }
        }

        // Vẽ Nhân vật chi tiết theo đúng trang bị (Kiếm, Giáo khiên, Cung, Gậy phép, Chùy khổng lồ)
        function drawCustomCharacter(entity, isEnemy) {
            let x = entity.x, y = entity.y, s = entity.size;
            let color = isEnemy ? '#e74c3c' : '#3498db';
            if (entity.type === 'giant' || entity.type === 'troll') color = isEnemy ? '#8e44ad' : '#f39c12';
            if (entity.type === 'mage' || entity.type === 'demon_mage') color = isEnemy ? '#e67e22' : '#9b59b6';
            if (entity.type === 'miner') color = '#e67e22';

            ctx.save();
            ctx.translate(x, y);

            // Đầu & Nón
            ctx.fillStyle = color; ctx.beginPath(); ctx.arc(0, -12 * s, 8 * s, 0, Math.PI * 2); ctx.fill();
            if (entity.type === 'lancer' || entity.type === 'footman') {
                ctx.fillStyle = '#bdc3c7'; ctx.fillRect(-7*s, -18*s, 14*s, 5*s); // Nón sắt
            }
            if (entity.type === 'mage') {
                ctx.fillStyle = '#8e44ad'; ctx.beginPath(); ctx.moveTo(0, -25*s); ctx.lineTo(-8*s, -14*s); ctx.lineTo(8*s, -14*s); ctx.fill(); // Nón phép
            }

            // Thân & Trang bị vũ khí sau lưng/tay
            ctx.strokeStyle = color; ctx.lineWidth = 3 * s;
            ctx.beginPath(); ctx.moveTo(0, -4 * s); ctx.lineTo(0, 10 * s); ctx.stroke();

            if (entity.type === 'archer') {
                // Bao cung & Cung phía sau
                ctx.strokeStyle = '#d4af37'; ctx.beginPath(); ctx.arc(6*s, -4*s, 8*s, 0, Math.PI); ctx.stroke();
            } else if (entity.type === 'lancer') {
                // Giáo dài và khiên
                ctx.strokeStyle = '#fff'; ctx.beginPath(); ctx.moveTo(8*s, -15*s); ctx.lineTo(15*s, 15*s); ctx.stroke();
                ctx.fillStyle = '#2980b9'; ctx.fillRect(-12*s, -8*s, 6*s, 14*s); // Khiên
            } else if (entity.type === 'mage') {
                // Gậy phép phát sáng
                ctx.strokeStyle = '#e74c3c'; ctx.beginPath(); ctx.moveTo(10*s, -15*s); ctx.lineTo(10*s, 15*s); ctx.stroke();
                ctx.fillStyle = '#00d2ff'; ctx.beginPath(); ctx.arc(10*s, -16*s, 4*s, 0, Math.PI*2); ctx.fill();
            } else if (entity.type === 'giant') {
                // Gậy/Chùy to
                ctx.strokeStyle = '#5a3d28'; ctx.lineWidth = 6*s;
                ctx.beginPath(); ctx.moveTo(12*s, -20*s); ctx.lineTo(18*s, 20*s); ctx.stroke();
            } else if (entity.type === 'miner') {
                // Cúp đào vàng
                ctx.strokeStyle = '#bdc3c7'; ctx.beginPath(); ctx.moveTo(8*s, -10*s); ctx.lineTo(15*s, -5*s); ctx.stroke();
            } else {
                // Kiếm sĩ cầm kiếm
                ctx.strokeStyle = '#bdc3c7'; ctx.beginPath(); ctx.moveTo(8*s, -5*s); ctx.lineTo(14*s, 10*s); ctx.stroke();
            }

            // Chân di chuyển
            let swing = Math.sin(animFrame * 0.2) * 6;
            ctx.strokeStyle = color; ctx.lineWidth = 3 * s;
            ctx.beginPath(); ctx.moveTo(0, 10 * s); ctx.lineTo(-6 * s, 20 * s + swing); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(0, 10 * s); ctx.lineTo(6 * s, 20 * s - swing); ctx.stroke();

            // Thanh Máu & Mana
            ctx.fillStyle = "#000"; ctx.fillRect(-15 * s, -30 * s, 30 * s, 4);
            ctx.fillStyle = "#2ecc71"; ctx.fillRect(-15 * s, -30 * s, (entity.hp / entity.maxHp) * 30 * s, 4);
            ctx.fillStyle = "#000"; ctx.fillRect(-15 * s, -25 * s, 30 * s, 3);
            ctx.fillStyle = "#00d2ff"; ctx.fillRect(-15 * s, -25 * s, (entity.mana / entity.maxMana) * 30 * s, 3);

            ctx.restore();
        }

        // --- VÒNG LẶP CHÍNH ---
        function gameLoop() {
            animFrame++;
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = "#63472d"; ctx.fillRect(0, 110, canvas.width, 250);

            drawCastle();
            drawGoldMine();
            drawDemonPortal();

            // Đếm ngược hiệu ứng phẫn nộ 15 giây (900 frames)
            if (castleEnragedTimer > 0) castleEnragedTimer--;
            if (portalEnragedTimer > 0) portalEnragedTimer--;

            // KÍCH HOẠT PHẪN NỘ KHI <50% MÁU (GIẢM 99% SÁT THƯƠNG TRONG 15 GIÂY & TRIỆU HỒI LÍNH/QUÁI)
            if (castleHp / castleMaxHp < 0.5 && castleEnragedTimer === 0) {
                castleEnragedTimer = 900; // 15 giây
                for(let i = 0; i < 30; i++) {
                    let types = ['footman', 'archer', 'lancer'];
                    units.push(createUnitObject(types[i % 3]));
                }
                createParticles(100, 200, '#00d2ff', 40);
            }

            if (portalHp / portalMaxHp < 0.5 && portalEnragedTimer === 0) {
                portalEnragedTimer = 900; // 15 giây
                for(let i = 0; i < 40; i++) {
                    let types = ['goblin', 'orc', 'demon_mage'];
                    enemies.push(createEnemyObject(types[i % 3]));
                }
                createParticles(canvas.width - 100, 200, '#e74c3c', 40);
            }

            // XỬ LÝ QUÂN TA
            units.forEach((u, uIdx) => {
                if (u.type === 'miner') return; // Thợ mỏ tự khai thác vàng

                let targetX = u.x;
                if (currentCommand === 'ATTACK') targetX = canvas.width - 130;
                else if (currentCommand === 'DEFEND') targetX = 320;
                else if (currentCommand === 'RETREAT') targetX = 180;

                let enemyNear = enemies.find(e => Math.hypot(e.x - u.x, e.y - u.y) <= u.range);
                if (!enemyNear && Math.abs(u.x - targetX) > 10) {
                    u.x += u.x < targetX ? u.speed : -u.speed;
                }

                // Pháp sư triệu hồi lính yếu hỗ trợ
                if (u.type === 'mage') {
                    u.summonCd = (u.summonCd || 0) + 1;
                    if (u.summonCd >= 250 && getCurrentPopulation() < 98) {
                        u.summonCd = 0;
                        units.push({
                            x: u.x + 10, y: u.y + (Math.random()*30 - 15),
                            type: 'footman', hp: 50, maxHp: 50, dmg: 8, range: 30, speed: 1.3, size: 0.7,
                            mana: 0, maxMana: 100, attackCd: 0
                        });
                        createParticles(u.x, u.y, '#9b59b6', 10);
                    }
                }

                if (u.attackCd > 0) u.attackCd--;
                else {
                    let target = enemies.find(e => Math.hypot(e.x - u.x, e.y - u.y) <= u.range);
                    if (target) {
                        target.hp -= u.dmg;
                        u.mana = Math.min(u.maxMana, u.mana + 25);
                        createParticles(target.x, target.y, '#fff', 4);
                        u.attackCd = 30;
                    } else if (u.x >= canvas.width - 140) {
                        let dmg = (portalEnragedTimer > 0) ? u.dmg * 0.01 : u.dmg; // Giảm 99% dame trong 15s
                        portalHp -= dmg;
                        u.mana = Math.min(u.maxMana, u.mana + 15);
                        u.attackCd = 35;
                        updateUI();
                    }
                }

                if (u.mana >= u.maxMana) {
                    u.mana = 0; u.hp = Math.min(u.maxHp, u.hp + 60);
                    enemies.forEach(e => { if (Math.hypot(e.x - u.x, e.y - u.y) < 130) e.hp -= 50; });
                    createParticles(u.x, u.y, '#00d2ff', 25);
                }

                drawCustomCharacter(u, false);
                if (u.hp <= 0) units.splice(uIdx, 1);
            });

            // XỬ LÝ QUÁI VẬT
            enemies.forEach((e, eIdx) => {
                let unitNear = units.find(u => Math.hypot(u.x - e.x, u.y - e.y) <= e.range);
                if (!unitNear && e.x > 140) { e.x -= e.speed; }

                if (e.attackCd > 0) e.attackCd--;
                else {
                    let target = units.find(u => Math.hypot(u.x - e.x, u.y - e.y) <= e.range);
                    if (target) {
                        target.hp -= e.dmg;
                        e.mana = Math.min(e.maxMana, e.mana + 20);
                        createParticles(target.x, target.y, '#e74c3c', 4);
                        e.attackCd = 32;
                    } else if (e.x <= 140) {
                        let dmg = (castleEnragedTimer > 0) ? e.dmg * 0.01 : e.dmg; // Giảm 99% dame trong 15s
                        castleHp -= dmg;
                        e.mana = Math.min(e.maxMana, e.mana + 15);
                        e.attackCd = 35;
                        updateUI();
                    }
                }

                drawCustomCharacter(e, true);
                if (e.hp <= 0) { enemies.splice(eIdx, 1); gold += 22; updateUI(); }
            });

            particles.forEach((p, idx) => {
                p.x += p.vx; p.y += p.vy; p.life--;
                ctx.fillStyle = p.color; ctx.fillRect(p.x, p.y, 3, 3);
                if (p.life <= 0) particles.splice(idx, 1);
            });

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

st.components.v1.html(game_html, height=550, scrolling=False)
