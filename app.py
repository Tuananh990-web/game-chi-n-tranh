<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stick War Mini Prototype</title>
    <style>
        body {
            margin: 0;
            background-color: #1a1a1a;
            color: white;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            overflow: hidden;
        }
        #game-container {
            position: relative;
            width: 800px;
            height: 450px;
            background: linear-gradient(to bottom, #d47a3e 0%, #f4c27a 60%, #8c5830 100%);
            border: 4px solid #4a2e18;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            overflow: hidden;
        }
        /* HUD Top Bar */
        .hud {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 50px;
            background: rgba(0, 0, 0, 0.6);
            display: flex;
            align-items: center;
            justify-content: space-around;
            z-index: 10;
            border-bottom: 2px solid #b58900;
        }
        .btn-spawn {
            background: #b58900;
            color: #fff;
            border: 2px solid #ffcc00;
            padding: 5px 10px;
            cursor: pointer;
            font-weight: bold;
            border-radius: 4px;
            font-size: 12px;
        }
        .btn-spawn:hover {
            background: #d4a017;
        }
        .stats {
            font-size: 14px;
            font-weight: bold;
            color: #ffcc00;
        }
        /* Canvas game */
        canvas {
            display: block;
            background: transparent;
        }
    </style>
</head>
<body>

    <h2>Stick War 2 Style - Trò chơi mô phỏng</h2>
    <div id="game-container">
        <div class="hud">
            <div class="stats">Vàng: <span id="gold-count">100</span></div>
            <button class="btn-spawn" onclick="spawnUnit('miner')">Thợ Mỏ (50 🟡)</button>
            <button class="btn-spawn" onclick="spawnUnit('sword')">Lính Kiếm (100 🟡)</button>
            <button class="btn-spawn" onclick="spawnUnit('archidon')">Cung Thủ (120 🟡)</button>
        </div>
        <canvas id="gameCanvas" width="800" height="400"></canvas>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let gold = 100;
        let units = [];

        function updateGoldDisplay() {
            document.getElementById("gold-count").textContent = gold;
        }

        function spawnUnit(type) {
            let cost = type === 'miner' ? 50 : type === 'sword' ? 100 : 120;
            if (gold >= cost) {
                gold -= cost;
                updateGoldDisplay();
                units.push({
                    type: type,
                    x: type === 'miner' ? 100 : 50,
                    y: 320,
                    speed: type === 'miner' ? 1 : 1.5,
                    direction: 1
                });
            }
        }

        // Tự động tăng vàng theo thời gian từ thợ mỏ
        setInterval(() => {
            let miners = units.filter(u => u.type === 'miner').length;
            gold += 5 + (miners * 5);
            updateGoldDisplay();
        }, 2000);

        function gameLoop() {
            // Xóa màn hình
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ bối cảnh (Mặt đất & Mặt trời)
            ctx.fillStyle = "#ffcc00";
            ctx.beginPath();
            ctx.arc(650, 120, 50, 0, Math.PI * 2);
            ctx.fill();

            // Đất
            ctx.fillStyle = "#6e4726";
            ctx.fillRect(0, 350, canvas.width, 50);
            ctx.fillStyle = "#4a2e18";
            ctx.fillRect(0, 355, canvas.width, 5);

            // Tượng vàng bên phải
            ctx.fillStyle = "#ffd700";
            ctx.fillRect(720, 250, 40, 100);
            ctx.fillStyle = "#b8860b";
            ctx.font = "12px Arial";
            ctx.fillText("TƯỢNG", 722, 240);

            // Vẽ nhân vật người que
            units.forEach(unit => {
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 3;

                // Thân người que
                ctx.beginPath();
                ctx.arc(unit.x, unit.y - 15, 8, 0, Math.PI * 2); // Đầu đen tròn đặc
                ctx.fillStyle = "#000";
                ctx.fill();
                ctx.stroke();

                // Thân
                ctx.beginPath();
                ctx.moveTo(unit.x, unit.y - 7);
                ctx.lineTo(unit.x, unit.y + 15);
                ctx.stroke();

                // Chân & Tay
                ctx.beginPath();
                ctx.moveTo(unit.x, unit.y + 15);
                ctx.lineTo(unit.x - 6, unit.y + 30);
                ctx.moveTo(unit.x, unit.y + 15);
                ctx.lineTo(unit.x + 6, unit.y + 30);
                ctx.stroke();

                // Phân loại trang bị vũ khí
                if (unit.type === 'sword') {
                    ctx.strokeStyle = "#silver";
                    ctx.beginPath();
                    ctx.moveTo(unit.x + 5, unit.y);
                    ctx.lineTo(unit.x + 18, unit.y - 5);
                    ctx.stroke();
                } else if (unit.type === 'archidon') {
                    ctx.strokeStyle = "#8b4513";
                    ctx.beginPath();
                    ctx.arc(unit.x + 8, unit.y, 10, -Math.PI/2, Math.PI/2);
                    ctx.stroke();
                }

                // Di chuyển nhân vật đơn giản
                if (unit.x < 700) {
                    unit.x += unit.speed;
                }
            });

            requestAnimationFrame(gameLoop);
        }

        gameLoop();
    </script>
</body>
</html>
