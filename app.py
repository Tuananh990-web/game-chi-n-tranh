<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Game Chiến Tranh - Bắn Pháo</title>
    <style>
        body { margin: 0; background: #111; color: white; text-align: center; font-family: sans-serif; }
        canvas { background: #222; border: 2px solid #555; display: block; margin: 20px auto; }
    </style>
</head>
<body>
    <h1>Chiến Tranh Phòng Thủ Pháo Đài</h1>
    <p>Bấm chuột vào khu vực game để bắn đại bác diệt địch!</p>
    <canvas id="gameCanvas" width="800" height="400"></canvas>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        let score = 0;
        let enemies = [];
        let bullets = [];

        // Tạo kẻ địch
        function spawnEnemy() {
            enemies.push({ x: canvas.width, y: Math.random() * (canvas.height - 40) + 20, speed: 2, size: 20 });
        }
        setInterval(spawnEnemy, 1500);

        // Bắt sự kiện click chuột để bắn
        canvas.addEventListener('click', (e) => {
            const rect = canvas.getBoundingClientRect();
            const clickX = e.clientX - rect.left;
            const clickY = e.clientY - rect.top;
            bullets.push({ x: 30, y: canvas.height / 2, targetX: clickX, targetY: clickY, speed: 7 });
        });

        // Vòng lặp cập nhật và vẽ game
        function update() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ pháo đài (Người chơi)
            ctx.fillStyle = '#4CAF50';
            ctx.fillRect(10, canvas.height / 2 - 25, 30, 50);

            // Cập nhật đạn
            bullets.forEach((b, i) => {
                const angle = Math.atan2(b.targetY - b.y, b.targetX - b.x);
                b.x += Math.cos(angle) * b.speed;
                b.y += Math.sin(angle) * b.speed;
                
                ctx.fillStyle = '#FFD700';
                ctx.beginPath();
                ctx.arc(b.x, b.y, 5, 0, Math.PI * 2);
                ctx.fill();

                if (b.x > canvas.width || b.y > canvas.height || b.x < 0 || b.y < 0) bullets.splice(i, 1);
            });

            // Cập nhật kẻ địch
            enemies.forEach((e, ei) => {
                e.x -= e.speed;
                ctx.fillStyle = '#FF5252';
                ctx.fillRect(e.x, e.y, e.size, e.size);

                // Va chạm đạn với địch
                bullets.forEach((b, bi) => {
                    if (b.x > e.x && b.x < e.x + e.size && b.y > e.y && b.y < e.y + e.size) {
                        enemies.splice(ei, 1);
                        bullets.splice(bi, 1);
                        score += 10;
                    }
                });
            });

            // Điểm số
            ctx.fillStyle = '#FFF';
            ctx.font = '18px Arial';
            ctx.fillText(`Điểm: ${score}`, 20, 30);

            requestAnimationFrame(update);
        }

        update();
    </script>
</body>
</html>
