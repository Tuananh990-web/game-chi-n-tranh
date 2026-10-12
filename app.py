import streamlit as st

st.set_page_config(
    page_title="Kháng Chiến Việt Nam - Quân Sự Edition",
    page_icon="⭐",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #0d1b1e; color: #ffffff; font-family: 'Segoe UI', Tahoma, sans-serif; }
    iframe { border-radius: 12px; box-shadow: 0 15px 50px rgba(0,0,0,0.98); }
    .title-text { text-align: center; color: #f1c40f; text-transform: uppercase; font-weight: 900; letter-spacing: 2px; }
    .sub-text { text-align: center; color: #a3e4d7; font-size: 13px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-text'>⭐ KHÁNG CHIẾN VIỆT NAM - TÁC CHIẾN QUÂN SỰ ⭐</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Trang bị Súng, Xe tăng, Máy bay Oanh tạc Bom & Hệ thống Âm thanh Hào hùng!</p>", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Khang Chien Viet Nam Full FX</title>
    <style>
        body { margin: 0; background: #0d1b1e; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; overflow: hidden; }
        canvas { background: linear-gradient(to bottom, #27ae60 0%, #1e8449 70%, #145a32 100%); border: 4px solid #145a32; border-radius: 10px; box-shadow: 0 15px 40px rgba(0,0,0,0.95); display: block; margin: 4px auto; }
        .ui-panel { display: flex; justify-content: center; flex-wrap: wrap; gap: 5px; margin-top: 4px; }
        .cmd-panel { display: flex; justify-content: center; gap: 6px; margin-top: 4px; }
        .music-panel { display: flex; justify-content: center; gap: 8px; margin-top: 6px; background: #112a2e; padding: 6px; border-radius: 6px; border: 1px solid #f1c40f; width: fit-content; margin-left: auto; margin-right: auto; }
        button { background: #7d6608; color: #fff; border: 2px solid #f1c40f; padding: 6px 11px; font-weight: bold; font-size: 11px; border-radius: 4px; cursor: pointer; transition: 0.2s; text-transform: uppercase; }
        button:hover { background: #b7950b; transform: scale(1.05); }
        button:active { transform: scale(0.95); }
        .cmd-btn { background: #1b4f72; border-color: #5dade2; }
        .skill-btn { background: #512e5f; border-color: #f39c12; }
        .tech-btn { background: #145a32; border-color: #2ecc71; }
        .music-btn { background: #900C3F; border-color: #FFC300; }
        .stats { font-size: 13px; font-weight: bold; color: #f1c40f; margin-bottom: 3px; }
    </style>
</head>
<body>

    <div class="stats">
        🏛️ CĂN CỨ KHÁNG CHIẾN: <span id="hpText">3000</span> | ⚔️ ĐỒNG BÀO/ĐỊCH: <span id="enemyHpText">3000</span> | 🌾 LƯƠNG THỰC: <span id="goldText">450</span> | 👥 QUÂN SỐ: <span id="popText">0</span>/100 | 🎖️ CẤP HUÂN CHƯƠNG: <span id="techText">1</span>
    </div>

    <canvas id="gameCanvas" width="980" height="380"></canvas>

    <div class="music-panel">
        <span style="font-size:12px; font-weight:bold; color:#f1c40f; align-self:center;">🎵 ÂM THANH QUÂN SỰ:</span>
        <button class="music-btn" onclick="playMarchTone()">🎺 Hành Khúc Chiến Thắng</button>
        <button class="music-btn" onclick="playSiren()">📯 Còi Báo Động / Tiến Công</button>
        <button class="music-btn" onclick="stopAudio()">🔇 Tắt Âm Thanh</button>
    </div>

    <div class="cmd-panel">
        <button class="cmd-btn" id="btnAttack">⚔️ TẤN CÔNG</button>
        <button class="cmd-btn" id="btnDefend">🛡️ PHÒNG THỦ</button>
        <button class="cmd-btn" id="btnHold">🛑 BÁM TRỤ</button>
        <button class="tech-btn" id="btnTech">⬆️ NÂNG CẤP VŨ KHÍ (150G)</button>
        <button class="skill-btn" id="btnSpin">🔫 XUNG PHONG MÃ TẤU</button>
        <button class="skill-btn" id="btnEarth">💣 MÁY BAY THẢ BOM</button>
    </div>

    <div class="ui-panel">
        <button id="spawnMiner">🌾 Dân Quân Tải Đạn (30g)</button>
        <button id="spawnSwordwrath">🗡️ Du Kích Cận Chiến (40g)</button>
        <button id="spawnArchidon">🔫 Xạ Thủ Bắn Súng (50g)</button>
        <button id="spawnSpearton">🛡️ Tự Vệ Khiên Thép (70g)</button>
        <button id="spawnMagikill">⭐ Cán Bộ Chỉ Huy (100g)</button>
        <button id="spawnGiant">🚜 Xe Tăng Hỏa Lực (160g)</button>
    </div>

    <script>
        // HỆ THỐNG ÂM THANH WEB AUDIO API (ĐẢM BẢO NGHẸ ĐƯỢC 100%)
        let audioCtx = null;
        let isPlayingLoop = false;
        let soundTimer = null;

        function initAudio() {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
        }

        function playMarchTone() {
            initAudio();
            stopAudio();
            isPlayingLoop = true;
            let notes = [261.63, 329.63, 392.00, 523.25, 392.00, 523.25];
            let noteIdx = 0;
            soundTimer = setInterval(() => {
                if (!isPlayingLoop) return;
                let osc = audioCtx.createOscillator();
                let gain = audioCtx.createGain();
                osc.type = 'triangle';
                osc.frequency.value = notes[noteIdx % notes.length];
                gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.3);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.3);
                noteIdx++;
            }, 350);
        }

        function playSiren() {
            initAudio();
            stopAudio();
            let osc = audioCtx.createOscillator();
            let gain = audioCtx.createGain();
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(300, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(800, audioCtx.currentTime + 1.2);
            gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 1.5);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 1.5);
        }

        function stopAudio() {
            isPlayingLoop = false;
            if (soundTimer) clearInterval(soundTimer);
        }

        class ParticleSystem {
            constructor() { this.particles = []; }
            emit(x, y, color, count = 15) {
                for (let i = 0; i < count; i++) {
                    this.particles.push({
                        x, y, vx: (Math.random() - 0.5) * 6, vy: (Math.random() - 0.5) * 6,
                        radius: Math.random() * 3.5 + 1, color, alpha: 1.0, decay: Math.random() * 0.03 + 0.02
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
            constructor(x, y, type, isEnemy, stats, techLevel = 1) {
                this.x = x; this.y = y; this.type = type; this.isEnemy = isEnemy;
                this.hp = stats.hp; this.maxHp = stats.hp; this.dmg = stats.dmg;
                this.range = stats.range; this.speed = stats.speed; this.size = stats.size;
                this.attackCd = 0; this.state = 'going'; this.goldBag = 0;
                this.isSpinning = 0; this.mineTarget = null;
                this.techLevel = techLevel;
            }
            draw(ctx, animFrame) {
                ctx.save();
                ctx.translate(this.x, this.y);
                if (this.isSpinning > 0) ctx.rotate((50 - this.isSpinning) * 0.5);

                let unitColor = '#27ae60';
                if (this.isEnemy) unitColor = '#c0392b';
                else {
                    if (this.type === 'miner') unitColor = '#d35400';
                    else if (this.type === 'archidon') unitColor = '#229954';
                    else if (this.type === 'spearton') unitColor = '#117a65';
                    else if (this.type === 'magikill') unitColor = '#f1c40f';
                    else if (this.type === 'giant') unitColor = '#2c3e50';
                }

                if (this.type === 'giant') {
                    // VẼ XE TĂNG TÁC CHIẾN HỎA LỰC HẠNG NẶNG
                    ctx.fillStyle = this.isEnemy ? "#78281f" : "#1e8449";
                    ctx.fillRect(-22, -12, 44, 20); // Thân xe
                    ctx.fillStyle = "#111"; ctx.fillRect(-24, 8, 48, 6); // Bánh xích
                    ctx.fillStyle = "#2c3e50"; ctx.fillRect(-10, -18, 20, 10); // Tháp pháo
                    ctx.fillRect(this.isEnemy ? -30 : 10, -15, 20, 4); // Nòng pháo
                } else {
                    // VẼ CHIẾN SĨ DÂN QUÂN / QUÂN ĐỊCH
                    ctx.fillStyle = "#000"; ctx.beginPath(); ctx.arc(0, -14 * this.size, 6 * this.size, 0, Math.PI * 2); ctx.fill();
                    ctx.fillStyle = this.isEnemy ? "#78281f" : "#27ae60"; ctx.fillRect(-7 * this.size, -22 * this.size, 14 * this.size, 4 * this.size);

                    if (!this.isEnemy && this.techLevel > 1) {
                        ctx.fillStyle = this.techLevel === 2 ? "#bdc3c7" : "#f1c40f";
                        ctx.fillRect(-5 * this.size, -12 * this.size, 10 * this.size, 8 * this.size);
                    }

                    // SÚNG AK / BẮN SÚNG TẦM XA
                    if (this.type === 'archidon') {
                        ctx.fillStyle = "#2c3e50";
                        ctx.fillRect(2, -8, 12, 3); // Nòng súng AK
                    }

                    ctx.strokeStyle = unitColor; ctx.lineWidth = 3.5 * this.size;
                    ctx.beginPath(); ctx.moveTo(0, -8 * this.size); ctx.lineTo(0, 8 * this.size); ctx.stroke();
                    let swing = Math.sin(animFrame * 0.3) * 5;
                    ctx.beginPath(); ctx.moveTo(0, 8 * this.size); ctx.lineTo(-5 * this.size, 18 * this.size + swing); ctx.stroke();
                    ctx.beginPath(); ctx.moveTo(0, 8 * this.size); ctx.lineTo(5 * this.size, 18 * this.size - swing); ctx.stroke();
                }

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
                this.animFrame = 0; this.planeX = -100; this.isPlaneActive = false;
                this.particles = new ParticleSystem();
                this.goldMines = [
                    { x: 150, y: 130, miner: null }, { x: 200, y: 180, miner: null }, { x: 250, y: 240, miner: null },
                    { x: 170, y: 290, miner: null }, { x: 220, y: 110, miner: null }, { x: 270, y: 160, miner: null }
                ];
                this.units = []; this.enemies = []; this.floatingTexts = [];
                this.initListeners();
            }
            initListeners() {
                this.canvas.addEventListener('click', (e) => {
                    initAudio();
                    if (this.showBriefing) {
                        const rect = this.canvas.getBoundingClientRect();
                        const mouseX = e.clientX - rect.left; const mouseY = e.clientY - rect.top;
                        if (mouseX >= this.canvas.width / 2 - 55 && mouseX <= this.canvas.width / 2 + 55 && mouseY >= 250 && mouseY <= 295) {
                            this.showBriefing = false;
                        }
                    }
                });

                document.getElementById('btnAttack').onclick = () => this.setCommand('ATTACK');
                document.getElementById('btnDefend').onclick = () => this.setCommand('DEFEND');
                document.getElementById('btnHold').onclick = () => this.setCommand('HOLD');
                document.getElementById('btnTech').onclick = () => this.upgradeTech();
                document.getElementById('btnSpin').onclick = () => this.triggerSkill('spin');
                document.getElementById('btnEarth').onclick = () => this.triggerSkill('earthquake');

                document.getElementById('spawnMiner').onclick = () => this.spawnUnit('miner');
                document.getElementById('spawnSwordwrath').onclick = () => this.spawnUnit('swordwrath');
                document.getElementById('spawnArchidon').onclick = () => this.spawnUnit('archidon');
                document.getElementById('spawnSpearton').onclick = () => this.spawnUnit('spearton');
                document.getElementById('spawnMagikill').onclick = () => this.spawnUnit('magikill');
                document.getElementById('spawnGiant').onclick = () => this.spawnUnit('giant');
            }
            setCommand(cmd) { this.currentCommand = cmd; }
            addFloatingText(text, x, y, color = '#f1c40f') {
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
                    this.units.forEach(u => {
                        u.techLevel = this.techLevel;
                        u.dmg = Math.floor(u.dmg * 1.3);
                        u.maxHp = Math.floor(u.maxHp * 1.25);
                        u.hp = u.maxHp;
                    });
                    this.particles.emit(this.canvas.width / 2, 180, '#2ecc71', 35);
                    this.addFloatingText("⭐ CẢI TIẾN CÔNG NGHỆ VŨ KHÍ (CẤP " + this.techLevel + ")!", this.canvas.width / 2, 90, '#2ecc71');
                    this.updateUI();
                }
            }
            triggerSkill(type) {
                if (this.showBriefing || this.gameOver) return;
                if (type === 'spin') {
                    this.units.filter(u => u.type === 'swordwrath').forEach(u => {
                        u.isSpinning = 50;
                        this.particles.emit(u.x, u.y, '#f1c40f', 20);
                        this.addFloatingText("Xung Phong!", u.x, u.y - 25, '#f1c40f');
                    });
                } else if (type === 'earthquake') {
                    // MÁY BAY OANH TẠC THẢ BOM
                    this.isPlaneActive = true; this.planeX = -100;
                    this.screenShake = 35;
                    this.particles.emit(this.canvas.width / 2, this.canvas.height / 2, '#e74c3c', 60);
                    this.enemies.forEach(e => {
                        e.hp -= (100 * this.techLevel);
                        this.particles.emit(e.x, e.y, '#e74c3c', 12);
                        this.addFloatingText("-" + (100 * this.techLevel) + " Thả Bom", e.x, e.y, '#e74c3c');
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
                    let unit = new GameObject(80, 130 + Math.random() * 180, type, false, {
                        hp: stats.hp * (1 + (this.techLevel - 1) * 0.25),
                        dmg: stats.dmg * (1 + (this.techLevel - 1) * 0.3),
                        range: stats.range, speed: stats.speed, size: stats.size
                    }, this.techLevel);

                    if (type === 'miner') {
                        let freeMine = this.goldMines.find(m => !m.miner);
                        if (freeMine) { freeMine.miner = unit; unit.mineTarget = freeMine; }
                        else { unit.mineTarget = this.goldMines[0]; }
                    }
                    this.units.push(unit);
                    this.particles.emit(unit.x, unit.y, '#f1c40f', 10);
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
                this.ctx.fillStyle = "#27ae60"; this.ctx.fillRect(0, 90, this.canvas.width, 290);
                this.ctx.fillStyle = "#1e8449"; this.ctx.fillRect(0, 90, this.canvas.width, 6);

                this.ctx.fillStyle = "#b7950b"; this.ctx.fillRect(15, 50, 45, 240);
                this.ctx.fillStyle = "#f1c40f"; this.ctx.beginPath(); this.ctx.arc(37, 45, 18, 0, Math.PI * 2); this.ctx.fill();

                this.goldMines.forEach((m, idx) => {
                    this.ctx.fillStyle = "#f1c40f";
                    this.ctx.beginPath(); this.ctx.arc(m.x, m.y, 13, 0, Math.PI * 2); this.ctx.fill();
                    this.ctx.strokeStyle = "#fff"; this.ctx.lineWidth = 1.5; this.ctx.stroke();
                    this.ctx.fillStyle = "#000"; this.ctx.font = "bold 9px 'Segoe UI'";
                    this.ctx.fillText("V" + (idx + 1), m.x - 5, m.y + 3);
                });

                this.ctx.fillStyle = "#641e16"; this.ctx.fillRect(this.canvas.width - 60, 50, 45, 240);
                this.ctx.fillStyle = "#922b21"; this.ctx.beginPath(); this.ctx.arc(this.canvas.width - 37, 45, 18, 0, Math.PI * 2); this.ctx.fill();

                // VẼ MÁY BAY BAY THẢ BOM TRÊN BẦU TRỜI
                if (this.isPlaneActive) {
                    this.planeX += 8;
                    this.ctx.fillStyle = "#7f8c8d";
                    this.ctx.fillRect(this.planeX, 30, 40, 10); // Thân máy bay
                    this.ctx.fillRect(this.planeX + 15, 20, 10, 30); // Cánh
                    if (this.planeX > this.canvas.width + 50) this.isPlaneActive = false;
                }
            }
            drawBriefingScroll() {
                this.ctx.fillStyle = "rgba(0, 0, 0, 0.85)"; this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
                this.ctx.fillStyle = "#f5f5dc"; this.ctx.fillRect(130, 40, this.canvas.width - 260, 280);
                this.ctx.fillStyle = "#5d4037"; this.ctx.fillRect(115, 30, 25, 300); this.ctx.fillRect(this.canvas.width - 140, 30, 25, 300);
                this.ctx.strokeStyle = "#d7ccc8"; this.ctx.lineWidth = 3; this.ctx.strokeRect(130, 40, this.canvas.width - 260, 280);

                this.ctx.fillStyle = "#111"; this.ctx.font = "bold 22px 'Segoe UI'"; this.ctx.textAlign = "center";
                this.ctx.fillText("Bảo Vệ Vùng Giải Phóng", this.canvas.width / 2, 85);
                this.ctx.font = "13px 'Segoe UI'";
                this.ctx.fillText("Kẻ địch đang dồn lực tiến công vào căn cứ. Hãy huy động dân quân,", this.canvas.width / 2, 125);
                this.ctx.fillText("phát triển lực lượng và anh dũng đẩy lùi các đợt tấn công!", this.canvas.width / 2, 148);
                this.ctx.fillStyle = "#c0392b"; this.ctx.font = "bold 14px 'Segoe UI'";
                this.ctx.fillText("Quyết tử cho Tổ quốc quyết sinh!", this.canvas.width / 2, 190);

                this.ctx.fillStyle = "#1b4f72"; this.ctx.fillRect(this.canvas.width / 2 - 50, 235, 100, 36);
                this.ctx.strokeStyle = "#5dade2"; this.ctx.lineWidth = 2; this.ctx.strokeRect(this.canvas.width / 2 - 50, 235, 100, 36);
                this.ctx.fillStyle = "#fff"; this.ctx.font = "bold 15px 'Segoe UI'";
                this.ctx.fillText("XUẤT QUÂN", this.canvas.width / 2, 258);
                this.ctx.textAlign = "left";
            }
            run() {
                if (this.statueHp <= 0 || this.enemyStatueHp <= 0) {
                    this.gameOver = true;
                    this.ctx.fillStyle = "rgba(0,0,0,0.9)"; this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
                    this.ctx.fillStyle = this.statueHp > 0 ? "#2ecc71" : "#e74c3c";
                    this.ctx.font = "bold 32px 'Segoe UI'"; this.ctx.textAlign = "center";
                    this.ctx.fillText(this.statueHp > 0 ? "⭐ CHIẾN THẮNG! GIẢI PHÓNG HOÀN TOÀN!" : "💀 CĂN CỨ ĐÃ THẤT THỦ!", this.canvas.width / 2, this.canvas.height / 2);
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
                                let dx = 70 - u.x; let dy = 180 - u.y;
                                let dist = Math.hypot(dx, dy);
                                if (dist > 3) { u.x += (dx / dist) * u.speed; u.y += (dy / dist) * u.speed; }
                                else {
                                    this.gold += u.goldBag || 15; u.goldBag = 0; u.state = 'going';
                                    this.particles.emit(70, 180, '#f1c40f', 8);
                                    this.addFloatingText("+" + (15 * this.techLevel) + " Lương thực", 70, 180, '#f1c40f');
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
                                this.addFloatingText("-" + Math.floor(u.dmg), nearestEnemy.x, nearestEnemy.y - 15, '#e74c3c');
                                u.attackCd = 28;
                            }
                        } else {
                            let targetX = this.currentCommand === 'ATTACK' ? this.canvas.width - 70 : 280;
                            if (u.x < targetX) { u.x += u.speed; }
                            else if (this.currentCommand === 'ATTACK' && u.x >= this.canvas.width - 80) {
                                if (u.attackCd > 0) u.attackCd--;
                                else {
                                    this.enemyStatueHp -= u.dmg;
                                    this.particles.emit(this.canvas.width - 60, 160, '#f1c40f', 10);
                                    this.addFloatingText("-" + Math.floor(u.dmg), this.canvas.width - 60, 160, '#f1c40f');
                                    u.attackCd = 35;
                                    this.updateUI();
                                }
                            }
                        }
                    }
                    u.draw(this.ctx, this.animFrame);
                    if (u.hp <= 0) this.units.splice(idx, 1);
                });

                this.enemies.forEach((e, idx) => {
                    let nearestUnit = this.units.find(u => u.type !== 'miner' && Math.hypot(u.x - e.x, u.y - e.y) <= e.range);
                    if (nearestUnit) {
                        if (e.attackCd > 0) e.attackCd--;
                        else {
                            nearestUnit.hp -= e.dmg;
                            this.particles.emit(nearestUnit.x, nearestUnit.y, '#f1c40f', 6);
                            this.addFloatingText("-" + Math.floor(e.dmg), nearestUnit.x, nearestUnit.y - 15, '#f1c40f');
                            e.attackCd = 32;
                        }
                    } else {
                        e.x -= e.speed;
                        if (e.x <= 70) {
                            if (e.attackCd > 0) e.attackCd--;
                            else {
                                this.statueHp -= e.dmg;
                                this.particles.emit(50, 160, '#e74c3c', 10);
                                this.addFloatingText("-" + Math.floor(e.dmg), 50, 160, '#e74c3c');
                                e.attackCd = 38;
                                this.updateUI();
                            }
                        }
                    }
                    e.draw(this.ctx, this.animFrame);
                    if (e.hp <= 0) { this.enemies.splice(idx, 1); this.gold += 35; this.particles.emit(e.x, e.y, '#f1c40f', 12); this.updateUI(); }
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

        setInterval(() => {
            if (!GameManager.showBriefing && !GameManager.gameOver && GameManager.enemyStatueHp > 0 && GameManager.enemies.length < 30) {
                let types = ['goblin', 'orc', 'shadow_mage', 'giant'];
                let t = types[Math.floor(Math.random() * types.length)];
                let stats = {
                    goblin: { hp: 110, dmg: 14, range: 30, speed: 1.4, size: 0.95 },
                    orc: { hp: 230, dmg: 26, range: 35, speed: 1.0, size: 1.2 },
                    shadow_mage: { hp: 160, dmg: 38, range: 150, speed: 0.8, size: 1.05 },
                    giant: { hp: 650, dmg: 60, range: 50, speed: 0.5, size: 1.85 }
                }[t];

                GameManager.enemies.push(new GameObject(GameManager.canvas.width - 80, 130 + Math.random() * 180, t, true, stats));
            }
        }, 3200);

        GameManager.run();
    </script>
</body>
</html>
"""

st.components.v1.html(game_html, height=520, scrolling=False)
