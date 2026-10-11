import streamlit as st

st.set_page_config(page_title="Kingdom War 2D Defense", page_icon="🏰", layout="wide")

# CSS tinh chỉnh giao diện cho gọn gàng, đẹp mắt
st.markdown("""
    <style>
    .stApp {
        background-color: #1a1a1a;
        color: white;
    }
    iframe {
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.6);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏰 Kingdom War: 2D Defense Battle")
st.markdown("Chỉ huy đội quân, xây dựng tháp phòng thủ và tiêu diệt lũ quái vật tấn công vương quốc!")

# Mã HTML/JS trò chơi canvas trực quan hoàn chỉnh nhúng vào Streamlit
game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Kingdom War 2D</title>
    <style>
        body {
            margin: 0;
            background: #121212;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            text-align: center;
            overflow: hidden;
        }
        canvas {
            background: #2e6f40;
            border: 4px solid #4a3319;
            border-radius: 8px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
            cursor: crosshair;
            display: block;
            margin: 10px auto;
        }
        .ui-panel {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 8px;
        }
        button {
            background: #b5832a;
            color: white;
            border: 2px solid #ffcc4d;
            padding: 8px 16px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            transition: 0.2s;
        }
        button:hover {
            background: #d49a33;
            transform: scale(1.05);
        }
        .stats {
            font-size: 16px;
            font-weight: bold;
            color: #ffcc4d;
        }
    </style>
</head>
<body>

    <div class="stats">
        ❤️ Máu Thành: <span id="hpText">100</span> | 💰 Vàng: <span id="goldText">150</span> | ⚔️ Đã Diệt: <span id="killText">0</span>
    </div>

    <canvas id="gameCanvas" width="900" height="450"></canvas>

    <div class="ui-panel">
        <button onclick="spawnUnit('footman')">🛡️ Triệu Hồi Bộ Binh (50 Gold)</button>
        <button onclick="spawnUnit('archer')">🏹 Triệu Hồi Cung Thủ (70 Gold)</button>
        <button onclick="castSpell('meteor')">☄️ Mưa Thiên Thạch</button>
        <button onclick="castSpell('freeze')">❄️ Đóng Băng Kẻ Địch</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let hp = 100;
        let gold = 150;
        let kills = 0;
        let freezeTimer = 0;

        let units = [];
        let enemies = [];
        let projectiles = [];
        let particles = [];

        // Khởi tạo đợt quái vật định kỳ
        setInterval(() => {
            if (enemies.length < 8) {
                enemies.push({
                    x: canvas.width + 30,
                    y: 120 + Math.random() * 260,
                    hp: 40 + kills * 5,
                    maxHp: 40 + kills * 5,
                    speed: 0.8 + Math.random() * 0.6,
                    type: Math.random() > 0.5 ? 'goblin' : 'orc'
                });
            }
        }, 2500);

        // Thu thập vàng tự động theo thời gian
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
                    x: 180 + Math.random() * 60,
                    y: 140 + Math.random() * 220,
                    type: type,
                    attackCooldown: 0
                });
                updateUI();
            }
        }

        function castSpell(type) {
            if (type === 'meteor') {
                enemies.forEach(e => {
                    e.hp -= 50;
                    createParticles(e.x, e.y, '#ff4500', 15);
                });
            } else if (type === 'freeze') {
                freezeTimer = 180; // Đóng băng trong 3 giây
            }
        }

        function createParticles(x, y, color, count) {
            for (let i = 0; i < count; i++) {
                particles.push({
                    x: x, y: y,
                    vx: (Math.random() - 0.5) * 6,
                    vy: (Math.random() - 0.5) * 6,
                    life: 25,
                    color: color
                });
            }
        }

        // Vòng lặp game chính (Game Loop)
        function gameLoop() {
            // Xóa màn hình
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ địa hình (Đường đi & Thành trì)
            ctx.fillStyle = "#3b5323";
            ctx.fillRect(0, 100, canvas.width, 280);
            
            // Đường mòn
            ctx.fillStyle = "#8c6747";
            ctx.fillRect(0, 150, canvas.width, 180);

            // Căn cứ bên trái (Castle)
            ctx.fillStyle = "#2c3e50";
            ctx.fillRect(0, 80, 100, 320);
            ctx.fillStyle = "#34495e";
            ctx.fillRect(80, 100, 30, 280);
            ctx.fillStyle = "#e74c3c";
            ctx.fillRect(35, 120, 30, 40); // Cờ thành

            // Tháp phòng thủ tự động
            ctx.fillStyle = "#111";
            ctx.fillRect(40, 40, 40, 60);
            ctx.fillStyle = "#3498db";
            ctx.beginPath(); ctx.arc(60, 50, 12, 0, Math.PI * 2); ctx.fill();

            // Cổng quái vật bên phải (Demon Portal)
            ctx.fillStyle = "#4a154b";
            ctx.beginPath(); ctx.arc(canvas.width - 40, 240, 45, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = "#e81cff";
            ctx.beginPath(); ctx.arc(canvas.width - 40, 240, 25, 0, Math.PI * 2); ctx.fill();

            // Cập nhật và vẽ Quái vật
            enemies.forEach((enemy, index) => {
                if (freezeTimer <= 0) {
                    enemy.x -= enemy.speed;
                }

                // Quái đánh vào thành
                if (enemy.x <= 100) {
                    hp -= 10;
                    enemies.splice(index, 1);
                    updateUI();
                }

                // Vẽ quái
                ctx.fillStyle = enemy.type === 'goblin' ? '#2ecc71' : '#e74c3c';
                ctx.beginPath(); ctx.arc(enemy.x, enemy.y, 14, 0, Math.PI * 2); ctx.fill();
                
                // Thanh máu quái
                ctx.fillStyle = "#000";
                ctx.fillRect(enemy.x - 15, enemy.y - 22, 30, 5);
                ctx.fillStyle = "#2ecc71";
                ctx.fillRect(enemy.x - 15, enemy.y - 22, (enemy.hp / enemy.maxHp) * 30, 5);

                if (enemy.hp <= 0) {
                    enemies.splice(index, 1);
                    gold += 25;
                    kills++;
                    createParticles(enemy.x, enemy.y, '#f1c40f', 10);
                    updateUI();
                }
            });

            if (freezeTimer > 0) freezeTimer--;

            // Cập nhật và vẽ Lính phe ta
            units.forEach((unit) => {
                ctx.fillStyle = unit.type === 'footman' ? '#2980b9' : '#e67e22';
                ctx.fillRect(unit.x - 8, unit.y - 8, 16, 16);

                // Lính tấn công quái gần nhất
                if (unit.attackCooldown > 0) unit.attackCooldown--;
                else {
                    let target = enemies.find(e => Math.hypot(e.x - unit.x, e.y - unit.y) < 70);
                    if (target) {
                        target.hp -= unit.type === 'footman' ? 12 : 18;
                        createParticles(target.x, target.y, '#fff', 5);
                        unit.attackCooldown = 40;
                    }
                }
            });

            // Hiệu ứng hạt (Particles)
            particles.forEach((p, index) => {
                p.x += p.vx; p.y += p.vy; p.life--;
                ctx.fillStyle = p.color;
                ctx.fillRect(p.x, p.y, 3, 3);
                if (p.life <= 0) particles.splice(index, 1);
            });

            // Kiểm tra kết thúc game
            if (hp <= 0) {
                ctx.fillStyle = "rgba(0,0,0,0.85)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "red";
                ctx.font = "bold 40px Arial";
                ctx.fillText("THÀNH TRÌ ĐÃ THẤT THỦ!", canvas.width / 2 - 220, canvas.height / 2);
                return;
            }

            requestAnimationFrame(gameLoop);
        }

        gameLoop();
    </script>
</body>
</html>
"""

# Nhúng game vào Streamlit
st.components.v1.html(game_html, height=540, scrolling=False)
