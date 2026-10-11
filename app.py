import streamlit as st

st.set_page_config(page_title="Kingdom War - Boss Edition", page_icon="👑", layout="wide")

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

st.title("👑 Kingdom War: Đại Chiến Người Que & Boss Ác Quỷ")
st.markdown("Xây dựng quân đoàn người que, phòng thủ tòa thành và chiến đấu với Boss khổng lồ!")

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Kingdom War Boss Edition</title>
    <style>
        body {
            margin: 0;
            background: #151515;
            color: white;
            font-family: 'Segoe UI', Tahoma, sans-serif;
            text-align: center;
            overflow: hidden;
        }
        canvas {
            background: linear-gradient(to bottom, #1e3f20, #2c5e2a);
            border: 4px solid #5a3d28;
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
            background: #b8860b;
            color: white;
            border: 2px solid #ffd700;
            padding: 9px 16px;
            font-weight: bold;
            font-size: 13px;
            border-radius: 6px;
            cursor: pointer;
            transition: 0.2s;
        }
        button:hover {
            background: #daa520;
            transform: scale(1.06);
        }
        .stats {
            font-size: 15px;
            font-weight: bold;
            color: #ffd700;
            margin-bottom: 4px;
        }
    </style>
</head>
<body>

    <div class="stats">
        🏰 Máu Thành: <span id="hpText">100</span> | 💰 Vàng: <span id="goldText">160</span> | ⚔️ Đã Diệt: <span id="killText">0</span> | 👹 Trạng Thái Boss: <span id="bossStatus" style="color: #2ecc71;">Bình thường</span>
    </div>

    <canvas id="gameCanvas" width="920" height="420"></canvas>

    <div class="ui-panel">
        <button onclick="toggleAudio()">🔊 Bật/Tắt Âm Thanh</button>
        <button onclick="spawnUnit('footman')">🛡️ Lính Kiếm (50 Gold)</button>
        <button onclick="spawnUnit('archer')">🏹 Lính Cung (70 Gold)</button>
        <button onclick="castSpell('meteor')">☄️ Mưa Thiên Thạch</button>
        <button onclick="castSpell('freeze')">❄️ Đóng Băng</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let hp = 100;
        let gold = 160;
        let kills = 0;
        let freezeTimer = 0;
        let audioEnabled = false;
        let bossSpawned = false;

        let units = [];
        let enemies = [];
        let particles = [];
        let animFrame = 0;

        let audioCtx = null;
        let bgmInterval = null;

        function toggleAudio() {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            audioEnabled = !audioEnabled;
            if (audioEnabled) startBGM(); else stopBGM();
        }

        function playSound(freq, type, duration) {
            if (!audioEnabled || !audioCtx) return;
            try {
                let osc = audioCtx.createOscillator();
                let gain = audioCtx.createGain();
                osc.type = type;
                osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + duration);
            } catch(e) {}
        }

        function startBGM() {
            if (bgmInterval) return;
            const notes = [200, 230, 260, 290, 320];
            bgmInterval = setInterval(() => {
                if (!audioEnabled) return;
                let note = notes[Math.floor(Math.random() * notes.length)];
                playSound(note, 'triangle', 0.25);
            }, 450);
        }

        function stopBGM() {
            if (bgmInterval) { clearInterval(bgmInterval); bgmInterval = null; }
        }

        // Sinh quái định kỳ (hoặc Boss nếu đủ điểm)
        setInterval(() => {
            if (bossSpawned) return;

            // Cứ mỗi 10 mạng sẽ xuất hiện Boss Ác Quỷ khổng lồ
            if (kills > 0 && kills % 10 === 0 && !enemies.some(e => e.isBoss)) {
                bossSpawned = true;
                document.getElementById("bossStatus").innerText = "⚠️ BOSS ĐANG TẤN CÔNG!";
                document.getElementById("bossStatus").style.color = "#e74c3c";
                enemies.push({
                    x: canvas.width + 50,
                    y: 200,
                    hp: 300,
                    maxHp: 300,
                    speed: 0.4,
                    type: 'boss',
                    isBoss: true
                });
                playSound(100, 'sawtooth', 1.0);
                return;
            }

            if (enemies.length < 8) {
                enemies.push({
                    x: canvas.width + 30,
                    y: 110 + Math.random() * 250,
                    hp: 40 + kills * 3,
                    maxHp: 40 + kills * 3,
                    speed: 0.7 + Math.random() * 0.5,
                    type: Math.random() > 0.4 ? 'goblin' : 'orc',
                    isBoss: false
                });
            }
        }, 2000);

        setInterval(() => {
            gold += 15;
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
                    x: 190 + Math.random() * 40,
                    y: 130 + Math.random() * 230,
                    type: type,
                    attackCooldown: 0
                });
                playSound(450, 'square', 0.12);
                updateUI();
            }
        }

        function castSpell(type) {
            if (type === 'meteor') {
                enemies.forEach(e => {
                    e.hp -= e.isBoss ? 50 : 70;
                    createParticles(e.x, e.y, '#ff4500', 16);
                });
                playSound(130, 'sawtooth', 0.5);
            } else if (type === 'freeze') {
                freezeTimer = 180;
                playSound(750, 'sine', 0.4);
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

        // Vẽ Tòa thành hoành tráng bên trái
        function drawCastle() {
            // Thân tường thành chính
            ctx.fillStyle = "#3e4a59";
            ctx.fillRect(0, 50, 110, 330);

            // Các khối gạch tường thành
            ctx.fillStyle = "#2c3e50";
            for(let i = 60; i < 370; i += 30) {
                ctx.fillRect(10, i, 40, 20);
                ctx.fillRect(60, i + 15, 40, 20);
            }

            // Tháp canh phía trên
            ctx.fillRect(15, 20, 35, 45);
            ctx.fillRect(65, 20, 35, 45);

            // Cổng thành lớn
            ctx.fillStyle = "#1a252f";
            ctx.beginPath();
            ctx.arc(65, 300, 25, Math.PI, 0, false);
            ctx.fill();
            ctx.fillRect(40, 300, 50, 80);

            // Cờ vương quốc trên đỉnh tháp
            ctx.fillStyle = "#e74c3c";
            ctx.fillRect(30, 0, 15, 20);
            ctx.fillRect(80, 0, 15, 20);
        }

        function drawStickman(x, y, color, isArcher, isMoving) {
            ctx.strokeStyle = color;
            ctx.lineWidth = 2.5;
            let legSwing = isMoving ? Math.sin(animFrame * 0.3) * 8 : 0;

            // Đầu
            ctx.beginPath(); ctx.arc(x, y - 14, 6, 0, Math.PI * 2); ctx.stroke();
            // Thân
            ctx.beginPath(); ctx.moveTo(x, y - 8); ctx.lineTo(x, y + 6); ctx.stroke();
            // Tay vũ khí
            ctx.beginPath(); ctx.moveTo(x, y - 4);
            if (isArcher) {
                ctx.lineTo(x + 10, y - 6); ctx.stroke();
                ctx.strokeStyle = '#d4af37';
                ctx.beginPath(); ctx.arc(x + 10, y - 6, 8, -Math.PI/2, Math.PI/2); ctx.stroke();
            } else {
                ctx.lineTo(x + 10, y + 2); ctx.stroke();
            }
            // Chân
            ctx.strokeStyle = color;
            ctx.beginPath();
            ctx.moveTo(x, y + 6); ctx.lineTo(x - 6, y + 18 + legSwing);
            ctx.moveTo(x, y + 6); ctx.lineTo(x + 6, y + 18 - legSwing);
            ctx.stroke();
        }

        function drawMonster(enemy) {
            let x = enemy.x, y = enemy.y;
            let hpRatio = enemy.hp / enemy.maxHp;

            if (enemy.isBoss) {
                // Vẽ BOSS ÁC QUỶ KHỔNG LỒ
                ctx.fillStyle = "#8b0000";
                ctx.strokeStyle = "#ff4500";
                ctx.lineWidth = 3;
                ctx.beginPath(); ctx.arc(x, y - 10, 26, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

                // Sừng Boss
                ctx.fillStyle = "#ffcc00";
                ctx.beginPath();
                ctx.moveTo(x - 15, y - 25); ctx.lineTo(x - 28, y - 45); ctx.lineTo(x - 8, y - 30);
                ctx.moveTo(x + 15, y - 25); ctx.lineTo(x + 28, y - 45); ctx.lineTo(x + 8, y - 30);
                ctx.fill();

                // Thanh máu Boss (to hơn)
                ctx.fillStyle = "#000";
                ctx.fillRect(x - 35, y - 55, 70, 7);
                ctx.fillStyle = "#e74c3c";
                ctx.fillRect(x - 35, y - 55, hpRatio * 70, 7);
            } else {
                // Quái thường (Goblin / Orc)
                ctx.fillStyle = enemy.type === 'goblin' ? '#2ecc71' : '#e67e22';
                ctx.strokeStyle = '#111';
                ctx.lineWidth = 2;
                ctx.beginPath(); ctx.arc(x, y - 6, 12, 0, Math.PI * 2); ctx.fill(); ctx.stroke();

                // Thanh máu thường
                ctx.fillStyle = "#000";
                ctx.fillRect(x - 16, y - 28, 32, 5);
                ctx.fillStyle = "#2ecc71";
                ctx.fillRect(x - 16, y - 28, hpRatio * 32, 5);
            }
        }

        function gameLoop() {
            animFrame++;
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Đường đi chiến trường
            ctx.fillStyle = "#7a5230";
            ctx.fillRect(0, 100, canvas.width, 260);

            // Vẽ Tòa Thành Cố Thủ
            drawCastle();

            // Cổng ác quỷ xuất hiện bên phải
            ctx.fillStyle = "#4a154b";
            ctx.beginPath(); ctx.arc(canvas.width - 35, 230, 45, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = "#9b59b6";
            ctx.beginPath(); ctx.arc(canvas.width - 35, 230, 25, 0, Math.PI * 2); ctx.fill();

            // Cập nhật & vẽ Quái vật & Boss
            enemies.forEach((enemy, index) => {
                if (freezeTimer <= 0) {
                    enemy.x -= enemy.speed;
                }

                // Quái / Boss đánh vào thành
                if (enemy.x <= 110) {
                    hp -= enemy.isBoss ? 40 : 10;
                    if (enemy.isBoss) {
                        bossSpawned = false;
                        document.getElementById("bossStatus").innerText = "Bình thường";
                        document.getElementById("bossStatus").style.color = "#2ecc71";
                    }
                    enemies.splice(index, 1);
                    playSound(90, 'sawtooth', 0.5);
                    updateUI();
                }

                drawMonster(enemy);

                if (enemy.hp <= 0) {
                    if (enemy.isBoss) {
                        bossSpawned = false;
                        gold += 150;
                        kills += 5;
                        document.getElementById("bossStatus").innerText = "Đã hạ Boss!";
                        document.getElementById("bossStatus").style.color = "#f1c40f";
                    } else {
                        gold += 25;
                        kills++;
                    }
                    enemies.splice(index, 1);
                    createParticles(enemy.x, enemy.y, '#f1c40f', enemy.isBoss ? 30 : 10);
                    playSound(550, 'sine', 0.2);
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
                    let target = enemies.find(e => Math.hyp
