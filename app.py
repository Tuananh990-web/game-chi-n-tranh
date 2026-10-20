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
    .sub-text { text-align: center; color: #a3e4d7; font-size: 14px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-text'>⭐ KHÁNG CHIẾN VIỆT NAM - CHIẾN DỊCH TOÀN DIỆN ⭐</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Bổ sung Lời dẫn truyện qua màn, Sửa lỗi đứng hình & Cấp độ kẻ địch!</p>", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Khang Chien Viet Nam Full FX</title>
    <style>
        body { margin: 0; background: #0d1b1e; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; overflow: hidden; user-select: none; }
        canvas { background: #145a32; border: 4px solid #f1c40f; border-radius: 10px; box-shadow: 0 10px 30px rgba(241, 196, 15, 0.2); display: block; margin: 4px auto; cursor: pointer; }
        .ui-panel { display: flex; justify-content: center; flex-wrap: wrap; gap: 5px; margin-top: 4px; }
        .cmd-panel { display: flex; justify-content: center; flex-wrap: wrap; gap: 6px; margin-top: 4px; }
        .music-panel { display: flex; justify-content: center; flex-wrap: wrap; gap: 8px; margin-top: 6px; background: #112a2e; padding: 6px; border-radius: 6px; border: 1px solid #f1c40f; width: fit-content; margin-left: auto; margin-right: auto; }
        button { background: linear-gradient(145deg, #7d6608, #5a4906); color: #fff; border: 1px solid #f1c40f; padding: 6px 11px; font-weight: bold; font-size: 11px; border-radius: 4px; cursor: pointer; transition: 0.2s; text-transform: uppercase; box-shadow: 2px 2px 5px rgba(0,0,0,0.5); }
        button:hover { background: #b7950b; transform: translateY(-2px); }
        button:active { transform: scale(0.95); }
        .cmd-btn { background: linear-gradient(145deg, #1b4f72, #154360); border-color: #5dade2; }
        .bunker-btn { background: linear-gradient(145deg, #d35400, #a04000); border-color: #f39c12; animation: pulse 2s infinite; }
        .skill-btn { background: linear-gradient(145deg, #512e5f, #4a235a); border-color: #f39c12; }
        .tech-btn { background: linear-gradient(145deg, #145a32, #0e4324); border-color: #2ecc71; }
        .music-btn { background: linear-gradient(145deg, #900C3F, #780933); border-color: #FFC300; }
        .stats { font-size: 14px; font-weight: bold; color: #f1c40f; margin-bottom: 3px; }
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(243, 156, 18, 0.7); } 70% { box-shadow: 0 0 0 10px rgba(243, 156, 18, 0); } 100% { box-shadow: 0 0 0 0 rgba(243, 156, 18, 0); } }
    </style>
</head>
<body>

    <div class="stats">
        🚩 LEVEL: <span id="levelText">1</span> | 🏛️ CĂN CỨ: <span id="hpText">3000</span> | ⚔️ ĐỊCH: <span id="enemyHpText">3000</span> | 🌾 LƯƠNG: <span id="goldText">450</span> | 👥 QUÂN: <span id="popText">0</span>/100 | 🎖️ CẤP: <span id="techText">1</span>
    </div>

    <canvas id="gameCanvas" width="980" height="360"></canvas>

    <div class="music-panel">
        <span style="font-size:12px; font-weight:bold; color:#f1c40f; align-self:center;">🎵 NHẠC & ÂM THANH:</span>
        <button class="music-btn" onclick="playExternalMusic('https://upload.wikimedia.org/wikipedia/commons/e/e5/Tien_Quan_Ca_instrumental.ogg')">🎶 Tiến Quân Ca</button>
        <button class="music-btn" onclick="playMarchTone()">🎺 Kèn Xung Phong</button>
        <button class="music-btn" onclick="stopAllAudio()">🔇 Tắt Toàn Bộ</button>
    </div>

    <div class="cmd-panel">
        <button class="cmd-btn" id="btnAttack">⚔️ TẤN CÔNG</button>
        <button class="cmd-btn" id="btnDefend">🛡️ PHÒNG THỦ</button>
        <button class="bunker-btn" id="btnBunker">🕳️ CHUI HẦM TRÚ ẨN</button>
        <button class="tech-btn" id="btnTech">⬆️ NÂNG CẤP VŨ KHÍ (150G)</button>
        <button class="skill-btn" id="btnSpin">🔫 XUNG PHONG MÃ TẤU</button>
        <button class="skill-btn" id="btnEarth">💣 GỌI MÁY BAY HỖ TRỢ</button>
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
        // HỆ THỐNG ÂM THANH MP3 VÀ WEB AUDIO API
        let bgMusic = new Audio();
        bgMusic.loop = true; bgMusic.volume = 0.5;
        
        function playExternalMusic(url) {
            bgMusic.src = url;
            bgMusic.play().catch(e => console.log("Trình duyệt chặn tự động phát nhạc."));
        }

        let audioCtx = null;
        let isPlayingLoop = false;
        let soundTimer = null;

        function initAudio() {
            if (!audioCtx) { audioCtx = new (window.AudioContext || window.webkitAudioContext)(); }
            if (audioCtx.state === 'suspended') { audioCtx.resume(); }
        }

        function playMarchTone() {
            initAudio(); stopWebAudio(); isPlayingLoop = true;
            let notes = [261.63, 329.63, 392.00, 523.25, 392.00, 523.25]; let noteIdx = 0;
            soundTimer = setInterval(() => {
                if (!isPlayingLoop) return;
                let osc = audioCtx.createOscillator(); let gain = audioCtx.createGain();
                osc.type = 'square'; osc.frequency.value = notes[noteIdx % notes.length];
                gain.gain.setValueAtTime(0.1, audioCtx.currentTime); gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.3);
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.start(); osc.stop(audioCtx.currentTime + 0.3); noteIdx++;
            }, 350);
        }

        function playAirRaidSiren() {
            initAudio(); stopWebAudio(); isPlayingLoop = true;
            let osc = audioCtx.createOscillator(); let gain = audioCtx.createGain();
            osc.type = 'sawtooth'; osc.frequency.setValueAtTime(300, audioCtx.currentTime); 
            osc.frequency.linearRampToValueAtTime(700, audioCtx.currentTime + 2.0); // Còi hụ lên
            osc.frequency.linearRampToValueAtTime(300, audioCtx.currentTime + 4.0); // Còi hụ xuống
            gain.gain.setValueAtTime(0.2, audioCtx.currentTime); gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 4.0);
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.start(); osc.stop(audioCtx.currentTime + 4.0);
        }

        function stopWebAudio() {
            isPlayingLoop = false; if (soundTimer) clearInterval(soundTimer);
        }
        function stopAllAudio() {
            bgMusic.pause(); stopWebAudio();
        }

        class ParticleSystem {
            constructor() { this.particles = []; }
            emit(x, y, color, count = 15) {
                for (let i = 0; i < count; i++) {
                    this.particles.push({
                        x, y, vx: (Math.random() - 0.5) * 8, vy: (Math.random() - 0.5) * 8 - 1,
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
                this.isSpinning = 0; this.mineTarget = null; this.techLevel = techLevel;
            }
            draw(ctx, animFrame, isHiding = false) {
                ctx.save();
                ctx.translate(this.x, this.y);
                
                // HIỆU ỨNG CHUI HẦM: Lính ta sẽ xoay 90 độ nằm sấp xuống đất
                if (!this.isEnemy && isHiding && this.type !== 'giant') {
                    ctx.rotate(Math.PI / 2);
                    ctx.translate(10, -10); // Điều chỉnh tọa độ khi nằm sấp
                } else if (this.isSpinning > 0) {
                    ctx.rotate((50 - this.isSpinning) * 0.5);
                }

                ctx.shadowColor = 'rgba(0, 0, 0, 0.4)';
                ctx.shadowBlur = 6; ctx.shadowOffsetX = 2; ctx.shadowOffsetY = 4;

                let unitColor = '#3498db'; // Lính ta
                if (this.isEnemy) unitColor = '#c0392b'; // Lính địch
                else {
                    if (this.type === 'miner') unitColor = '#f39c12';
                    else if (this.type === 'archidon') unitColor = '#229954';
                    else if (this.type === 'spearton') unitColor = '#117a65';
                    else if (this.type === 'magikill') unitColor = '#f1c40f';
                    else if (this.type === 'giant') unitColor = '#4B5320'; // Xanh rằn ri
                }

                if (this.type === 'giant') {
                    // XE TĂNG RẰN RI (CAMO) THỰC TẾ HƠN
                    ctx.fillStyle = this.isEnemy ? "#78281f" : unitColor;
                    ctx.beginPath();
                    if(ctx.roundRect) ctx.roundRect(-25, -15, 50, 22, 5); else ctx.fillRect(-25, -15, 50, 22);
                    ctx.fill();
                    
                    // Chi tiết rằn ri (Camo) cho phe ta
                    if(!this.isEnemy) {
                        ctx.fillStyle = "#3e4215"; ctx.beginPath(); ctx.arc(-10, -10, 6, 0, Math.PI*2); ctx.fill();
                        ctx.fillStyle = "#2c300f"; ctx.beginPath(); ctx.arc(15, -5, 8, 0, Math.PI*2); ctx.fill();
                    }
                    
                    // Bánh xích
                    ctx.fillStyle = "#111"; ctx.fillRect(-28, 7, 56, 8); 
                    ctx.fillStyle = "#555";
                    for(let i=-24; i<=24; i+=12) { ctx.beginPath(); ctx.arc(i, 11, 3, 0, Math.PI*2); ctx.fill(); }
                    
                    // Tháp pháo & nòng pháo
                    ctx.fillStyle = "#2c3e50"; ctx.beginPath(); ctx.arc(0, -15, 12, Math.PI, 0); ctx.fill();
                    ctx.lineWidth = 4; ctx.strokeStyle = "#111";
                    ctx.beginPath(); ctx.moveTo(0, -20); ctx.lineTo(this.isEnemy ? -35 : 35, -20); ctx.stroke();
                } else {
                    // CHI TIẾT BỘ BINH
                    ctx.fillStyle = "#f5cba7"; // Da
                    ctx.beginPath(); ctx.arc(0, -16 * this.size, 5 * this.size, 0, Math.PI * 2); ctx.fill();
                    
                    ctx.fillStyle = this.isEnemy ? "#922b21" : "#1e8449"; 
                    ctx.fillRect(-6 * this.size, -22 * this.size, 12 * this.size, 5 * this.size); // Mũ cối

                    if (!this.isEnemy && this.techLevel > 1) {
                        ctx.fillStyle = this.techLevel === 2 ? "#bdc3c7" : "#f1c40f"; // Sao trên nón
                        ctx.fillRect(-3 * this.size, -21 * this.size, 6 * this.size, 3 * this.size); 
                    }

                    // Thân
                    ctx.fillStyle = unitColor;
                    ctx.fillRect(-5 * this.size, -11 * this.size, 10 * this.size, 12 * this.size); 

                    // Vũ khí
                    if (this.type === 'archidon') {
                        ctx.fillStyle = "#111"; ctx.fillRect(this.isEnemy ? -15 : 2, -4, 15, 3); // Súng đen
                    } else if (this.type === 'spearton') {
                        ctx.fillStyle = "#7f8c8d"; ctx.fillRect(this.isEnemy ? -12 : 12, -15, 4, 20); // Khiên/Giáp
                    }

                    // Chân cử động
                    ctx.shadowColor = 'transparent'; 
                    ctx.strokeStyle = "#222"; ctx.lineWidth = 3 * this.size;
                    let swing = 0;
                    if (!isHiding || this.isEnemy) {
                        swing = (this.state === 'going' || this.state === 'returning') ? Math.sin(animFrame * 0.4) * 6 : 0;
                        if(this.isEnemy) swing = Math.sin(animFrame * 0.4) * 6; 
                    }
                    ctx.beginPath(); ctx.moveTo(-2, 1 * this.size); ctx.lineTo(-4 * this.size, 11 * this.size + swing); ctx.stroke();
                    ctx.beginPath(); ctx.moveTo(2, 1 * this.size); ctx.lineTo(4 * this.size, 11 * this.size - swing); ctx.stroke();
                }

                // THANH MÁU GRADIENT
                ctx.shadowColor = 'transparent'; 
                ctx.fillStyle = "#000"; ctx.fillRect(-15, -38, 30, 4);
                let hpPercent = this.hp / this.maxHp;
                let hpGrad = ctx.createLinearGradient(-15, 0, 15, 0);
                hpGrad.addColorStop(0, "#e74c3c"); hpGrad.addColorStop(1, hpPercent > 0.5 ? "#2ecc71" : "#f1c40f");
                ctx.fillStyle = hpGrad; ctx.fillRect(-15, -38, 30 * hpPercent, 4);
                
                ctx.restore();
            }
        }

        class RTSGameManager {
            constructor() {
                this.canvas = document.getElementById("gameCanvas");
                this.ctx = this.canvas.getContext("2d");
                this.level = 1; this.maxLevel = 3;
                this.statueHp = 3000; this.enemyStatueHp = 3000;
                this.gold = 450; this.techLevel = 1; this.currentCommand = 'ATTACK';
                this.gameOver = false; this.levelComplete = false; this.showBriefing = true; 
                this.screenShake = 0; this.animFrame = 0; 
                
                this.isHiding = false; 
                this.airRaidWarning = 0; 
                this.enemyBomberX = -200; 
                this.isEnemyBomberActive = false;
                
                this.planeX = -100; this.isPlaneActive = false; 
                
                this.particles = new ParticleSystem();
                this.goldMines = [
                    { x: 150, y: 130, miner: null }, { x: 200, y: 180, miner: null }, { x: 250, y: 240, miner: null },
                    { x: 170, y: 290, miner: null }, { x: 220, y: 110, miner: null }, { x: 270, y: 160, miner: null }
                ];
                this.units = []; this.enemies = []; this.floatingTexts = [];
                
                this.mapColors = {
                    1: { bg: 'linear-gradient(to bottom, #4ca1af 0%, #27ae60 100%)', base1: '#b7950b', base2: '#641e16' }, 
                    2: { bg: 'linear-gradient(to bottom, #141e30 0%, #243b55 100%)', base1: '#5a6268', base2: '#343a40' }, 
                    3: { bg: 'linear-gradient(to bottom, #e55d87 0%, #b33939 100%)', base1: '#8e44ad', base2: '#4a235a' }  
                };

                this.initListeners();
            }
            
            initListeners() {
                this.canvas.addEventListener('click', (e) => {
                    initAudio();
                    const rect = this.canvas.getBoundingClientRect();
                    const mouseX = e.clientX - rect.left; const mouseY = e.clientY - rect.top;
                    
                    // Nút XUẤT QUÂN ở Briefing
                    if (this.showBriefing) { 
                        if (mouseX >= this.canvas.width / 2 - 60 && mouseX <= this.canvas.width / 2 + 60 && mouseY >= 235 && mouseY <= 275) {
                            this.showBriefing = false;
                        }
                        return; 
                    }
                    
                    // Click Màn Hình Chuyển Level
                    if (this.levelComplete) { this.nextLevel(); return; }
                    
                    // Click Chơi Lại khi thua/thắng toàn bộ
                    if (this.gameOver) { 
                        this.resetGame(true); 
                        this.showBriefing = true; 
                        this.run(); // KHỞI ĐỘNG LẠI VÒNG LẶP SAU KHI THUA
                        return; 
                    }
                });

                document.getElementById('btnAttack').onclick = () => this.setCommand('ATTACK');
                document.getElementById('btnDefend').onclick = () => this.setCommand('DEFEND');
                
                let btnBunker = document.getElementById('btnBunker');
                btnBunker.onclick = () => {
                    this.isHiding = !this.isHiding;
                    if(this.isHiding) {
                        btnBunker.style.background = "linear-gradient(145deg, #2ecc71, #27ae60)";
                        btnBunker.innerText = "🏃 ĐANG TRÚ ẨN (BẤM ĐỂ DẬY)";
                        this.addFloatingText("Toàn quân Chui Hầm!", this.canvas.width/2, 200, '#2ecc71');
                    } else {
                        btnBunker.style.background = "linear-gradient(145deg, #d35400, #a04000)";
                        btnBunker.innerText = "🕳️ CHUI HẦM TRÚ ẨN";
                        this.addFloatingText("Toàn quân Tấn Công!", this.canvas.width/2, 200, '#e74c3c');
                    }
                };

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
            
            triggerAirRaidWarning() {
                if (this.isEnemyBomberActive || this.airRaidWarning > 0 || this.showBriefing || this.gameOver || this.levelComplete) return;
                this.airRaidWarning = 200; 
                playAirRaidSiren();
            }

            nextLevel() {
                this.level++;
                if (this.level > this.maxLevel) { this.gameOver = true; return; }
                this.canvas.style.background = this.mapColors[this.level].bg;
                this.resetGame(false); // false = không reset toàn bộ, chỉ reset map
                this.showBriefing = true; // Hiện lại briefing bối cảnh mới
                this.run(); // KHỞI ĐỘNG LẠI VÒNG LẶP CHO LEVEL MỚI
            }

            resetGame(fullReset = true) {
                if(fullReset) { this.level = 1; this.canvas.style.background = this.mapColors[1].bg; this.techLevel = 1; this.gold = 450; }
                else { this.gold += 500; } // Thưởng qua màn
                
                this.statueHp = 3000; this.enemyStatueHp = 3000 + (this.level * 1500); // Địch trâu hơn rõ rệt
                this.units = []; this.enemies = []; this.floatingTexts = [];
                this.isHiding = false; document.getElementById('btnBunker').style.background = "linear-gradient(145deg, #d35400, #a04000)"; document.getElementById('btnBunker').innerText = "🕳️ CHUI HẦM TRÚ ẨN";
                this.airRaidWarning = 0; this.isEnemyBomberActive = false;
                
                this.goldMines.forEach(m => m.miner = null);
                this.gameOver = false; this.levelComplete = false;
                document.getElementById("levelText").innerText = this.level;
                this.updateUI();
            }

            setCommand(cmd) { this.currentCommand = cmd; this.isHiding = false; document.getElementById('btnBunker').style.background = "linear-gradient(145deg, #d35400, #a04000)"; document.getElementById('btnBunker').innerText = "🕳️ CHUI HẦM TRÚ ẨN"; }
            addFloatingText(text, x, y, color = '#f1c40f') { this.floatingTexts.push({ text, x, y, alpha: 1.0, color }); }
            
            getCurrentPopulation() {
                let count = 0;
                this.units.forEach(u => {
                    if (u.type === 'spearton') count += 3; else if (u.type === 'magikill') count += 5;
                    else if (u.type === 'giant') count += 4; else count += 1;
                });
                return count;
            }

            upgradeTech() {
                if (this.showBriefing || this.gameOver || this.levelComplete) return;
                if (this.gold >= 150 && this.techLevel < 3) {
                    this.gold -= 150; this.techLevel++;
                    document.getElementById("techText").innerText = this.techLevel;
                    this.units.forEach(u => {
                        u.techLevel = this.techLevel; u.dmg = Math.floor(u.dmg * 1.3); u.maxHp = Math.floor(u.maxHp * 1.25); u.hp = u.maxHp;
                    });
                    this.particles.emit(this.canvas.width / 2, 180, '#2ecc71', 35);
                    this.addFloatingText("⭐ CẢI TIẾN CÔNG NGHỆ (CẤP " + this.techLevel + ")!", this.canvas.width / 2, 90, '#2ecc71');
                    this.updateUI();
                }
            }

            triggerSkill(type) {
                if (this.showBriefing || this.gameOver || this.levelComplete) return;
                if (type === 'spin') {
                    this.units.filter(u => u.type === 'swordwrath').forEach(u => {
                        u.isSpinning = 50; this.particles.emit(u.x, u.y, '#f1c40f', 20); this.addFloatingText("Xung Phong!", u.x, u.y - 25, '#f1c40f');
                    });
                } else if (type === 'earthquake') {
                    this.isPlaneActive = true; this.planeX = -100; this.screenShake = 35;
                    this.particles.emit(this.canvas.width / 2, this.canvas.height / 2, '#e74c3c', 60);
                    this.enemies.forEach(e => {
                        e.hp -= (100 * this.techLevel); this.particles.emit(e.x, e.y, '#e74c3c', 12);
                        this.addFloatingText("-" + (100 * this.techLevel) + " Thả Bom", e.x, e.y, '#e74c3c');
                    });
                }
            }

            spawnUnit(type) {
                if (this.showBriefing || this.gameOver || this.levelComplete) return;
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
                    this.units.push(unit); this.particles.emit(unit.x, unit.y, '#f1c40f', 10); this.updateUI();
                }
            }

            updateUI() {
                document.getElementById("hpText").innerText = Math.max(0, Math.floor(this.statueHp));
                document.getElementById("enemyHpText").innerText = Math.max(0, Math.floor(this.enemyStatueHp));
                document.getElementById("goldText").innerText = this.gold;
                document.getElementById("popText").innerText = this.getCurrentPopulation();
            }

            drawScene() {
                let bases = this.mapColors[this.level];
                this.ctx.fillStyle = bases.base1; this.ctx.fillRect(15, 50, 45, 240);
                this.ctx.fillStyle = "#f1c40f"; this.ctx.beginPath(); this.ctx.arc(37, 45, 18, 0, Math.PI * 2); this.ctx.fill();

                this.goldMines.forEach((m, idx) => {
                    this.ctx.fillStyle = "#f1c40f"; this.ctx.beginPath(); this.ctx.arc(m.x, m.y, 13, 0, Math.PI * 2); this.ctx.fill();
                    this.ctx.strokeStyle = "#fff"; this.ctx.lineWidth = 1.5; this.ctx.stroke();
                    this.ctx.fillStyle = "#000"; this.ctx.font = "bold 9px 'Segoe UI'"; this.ctx.fillText("V" + (idx + 1), m.x - 5, m.y + 3);
                });

                this.ctx.fillStyle = bases.base2; this.ctx.fillRect(this.canvas.width - 60, 50, 45, 240);
                this.ctx.fillStyle = "#922b21"; this.ctx.beginPath(); this.ctx.arc(this.canvas.width - 37, 45, 18, 0, Math.PI * 2); this.ctx.fill();

                if (this.airRaidWarning > 0) {
                    if (this.animFrame % 20 < 10) {
                        this.ctx.fillStyle = "rgba(231, 76, 60, 0.3)";
                        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
                    }
                    this.ctx.fillStyle = "#fff"; this.ctx.font = "bold 24px 'Segoe UI'"; this.ctx.textAlign = "center";
                    this.ctx.fillText("⚠️ CẢNH BÁO: MÁY BAY ĐỊCH SẮP THẢ BOM! CHUI HẦM NGAY!", this.canvas.width / 2, 80);
                    this.ctx.textAlign = "left";
                }

                if (this.isEnemyBomberActive) {
                    this.enemyBomberX += 10;
                    this.ctx.shadowBlur = 15; this.ctx.shadowColor = 'rgba(0,0,0,0.8)'; this.ctx.shadowOffsetY = 40;
                    
                    this.ctx.fillStyle = "#111"; 
                    this.ctx.beginPath(); this.ctx.arc(this.enemyBomberX, 40, 25, 0, Math.PI*2); this.ctx.fill();
                    this.ctx.beginPath(); this.ctx.moveTo(this.enemyBomberX + 15, 40); this.ctx.lineTo(this.enemyBomberX - 25, 10); this.ctx.lineTo(this.enemyBomberX - 10, 40); this.ctx.fill();
                    this.ctx.beginPath(); this.ctx.moveTo(this.enemyBomberX + 15, 40); this.ctx.lineTo(this.enemyBomberX - 25, 70); this.ctx.lineTo(this.enemyBomberX - 10, 40); this.ctx.fill();
                    this.ctx.shadowBlur = 0; this.ctx.shadowOffsetY = 0;
                    
                    if (this.enemyBomberX % 50 < 10) {
                        this.screenShake = 15;
                        this.particles.emit(this.enemyBomberX - 20, 150 + Math.random()*100, '#e74c3c', 30); 
                        
                        this.units.forEach(u => {
                            if (!this.isHiding) {
                                u.hp -= 200; 
                                this.addFloatingText("-200 Bom Địch", u.x, u.y, '#e74c3c');
                            } else {
                                this.addFloatingText("Né tránh", u.x, u.y, '#2ecc71');
                            }
                        });
                    }
                    if (this.enemyBomberX > this.canvas.width + 100) this.isEnemyBomberActive = false;
                }

                if (this.isPlaneActive) {
                    this.planeX += 8;
                    this.ctx.shadowBlur = 15; this.ctx.shadowColor = 'rgba(0,0,0,0.6)'; this.ctx.shadowOffsetY = 40;
                    this.ctx.fillStyle = "#34495e"; this.ctx.beginPath(); this.ctx.arc(this.planeX, 50, 20, 0, Math.PI*2); this.ctx.fill();
                    this.ctx.fillStyle = "#2c3e50";
                    this.ctx.beginPath(); this.ctx.moveTo(this.planeX - 10, 50); this.ctx.lineTo(this.planeX + 15, 50); this.ctx.lineTo(this.planeX - 15, 20); this.ctx.fill();
                    this.ctx.beginPath(); this.ctx.moveTo(this.planeX - 10, 50); this.ctx.lineTo(this.planeX + 15, 50); this.ctx.lineTo(this.planeX - 15, 80); this.ctx.fill();
                    this.ctx.shadowBlur = 0; this.ctx.shadowOffsetY = 0;
                    
                    if (this.planeX % 60 < 8) this.particles.emit(this.planeX, 60, '#f1c40f', 15); 
                    if (this.planeX > this.canvas.width + 100) this.isPlaneActive = false;
                }
            }
            
            drawBriefingScroll() {
                this.ctx.fillStyle = "rgba(0, 0, 0, 0.85)"; this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
                this.ctx.fillStyle = "#f5f5dc"; this.ctx.fillRect(130, 40, this.canvas.width - 260, 280);
                this.ctx.strokeStyle = "#d7ccc8"; this.ctx.lineWidth = 3; this.ctx.strokeRect(130, 40, this.canvas.width - 260, 280);

                this.ctx.fillStyle = "#111"; this.ctx.textAlign = "center";
                
                // LỜI DẪN TRUYỆN QUA TỪNG LEVEL
                if (this.level === 1) {
                    this.ctx.font = "bold 22px 'Segoe UI'"; this.ctx.fillText("Bảo Vệ Vùng Giải Phóng (Level 1)", this.canvas.width / 2, 85);
                    this.ctx.font = "14px 'Segoe UI'";
                    this.ctx.fillText("Kẻ địch sẽ dùng Không Quân rải bom thảm sát. Khi nghe CÒI BÁO ĐỘNG,", this.canvas.width / 2, 125);
                    this.ctx.fillText("hãy lập tức ấn nút [CHUI HẦM] để bảo toàn lực lượng!", this.canvas.width / 2, 148);
                } else if (this.level === 2) {
                    this.ctx.font = "bold 22px 'Segoe UI'"; this.ctx.fillText("Tập Kích Ban Đêm (Level 2)", this.canvas.width / 2, 85);
                    this.ctx.font = "14px 'Segoe UI'";
                    this.ctx.fillText("Địch đã gọi viện binh hùng hậu. Không quân của chúng ném bom rát hơn.", this.canvas.width / 2, 125);
                    this.ctx.fillText("Máu và sát thương lính địch tăng 50%. Hãy cẩn thận phòng tuyến!", this.canvas.width / 2, 148);
                } else if (this.level === 3) {
                    this.ctx.font = "bold 22px 'Segoe UI'"; this.ctx.fillText("Hoàng Hôn Đẫm Máu (Level 3)", this.canvas.width / 2, 85);
                    this.ctx.font = "14px 'Segoe UI'";
                    this.ctx.fillText("Trận chiến quyết định! Kẻ địch tung toàn bộ lực lượng tinh nhuệ nhất.", this.canvas.width / 2, 125);
                    this.ctx.fillText("Sức mạnh địch tăng gấp đôi! Hãy dùng mọi nguồn lực để chiến thắng!", this.canvas.width / 2, 148);
                }

                this.ctx.fillStyle = "#c0392b"; this.ctx.font = "bold 15px 'Segoe UI'";
                this.ctx.fillText("Quyết tử cho Tổ quốc quyết sinh!", this.canvas.width / 2, 190);

                this.ctx.fillStyle = "#1b4f72"; this.ctx.fillRect(this.canvas.width / 2 - 60, 235, 120, 40);
                this.ctx.fillStyle = "#fff"; this.ctx.font = "bold 16px 'Segoe UI'";
                this.ctx.fillText("XUẤT QUÂN", this.canvas.width / 2, 260);
                this.ctx.textAlign = "left";
            }

            drawMenuOverlay(title, subtitle, btnText, color) {
                this.ctx.fillStyle = "rgba(0, 0, 0, 0.85)"; this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
                this.ctx.fillStyle = color; this.ctx.font = "bold 32px 'Segoe UI'"; this.ctx.textAlign = "center";
                this.ctx.fillText(title, this.canvas.width / 2, this.canvas.height / 2 - 20);
                this.ctx.fillStyle = "#fff"; this.ctx.font = "16px 'Segoe UI'";
                this.ctx.fillText(subtitle, this.canvas.width / 2, this.canvas.height / 2 + 10);
                
                this.ctx.fillStyle = "#34495e"; this.ctx.fillRect(this.canvas.width / 2 - 100, this.canvas.height / 2 + 40, 200, 45);
                this.ctx.fillStyle = "#fff"; this.ctx.font = "bold 16px 'Segoe UI'";
                this.ctx.fillText(btnText, this.canvas.width / 2, this.canvas.height / 2 + 68);
                this.ctx.textAlign = "left";
            }

            run() {
                if (this.statueHp <= 0) {
                    this.gameOver = true;
                    this.drawMenuOverlay("💀 CĂN CỨ ĐÃ THẤT THỦ!", "Thất bại tại Level " + this.level, "BẤM VÀO ĐÂY ĐỂ CHƠI LẠI", "#e74c3c");
                    return;
                }
                
                if (this.enemyStatueHp <= 0 && !this.levelComplete && !this.gameOver) {
                    if (this.level >= this.maxLevel) {
                        this.gameOver = true;
                        this.drawMenuOverlay("⭐ CHIẾN THẮNG CUỐI CÙNG!", "Giải phóng hoàn toàn đất nước!", "BẤM ĐỂ CHƠI LẠI TỪ ĐẦU", "#f1c40f");
                    } else {
                        this.levelComplete = true;
                        this.drawMenuOverlay("🎖️ HOÀN THÀNH LEVEL " + this.level, "Căn cứ địch đã bị phá hủy. Hãy tiến sang khu vực tiếp theo!", "BẤM VÀO ĐÂY ĐỂ QUA MÀN", "#2ecc71");
                    }
                    return; // Lệnh này giúp dừng vòng lặp hiện tại, chờ click chuột để sang level mới
                }

                this.animFrame++;
                this.ctx.save();
                if (this.screenShake > 0) {
                    this.screenShake--; this.ctx.translate((Math.random() - 0.5) * 10, (Math.random() - 0.5) * 10);
                }

                this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                this.drawScene();

                if (this.showBriefing) {
                    this.drawBriefingScroll(); this.ctx.restore(); requestAnimationFrame(() => this.run()); return;
                }

                if (this.airRaidWarning > 0) {
                    this.airRaidWarning--;
                    if (this.airRaidWarning === 1) {
                        this.isEnemyBomberActive = true; this.enemyBomberX = -100;
                    }
                }

                this.particles.updateAndDraw(this.ctx);

                this.units.forEach((u, idx) => {
                    if (u.isSpinning > 0) u.isSpinning--;
                    
                    if (this.isHiding && u.type !== 'miner') {
                        // Nằm im chui hầm
                    } else {
                        if (u.type === 'miner') {
                            if (u.mineTarget) {
                                let moveSpeed = this.isHiding ? u.speed * 0.3 : u.speed; 
                                if (u.state === 'going') {
                                    let dx = u.mineTarget.x - u.x; let dy = u.mineTarget.y - u.y; let dist = Math.hypot(dx, dy);
                                    if (dist > 3) { u.x += (dx / dist) * moveSpeed; u.y += (dy / dist) * moveSpeed; }
                                    else { u.state = 'mining'; }
                                } else if (u.state === 'mining') {
                                    u.goldBag = 15 * this.techLevel; u.state = 'returning';
                                } else if (u.state === 'returning') {
                                    let dx = 70 - u.x; let dy = 180 - u.y; let dist = Math.hypot(dx, dy);
                                    if (dist > 3) { u.x += (dx / dist) * moveSpeed; u.y += (dy / dist) * moveSpeed; }
                                    else {
                                        this.gold += u.goldBag || 15; u.goldBag = 0; u.state = 'going';
                                        this.particles.emit(70, 180, '#f1c40f', 8);
                                        this.addFloatingText("+" + (15 * this.techLevel) + " Lương", 70, 180, '#f1c40f');
                                        this.updateUI();
                                    }
                                }
                            }
                        } else {
                            let nearestEnemy = this.enemies.find(e => Math.hypot(e.x - u.x, e.y - u.y) <= u.range);
                            if (nearestEnemy) {
                                if (u.attackCd > 0) u.attackCd--;
                                else {
                                    nearestEnemy.hp -= u.dmg; this.particles.emit(nearestEnemy.x, nearestEnemy.y, '#e74c3c', 6);
                                    this.addFloatingText("-" + Math.floor(u.dmg), nearestEnemy.x, nearestEnemy.y - 15, '#e74c3c');
                                    u.attackCd = 28;
                                }
                            } else {
                                let targetX = this.currentCommand === 'ATTACK' ? this.canvas.width - 70 : 280;
                                if (u.x < targetX) { u.x += u.speed; }
                                else if (this.currentCommand === 'ATTACK' && u.x >= this.canvas.width - 80) {
                                    if (u.attackCd > 0) u.attackCd--;
                                    else {
                                        this.enemyStatueHp -= u.dmg; this.particles.emit(this.canvas.width - 60, 160, '#f1c40f', 10);
                                        this.addFloatingText("-" + Math.floor(u.dmg), this.canvas.width - 60, 160, '#f1c40f');
                                        u.attackCd = 35; this.updateUI();
                                    }
                                }
                            }
                        }
                    }
                    u.draw(this.ctx, this.animFrame, this.isHiding);
                    if (u.hp <= 0) this.units.splice(idx, 1);
                });

                this.enemies.forEach((e, idx) => {
                    let nearestUnit = this.units.find(u => u.type !== 'miner' && Math.hypot(u.x - e.x, u.y - e.y) <= e.range);
                    if (nearestUnit && !this.isHiding) { 
                        if (e.attackCd > 0) e.attackCd--;
                        else {
                            nearestUnit.hp -= e.dmg; this.particles.emit(nearestUnit.x, nearestUnit.y, '#f1c40f', 6);
                            this.addFloatingText("-" + Math.floor(e.dmg), nearestUnit.x, nearestUnit.y - 15, '#f1c40f');
                            e.attackCd = 32;
                        }
                    } else {
                        e.x -= e.speed;
                        if (e.x <= 70) {
                            if (e.attackCd > 0) e.attackCd--;
                            else {
                                this.statueHp -= e.dmg; this.particles.emit(50, 160, '#e74c3c', 10);
                                this.addFloatingText("-" + Math.floor(e.dmg), 50, 160, '#e74c3c');
                                e.attackCd = 38; this.updateUI();
                            }
                        }
                    }
                    e.draw(this.ctx, this.animFrame, false);
                    if (e.hp <= 0) { this.enemies.splice(idx, 1); this.gold += (35 + this.level*10); this.particles.emit(e.x, e.y, '#f1c40f', 12); this.updateUI(); }
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
            if (!GameManager.showBriefing && !GameManager.gameOver && !GameManager.levelComplete && GameManager.enemyStatueHp > 0 && GameManager.enemies.length < 30) {
                let types = ['goblin', 'orc', 'shadow_mage', 'giant'];
                let t = types[Math.floor(Math.random() * types.length)];
                let levelMult = 1 + (GameManager.level - 1) * 0.5; 
                let stats = {
                    goblin: { hp: 110 * levelMult, dmg: 14 * levelMult, range: 30, speed: 1.4, size: 0.95 },
                    orc: { hp: 230 * levelMult, dmg: 26 * levelMult, range: 35, speed: 1.0, size: 1.2 },
                    shadow_mage: { hp: 160 * levelMult, dmg: 38 * levelMult, range: 150, speed: 0.8, size: 1.05 },
                    giant: { hp: 650 * levelMult, dmg: 60 * levelMult, range: 50, speed: 0.5, size: 1.85 }
                }[t];
                GameManager.enemies.push(new GameObject(GameManager.canvas.width - 80, 130 + Math.random() * 180, t, true, stats));
            }
        }, 3200);

        setInterval(() => {
            if (!GameManager.showBriefing && !GameManager.gameOver && !GameManager.levelComplete && GameManager.level >= 1) {
                GameManager.triggerAirRaidWarning();
            }
        }, 40000);

        GameManager.run();
    </script>
</body>
</html>
"""

st.components.v1.html(game_html, height=580, scrolling=False)
