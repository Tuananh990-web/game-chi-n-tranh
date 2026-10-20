import streamlit as st

st.set_page_config(
    page_title="Kháng Chiến Việt Nam - Đại Cáo Bình Ngô",
    page_icon="⭐",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #050a0a; color: #ffffff; font-family: 'Segoe UI', Tahoma, sans-serif; }
    iframe { border-radius: 12px; box-shadow: 0 15px 50px rgba(0,0,0,0.98); border: 2px solid #f1c40f; }
    .title-text { text-align: center; color: #f1c40f; text-transform: uppercase; font-weight: 900; letter-spacing: 3px; margin-bottom: 0px; text-shadow: 0 0 10px #f1c40f; }
    .sub-text { text-align: center; color: #a3e4d7; font-size: 15px; margin-bottom: 10px; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-text'>⭐ KHÁNG CHIẾN VIỆT NAM - CHIẾN DỊCH TỔNG LỰC ⭐</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Đồ họa Hạt nâng cao, Đạn đạo (Tên, Pháo), Hiệu ứng Thời tiết & Viện binh Nhảy Dù!</p>", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Khang Chien Viet Nam Pro FX</title>
    <style>
        body { margin: 0; background: #050a0a; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; overflow: hidden; user-select: none; }
        canvas { border-radius: 8px; display: block; margin: 4px auto; cursor: crosshair; box-shadow: inset 0 0 50px rgba(0,0,0,0.8); }
        .ui-panel, .cmd-panel, .music-panel { display: flex; justify-content: center; flex-wrap: wrap; gap: 6px; margin-top: 5px; }
        .music-panel { background: rgba(17, 42, 46, 0.8); padding: 6px 15px; border-radius: 8px; border: 1px solid #f1c40f; width: fit-content; margin: 5px auto; }
        button { background: linear-gradient(145deg, #7d6608, #4a3c04); color: #fff; border: 1px solid #f1c40f; padding: 7px 14px; font-weight: bold; font-size: 12px; border-radius: 5px; cursor: pointer; transition: all 0.2s; text-transform: uppercase; text-shadow: 1px 1px 2px #000; box-shadow: 0 4px 6px rgba(0,0,0,0.5); }
        button:hover { background: #f1c40f; color: #000; transform: translateY(-2px); box-shadow: 0 6px 12px rgba(241,196,15,0.4); border-color: #fff; }
        button:active { transform: scale(0.95); }
        .cmd-btn { background: linear-gradient(145deg, #1b4f72, #0d283a); border-color: #5dade2; }
        .cmd-btn:hover { background: #5dade2; color: #000; }
        .bunker-btn { background: linear-gradient(145deg, #c0392b, #78281f); border-color: #e74c3c; animation: pulse 1.5s infinite; }
        .skill-btn { background: linear-gradient(145deg, #6c3483, #4a235a); border-color: #9b59b6; }
        .tech-btn { background: linear-gradient(145deg, #1e8449, #0e4324); border-color: #2ecc71; }
        .music-btn { background: linear-gradient(145deg, #922b21, #4a1510); border-color: #e74c3c; }
        .stats { font-size: 14px; font-weight: bold; color: #f1c40f; margin-bottom: 2px; text-shadow: 1px 1px 3px #000; background: rgba(0,0,0,0.5); padding: 4px; border-radius: 5px; display: inline-block; }
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.7); } 70% { box-shadow: 0 0 0 12px rgba(231, 76, 60, 0); } 100% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0); } }
    </style>
</head>
<body>

    <div class="stats">
        🚩 MÀN: <span id="levelText" style="color:#fff;">1</span> | 🏛️ THÀNH TA: <span id="hpText" style="color:#2ecc71;">3000</span> <span id="ourShield" style="color:#3498db; font-size:11px;"></span> | ⚔️ THÀNH ĐỊCH: <span id="enemyHpText" style="color:#e74c3c;">3000</span> <span id="enemyShield" style="color:#f1c40f; font-size:11px;"></span> | 🌾 LƯƠNG: <span id="goldText" style="color:#f1c40f;">450</span> | 👥 QUÂN: <span id="popText" style="color:#fff;">0</span>/100
    </div>

    <canvas id="gameCanvas" width="1020" height="400"></canvas>

    <div class="music-panel">
        <span style="font-size:13px; font-weight:900; color:#f1c40f;">🎵 ÂM THANH:</span>
        <button class="music-btn" onclick="playExternalMusic('https://upload.wikimedia.org/wikipedia/commons/e/e5/Tien_Quan_Ca_instrumental.ogg')">🎶 Tiến Quân Ca</button>
        <button class="music-btn" onclick="playMarchTone()">🎺 Kèn Báo Động</button>
        <button class="music-btn" onclick="stopAllAudio()">🔇 Tắt Nhạc</button>
    </div>

    <div class="cmd-panel">
        <button class="cmd-btn" id="btnAttack">⚔️ TẤN CÔNG ĐỊCH</button>
        <button class="cmd-btn" id="btnDefend">🛡️ LÙI VỀ PHÒNG THỦ</button>
        <button class="bunker-btn" id="btnBunker">🕳️ CHUI HẦM BẢO TOÀN LỰC LƯỢNG</button>
        <button class="tech-btn" id="btnTech">⬆️ NÂNG CẤP HỎA LỰC (150G)</button>
        <button class="skill-btn" id="btnEarth">💣 GỌI KHÔNG QUÂN NÉM BOM</button>
    </div>

    <div class="ui-panel">
        <button id="spawnMiner">🌾 Dân Quân (30g)</button>
        <button id="spawnSwordwrath">🗡️ Du Kích Dao Quắm (40g)</button>
        <button id="spawnArchidon">🔫 Xạ Thủ Súng Trường (50g)</button>
        <button id="spawnSpearton">🛡️ Tự Vệ Khiên (70g)</button>
        <button id="spawnMagikill">⭐ Cán Bộ Truyền Tin (100g)</button>
        <button id="spawnGiant">🚜 Thiết Giáp (160g)</button>
    </div>

    <script>
        // ================= AUDIO ENGINE =================
        let bgMusic = new Audio(); bgMusic.loop = true; bgMusic.volume = 0.5;
        function playExternalMusic(url) { bgMusic.src = url; bgMusic.play().catch(e => console.log("Blocked by browser auto-play policy")); }
        let audioCtx = null; let isPlayingLoop = false; let soundTimer = null;
        function initAudio() { if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)(); if (audioCtx.state === 'suspended') audioCtx.resume(); }
        
        function playMarchTone() {
            initAudio(); stopWebAudio(); isPlayingLoop = true;
            let notes = [392.00, 523.25, 659.25, 523.25]; let noteIdx = 0;
            soundTimer = setInterval(() => {
                if (!isPlayingLoop) return;
                let osc = audioCtx.createOscillator(); let gain = audioCtx.createGain();
                osc.type = 'square'; osc.frequency.value = notes[noteIdx % notes.length];
                gain.gain.setValueAtTime(0.1, audioCtx.currentTime); gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.4);
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.start(); osc.stop(audioCtx.currentTime + 0.4); noteIdx++;
            }, 400);
        }
        function playAirRaidSiren() {
            initAudio(); stopWebAudio(); isPlayingLoop = true;
            let osc = audioCtx.createOscillator(); let gain = audioCtx.createGain();
            osc.type = 'sawtooth'; osc.frequency.setValueAtTime(400, audioCtx.currentTime); 
            osc.frequency.linearRampToValueAtTime(800, audioCtx.currentTime + 2.0);
            osc.frequency.linearRampToValueAtTime(400, audioCtx.currentTime + 4.0);
            gain.gain.setValueAtTime(0.2, audioCtx.currentTime); gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 4.0);
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.start(); osc.stop(audioCtx.currentTime + 4.0);
        }
        function stopWebAudio() { isPlayingLoop = false; if (soundTimer) clearInterval(soundTimer); }
        function stopAllAudio() { bgMusic.pause(); stopWebAudio(); }

        // ================= GRAPHICS ENGINE =================
        class ParticleSystem {
            constructor() { this.particles = []; }
            emit(x, y, color, count = 15, isBlood = false) {
                for (let i = 0; i < count; i++) {
                    this.particles.push({
                        x, y, 
                        vx: (Math.random() - 0.5) * (isBlood ? 6 : 10), 
                        vy: (Math.random() - 0.5) * 10 - 2,
                        radius: Math.random() * (isBlood ? 4 : 5) + 1, 
                        color, alpha: 1.0, 
                        decay: Math.random() * 0.03 + 0.02,
                        gravity: isBlood ? 0.2 : 0.05
                    });
                }
            }
            updateAndDraw(ctx) {
                this.particles.forEach((p, idx) => {
                    p.vy += p.gravity; // Trọng lực
                    p.x += p.vx; p.y += p.vy; p.alpha -= p.decay;
                    ctx.fillStyle = p.color; ctx.globalAlpha = Math.max(0, p.alpha);
                    ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2); ctx.fill();
                    ctx.globalAlpha = 1.0;
                    if (p.alpha <= 0 || p.y > 400) this.particles.splice(idx, 1);
                });
            }
        }

        // HỆ THỐNG ĐẠN ĐẠO (TÊN, ĐẠN PHÁO, LỬA)
        class Projectile {
            constructor(x, y, target, type, dmg, isEnemy) {
                this.x = x; this.y = y; this.target = target; this.type = type; this.dmg = dmg; this.isEnemy = isEnemy;
                this.speed = type === 'arrow' ? 8 : (type === 'cannon' ? 12 : 5);
                this.active = true;
                
                // Tính toán góc bắn
                let dx = target.x - x; let dy = target.y - y;
                let dist = Math.hypot(dx, dy);
                this.vx = (dx / dist) * this.speed; this.vy = (dy / dist) * this.speed;
                this.angle = Math.atan2(dy, dx);
            }
            updateAndDraw(ctx, particles) {
                if (!this.active) return;
                this.x += this.vx; this.y += this.vy;

                ctx.save(); ctx.translate(this.x, this.y); ctx.rotate(this.angle);
                
                if (this.type === 'arrow') {
                    // Mũi tên
                    ctx.fillStyle = "#ecf0f1"; ctx.fillRect(-6, -1, 12, 2);
                    ctx.fillStyle = "#bdc3c7"; ctx.beginPath(); ctx.moveTo(6, -2); ctx.lineTo(10, 0); ctx.lineTo(6, 2); ctx.fill();
                } else if (this.type === 'cannon') {
                    // Đạn pháo
                    ctx.fillStyle = "#e67e22"; ctx.beginPath(); ctx.arc(0, 0, 4, 0, Math.PI*2); ctx.fill();
                    particles.emit(this.x, this.y, '#f39c12', 1); // Khói đạn
                } else if (this.type === 'magic') {
                    // Quả cầu lửa
                    ctx.shadowBlur = 10; ctx.shadowColor = "#3498db";
                    ctx.fillStyle = this.isEnemy ? "#c0392b" : "#3498db";
                    ctx.beginPath(); ctx.arc(0, 0, 5 + Math.random()*2, 0, Math.PI*2); ctx.fill();
                    particles.emit(this.x, this.y, this.isEnemy ? '#e74c3c' : '#3498db', 2);
                }
                ctx.restore();

                // Va chạm
                if (this.target && this.target.hp > 0) {
                    let hitDist = Math.hypot(this.target.x - this.x, this.target.y - this.y);
                    if (hitDist < 20) {
                        this.target.hp -= this.dmg;
                        particles.emit(this.x, this.y, this.type==='cannon'?'#e74c3c':'#f1c40f', this.type==='cannon'?15:5);
                        this.active = false;
                    }
                } else if (!this.target || this.target.hp <= 0) {
                    this.active = false; // Mất mục tiêu
                }
            }
        }

        class GameObject {
            constructor(x, y, type, isEnemy, stats, techLevel = 1) {
                this.x = x; this.y = y; this.type = type; this.isEnemy = isEnemy;
                this.hp = stats.hp; this.maxHp = stats.hp; this.dmg = stats.dmg;
                this.range = stats.range; this.speed = stats.speed; this.size = stats.size;
                
                this.attackCd = 0; this.maxCd = type === 'giant' ? 80 : 35; 
                this.state = 'spawning'; // Hiệu ứng nhảy dù/xuất hiện
                this.spawnY = -50; 
                this.goldBag = 0; this.mineTarget = null; this.techLevel = techLevel;
            }
            
            draw(ctx, animFrame, isHiding = false) {
                ctx.save();
                
                // Hiệu ứng Nhảy dù xuất hiện (Viện binh)
                if (this.state === 'spawning') {
                    this.spawnY += 5;
                    ctx.translate(this.x, this.spawnY);
                    if (this.spawnY >= this.y) { this.state = 'going'; this.spawnY = this.y; }
                    
                    // Vẽ Dù
                    if(this.spawnY < this.y - 10) {
                        ctx.fillStyle = "#ecf0f1"; ctx.beginPath(); ctx.arc(0, -40, 20, Math.PI, 0); ctx.fill();
                        ctx.strokeStyle = "#fff"; ctx.lineWidth=1;
                        ctx.beginPath(); ctx.moveTo(-20, -40); ctx.lineTo(0, -10); ctx.stroke();
                        ctx.beginPath(); ctx.moveTo(20, -40); ctx.lineTo(0, -10); ctx.stroke();
                    }
                } else {
                    ctx.translate(this.x, this.y);
                }

                // Chui hầm nằm sấp
                if (!this.isEnemy && isHiding && this.type !== 'giant') {
                    ctx.rotate(Math.PI / 2); ctx.translate(15, -15);
                }

                // Lật hình cho phe địch
                if (this.isEnemy) { ctx.scale(-1, 1); }

                ctx.shadowColor = 'rgba(0, 0, 0, 0.4)'; ctx.shadowBlur = 5; ctx.shadowOffsetY = 4;

                let colorTa = '#2980b9'; let colorDich = '#c0392b';
                let unitColor = this.isEnemy ? colorDich : colorTa;
                if (this.type === 'miner') unitColor = '#d35400';
                else if (this.type === 'giant') unitColor = this.isEnemy ? '#641e16' : '#273746'; // Camo đậm

                if (this.type === 'giant') {
                    // XE TĂNG (CÓ HIỆU ỨNG GIẬT NÒNG KHI BẮN)
                    ctx.fillStyle = unitColor;
                    if(ctx.roundRect) ctx.roundRect(-30, -20, 60, 25, 4); else ctx.fillRect(-30, -20, 60, 25);
                    ctx.fill();
                    
                    // Bánh xích quay
                    ctx.fillStyle = "#111"; ctx.fillRect(-32, 5, 64, 10); 
                    ctx.fillStyle = "#7f8c8d";
                    let treadOffset = (animFrame % 10) - 20;
                    for(let i=treadOffset; i<=30; i+=12) { ctx.beginPath(); ctx.arc(i, 10, 4, 0, Math.PI*2); ctx.fill(); }
                    
                    // Tháp pháo và Nòng pháo giật lùi
                    ctx.fillStyle = "#2c3e50"; ctx.beginPath(); ctx.arc(0, -20, 14, Math.PI, 0); ctx.fill();
                    let recoil = (this.attackCd > this.maxCd - 8) ? -8 : 0; // Giật lùi
                    ctx.lineWidth = 5; ctx.strokeStyle = "#000";
                    ctx.beginPath(); ctx.moveTo(0, -25); ctx.lineTo(40 + recoil, -25); ctx.stroke();
                } else {
                    // BỘ BINH
                    ctx.fillStyle = "#f1c40f"; // Da vàng
                    ctx.beginPath(); ctx.arc(0, -18 * this.size, 6 * this.size, 0, Math.PI * 2); ctx.fill();
                    
                    // Mũ
                    ctx.fillStyle = this.isEnemy ? "#922b21" : "#145a32"; 
                    ctx.fillRect(-7 * this.size, -24 * this.size, 14 * this.size, 5 * this.size); 
                    if (!this.isEnemy && this.techLevel > 1) {
                        ctx.fillStyle = "#f1c40f"; ctx.fillRect(-2 * this.size, -23 * this.size, 4 * this.size, 3 * this.size); 
                    }

                    // Thân áo
                    ctx.fillStyle = unitColor;
                    ctx.fillRect(-6 * this.size, -12 * this.size, 12 * this.size, 14 * this.size); 

                    // VŨ KHÍ & ANIMATION ĐÁNH
                    let armAngle = 0;
                    if (this.attackCd > this.maxCd - 10) armAngle = Math.PI/3; // Vung tay khi đánh

                    ctx.save();
                    ctx.translate(0, -8);
                    ctx.rotate(armAngle);
                    if (this.type === 'archidon') {
                        // Súng / Cung
                        ctx.fillStyle = "#111"; ctx.fillRect(0, -2, 20, 4); 
                        ctx.fillStyle = "#8d6e63"; ctx.fillRect(2, 0, 4, 5); 
                    } else if (this.type === 'spearton') {
                        // Giáo và Khiên
                        ctx.fillStyle = "#7f8c8d"; ctx.fillRect(-2, -15, 4, 30); // Giáo
                        ctx.fillStyle = "#34495e"; ctx.fillRect(5, -10, 6, 25); // Khiên
                    } else if (this.type === 'swordwrath') {
                        // Đao / Mã tấu
                        ctx.fillStyle = "#bdc3c7";
                        ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(15, -15); ctx.lineTo(18, -10); ctx.fill();
                    } else if (this.type === 'magikill') {
                        // Trượng chỉ huy
                        ctx.fillStyle = "#f39c12"; ctx.fillRect(5, -20, 3, 30);
                        ctx.fillStyle = "#e74c3c"; ctx.beginPath(); ctx.arc(6, -20, 5, 0, Math.PI*2); ctx.fill();
                    }
                    ctx.restore();

                    // Chân cử động
                    ctx.shadowColor = 'transparent'; 
                    ctx.strokeStyle = "#111"; ctx.lineWidth = 4 * this.size;
                    let swing = 0;
                    if ((this.state === 'going' || this.state === 'returning') && !isHiding) {
                        swing = Math.sin(animFrame * 0.5) * 8;
                    }
                    ctx.beginPath(); ctx.moveTo(-3, 2 * this.size); ctx.lineTo(-5 * this.size, 12 * this.size + swing); ctx.stroke();
                    ctx.beginPath(); ctx.moveTo(3, 2 * this.size); ctx.lineTo(5 * this.size, 12 * this.size - swing); ctx.stroke();
                }

                // THANH MÁU
                ctx.shadowColor = 'transparent'; 
                ctx.fillStyle = "#000"; ctx.fillRect(-15, -45, 30, 5);
                let hpPercent = Math.max(0, this.hp / this.maxHp);
                ctx.fillStyle = hpPercent > 0.5 ? "#2ecc71" : (hpPercent > 0.2 ? "#f1c40f" : "#e74c3c");
                ctx.fillRect(-15, -45, 30 * hpPercent, 5);
                
                ctx.restore();
            }
        }

        class RTSGameManager {
            constructor() {
                this.canvas = document.getElementById("gameCanvas");
                this.ctx = this.canvas.getContext("2d");
                this.level = 1; this.maxLevel = 3;
                this.statueHp = 3000; this.enemyStatueHp = 3000;
                this.gold = 500; this.techLevel = 1; this.currentCommand = 'ATTACK';
                this.gameOver = false; this.levelComplete = false; this.showBriefing = true; 
                this.screenShake = 0; this.animFrame = 0; 
                
                this.isHiding = false; 
                this.airRaidWarning = 0; this.airRaidTimer = 0; 
                this.enemyBomberX = -200; this.isEnemyBomberActive = false;
                this.planeX = -100; this.isPlaneActive = false; 
                
                // Cơ chế Tử thủ viện binh
                this.ourEmergencyTriggered = false; this.enemyEmergencyTriggered = false;
                this.ourShieldTimer = 0; this.enemyShieldTimer = 0;

                this.particles = new ParticleSystem();
                this.projectiles = []; // Quản lý đạn bay
                
                this.goldMines = [
                    { x: 180, y: 150, miner: null }, { x: 230, y: 200, miner: null }, { x: 280, y: 260, miner: null },
                    { x: 200, y: 320, miner: null }, { x: 260, y: 130, miner: null }, { x: 310, y: 180, miner: null }
                ];
                this.units = []; this.enemies = []; this.floatingTexts = [];
                
                // Map Đẹp Hơn
                this.mapColors = {
                    1: { sky: 'linear-gradient(to bottom, #5dade2 0%, #aed6f1 60%, #2ecc71 60%, #27ae60 100%)', sun: true, clouds: true }, 
                    2: { sky: 'linear-gradient(to bottom, #154360 0%, #2980b9 55%, #1e8449 55%, #145a32 100%)', moon: true, stars: true }, 
                    3: { sky: 'linear-gradient(to bottom, #641e16 0%, #c0392b 55%, #7e5109 55%, #4a235a 100%)', rain: true, lightning: true }  
                };
                
                this.clouds = Array.from({length: 8}, () => ({x: Math.random()*1200, y: 20+Math.random()*80, speed: 0.1+Math.random()*0.3, scale: 0.5+Math.random()*1}));
                this.stars = Array.from({length: 80}, () => ({x: Math.random()*1200, y: Math.random()*200, radius: Math.random()*1.5+0.5, blink: Math.random()*0.1}));
                this.rain = Array.from({length: 150}, () => ({x: Math.random()*1200, y: Math.random()*400, speedY: 15+Math.random()*10, speedX: -3-Math.random()*4}));

                this.initListeners();
            }
            
            initListeners() {
                this.canvas.addEventListener('click', (e) => {
                    initAudio();
                    const rect = this.canvas.getBoundingClientRect();
                    const mouseX = e.clientX - rect.left; const mouseY = e.clientY - rect.top;
                    
                    if (this.showBriefing) { this.showBriefing = false; return; }
                    if (this.levelComplete) { this.nextLevel(); return; }
                    if (this.gameOver) { this.resetGame(true); this.showBriefing = true; this.run(); return; }
                });

                document.getElementById('btnAttack').onclick = () => this.setCommand('ATTACK');
                document.getElementById('btnDefend').onclick = () => this.setCommand('DEFEND');
                
                let btnBunker = document.getElementById('btnBunker');
                btnBunker.onclick = () => {
                    this.isHiding = !this.isHiding;
                    if(this.isHiding) {
                        btnBunker.style.background = "linear-gradient(145deg, #2ecc71, #27ae60)"; btnBunker.innerText = "🏃 ĐANG TRÚ ẨN (BẤM ĐỂ DẬY)";
                        this.addFloatingText("Toàn quân Chui Hầm!", this.canvas.width/2, 200, '#2ecc71');
                    } else {
                        btnBunker.style.background = "linear-gradient(145deg, #c0392b, #78281f)"; btnBunker.innerText = "🕳️ CHUI HẦM BẢO TOÀN LỰC LƯỢNG";
                        this.addFloatingText("Toàn quân Tấn Công!", this.canvas.width/2, 200, '#e74c3c');
                    }
                };

                document.getElementById('btnTech').onclick = () => this.upgradeTech();
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
                this.airRaidWarning = 200; playAirRaidSiren();
            }

            nextLevel() {
                this.level++; if (this.level > this.maxLevel) { this.gameOver = true; return; }
                this.canvas.style.background = this.mapColors[this.level].sky;
                this.resetGame(false); this.showBriefing = true; this.run(); 
            }

            resetGame(fullReset = true) {
                if(fullReset) { this.level = 1; this.canvas.style.background = this.mapColors[1].sky; this.techLevel = 1; this.gold = 500; }
                else { this.gold += 800; } 
                
                this.statueHp = 3000; this.enemyStatueHp = 3000 + (this.level * 2000); 
                this.units = []; this.enemies = []; this.floatingTexts = []; this.projectiles = [];
                this.isHiding = false; document.getElementById('btnBunker').style.background = "linear-gradient(145deg, #c0392b, #78281f)"; document.getElementById('btnBunker').innerText = "🕳️ CHUI HẦM BẢO TOÀN LỰC LƯỢNG";
                this.airRaidWarning = 0; this.isEnemyBomberActive = false; this.airRaidTimer = 0; 
                
                this.ourEmergencyTriggered = false; this.enemyEmergencyTriggered = false;
                this.ourShieldTimer = 0; this.enemyShieldTimer = 0;
                
                this.goldMines.forEach(m => m.miner = null);
                this.gameOver = false; this.levelComplete = false;
                document.getElementById("levelText").innerText = this.level;
                this.updateUI();
            }

            setCommand(cmd) { this.currentCommand = cmd; this.isHiding = false; document.getElementById('btnBunker').style.background = "linear-gradient(145deg, #c0392b, #78281f)"; document.getElementById('btnBunker').innerText = "🕳️ CHUI HẦM BẢO TOÀN LỰC LƯỢNG"; }
            addFloatingText(text, x, y, color = '#f1c40f', isBig=false) { this.floatingTexts.push({ text, x, y, alpha: 1.0, color, isBig }); }
            getCurrentPopulation() { let count = 0; this.units.forEach(u => { if (u.type === 'spearton') count += 3; else if (u.type === 'magikill') count += 5; else if (u.type === 'giant') count += 4; else count += 1; }); return count; }

            upgradeTech() {
                if (this.showBriefing || this.gameOver || this.levelComplete) return;
                if (this.gold >= 150 && this.techLevel < 3) {
                    this.gold -= 150; this.techLevel++;
                    this.units.forEach(u => { u.techLevel = this.techLevel; u.dmg = Math.floor(u.dmg * 1.3); u.maxHp = Math.floor(u.maxHp * 1.25); u.hp = u.maxHp; });
                    this.particles.emit(120, 200, '#2ecc71', 50);
                    this.addFloatingText("⭐ NÂNG CẤP HỎA LỰC LEVEL " + this.techLevel, 120, 100, '#2ecc71', true);
                    this.updateUI();
                }
            }

            triggerSkill(type) {
                if (this.showBriefing || this.gameOver || this.levelComplete) return;
                if (type === 'earthquake' && this.gold >= 100) {
                    this.gold -= 100;
                    this.isPlaneActive = true; this.planeX = -100; this.screenShake = 40;
                    this.particles.emit(this.canvas.width / 2, this.canvas.height / 2, '#e74c3c', 80);
                    this.enemies.forEach(e => { e.hp -= (150 * this.techLevel); this.particles.emit(e.x, e.y, '#e74c3c', 15); this.addFloatingText("-" + (150 * this.techLevel), e.x, e.y, '#e74c3c', true); });
                }
            }

            spawnUnit(type) {
                if (this.showBriefing || this.gameOver || this.levelComplete) return;
                let costs = { miner: 30, swordwrath: 40, archidon: 50, spearton: 70, magikill: 100, giant: 160 };
                let pops = { miner: 1, swordwrath: 1, archidon: 1, spearton: 3, magikill: 5, giant: 4 };
                let stats = {
                    miner: { hp: 120, dmg: 8, range: 30, speed: 1.6, size: 0.95 },
                    swordwrath: { hp: 180, dmg: 24, range: 40, speed: 1.4, size: 1.0 },
                    archidon: { hp: 130, dmg: 32, range: 240, speed: 1.2, size: 1.0 },
                    spearton: { hp: 300, dmg: 40, range: 65, speed: 1.0, size: 1.2 },
                    magikill: { hp: 150, dmg: 55, range: 220, speed: 0.9, size: 1.05 },
                    giant: { hp: 900, dmg: 85, range: 250, speed: 0.6, size: 1.95 } // Xe tăng bắn xa
                }[type];

                if (this.gold >= costs[type] && this.getCurrentPopulation() + pops[type] <= 100) {
                    this.gold -= costs[type];
                    let unit = new GameObject(110, 150 + Math.random() * 200, type, false, {
                        hp: stats.hp * (1 + (this.techLevel - 1) * 0.25), dmg: stats.dmg * (1 + (this.techLevel - 1) * 0.3), range: stats.range, speed: stats.speed, size: stats.size
                    }, this.techLevel);

                    if (type === 'miner') {
                        let freeMine = this.goldMines.find(m => !m.miner);
                        if (freeMine) { freeMine.miner = unit; unit.mineTarget = freeMine; } else { unit.mineTarget = this.goldMines[0]; }
                    }
                    this.units.push(unit); this.particles.emit(unit.x, unit.y, '#3498db', 10); this.updateUI();
                }
            }

            updateUI() {
                document.getElementById("hpText").innerText = Math.max(0, Math.floor(this.statueHp));
                document.getElementById("enemyHpText").innerText = Math.max(0, Math.floor(this.enemyStatueHp));
                document.getElementById("goldText").innerText = Math.floor(this.gold);
                document.getElementById("popText").innerText = this.getCurrentPopulation();
                
                if(this.ourShieldTimer > 0) document.getElementById("ourShield").innerText = `(GIÁP TỬ THỦ: ${Math.ceil(this.ourShieldTimer/60)}s)`;
                else document.getElementById("ourShield").innerText = "";
                
                if(this.enemyShieldTimer > 0) document.getElementById("enemyShield").innerText = `(GIÁP TỬ THỦ: ${Math.ceil(this.enemyShieldTimer/60)}s)`;
                else document.getElementById("enemyShield").innerText = "";
            }

            drawEnvironment() {
                let env = this.mapColors[this.level];
                // Mặt đất xa gần
                this.ctx.fillStyle = "rgba(0,0,0,0.2)"; this.ctx.fillRect(0, 150, this.canvas.width, 250);
                
                if(env.sun) {
                    this.ctx.fillStyle = "rgba(241, 196, 15, 0.8)"; this.ctx.shadowBlur = 40; this.ctx.shadowColor = "#f1c40f";
                    this.ctx.beginPath(); this.ctx.arc(100, 60, 30, 0, Math.PI*2); this.ctx.fill(); this.ctx.shadowBlur = 0;
                }
                if(env.clouds) {
                    this.ctx.fillStyle = "rgba(255, 255, 255, 0.6)";
                    this.clouds.forEach(c => {
                        c.x += c.speed; if (c.x > this.canvas.width + 50) c.x = -50;
                        this.ctx.beginPath(); this.ctx.arc(c.x, c.y, 20*c.scale, 0, Math.PI*2); this.ctx.fill();
                        this.ctx.beginPath(); this.ctx.arc(c.x+20*c.scale, c.y-15*c.scale, 25*c.scale, 0, Math.PI*2); this.ctx.fill();
                        this.ctx.beginPath(); this.ctx.arc(c.x+40*c.scale, c.y, 20*c.scale, 0, Math.PI*2); this.ctx.fill();
                    });
                }
                if(env.moon) {
                    this.ctx.fillStyle = "#ecf0f1"; this.ctx.shadowBlur = 30; this.ctx.shadowColor = "#ecf0f1";
                    this.ctx.beginPath(); this.ctx.arc(120, 60, 25, 0, Math.PI*2); this.ctx.fill(); 
                    this.ctx.fillStyle = "rgba(21, 67, 96, 1)"; this.ctx.beginPath(); this.ctx.arc(130, 55, 20, 0, Math.PI*2); this.ctx.fill(); // Nguyệt thực
                    this.ctx.shadowBlur = 0;
                }
                if(env.stars) {
                    this.ctx.fillStyle = "#fff";
                    this.stars.forEach(s => {
                        s.alpha = 0.5 + Math.sin(this.animFrame * s.blink + s.x) * 0.5;
                        this.ctx.globalAlpha = Math.max(0, s.alpha);
                        this.ctx.beginPath(); this.ctx.arc(s.x, s.y, s.radius, 0, Math.PI*2); this.ctx.fill();
                    });
                    this.ctx.globalAlpha = 1.0;
                }
                if(env.lightning && Math.random() < 0.01) {
                    this.ctx.fillStyle = "rgba(255,255,255,0.4)"; this.ctx.fillRect(0,0,this.canvas.width, this.canvas.height);
                    this.screenShake = 10;
                }
            }
            
            drawRain() {
                if(this.mapColors[this.level].rain) {
                    this.ctx.strokeStyle = "rgba(174, 214, 241, 0.5)"; this.ctx.lineWidth = 2;
                    this.rain.forEach(r => {
                        r.y += r.speedY; r.x += r.speedX;
                        if (r.y > this.canvas.height) { r.y = -20; r.x = Math.random() * (this.canvas.width+400); }
                        this.ctx.beginPath(); this.ctx.moveTo(r.x, r.y); this.ctx.lineTo(r.x - r.speedX, r.y - r.speedY); this.ctx.stroke();
                    });
                }
            }

            drawBases() {
                // Thành Ta
                this.ctx.shadowBlur = 10; this.ctx.shadowColor = "#000";
                this.ctx.fillStyle = "#5d4037"; this.ctx.fillRect(10, 100, 80, 300); // Tường gạch
                this.ctx.fillStyle = "#3e2723"; this.ctx.fillRect(10, 80, 20, 30); this.ctx.fillRect(40, 80, 20, 30); this.ctx.fillRect(70, 80, 20, 30); // Răng cưa
                
                // Lá chắn tử thủ ta
                if(this.ourShieldTimer > 0) {
                    this.ctx.shadowBlur = 30; this.ctx.shadowColor = "#3498db";
                    this.ctx.strokeStyle = `rgba(52, 152, 219, ${0.5 + Math.sin(this.animFrame*0.1)*0.3})`;
                    this.ctx.lineWidth = 8;
                    this.ctx.beginPath(); this.ctx.arc(50, 250, 140, -Math.PI/2, Math.PI/2); this.ctx.stroke();
                    this.ctx.shadowBlur = 0;
                }

                // Cột Cờ sao vàng
                this.ctx.fillStyle = "#bdc3c7"; this.ctx.fillRect(50, 10, 4, 80);
                this.ctx.fillStyle = "#e74c3c"; 
                this.ctx.beginPath(); this.ctx.moveTo(54, 15); this.ctx.lineTo(95, 30 + Math.sin(this.animFrame*0.15)*10); this.ctx.lineTo(54, 55); this.ctx.fill();
                this.ctx.fillStyle = "#f1c40f"; this.ctx.beginPath(); this.ctx.arc(65, 35, 6, 0, Math.PI*2); this.ctx.fill();

                // Lương thực
                this.goldMines.forEach((m, idx) => {
                    this.ctx.fillStyle = "#f39c12"; this.ctx.beginPath(); this.ctx.arc(m.x, m.y, 16, 0, Math.PI * 2); this.ctx.fill();
                    this.ctx.fillStyle = "#e67e22"; this.ctx.beginPath(); this.ctx.arc(m.x-4, m.y+4, 12, 0, Math.PI * 2); this.ctx.fill();
                    this.ctx.fillStyle = "#fff"; this.ctx.font = "bold 10px 'Segoe UI'"; this.ctx.fillText("L" + (idx + 1), m.x - 8, m.y + 4);
                });

                // Thành Địch
                let ex = this.canvas.width - 90;
                this.ctx.fillStyle = "#1c2833"; this.ctx.fillRect(ex, 100, 80, 300); 
                this.ctx.fillStyle = "#111"; this.ctx.fillRect(ex, 80, 20, 30); this.ctx.fillRect(ex+30, 80, 20, 30); this.ctx.fillRect(ex+60, 80, 20, 30); 

                // Lá chắn tử thủ địch
                if(this.enemyShieldTimer > 0) {
                    this.ctx.shadowBlur = 30; this.ctx.shadowColor = "#e74c3c";
                    this.ctx.strokeStyle = `rgba(231, 76, 60, ${0.5 + Math.sin(this.animFrame*0.1)*0.3})`;
                    this.ctx.lineWidth = 8;
                    this.ctx.beginPath(); this.ctx.arc(ex+40, 250, 140, Math.PI/2, Math.PI*1.5); this.ctx.stroke();
                    this.ctx.shadowBlur = 0;
                }

                // Cờ địch
                this.ctx.fillStyle = "#bdc3c7"; this.ctx.fillRect(ex+36, 10, 4, 80);
                this.ctx.fillStyle = "#000"; 
                this.ctx.beginPath(); this.ctx.moveTo(ex+36, 15); this.ctx.lineTo(ex-5, 30 + Math.sin(this.animFrame*0.15)*10); this.ctx.lineTo(ex+36, 55); this.ctx.fill();
            }

            drawMenuOverlay(title, subtitle, btnText, color) {
                this.ctx.fillStyle = "rgba(0, 0, 0, 0.85)"; this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
                this.ctx.fillStyle = color; this.ctx.font = "900 38px 'Segoe UI'"; this.ctx.textAlign = "center"; this.ctx.shadowBlur = 20; this.ctx.shadowColor = color;
                this.ctx.fillText(title, this.canvas.width / 2, this.canvas.height / 2 - 30); this.ctx.shadowBlur = 0;
                this.ctx.fillStyle = "#ecf0f1"; this.ctx.font = "italic 18px 'Segoe UI'";
                this.ctx.fillText(subtitle, this.canvas.width / 2, this.canvas.height / 2 + 15);
                this.ctx.fillStyle = "linear-gradient(145deg, #1b4f72, #0d283a)"; this.ctx.fillRect(this.canvas.width / 2 - 140, this.canvas.height / 2 + 50, 280, 50);
                this.ctx.fillStyle = "#f1c40f"; this.ctx.font = "bold 18px 'Segoe UI'";
                this.ctx.fillText(btnText, this.canvas.width / 2, this.canvas.height / 2 + 82); this.ctx.textAlign = "left";
            }
            
            spawnEmergencyUnits(isEnemy) {
                let count = 30; 
                if(isEnemy) { count = this.level === 1 ? 30 : (this.level === 2 ? 40 : 60); }
                
                for(let i=0; i<count; i++) {
                    if (isEnemy) {
                        let types = ['goblin', 'orc', 'shadow_mage', 'giant']; let t = types[Math.floor(Math.random() * types.length)];
                        let levelMult = 1 + (this.level - 1) * 0.5; 
                        let stats = { goblin: { hp: 110*levelMult, dmg: 14*levelMult, range: 40, speed: 1.4, size: 0.95 }, orc: { hp: 230*levelMult, dmg: 26*levelMult, range: 45, speed: 1.0, size: 1.2 }, shadow_mage: { hp: 160*levelMult, dmg: 38*levelMult, range: 240, speed: 0.8, size: 1.05 }, giant: { hp: 650*levelMult, dmg: 60*levelMult, range: 250, speed: 0.5, size: 1.85 } }[t];
                        this.enemies.push(new GameObject(this.canvas.width - 120 + Math.random()*40, 150 + Math.random() * 200, t, true, stats));
                    } else {
                        let types = ['swordwrath', 'archidon', 'spearton']; let t = types[Math.floor(Math.random() * types.length)];
                        let stats = { swordwrath: { hp: 180, dmg: 24, range: 40, speed: 1.4, size: 1.0 }, archidon: { hp: 130, dmg: 32, range: 240, speed: 1.2, size: 1.0 }, spearton: { hp: 300, dmg: 40, range: 65, speed: 1.0, size: 1.2 } }[t];
                        this.units.push(new GameObject(120 - Math.random()*40, 150 + Math.random() * 200, t, false, { hp: stats.hp * (1 + (this.techLevel - 1) * 0.25), dmg: stats.dmg * (1 + (this.techLevel - 1) * 0.3), range: stats.range, speed: stats.speed, size: stats.size }, this.techLevel));
                    }
                }
            }

            run() {
                if (this.statueHp <= 0) { this.gameOver = true; this.drawMenuOverlay("💀 THÀNH TRÌ ĐÃ VỠ!", "Quân ta đã hy sinh anh dũng tại Level " + this.level, "BẤM VÀO ĐÂY ĐỂ CHƠI LẠI", "#e74c3c"); return; }
                if (this.enemyStatueHp <= 0 && !this.levelComplete && !this.gameOver) {
                    if (this.level >= this.maxLevel) { this.gameOver = true; this.drawMenuOverlay("⭐ ĐẠI CÁO BÌNH NGÔ!", "Giải phóng toàn vẹn lãnh thổ Tổ quốc!", "BẤM ĐỂ CHƠI LẠI TỪ ĐẦU", "#f1c40f"); } 
                    else { this.levelComplete = true; this.drawMenuOverlay("🎖️ HOÀN THÀNH MÀN " + this.level, "Căn cứ địch đã bị san phẳng. Chuẩn bị tiến công!", "BẤM VÀO ĐÂY ĐỂ QUA MÀN", "#2ecc71"); }
                    return; 
                }

                this.animFrame++; this.ctx.save();
                if (this.screenShake > 0) { this.screenShake--; this.ctx.translate((Math.random() - 0.5) * 15, (Math.random() - 0.5) * 15); }

                this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                this.drawEnvironment();
                this.drawBases();

                if (this.showBriefing) { this.drawMenuOverlay("MÀN " + this.level + ": SẴN SÀNG CHIẾN ĐẤU", "Hãy cẩn thận Không Quân ném bom. Quân địch sẽ tử thủ khi gần chết!", "BẤM ĐỂ XUẤT QUÂN", "#3498db"); this.ctx.restore(); requestAnimationFrame(() => this.run()); return; }
                
                // KIỂM TRA TỬ THỦ CĂN CỨ
                if (this.ourShieldTimer > 0) this.ourShieldTimer--;
                if (this.enemyShieldTimer > 0) this.enemyShieldTimer--;
                
                let enemyMaxHp = 3000 + (this.level * 2000);
                if (this.enemyStatueHp <= enemyMaxHp/2 && !this.enemyEmergencyTriggered) {
                    this.enemyEmergencyTriggered = true; this.enemyShieldTimer = 900; 
                    this.spawnEmergencyUnits(true);
                    this.addFloatingText("ĐỊCH TỬ THỦ! VIỆN BINH NHẢY DÙ", this.canvas.width - 250, 100, '#e74c3c', true);
                    this.screenShake = 30;
                }
                
                if (this.statueHp <= 1500 && !this.ourEmergencyTriggered) {
                    this.ourEmergencyTriggered = true; this.ourShieldTimer = 900;
                    this.spawnEmergencyUnits(false);
                    let shieldPct = this.level === 1 ? 50 : (this.level === 2 ? 70 : 90);
                    this.addFloatingText(`TA TỬ THỦ! GIẢM ${shieldPct}% SÁT THƯƠNG`, 150, 100, '#3498db', true);
                    this.screenShake = 30;
                }
                
                this.updateUI(); 

                // Máy bay thả bom
                this.airRaidTimer++;
                let targetFrames = this.level === 1 ? 3600 : (this.level === 2 ? 1800 : 900); 
                if (this.airRaidTimer >= targetFrames) { this.triggerAirRaidWarning(); this.airRaidTimer = 0; }
                if (this.airRaidWarning > 0) { 
                    this.ctx.fillStyle = "rgba(231, 76, 60, 0.2)"; this.ctx.fillRect(0,0,this.canvas.width,this.canvas.height);
                    this.addFloatingText("⚠️ BÁO ĐỘNG KHÔNG QUÂN!", this.canvas.width/2-100, 80, '#e74c3c', true);
                    this.airRaidWarning--; if (this.airRaidWarning === 1) { this.isEnemyBomberActive = true; this.enemyBomberX = -100; } 
                }

                if (this.isEnemyBomberActive) {
                    this.enemyBomberX += 12;
                    this.ctx.fillStyle = "#111"; this.ctx.beginPath(); this.ctx.arc(this.enemyBomberX, 40, 30, 0, Math.PI*2); this.ctx.fill();
                    if (this.enemyBomberX % 40 < 12) {
                        this.screenShake = 20; this.particles.emit(this.enemyBomberX - 20, 150 + Math.random()*200, '#e74c3c', 40); 
                        this.units.forEach(u => {
                            if (!this.isHiding) { u.hp -= 250; this.addFloatingText("-250 Bom", u.x, u.y, '#e74c3c'); } 
                            else { this.addFloatingText("Trú ẩn thành công", u.x, u.y, '#2ecc71'); }
                        });
                    }
                    if (this.enemyBomberX > this.canvas.width + 150) this.isEnemyBomberActive = false;
                }

                if (this.isPlaneActive) {
                    this.planeX += 12;
                    this.ctx.fillStyle = "#34495e"; this.ctx.beginPath(); this.ctx.arc(this.planeX, 50, 25, 0, Math.PI*2); this.ctx.fill();
                    if (this.planeX % 40 < 12) { this.particles.emit(this.planeX, 60, '#f1c40f', 20); }
                    if (this.planeX > this.canvas.width + 150) this.isPlaneActive = false;
                }

                // Cập nhật hạt đạn đạo
                this.projectiles.forEach((proj, idx) => {
                    proj.updateAndDraw(this.ctx, this.particles);
                    if (!proj.active) this.projectiles.splice(idx, 1);
                });

                this.particles.updateAndDraw(this.ctx);

                // LÍNH TA
                this.units.forEach((u, idx) => {
                    if (u.isSpinning > 0) u.isSpinning--;
                    if (this.isHiding && u.type !== 'miner') { /* Nằm im */ } 
                    else {
                        if (u.type === 'miner') {
                            if (u.mineTarget) {
                                let moveSpeed = this.isHiding ? u.speed * 0.3 : u.speed; 
                                if (u.state === 'going') {
                                    let dx = u.mineTarget.x - u.x; let dy = u.mineTarget.y - u.y; let dist = Math.hypot(dx, dy);
                                    if (dist > 3) { u.x += (dx / dist) * moveSpeed; u.y += (dy / dist) * moveSpeed; } else { u.state = 'mining'; }
                                } else if (u.state === 'mining') {
                                    u.goldBag = 15 * this.techLevel; u.state = 'returning';
                                } else if (u.state === 'returning') {
                                    let dx = 90 - u.x; let dy = 250 - u.y; let dist = Math.hypot(dx, dy);
                                    if (dist > 3) { u.x += (dx / dist) * moveSpeed; u.y += (dy / dist) * moveSpeed; }
                                    else {
                                        this.gold += u.goldBag || 15; u.goldBag = 0; u.state = 'going';
                                        this.particles.emit(90, 250, '#f1c40f', 15); this.addFloatingText("+" + (15 * this.techLevel), 90, 250, '#f1c40f');
                                    }
                                }
                            }
                        } else {
                            let nearestEnemy = this.enemies.find(e => Math.abs(e.x - u.x) <= u.range);
                            if (nearestEnemy) {
                                if (u.attackCd > 0) u.attackCd--;
                                else { 
                                    // Tạo đạn hoặc chém trực tiếp
                                    if(u.type === 'archidon') this.projectiles.push(new Projectile(u.x, u.y-10, nearestEnemy, 'arrow', u.dmg, false));
                                    else if(u.type === 'magikill') this.projectiles.push(new Projectile(u.x, u.y-20, nearestEnemy, 'magic', u.dmg, false));
                                    else if(u.type === 'giant') { this.projectiles.push(new Projectile(u.x+30, u.y-20, nearestEnemy, 'cannon', u.dmg, false)); this.screenShake = 5; }
                                    else {
                                        nearestEnemy.hp -= u.dmg; this.particles.emit(nearestEnemy.x, nearestEnemy.y, '#e74c3c', 10, true); 
                                        this.addFloatingText("-" + Math.floor(u.dmg), nearestEnemy.x, nearestEnemy.y - 15, '#e74c3c'); 
                                    }
                                    u.attackCd = u.maxCd; 
                                }
                            } else {
                                let targetX = this.currentCommand === 'ATTACK' ? this.canvas.width - 120 : 250;
                                let distToBase = (this.canvas.width - 90) - u.x;
                                
                                if (this.currentCommand === 'ATTACK' && distToBase <= u.range) {
                                    if (u.attackCd > 0) u.attackCd--;
                                    else {
                                        let dmgMult = this.enemyShieldTimer > 0 ? 0.5 : 1; 
                                        let actualDmg = u.dmg * dmgMult;
                                        
                                        if(u.type === 'archidon' || u.type === 'magikill' || u.type === 'giant') {
                                            let pType = u.type === 'giant' ? 'cannon' : (u.type === 'archidon' ? 'arrow' : 'magic');
                                            this.projectiles.push(new Projectile(u.x, u.y-20, {x: this.canvas.width-90, y: 250, hp: 9999}, pType, actualDmg, false));
                                            if (u.type === 'giant') this.screenShake = 5;
                                        }
                                        this.enemyStatueHp -= actualDmg; 
                                        setTimeout(() => { this.particles.emit(this.canvas.width - 90, 250, '#f1c40f', 20); this.addFloatingText("-" + Math.floor(actualDmg), this.canvas.width - 90, 200 + Math.random()*50, '#f1c40f'); }, 200);
                                        u.attackCd = u.maxCd; 
                                    }
                                } else if (u.x < targetX) { u.x += u.speed; }
                            }
                        }
                    }
                    u.draw(this.ctx, this.animFrame, this.isHiding); if (u.hp <= 0) { this.particles.emit(u.x, u.y, '#e74c3c', 20, true); this.units.splice(idx, 1); }
                });

                // LÍNH ĐỊCH
                this.enemies.forEach((e, idx) => {
                    let nearestUnit = this.units.find(u => u.type !== 'miner' && Math.abs(u.x - e.x) <= e.range);
                    if (nearestUnit && !this.isHiding) { 
                        if (e.attackCd > 0) e.attackCd--;
                        else { 
                            if(e.type === 'shadow_mage') this.projectiles.push(new Projectile(e.x, e.y-20, nearestUnit, 'magic', e.dmg, true));
                            else if(e.type === 'giant') { this.projectiles.push(new Projectile(e.x-30, e.y-20, nearestUnit, 'cannon', e.dmg, true)); this.screenShake = 5; }
                            else {
                                nearestUnit.hp -= e.dmg; this.particles.emit(nearestUnit.x, nearestUnit.y, '#c0392b', 10, true); 
                                this.addFloatingText("-" + Math.floor(e.dmg), nearestUnit.x, nearestUnit.y - 15, '#c0392b'); 
                            }
                            e.attackCd = e.maxCd; 
                        }
                    } else {
                        let distToBase = e.x - 90; 
                        if (distToBase <= e.range) {
                            if (e.attackCd > 0) e.attackCd--;
                            else {
                                let dmgMult = 1;
                                if(this.ourShieldTimer > 0) { dmgMult = this.level === 1 ? 0.5 : (this.level === 2 ? 0.3 : 0.1); }
                                let actualDmg = e.dmg * dmgMult;
                                
                                if(e.type === 'shadow_mage' || e.type === 'giant') {
                                    let pType = e.type === 'giant' ? 'cannon' : 'magic';
                                    this.projectiles.push(new Projectile(e.x, e.y-20, {x: 90, y: 250, hp: 9999}, pType, actualDmg, true));
                                    if (e.type === 'giant') this.screenShake = 5;
                                }
                                this.statueHp -= actualDmg; 
                                setTimeout(() => { this.particles.emit(90, 250, '#e74c3c', 20); this.addFloatingText("-" + Math.floor(actualDmg), 90, 200 + Math.random()*50, '#e74c3c'); }, 200);
                                e.attackCd = e.maxCd; 
                            }
                        } else { e.x -= e.speed; }
                    }
                    e.draw(this.ctx, this.animFrame, false); 
                    if (e.hp <= 0) { this.particles.emit(e.x, e.y, '#7f8c8d', 20, true); this.enemies.splice(idx, 1); this.gold += (40 + this.level*15); this.addFloatingText("+" + (40 + this.level*15), e.x, e.y-20, '#f1c40f'); }
                });

                this.floatingTexts.forEach((ft, idx) => { 
                    ft.y -= 1.0; ft.alpha -= 0.02; 
                    this.ctx.fillStyle = ft.color; this.ctx.globalAlpha = Math.max(0, ft.alpha); 
                    this.ctx.font = ft.isBig ? "bold 20px 'Segoe UI'" : "bold 13px 'Segoe UI'"; 
                    this.ctx.fillText(ft.text, ft.x, ft.y); 
                    this.ctx.globalAlpha = 1.0; 
                    if (ft.alpha <= 0) this.floatingTexts.splice(idx, 1); 
                });
                
                this.drawRain(); // Vẽ mưa chèn lên trên cùng
                this.ctx.restore(); requestAnimationFrame(() => this.run());
            }
        }

        const GameManager = new RTSGameManager();

        setInterval(() => {
            if (!GameManager.showBriefing && !GameManager.gameOver && !GameManager.levelComplete && GameManager.enemyStatueHp > 0 && GameManager.enemies.length < 40) {
                let types = ['goblin', 'orc', 'shadow_mage', 'giant']; let t = types[Math.floor(Math.random() * types.length)];
                let levelMult = 1 + (GameManager.level - 1) * 0.5; 
                let stats = { goblin: { hp: 120*levelMult, dmg: 16*levelMult, range: 40, speed: 1.5, size: 0.95 }, orc: { hp: 250*levelMult, dmg: 30*levelMult, range: 45, speed: 1.1, size: 1.2 }, shadow_mage: { hp: 180*levelMult, dmg: 45*levelMult, range: 240, speed: 0.9, size: 1.05 }, giant: { hp: 750*levelMult, dmg: 70*levelMult, range: 250, speed: 0.5, size: 1.85 } }[t];
                GameManager.enemies.push(new GameObject(GameManager.canvas.width - 120, 150 + Math.random() * 200, t, true, stats));
            }
        }, 2800);

        GameManager.run();
    </script>
</body>
</html>
"""

st.components.v1.html(game_html, height=650, scrolling=False)
