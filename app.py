import streamlit as st

st.set_page_config(
    page_title="Stick War 2: Order Empire - Massive Engine",
    page_icon="⚔️",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #020408; color: #ffffff; font-family: 'Segoe UI', Tahoma, sans-serif; }
    iframe { border-radius: 12px; box-shadow: 0 15px 50px rgba(0,0,0,0.98); }
    .title-text { text-align: center; color: #ffcc00; text-transform: uppercase; font-weight: 900; letter-spacing: 2px; }
    .sub-text { text-align: center; color: #888888; font-size: 13px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-text'>⚔️ STICK WAR 2: ORDER EMPIRE - ULTIMATE MASTERPIECE ⚔️</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Massive RTS Architecture: Object-Oriented Entities, Particle Physics, Tactical AI & Flash 2D Art System</p>", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Stick War 2 Massive Engine</title>
    <style>
        body { margin: 0; background: #020408; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; overflow: hidden; }
        canvas { background: linear-gradient(to bottom, #5cb85c 0%, #4cae4c 70%, #398439 100%); border: 4px solid #2e6b2e; border-radius: 10px; box-shadow: 0 15px 40px rgba(0,0,0,0.95); display: block; margin: 4px auto; }
        .ui-panel { display: flex; justify-content: center; flex-wrap: wrap; gap: 5px; margin-top: 4px; }
        .cmd-panel { display: flex; justify-content: center; gap: 6px; margin-top: 4px; }
        button { background: #795548; color: #fff; border: 2px solid #ffcc00; padding: 6px 11px; font-weight: bold; font-size: 11px; border-radius: 4px; cursor: pointer; transition: 0.2s; text-transform: uppercase; }
        button:hover { background: #8d6e63; transform: scale(1.05); }
        .cmd-btn { background: #01579b; border-color: #4fc3f7; }
        .skill-btn { background: #4a148c; border-color: #ffb74d; }
        .tech-btn { background: #1b5e20; border-color: #81c784; }
        .stats { font-size: 13px; font-weight: bold; color: #ffcc00; margin-bottom: 3px; }
    </style>
</head>
<body>

    <div class="stats">
        🏰 ORDER HP: <span id="hpText">3000</span> | 👹 EMPIRE HP: <span id="enemyHpText">3000</span> | 💰 GOLD: <span id="goldText">450</span> | 👥 POP: <span id="popText">0</span>/100 | 💎 TECH: <span id="techText">1</span>
    </div>

    <canvas id="gameCanvas" width="980" height="400"></canvas>

    <div class="cmd-panel">
        <button class="cmd-btn" onclick="GameManager.setCommand('ATTACK')">⚔️ TẤN CÔNG</button>
        <button class="cmd-btn" onclick="GameManager.setCommand('DEFEND')">🛡️ PHÒNG THỦ</button>
        <button class="cmd-btn" onclick="GameManager.setCommand('HOLD')">🛑 GIỮ VỊ TRÍ</button>
        <button class="tech-btn" onclick="GameManager.upgradeTech()">⬆️ NÂNG CẤP (150G)</button>
        <button class="skill-btn" onclick="GameManager.triggerSkill('spin')">🌀 BÃO KIẾM</button>
        <button class="skill-btn" onclick="GameManager.triggerSkill('earthquake')">💥 ĐỘNG ĐẤT</button>
    </div>

    <div class="ui-panel">
        <button onclick="GameManager.spawnUnit('miner')">⛏️ Miner (30g)</button>
        <button onclick="GameManager.spawnUnit('swordwrath')">⚔️ Swordwrath (40g)</button>
        <button onclick="GameManager.spawnUnit('archidon')">🏹 Archidon (50g)</button>
        <button onclick="GameManager.spawnUnit('spearton')">🛡️ Spearton (70g)</button>
        <button onclick="GameManager.spawnUnit('magikill')">🧙 Magikill (100g)</button>
        <button onclick="GameManager.spawnUnit('giant')">🗿 Giant (160g)</button>
    </div>

    <script>
        class ParticleSystem {
            constructor() { this.particles = []; }
            emit(x, y, color, count = 15) {
                for (let i = 0; i < count; i++) {
                    this.particles.push({
                        x, y, vx: (Math.random() - 0.5) * 6, vy: (Math.random() - 0.5) * 6,
                        radius: Math.random() * 3 + 1, color, alpha: 1.0, decay: Math.random() * 0.03 + 0.02
                    });
                }
            }
            updateAndDraw(ctx) {
                this.particles.forEach((p, idx) => {
                    p.x += p.vx; p.y += p.vy; p.alpha -= p.decay;
                    ctx.fillStyle = p.color; ctx.globalAlpha = Math.max(0, p.alpha);
                    ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2); ctx.fill();
                    ctx.globalAlpha = 1.0;
                    if (p.alpha <= 0) this.particles.splice(idx, 1);
                });
            }
        }

        class GameObject {
            constructor(x, y, type, isEnemy, stats) {
                this.x = x; this.y = y; this.type = type; this.isEnemy = isEnemy;
                this.hp = stats.hp; this.maxHp = stats.hp; this.dmg = stats.dmg;
                this.range = stats.range; this.speed = stats.speed; this.size = stats.size;
                this.attackCd = 0; this.state = 'going'; this.goldBag = 0;
                this.isSpinning = 0; this.mineTarget = null;
            }
            draw(ctx, animFrame) {
                ctx.save();
                ctx.translate(this.x, this.y);
                if (this.isSpinning > 0) ctx.rotate((50 - this.isSpinning) * 0.5);

                let color = this.isEnemy ? '#e74c3c' : '#3498db';
                if (this.type === 'miner') color = '#f39c12';
                if (this.type === 'spearton') color = '#2980b9';
                if (this.type === 'giant' || this.type === 'troll') color = '#6d4c41';

                // Đầu đen tròn hoàn toàn chuẩn phong cách Flash Stick War
                ctx.fillStyle = "#000"; ctx.beginPath(); ctx.arc(0, -14 * this.size, 6 * this.size, 0, Math.PI * 2); ctx.fill();
                if (this.type === 'spearton') {
                    ctx.fillStyle = "#c0392b"; ctx.fillRect(-7 * this.size, -23 * this.size, 14 * this.size, 5 * this.size);
                }

                ctx.strokeStyle = color; ctx.lineWidth = 3.5 * this.size;
                ctx.beginPath(); ctx.moveTo(0, -8 * this.size); ctx.lineTo(0, 8 * this.size); ctx.stroke();
                let swing = Math.sin(animFrame * 0.3) * 5;
                ctx.beginPath(); ctx.moveTo(0, 8 * this.size); ctx.lineTo(-5 * this.size, 18 * this.size + swing); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(0, 8 * this.size); ctx.lineTo(5 * this.size, 18 * this.size - swing); ctx.stroke();

                ctx.fillStyle = "#000"; ctx.fillRect(-12 * this.size, -28 * this.size, 24 * this.size, 3.5);
                ctx.fillStyle = this.isEnemy ? "#e74c3c" : "#2ecc71";
                ctx.fillRect(-12 * this.size, -28 * this.size, (this.hp / this.maxHp) * 24 * this.size, 3.5);
                ctx.restore();
            }
        }

        class RTSGameManager {
            constructor() {
                this.canvas = document.getElementById("gameCanvas");
                this.ctx = this.canvas.getContext("2d");
                this.statueHp = 3000; this.enemyStatueHp = 3000;
                this.gold = 450; this.techLevel = 1; this.currentCommand = 'ATTACK';
                this.gameOver = false; this.showBriefing = true; this.screenShake = 0;
                this.animFrame = 0;
                this.particles = new ParticleSystem();
                this.goldMines = [
                    { x: 150, y: 140, miner: null }, { x: 200, y: 200, miner: null }, { x: 250, y: 270, miner: null },
                    { x: 170, y: 320, miner: null }, { x: 220, y: 120, miner: null }, { x: 270, y: 180, miner: null }
                ];
                this.units = []; this.enemies = []; this.floatingTexts = [];
                this.initListeners();
            }
            initListeners() {
                this.canvas.addEventListener('click', (e) => {
                    if (this.showBriefing) {
                        const rect = this.canvas.getBoundingClientRect();
                        const mouseX = e.clientX - rect.left; const mouseY = e.clientY - rect.top;
                        if (mouseX >= this.canvas.width / 2 - 55 && mouseX <= this.canvas.width / 2 + 55 && mouseY >= 270 && mouseY <= 315) {
                            this.showBriefing = false;
                        }
                    }
                });
            }
            setCommand(cmd) { this.currentCommand = cmd; }
            addFloatingText(text, x, y, color = '#ffcc00') {
                this.floatingTexts.push({ text, x, y, alpha: 1.0, color });
            }
            getCurrentPopulation() {
                let count = 0;
                this.units.forEach(u => {
                    if (u.type === 'spearton') count += 3;
                    else if (u.type === 'magikill') count += 5;
                    else if (u.type === 'giant') count += 4;
                    else count += 1;
                });
                return count;
            }
            upgradeTech() {
                if (this.showBriefing || this.gameOver) return;
                if (this.gold >= 150 && this.techLevel < 3) {
                    this.gold -= 150; this.techLevel++;
                    document.getElementById("techText").innerText = this.techLevel;
                    this.units.forEach(u => { u.dmg = Math.floor(u.dmg * 1.25); u.maxHp = Math.floor(u.maxHp * 1.2); u.hp = u.maxHp; });
                    this.particles.emit(this.canvas.width / 2, 200, '#81c784', 30);
                    this.addFloatingText("⬆️ CÔNG NGHỆ ĐÃ NÂNG CẤP!", this.canvas.width / 2, 100, '#81c784');
                    this.updateUI();
                }
            }
            triggerSkill(type) {
                if (this.showBriefing || this.gameOver) return;
                if (type === 'spin') {
                    this.units.filter(u => u.type === 'swordwrath').forEach(u => {
                        u.isSpinning = 50;
                        this.particles.emit(u.x, u.y, '#4fc3f7', 20);
                        this.addFloatingText("Bão Kiếm!", u.x, u.y - 25, '#4fc3f7');
                    });
                } else if (type === 'earthquake') {
                    this.screenShake = 30;
                    this.particles.emit(this.canvas.width / 2, this.canvas.height / 2, '#ffb74d', 50);
                    this.enemies.forEach(e => {
                        e.hp -= (90 * this.techLevel);
                        this.particles.emit(e.x, e.y, '#e53935', 10);
                        this.addFloatingText("-" + (90 * this.techLevel) + " Động Đất", e.x, e.y, '#e53935');
                    });
                }
            }
            spawnUnit(type) {
                if (this.showBriefing || this.gameOver) return;
                let costs = { miner: 30, swordwrath: 40, archidon: 50, spearton: 70, magikill: 100, giant: 160 };
                let pops = { miner: 1, swordwrath: 1, archidon: 1, spearton: 3, magikill: 5, giant: 4 };
                let stats = {
                    miner: { hp: 100, dmg: 8, range: 30, speed: 1.5, size: 0.95 },
                    swordwrath: { hp: 170, dmg: 22, range: 35, speed: 1.35, size: 1.0 },
                    archidon: { hp: 120, dmg: 28, range: 190, speed: 1.15, size: 1.0 },
                    spearton: { hp: 260, dmg: 34, range: 60, speed: 0.95, size: 1.2 },
                    magikill: { hp: 130, dmg: 45, range: 170, speed: 0.85, size: 1.05 },
                    giant: { hp: 800, dmg: 75, range: 55, speed: 0.55, size: 1.95 }
                }[type];

                if (this.gold >= costs[type] && this.getCurrentPopulation() + pops[type] <= 100) {
                    this.gold -= costs[type];
                    let unit = new GameObject(80, 140 + Math.random() * 200, type, false, {
                        hp: stats.hp * this.techLevel, dmg: stats.dmg * this.techLevel,
                        range: stats.range, speed: stats.speed, size: stats.size
                    });
                    if (type === 'miner') {
                        let freeMine = this.goldMines.find(m => !m.miner);
                        if (freeMine) { freeMine.miner = unit; unit.mineTarget = freeMine; }
                        else { unit.mineTarget = this.goldMines[0]; }
                    }
                    this.units.push(unit);
                    this.particles.emit(unit.x, unit.y, '#4fc3f7', 10);
                    this.updateUI();
                }
            }
            updateUI() {
                document.getElementById("hpText").innerText = Math.max(0, Math.floor(this.statueHp));
                document.getElementById("enemyHpText").innerText = Math.max(0, Math.floor(this.enemyStatueHp));
                document.getElementById("goldText").innerText = this.gold;
                document.getElementById("popText").innerText = this.getCurrentPopulation();
            }
            drawScene() {
                this.ctx.fillStyle = "#5cb85c"; this.ctx.fillRect(0, 100, this.canvas.width, 300);
                this.ctx.fillStyle = "#4cae4c"; this.ctx.fillRect(0, 100, this.canvas.width, 6);

                // Tượng Order
                this.ctx.fillStyle = "#d4af37"; this.ctx.fillRect(15, 60, 45, 260);
                this.ctx.fillStyle = "#f1c40f"; this.ctx.beginPath(); this.ctx.arc(37, 55, 18, 0, Math.PI * 2); this.ctx.fill();

                // 6 Mỏ vàng nhỏ
                this.goldMines.forEach((m, idx) => {
                    this.ctx.fillStyle = "#f1c40f";
                    this.ctx.beginPath(); this.ctx.arc(m.x, m.y, 14, 0, Math.PI * 2); this.ctx.fill();
                    this.ctx.strokeStyle = "#fff"; this.ctx.lineWidth = 1.5; this.ctx.stroke();
                    this.ctx.fillStyle = "#000"; this.ctx.font = "bold 9px 'Segoe UI'";
                    this.ctx.fillText("M" + (idx + 1), m.x - 5, m.y + 3);
                });

                // Tượng Empire
                this.ctx.fillStyle = "#78281f"; this.ctx.fillRect(this.canvas.width - 60, 60, 45, 260);
                this.ctx.fillStyle = "#922b21"; this.ctx.beginPath(); this.ctx.arc(this.canvas.width - 37, 55, 18, 0, Math.PI * 2); this.ctx.fill();
            }
            drawBriefingScroll() {
                this.ctx.fillStyle = "rgba(0, 0, 0, 0.85)"; this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
                this.ctx.fillStyle = "#f5f5dc"; this.ctx.fillRect(140, 50, this.canvas.width - 280, 300);
                this.ctx.fillStyle = "#5d4037"; this.ctx.fillRect(125, 40, 25, 320); this.ctx.fillRect(this.canvas.width - 150, 40, 25, 320);
                this.ctx.strokeStyle = "#d7ccc8"; this.ctx.lineWidth = 3; this.ctx.strokeRect(140, 50, this.canvas.width - 280, 300);

                this.ctx.fillStyle = "#111"; this.ctx.font = "bold 26px 'Segoe UI'"; this.ctx.textAlign = "center";
                this.ctx.fillText("Kiếm sĩ Phản công", this.canvas.width / 2, 100);
                this.ctx.font = "14px 'Segoe UI'";
                this.ctx.fillText("Trong nỗ lực giành lại đất đai, lượng Kiếm sĩ còn lại đang dồn toàn", this.canvas.width / 2, 145);
                this.ctx.fillText("lực còn lại để tấn công bạn!", this.canvas.width / 2, 170);
                this.ctx.fillStyle = "#b71c1c"; this.ctx.font = "bold 15px 'Segoe UI'";
                this.ctx.fillText("Hãy vượt qua cuộc phản công của Kiếm sĩ", this.canvas.width / 2, 220);

                this.ctx.fillStyle = "#1b4f72"; this.ctx.fillRect(this.canvas.width / 2 - 55, 270, 110, 40);
                this.ctx.strokeStyle = "#5dade2"; this.ctx.lineWidth = 2; this.ctx.strokeRect(this.canvas.width / 2 - 55, 270, 110, 40);
                this.ctx.fillStyle = "#fff"; this.ctx.font = "bold 16px 'Segoe UI'";
                this.ctx.fillText("OK", this.canvas.width / 2, 296);
                this.ctx.textAlign = "left";
            }
            run() {
                if (this.statueHp <= 0 || this.enemyStatueHp <= 0) {
                    this.gameOver = true;
                    this.ctx.fillStyle = "rgba(0,0,0,0.9)"; this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
                    this.ctx.fillStyle = this.statueHp > 0 ? "#2ecc71" : "#e74c3c";
                    this.ctx.font = "bold 36px 'Segoe UI'"; this.ctx.textAlign = "center";
                    this.ctx.fillText(this.statueHp > 0 ? "🏆 ORDER EMPIRE CHIẾN THẮNG!" : "💀 TÒA THÀNH ĐÃ THẤT THỦ!", this.canvas.width / 2, this.canvas.height / 2);
                    return;
                }

                this.animFrame++;
                this.ctx.save();
                if (this.screenShake > 0) {
                    this.screenShake--;
                    this.ctx.translate((Math.random() - 0.5) * 10, (Math.random() - 0.5) * 10);
                }

                this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                this.drawScene();

                if (this.showBriefing) {
                    this.drawBriefingScroll();
                    this.ctx.restore();
                    requestAnimationFrame(() => this.run());
                    return;
                }

                this.particles.updateAndDraw(this.ctx);

                // Quản lý thợ mỏ
                this.units.forEach((u, idx) => {
                    if (u.isSpinning > 0) u.isSpinning--;
                    if (u.type === 'miner') {
                        if (u.mineTarget) {
                            if (u.state === 'going') {
                                let dx = u.mineTarget.x - u.x; let dy = u.mineTarget.y - u.y;
                                let dist = Math.hypot(dx, dy);
                                if (dist > 3) { u.x += (dx / dist) * u.speed; u.y += (dy / dist) * u.speed; }
                                else { u.state = 'mining'; }
                            } else if (u.state === 'mining') {
                                u.goldBag = 15 * this.techLevel; u.state = 'returning';
                            } else if (u.state === 'returning') {
                                let dx = 70 - u.x; let dy = 200 - u.y;
                                let dist = Math.hypot(dx, dy);
                                if (dist > 3) { u.x += (dx / dist) * u.speed; u.y += (dy / dist) * u.speed; }
                                else {
                                    this.gold += u.goldBag || 15; u.goldBag = 0; u.state = 'going';
                                    this.particles.emit(70, 200, '#ffcc00', 8);
                                    this.addFloatingText("+" + (15 * this.techLevel) + " Gold", 70, 200, '#ffcc00');
                                    this.updateUI();
                                }
                            }
                        }
                    } else {
                        let nearestEnemy = this.enemies.find(e => Math.hypot(e.x - u.x, e.y - u.y) <= u.range);
                        if (nearestEnemy) {
                            if (u.attackCd > 0) u.attackCd--;
                            else {
                                nearestEnemy.hp -= u.dmg;
                                this.particles.emit(nearestEnemy.x, nearestEnemy.y, '#e74c3c', 6);
                                this.addFloatingText("-" + u.dmg, nearestEnemy.x, nearestEnemy.y - 15, '#e74c3c');
                                u.attackCd = 28;
                            }
                        } else {
                            let targetX = this.currentCommand === 'ATTACK' ? this.canvas.width - 70 : 280;
                            if (u.x < targetX) { u.x += u.speed; }
                            else if (this.currentCommand === 'ATTACK' && u.x >= this.canvas.width - 80) {
                                if (u.attackCd > 0) u.attackCd--;
                                else {
                                    this.enemyStatueHp -= u.dmg;
                                    this.particles.emit(this.canvas.width - 60, 180, '#ffcc00', 10);
                                    this.addFloatingText("-" + u.dmg, this.canvas.width - 60, 180, '#ffcc00');
                                    u.attackCd = 35;
                                    this.updateUI();
                                }
                            }
                        }
                    }
                    u.draw(this.ctx, this.animFrame);
                    if (u.hp <= 0) this.units.splice(idx, 1);
                });

                // Quản lý quái địch
                this.enemies.forEach((e, idx) => {
                    let nearestUnit = this.units.find(u => u.type !== 'miner' && Math.hypot(u.x - e.x, u.y - e.y) <= e.range);
                    if (nearestUnit) {
                        if (e.attackCd > 0) e.attackCd--;
                        else {
                            nearestUnit.hp -= e.dmg;
                            this.particles.emit(nearestUnit.x, nearestUnit.y, '#ffcc00', 6);
                            this.addFloatingText("-" + e.dmg, nearestUnit.x, nearestUnit.y - 15, '#ffcc00');
                            e.attackCd = 32;
                        }
                    } else {
                        e.x -= e.speed;
                        if (e.x <= 70) {
                            if (e.attackCd > 0) e.attackCd--;
                            else {
                                this.statueHp -= e.dmg;
                                this.particles.emit(50, 180, '#e74c3c', 10);
                                this.addFloatingText("-" + e.dmg, 50, 180, '#e74c3c');
                                e.attackCd = 38;
                                this.updateUI();
                            }
                        }
                    }
                    e.draw(this.ctx, this.animFrame);
                    if (e.hp <= 0) { this.enemies.splice(idx, 1); this.gold += 35; this.particles.emit(e.x, e.y, '#ffcc00', 12); this.updateUI(); }
                });

                this.floatingTexts.forEach((ft, idx) => {
                    ft.y -= 0.6; ft.alpha -= 0.02;
                    this.ctx.fillStyle = ft.color; this.ctx.globalAlpha = Math.max(0, ft.alpha);
                    this.ctx.font = "bold 12px 'Segoe UI'"; this.ctx.fillText(ft.text, ft.x, ft.y);
                    this.ctx.globalAlpha = 1.0;
                    if (ft.alpha <= 0) this.floatingTexts.splice(idx, 1);
                });

                this.ctx.restore();
                requestAnimationFrame(() => this.run());
            }
        }

        const GameManager = new RTSGameManager();

        // AI Spawner tự sinh quái định kỳ
        setInterval(() => {
            if (!GameManager.showBriefing && !GameManager.gameOver && GameManager.enemyStatueHp > 0 && GameManager.enemies.length < 30) {
                let types = ['goblin', 'orc', 'shadow_mage', 'troll'];
                let t = types[Math.floor(Math.random() * types.length)];
                let stats = {
                    goblin: { hp: 110, dmg: 14, range: 30, speed: 1.4, size: 0.95 },
                    orc: { hp: 230, dmg: 26, range: 35, speed: 1.0, size: 1.2 },
                    shadow_mage: { hp: 160, dmg: 38, range: 150, speed: 0.8, size: 1.05 },
                    troll: { hp: 650, dmg: 60, range: 50, speed: 0.5, size: 1.85 }
                }[t];

                GameManager.enemies.push(new GameObject(GameManager.canvas.width - 80, 140 + Math.random() * 200, t, true, stats));
            }
        }, 3200);

        GameManager.run();
    </script>
</body>
</html>
"""

st.components.v1.html(game_html, height=540, scrolling=False)
