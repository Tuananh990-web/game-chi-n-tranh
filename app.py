import streamlit as st

st.set_page_config(page_title="Kingdom War - Stickman Edition", page_icon="⚔️", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: white;
    }
    iframe {
        border-radius: 14px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚔️ Kingdom War: Người Que Đại Chiến & Âm Thanh Sống Động")
st.markdown("Triệu hồi người que thủ thành, tiêu diệt quái vật và thưởng thức âm thanh chiến trận hoành tráng!")

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Stickman Kingdom War</title>
    <style>
        body {
            margin: 0;
            background: #1a1a1a;
            color: white;
            font-family: 'Segoe UI', Tahoma, sans-serif;
            text-align: center;
            overflow: hidden;
        }
        canvas {
            background: linear-gradient(to bottom, #2d5a27, #3b7a30);
            border: 4px solid #4a3319;
            border-radius: 10px;
            box-shadow: 0 12px 35px rgba(0,0,0,0.9);
            cursor: crosshair;
            display: block;
            margin: 8px auto;
        }
        .ui-panel {
            display: flex;
            justify-content: center;
            gap: 12px;
            margin-top: 6px;
        }
        button {
            background: #c28827;
            color: white;
            border: 2px solid #ffde6b;
            padding: 9px 16px;
            font-weight: bold;
            font-size: 13px;
            border-radius: 6px;
            cursor: pointer;
            transition: 0.2s;
        }
        button:hover {
            background: #e6a738;
            transform: scale(1.06);
        }
        .stats {
            font-size: 15px;
            font-weight: bold;
            color: #ffde6b;
            margin-bottom: 4px;
        }
    </style>
</head>
<body>

    <div class="stats">
        ❤️ Máu Thành: <span id="hpText">100</span> | 💰 Vàng: <span id="goldText">150</span> | ⚔️ Đã Diệt: <span id="killText">0</span> | 🎵 Âm thanh: <span id="soundStatus" style="color: #2ecc71;">Bật</span>
    </div>

    <canvas id="gameCanvas" width="920" height="420"></canvas>

    <div class="ui-panel">
        <button onclick="toggleAudio()">🔊 Bật/Tắt Nhạc & Âm Thanh</button>
        <button onclick="spawnUnit('footman')">🛡️ Lính Người Que Kiếm (50 Gold)</button>
        <button onclick="spawnUnit('archer')">🏹 Lính Người Que Cung (70 Gold)</button>
        <button onclick="castSpell('meteor')">☄️ Mưa Thiên Thạch</button>
        <button onclick="castSpell('freeze')">❄️ Đóng Băng Quái</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let hp = 100;
        let gold = 150;
        let kills = 0;
        let freezeTimer = 0;
        let audioEnabled = false;

        let units = [];
        let enemies = [];
        let particles = [];
        let animFrame = 0;

        // --- WEB AUDIO API (Tạo nhạc nền & âm thanh chém/bắn không cần file ngoài) ---
        let audioCtx = null;
        let bgmInterval = null;

        function toggleAudio() {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            audioEnabled = !audioEnabled;
            document.getElementById("soundStatus").innerText = audioEnabled ? "Bật" : "Tắt";
            document.getElementById("soundStatus").style.color = audioEnabled ? "#2ecc71" : "#e74c3c";

            if (audioEnabled) {
                startBGM();
            } else {
                stopBGM();
            }
        }

        function playSound(freq, type, duration) {
            if (!audioEnabled || !audioCtx) return;
            try {
                let osc = audioCtx.createOscillator();
                let gain = audioCtx.createGain();
                osc.type = type;
                osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + duration);
            } catch(e) {}
        }

        function startBGM() {
            if (bgmInterval) return;
            // Nhạc nền chiến trận dạng chùm nốt nhạc giao hưởng giả lập
            const notes = [220, 247, 261, 293, 329, 349, 392];
            bgmInterval = setInterval(() => {
                if (!audioEnabled) return;
                let note = notes[Math.floor(Math.random() * notes.length)];
                playSound(note, 'triangle', 0.3);
            }, 400);
        }

        function stopBGM() {
            if (bgmInterval) {
                clearInterval(bgmInterval);
                bgmInterval = null;
            }
        }

        // --- HỆ THỐNG GAME SINH TỰ ĐỘNG ---
        setInterval(() => {
            if (enemies.length < 9) {
                enemies.push({
                    x: canvas.width + 30,
                    y: 110 + Math.random() * 250,
                    hp: 45 + kills * 4,
                    maxHp: 45 + kills * 4,
                    speed: 0.7 + Math.random() * 0.5,
                    type: Math.random() > 0.4 ? 'goblin' : 'orc'
                });
            }
        }, 2200);

        setInterval(() => {
            gold += 18;
            updateUI();
        }, 2000);

        function updateUI() {
            document.getElementById("hpText").innerText = Math.max(0, hp);
            document.getElementById("goldText").innerText = gold;
            document.getElementById("killText").innerText = kills;
        }

        function spawnUnit(type) {
            let cost = type === 'footman' ? 50 : 70;
            if (gold >= cost) {
                gold -= cost;
                units.push({
                    x: 180 + Math.random() * 50,
                    y: 130 + Math.random() * 230,
                    type: type,
                    attackCooldown: 0
                });
                playSound(500, 'square', 0.15);
                updateUI();
            }
        }

        function castSpell(type) {
            if (type === 'meteor') {
                enemies.forEach(e => {
                    e.hp -= 60;
                    createParticles(e.x, e.y, '#ff4500', 18);
                });
                playSound(150, 'sawtooth', 0.6);
            } else if (type === 'freeze') {
                freezeTimer = 200;
                playSound(800, 'sine', 0.5);
            }
        }

        function createParticles(x, y, color, count) {
            for (let i = 0; i < count; i++) {
                particles.push({
                    x: x, y: y,
                    vx: (Math.random() - 0.5) * 7,
                    vy: (Math.random() - 0.5) * 7,
                    life: 25,
                    color: color
                });
            }
        }

        // --- VẼ ĐỒ HỌA NGƯỜI QUE HOẠT HỌA ---
        function drawStickman(x, y, color, isArcher, isMoving) {
            ctx.strokeStyle = color;
            ctx.lineWidth = 2.5;
            ctx.fillStyle = color;

            let legSwing = isMoving ? Math.sin(animFrame * 0.3) * 8 : 0;

            // Đầu
            ctx.beginPath();
            ctx.arc(x, y - 14, 6, 0, Math.PI * 2);
            ctx.stroke();

            // Thân
            ctx.beginPath();
            ctx.moveTo(x, y - 8);
            ctx.lineTo(x, y + 6);
            ctx.stroke();

            // Tay cầm vũ khí
            ctx.beginPath();
            ctx.moveTo(x, y - 4);
            if (isArcher) {
                ctx.lineTo(x + 10, y - 6); // Cung
                ctx.stroke();
                ctx.strokeStyle = '#d4af37';
                ctx.beginPath(); ctx.arc(x + 10, y - 6, 8, -Math.PI/2, Math.PI/2); ctx.stroke();
            } else {
                ctx.lineTo(x + 10, y + 2); // Kiếm
                ctx.stroke();
            }

            // Chân bước đi
            ctx.strokeStyle = color;
            ctx.beginPath();
            ctx.moveTo(x, y + 6);
            ctx.lineTo(x - 6, y + 18 + legSwing);
            ctx.moveTo(x, y + 6);
            ctx.lineTo(x + 6, y + 18 - legSwing);
            ctx.stroke();
        }

        function drawMonster(x, y, type, hpRatio) {
            ctx.fillStyle = type === 'goblin' ? '#2ecc71' : '#e74c3c';
            ctx.strokeStyle = '#111';
            ctx.lineWidth = 2;

            // Thân quái to ngang người que
            ctx.beginPath();
            ctx.arc(x, y - 6, 11, 0, Math.PI * 2);
            ctx.fill(); ctx.stroke();

            // Sừng / Tai ác quỷ
            if (type === 'orc') {
                ctx.fillStyle = '#c0392b';
                ctx.beginPath();
                ctx.moveTo(x - 8, y - 14); ctx.lineTo(x - 14, y - 22); ctx.lineTo(x - 4, y - 16);
                ctx.moveTo(x + 8, y - 14); ctx.lineTo(x + 14, y - 22); ctx.lineTo(x + 4, y - 16);
                ctx.fill();
            }

            // Thanh máu quái
            ctx.fillStyle = "#000";
            ctx.fillRect(x - 16, y - 28, 32, 5);
            ctx.fillStyle = "#2ecc71";
            ctx.fillRect(x - 16, y - 28, hpRatio * 32, 5);
        }

        // --- VÒNG LẶP CHÍNH ---
        function gameLoop() {
            animFrame++;
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ Đường mòn & Thành trì
            ctx.fillStyle = "#8a623f";
            ctx.fillRect(0, 100, canvas.width, 260);

            // Căn cứ bên trái (Castle Tower)
            ctx.fillStyle = "#34495e";
            ctx.fillRect(0, 60, 95, 340);
            ctx.fillStyle = "#2c3e50";
            ctx.fillRect(75, 80, 25, 300);
            // Cờ thành
            ctx.fillStyle = "#e74c3c";
            ctx.fillRect(30, 90, 30, 25);

            // Cổng ác quỷ bên phải
            ctx.fillStyle = "#4a154b";
            ctx.beginPath(); ctx.arc(canvas.width - 35, 230, 42, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = "#e81cff";
            ctx.beginPath(); ctx.arc(canvas.width - 35, 230, 22, 0, Math.PI * 2); ctx.fill();

            // Cập nhật & vẽ Quái vật
            enemies.forEach((enemy, index) => {
                if (freezeTimer <= 0) {
                    enemy.x -= enemy.speed;
                }

                if (enemy.x <= 95) {
                    hp -= 12;
                    enemies.splice(index, 1);
                    playSound(100, 'sawtooth', 0.4);
                    updateUI();
                }

                drawMonster(enemy.x, enemy.y, enemy.type, enemy.hp / enemy.maxHp);

                if (enemy.hp <= 0) {
                    enemies.splice(index, 1);
                    gold += 30;
                    kills++;
                    createParticles(enemy.x, enemy.y, '#f1c40f', 12);
                    playSound(600, 'sine', 0.2);
                    updateUI();
                }
            });

            if (freezeTimer > 0) freezeTimer--;

            // Cập nhật & vẽ Lính người que phe ta
            units.forEach((unit) => {
                let isMoving = true;
                if (unit.attackCooldown > 0) {
                    unit.attackCooldown--;
                    isMoving = false;
                } else {
                    let target = enemies.find(e => Math.hypot(e.x - unit.x, e.y - unit.y) < 75);
                    if (target) {
                        target.hp -= unit.type === 'footman' ? 14 : 20;
                        createParticles(target.x, target.y, '#ffffff', 6);
                        playSound(350, 'square', 0.1);
                        unit.attackCooldown = 35;
                        isMoving = false;
                    }
                }

                let color = unit.type === 'footman' ? '#3498db' : '#f39c12';
                drawStickman(unit.x, unit.y, color, unit.type === 'archer', isMoving);
            });

            // Hiệu ứng hạt
            particles.forEach((p, index) => {
                p.x += p.vx; p.y += p.vy; p.life--;
                ctx.fillStyle = p.color;
                ctx.fillRect(p.x, p.y, 3, 3);
                if (p.life <= 0) particles.splice(index, 1);
            });

            // Màn hình kết thúc
            if (hp <= 0) {
                stopBGM();
                ctx.fillStyle = "rgba(0,0,0,0.85)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "red";
                ctx.font = "bold 38px Arial";
                ctx.fillText("THÀNH TRÌ ĐÃ THẤT THỦ!", canvas.width / 2 - 210, canvas.height / 2);
                return;
            }

            requestAnimationFrame(gameLoop);
        }

        gameLoop();
    </script>
</body>
</html>
"""

st.components.v1.html(game_html, height=520, scrolling=False)
