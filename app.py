import streamlit as st

st.set_page_config(
    page_title="Kháng Chiến Việt Nam - Tuyên Ngôn Lịch Sử",
    page_icon="⭐",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #05080a; color: #ffffff; font-family: 'Segoe UI', Tahoma, sans-serif; }
    iframe { border-radius: 12px; box-shadow: 0 0 60px rgba(241, 196, 15, 0.2); border: 2px solid #f1c40f; }
    .title-text { text-align: center; color: #f1c40f; text-transform: uppercase; font-weight: 900; letter-spacing: 4px; margin-bottom: 0px; text-shadow: 0 0 15px #f1c40f; }
    .sub-text { text-align: center; color: #a3e4d7; font-size: 15px; margin-bottom: 10px; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title-text'>⭐ KHÁNG CHIẾN VIỆT NAM - CHIẾN DỊCH TỔNG LỰC ⭐</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Đã sửa lỗi kẹt Màn 2 (Lỗi Máu Ảo). Tối ưu logic chuyển cảnh và Cutscene Ending!</p>", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Khang Chien Viet Nam - Master Edition</title>
    <style>
        body { margin: 0; background: #05080a; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; overflow: hidden; user-select: none; }
        canvas { border-radius: 8px; display: block; margin: 4px auto; cursor: crosshair; box-shadow: inset 0 0 80px rgba(0,0,0,0.9); }
        .panel-container { display: flex; flex-direction: column; align-items: center; gap: 8px; margin-top: 10px; }
        .ui-row { display: flex; justify-content: center; flex-wrap: wrap; gap: 8px; }
        .music-panel { background: rgba(17, 42, 46, 0.9); padding: 8px 20px; border-radius: 8px; border: 1px solid #f1c40f; box-shadow: 0 0 15px rgba(241,196,15,0.3); }
        button { background: linear-gradient(145deg, #7d6608, #4a3c04); color: #fff; border: 1px solid #f1c40f; padding: 8px 16px; font-weight: 900; font-size: 12px; border-radius: 5px; cursor: pointer; transition: all 0.2s; text-transform: uppercase; text-shadow: 1px 1px 2px #000; box-shadow: 0 4px 6px rgba(0,0,0,0.6); }
        button:hover { background: #f1c40f; color: #000; transform: translateY(-3px) scale(1.02); box-shadow: 0 8px 15px rgba(241,196,15,0.5); border-color: #fff; text-shadow: none; }
        button:active { transform: scale(0.95); }
        .cmd-btn { background: linear-gradient(145deg, #1b4f72, #0d283a); border-color: #5dade2; }
        .cmd-btn:hover { background: #5dade2; color: #000; }
        .bunker-btn { background: linear-gradient(145deg, #c0392b, #78281f); border-color: #e74c3c; animation: pulse 1.5s infinite; }
        .bunker-btn:hover { background: #e74c3c; color: #fff; animation: none; }
        .skill-btn { background: linear-gradient(145deg, #6c3483, #4a235a); border-color: #9b59b6; }
        .tech-btn { background: linear-gradient(145deg, #1e8449, #0e4324); border-color: #2ecc71; }
        .music-btn { background: linear-gradient(145deg, #922b21, #4a1510); border-color: #e74c3c; }
        .stats { font-size: 15px; font-weight: bold; color: #f1c40f; text-shadow: 1px 1px 4px #000; background: rgba(0,0,0,0.7); padding: 6px 15px; border-radius: 8px; display: inline-block; border: 1px solid #333; margin-bottom: 5px; }
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.8); } 70% { box-shadow: 0 0 0 15px rgba(231, 76, 60, 0); } 100% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0); } }
    </style>
</head>
<body>

    <div class="stats">
        🚩 MÀN: <span id="levelText" style="color:#fff;">1</span> | 🏛️ THÀNH TA: <span id="hpText" style="color:#2ecc71;">3000</span> <span id="ourShield" style="color:#3498db; font-size:11px;"></span> | ⚔️ ĐỊCH: <span id="enemyHpText" style="color:#e74c3c;">3000</span> <span id="enemyShield" style="color:#f1c40f; font-size:11px;"></span> | 🌾 LƯƠNG: <span id="goldText" style="color:#f1c40f;">450</span> | 👥 QUÂN: <span id="popText" style="color:#fff;">0</span>/100
    </div>

    <canvas id="gameCanvas" width="1020" height="420"></canvas>

    <div class="panel-container">
        <div class="ui-row music-panel">
            <span style="font-size:14px; font-weight:900; color:#f1c40f; align-self:center; letter-spacing:1px;">🎵 HỆ THỐNG ÂM THANH:</span>
            <button class="music-btn" onclick="playExternalMusic('https://upload.wikimedia.org/wikipedia/commons/e/e5/Tien_Quan_Ca_instrumental.ogg')">🎶 Tiến Quân Ca</button>
            <button class="music-btn" onclick="playMarchTone()">🎺 Kèn Xung Phong</button>
            <button class="music-btn" onclick="stopAllAudio()">🔇 Tắt Tất Cả</button>
        </div>

        <div class="ui-row">
            <button class="cmd-btn" id="btnAttack">⚔️ LỆNH: TIẾN CÔNG</button>
            <button class="cmd-btn" id="btnDefend">🛡️ LỆNH: TỬ THỦ</button>
            <button class="bunker-btn" id="btnBunker">🕳️ LỆNH: CHUI HẦM BẢO TOÀN</button>
            <button class="tech-btn" id="btnTech">⬆️ CẢI TIẾN HỎA LỰC (150G)</button>
            <button class="skill-btn" id="btnEarth">💣 ĐIỀU ĐỘNG KHÔNG QUÂN</button>
        </div>

        <div class="ui-row">
            <button id="spawnMiner">🌾 Dân Quân (30g)</button>
            <button id="spawnSwordwrath">🗡️ Du Kích Dao (40g)</button>
            <button id="spawnArchidon">🔫 Xạ Thủ (50g)</button>
            <button id="spawnSpearton">🛡️ Tự Vệ Khiên (70g)</button>
            <button id="spawnMagikill">⭐ Cán Bộ (100g)</button>
            <button id="spawnGiant">🚜 Xe Tăng (160g)</button>
        </div>
    </div>

    <script>
        // ======================= AUDIO ENGINE =======================
        let bgMusic = new Audio(); bgMusic.loop = true; bgMusic.volume = 0.4;
        let speechAudio = new Audio('https://upload.wikimedia.org/wikipedia/commons/e/e4/Tuyen_ngon_doc_lap.ogg');
        speechAudio.volume = 0.8;
        
        function playExternalMusic(url) { bgMusic.src = url; bgMusic.play().catch(e => console.log("Blocked by browser")); }
        
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
        function stopAllAudio() { bgMusic.pause(); speechAudio.pause(); speechAudio.currentTime = 0; stopWebAudio(); }

        // ======================= PHYSICS & PARTICLE ENGINE =======================
        class Particle {
            constructor(x, y, color, type) {
                this.x = x; this.y = y; this.color = color; this.type = type;
                this.active = true;
                
                if (type === 'blood') {
                    this.vx = (Math.random() - 0.5) * 6; this.vy = (Math.random() - 0.5) * 6 - 2;
                    this.radius = Math.random() * 3 + 1; this.gravity = 0.3; this.friction = 0.8; this.decay = 0.01;
                } else if (type === 'debris') {
                    this.vx = (Math.random() - 0.5) * 12; this.vy = -Math.random() * 10 - 2;
                    this.radius = Math.random() * 4 + 2; this.gravity = 0.5; this.friction = 0.6; this.decay = 0.02;
                } else {
                    this.vx = (Math.random() - 0.5) * 4; this.vy = (Math.random() - 0.5) * 4 - 1;
                    this.radius = Math.random() * 4 + 1; this.gravity = 0; this.friction = 0.95; this.decay = 0.03;
                }
                this.alpha = 1.0; this.groundY = 320 + Math.random() * 40;
            }
            updateAndDraw(ctx) {
                if (!this.active) return;
                this.vy += this.gravity; this.vx *= this.friction; 
                this.x += this.vx; this.y += this.vy;
                
                if (this.y >= this.groundY) {
                    this.y = this.groundY;
                    if (this.type === 'debris') { this.vy *= -0.5; this.vx *= 0.5; }
                    else if (this.type === 'blood') { this.vy = 0; this.vx = 0; this.decay = 0.002; }
                }
                
                this.alpha -= this.decay;
                if (this.alpha <= 0) { this.active = false; return; }
                
                ctx.globalAlpha = Math.max(0, this.alpha); ctx.fillStyle = this.color;
                if (this.type === 'debris') { ctx.fillRect(this.x, this.y, this.radius, this.radius); }
                else { ctx.beginPath(); ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2); ctx.fill(); }
                ctx.globalAlpha = 1.0;
            }
        }

        class ParticleSystem {
            constructor() { this.particles = []; }
            emit(x, y, color, type, count) {
                for (let i = 0; i < count; i++) this.particles.push(new Particle(x, y, color, type));
            }
            updateAndDraw(ctx) {
                if (this.particles.length > 500) this.particles.splice(0, this.particles.length - 500);
                this.particles.forEach(p => p.updateAndDraw(ctx));
                this.particles = this.particles.filter(p => p.active);
            }
        }

        // ======================= PROJECTILE ENGINE =======================
        class Projectile {
            constructor(x, y, target, type, dmg, isEnemy) {
                this.x = x; this.y = y; this.target = target; this.type = type; this.dmg = dmg; this.isEnemy = isEnemy;
                this.speed = type === 'arrow' ? 12 : (type === 'cannon' ? 15 : 7);
                this.active = true;
                let dx = target.x - x; let dy = target.y - y; let dist = Math.hypot(dx, dy);
                this.vx = (dx / dist) * this.speed; this.vy = (dy / dist) * this.speed;
                this.angle = Math.atan2(dy, dx);
            }
            updateAndDraw(ctx, particles) {
                if (!this.active) return;
                this.x += this.vx; this.y += this.vy;
                ctx.save(); ctx.translate(this.x, this.y); ctx.rotate(this.angle);
                
                if (this.type === 'arrow') {
                    ctx.fillStyle = "#ecf0f1"; ctx.fillRect(-8, -1, 16, 2);
                    ctx.fillStyle = "#95a5a6"; ctx.beginPath(); ctx.moveTo(8, -3); ctx.lineTo(14, 0); ctx.lineTo(8, 3); ctx.fill();
                } else if (this.type === 'cannon') {
                    ctx.fillStyle = "#e67e22"; ctx.beginPath(); ctx.arc(0, 0, 5, 0, Math.PI*2); ctx.fill();
                    ctx.fillStyle = "#f1c40f"; ctx.beginPath(); ctx.arc(0, 0, 3, 0, Math.PI*2); ctx.fill();
                    particles.emit(this.x, this.y, '#7f8c8d', 'smoke', 1); 
                } else if (this.type === 'magic') {
                    ctx.shadowBlur = 15; ctx.shadowColor = this.isEnemy ? "#e74c3c" : "#3498db";
                    ctx.fillStyle = this.isEnemy ? "#c0392b" : "#2980b9";
                    ctx.beginPath(); ctx.arc(0, 0, 6 + Math.random()*3, 0, Math.PI*2); ctx.fill();
                    particles.emit(this.x, this.y, this.isEnemy ? '#e74c3c' : '#3498db', 'spark', 2);
                }
                ctx.restore();

                if (this.target && this.target.hp > 0) {
                    let hitDist = Math.hypot(this.target.x - this.x, this.target.y - this.y);
                    if (hitDist < 25) {
                        this.target.hp -= this.dmg;
                        if(this.type === 'cannon') {
                            particles.emit(this.x, this.y, '#e74c3c', 'spark', 20);
                            particles.emit(this.x, this.y, '#333', 'debris', 10);
                        } else if (this.type === 'arrow') {
                            particles.emit(this.x, this.y, '#900C3F', 'blood', 10);
                        } else {
                            particles.emit(this.x, this.y, '#f1c40f', 'spark', 15);
                        }
                        this.active = false;
                    }
                } else if (!this.target || this.target.hp <= 0) { this.active = false; }
            }
        }

        // ======================= ENTITY ENGINE =======================
        class GameObject {
            constructor(x, y, type, isEnemy, stats, techLevel = 1) {
                this.x = x; this.y = y; this.type = type; this.isEnemy = isEnemy;
                this.hp = stats.hp; this.maxHp = stats.hp; this.dmg = stats.dmg;
                this.range = stats.range; this.speed = stats.speed; this.size = stats.size;
                this.attackCd = 0; this.maxCd = type === 'giant' ? 90 : 40; 
                this.state = 'spawning'; this.spawnY = -100; 
                this.goldBag = 0; this.mineTarget = null; this.techLevel = techLevel;
            }
            
            draw(ctx, animFrame, isHiding = false) {
                ctx.save();
                
                if (this.state === 'spawning') {
                    this.spawnY += 6; ctx.translate(this.x, this.spawnY);
                    if (this.spawnY >= this.y) { this.state = 'going'; this.spawnY = this.y; }
                    if(this.spawnY < this.y - 15) {
                        ctx.fillStyle = this.isEnemy ? "#555" : "#bdc3c7"; 
                        ctx.beginPath(); ctx.arc(0, -45, 25, Math.PI, 0); ctx.fill();
                        ctx.strokeStyle = "#fff"; ctx.lineWidth=1.5;
                        ctx.beginPath(); ctx.moveTo(-25, -45); ctx.lineTo(0, -10); ctx.stroke();
                        ctx.beginPath(); ctx.moveTo(25, -45); ctx.lineTo(0, -10); ctx.stroke();
                    }
                } else {
                    ctx.translate(this.x, this.y);
                }

                if (!this.isEnemy && isHiding && this.type !== 'giant') { ctx.rotate(Math.PI / 2); ctx.translate(15, -15); }
                if (this.isEnemy) ctx.scale(-1, 1);

                ctx.shadowColor = 'rgba(0, 0, 0, 0.5)'; ctx.shadowBlur = 8; ctx.shadowOffsetY = 5;

                let colorTa = '#2980b9'; let colorDich = '#c0392b';
                let unitColor = this.isEnemy ? colorDich : colorTa;
                if (this.type === 'miner') unitColor = '#d35400';
                else if (this.type === 'giant') unitColor = this.isEnemy ? '#4a2311' : '#273746'; 

                if (this.type === 'giant') {
                    ctx.fillStyle = unitColor;
                    if(ctx.roundRect) ctx.roundRect(-35, -25, 70, 30, 6); else ctx.fillRect(-35, -25, 70, 30);
                    ctx.fill();
                    ctx.fillStyle = this.isEnemy ? "#2c1005" : "#1a252f"; 
                    ctx.beginPath(); ctx.arc(-15, -15, 8, 0, Math.PI*2); ctx.fill();
                    ctx.beginPath(); ctx.arc(20, -5, 12, 0, Math.PI*2); ctx.fill();
                    ctx.beginPath(); ctx.arc(0, -20, 10, 0, Math.PI*2); ctx.fill();
                    
                    ctx.fillStyle = "#0a0a0a"; ctx.fillRect(-38, 5, 76, 12); 
                    ctx.fillStyle = "#7f8c8d";
                    let treadOffset = (this.state === 'going' ? (animFrame % 15) : 0) - 30;
                    for(let i=treadOffset; i<=35; i+=14) { ctx.beginPath(); ctx.arc(i, 11, 5, 0, Math.PI*2); ctx.fill(); }
                    
                    ctx.fillStyle = "#111"; ctx.beginPath(); ctx.arc(0, -25, 18, Math.PI, 0); ctx.fill();
                    let recoil = (this.attackCd > this.maxCd - 10) ? -12 : 0; 
                    ctx.lineWidth = 6; ctx.strokeStyle = "#000";
                    ctx.beginPath(); ctx.moveTo(0, -30); ctx.lineTo(45 + recoil, -30); ctx.stroke();
                    ctx.fillStyle = "#555"; ctx.fillRect(40 + recoil, -33, 8, 6);
                } else {
                    ctx.fillStyle = this.isEnemy ? "#d68910" : "#f5cba7";
                    ctx.beginPath(); ctx.arc(0, -20 * this.size, 7 * this.size, 0, Math.PI * 2); ctx.fill();
                    
                    ctx.fillStyle = this.isEnemy ? "#7b241c" : "#145a32"; 
                    ctx.beginPath(); ctx.arc(0, -22 * this.size, 8 * this.size, Math.PI, 0); ctx.fill();
                    ctx.fillRect(-8 * this.size, -22 * this.size, 16 * this.size, 3 * this.size); 
                    if (!this.isEnemy && this.techLevel > 1) { ctx.fillStyle = "#f1c40f"; ctx.fillRect(-2 * this.size, -24 * this.size, 4 * this.size, 4 * this.size); }

                    ctx.fillStyle = unitColor;
                    ctx.fillRect(-7 * this.size, -14 * this.size, 14 * this.size, 16 * this.size); 
                    ctx.fillStyle = "#3e2723"; ctx.fillRect(-7 * this.size, -2 * this.size, 14 * this.size, 3 * this.size);

                    let armAngle = 0; let swordSwing = 0;
                    if (this.attackCd > this.maxCd - 12) {
                        armAngle = Math.PI/4; 
                        if(this.type === 'swordwrath') swordSwing = Math.PI/2;
                    }

                    ctx.save();
                    ctx.translate(0, -10 * this.size);
                    ctx.rotate(armAngle);
                    
                    if (this.type === 'archidon') {
                        ctx.fillStyle = "#111"; ctx.fillRect(0, -3, 24, 5); 
                        ctx.fillStyle = "#8d6e63"; ctx.fillRect(2, 0, 5, 6); 
                    } else if (this.type === 'spearton') {
                        ctx.fillStyle = "#95a5a6"; ctx.fillRect(-3, -20, 4, 40); 
                        ctx.fillStyle = "#e74c3c"; ctx.beginPath(); ctx.arc(-1, -20, 3, 0, Math.PI*2); ctx.fill(); 
                        ctx.fillStyle = "#2c3e50"; ctx.fillRect(8, -12, 8, 30); 
                    } else if (this.type === 'swordwrath') {
                        ctx.rotate(swordSwing);
                        ctx.fillStyle = "#bdc3c7"; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(18, -18); ctx.lineTo(22, -12); ctx.fill(); 
                    } else if (this.type === 'magikill') {
                        ctx.fillStyle = "#f39c12"; ctx.fillRect(8, -25, 4, 40); 
                        ctx.fillStyle = "#3498db"; ctx.shadowBlur = 10; ctx.shadowColor = "#3498db"; 
                        ctx.beginPath(); ctx.arc(10, -25, 7 + Math.random()*2, 0, Math.PI*2); ctx.fill(); 
                    } else if (this.type === 'miner') {
                        ctx.fillStyle = "#7f8c8d"; ctx.fillRect(0, -15, 4, 30); 
                        ctx.fillRect(-8, -15, 20, 4); 
                    }
                    ctx.restore();

                    ctx.shadowColor = 'transparent'; ctx.strokeStyle = "#111"; ctx.lineWidth = 4 * this.size;
                    let swing = 0;
                    if ((this.state === 'going' || this.state === 'returning') && (!isHiding || this.isEnemy)) {
                        swing = Math.sin(animFrame * 0.6) * 10;
                    }
                    ctx.beginPath(); ctx.moveTo(-4, 2 * this.size); ctx.lineTo(-6 * this.size, 14 * this.size + swing); ctx.stroke();
                    ctx.beginPath(); ctx.moveTo(4, 2 * this.size); ctx.lineTo(6 * this.size, 14 * this.size - swing); ctx.stroke();
                }

                ctx.shadowColor = 'transparent'; 
                ctx.fillStyle = "rgba(0,0,0,0.8)"; ctx.fillRect(-20, -55, 40, 6);
                let hpPercent = Math.max(0, this.hp / this.maxHp);
                ctx.fillStyle = hpPercent > 0.5 ? "#2ecc71" : (hpPercent > 0.2 ? "#f1c40f" : "#e74c3c");
                ctx.fillRect(-19, -54, 38 * hpPercent, 4);
                
                ctx.restore();
            }
        }

        // ======================= CORE GAME MANAGER =======================
        class RTSGameManager {
            constructor() {
                this.canvas = document.getElementById("gameCanvas");
                this.ctx = this.canvas.getContext("2d");
                
                this.level = 1; this.maxLevel = 3;
                this.statueHp = 3000; this.enemyStatueHp = 3000;
                this.gold = 500; this.techLevel = 1; this.currentCommand = 'ATTACK';
                
                this.state = 'MENU'; 
                this.transitionTimer = 0;
                this.screenShake = 0; this.animFrame = 0; 
                
                this.isHiding = false; 
                this.airRaidWarning = 0; this.airRaidTimer = 0; 
                this.enemyBomberX = -200; this.isEnemyBomberActive = false;
                this.planeX = -100; this.isPlaneActive = false; 
                
                this.ourEmergencyTriggered = false; this.enemyEmergencyTriggered = false;
                this.ourShieldTimer = 0; this.enemyShieldTimer = 0;

                this.particles = new ParticleSystem();
                this.projectiles = []; 
                
                this.goldMines = [ { x: 180, y: 150, miner: null }, { x: 230, y: 200, miner: null }, { x: 280, y: 260, miner: null }, { x: 200, y: 340, miner: null }, { x: 260, y: 130, miner: null }, { x: 310, y: 180, miner: null } ];
                this.units = []; this.enemies = []; this.floatingTexts = [];
                
                this.mapColors = {
                    1: { sky: 'linear-gradient(to bottom, #3498db 0%, #85c1e9 50%, #2ecc71 50%, #27ae60 100%)', sun: true, clouds: true, mtn1: '#21618c', mtn2: '#2874a6' }, 
                    2: { sky: 'linear-gradient(to bottom, #154360 0%, #1a5276 50%, #1e8449 50%, #145a32 100%)', moon: true, stars: true, mtn1: '#0e2b3e', mtn2: '#123955' }, 
                    3: { sky: 'linear-gradient(to bottom, #641e16 0%, #922b21 50%, #7e5109 50%, #4a235a 100%)', rain: true, lightning: true, mtn1: '#4a1510', mtn2: '#621c16' }  
                };
                
                this.clouds = Array.from({length: 8}, () => ({x: Math.random()*1200, y: 20+Math.random()*80, speed: 0.1+Math.random()*0.3, scale: 0.5+Math.random()*1}));
                this.stars = Array.from({length: 100}, () => ({x: Math.random()*1200, y: Math.random()*200, radius: Math.random()*1.5+0.5, blink: Math.random()*0.1}));
                this.rain = Array.from({length: 200}, () => ({x: Math.random()*1500, y: Math.random()*450, speedY: 20+Math.random()*15, speedX: -4-Math.random()*5}));

                this.speechY = this.canvas.height;
                this.speechLines = [
                    "Hỡi đồng bào cả nước,",
                    "Tất cả mọi người đều sinh ra có quyền bình đẳng.",
                    "Tạo hóa cho họ những quyền không ai có thể xâm phạm được;",
                    "Trong những quyền ấy, có quyền được sống, quyền tự do và quyền mưu cầu hạnh phúc.",
                    "...",
                    "Nước Việt Nam có quyền hưởng tự do và độc lập,",
                    "và sự thật đã thành một nước tự do độc lập.",
                    "Toàn thể dân tộc Việt Nam quyết đem tất cả tinh thần và lực lượng,",
                    "tính mạng và của cải để giữ vững quyền tự do, độc lập ấy.",
                    "",
                    "⭐ CHIẾN DỊCH HOÀN TOÀN THẮNG LỢI ⭐"
                ];

                this.initListeners();
            }
            
            initListeners() {
                this.canvas.addEventListener('click', (e) => {
                    initAudio();
                    const rect = this.canvas.getBoundingClientRect();
                    const mouseX = e.clientX - rect.left; const mouseY = e.clientY - rect.top;
                    
                    if (this.state === 'MENU') { 
                        if (mouseX >= this.canvas.width/2 - 160 && mouseX <= this.canvas.width/2 + 160 && mouseY >= 240 && mouseY <= 320) {
                            this.state = 'PLAYING';
                        }
                        return; 
                    }
                    if (this.state === 'GAME_OVER') { this.resetGame(true); this.state = 'MENU'; this.run(); return; }
                    if (this.state === 'VICTORY_SPEECH') { this.resetGame(true); this.state = 'MENU'; return; }
                });

                document.getElementById('btnAttack').onclick = () => this.setCommand('ATTACK');
                document.getElementById('btnDefend').onclick = () => this.setCommand('DEFEND');
                
                let btnBunker = document.getElementById('btnBunker');
                btnBunker.onclick = () => {
                    this.isHiding = !this.isHiding;
                    if(this.isHiding) {
                        btnBunker.style.background = "linear-gradient(145deg, #2ecc71, #27ae60)"; btnBunker.innerText = "🏃 ĐANG TRÚ ẨN (BẤM ĐỂ DẬY)";
                        this.addFloatingText("Toàn quân Chui Hầm!", this.canvas.width/2, 200, '#2ecc71', true);
                    } else {
                        btnBunker.style.background = "linear-gradient(145deg, #c0392b, #78281f)"; btnBunker.innerText = "🕳️ LỆNH: CHUI HẦM BẢO TOÀN";
                        this.addFloatingText("Toàn quân Tấn Công!", this.canvas.width/2, 200, '#e74c3c', true);
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
                if (this.isEnemyBomberActive || this.airRaidWarning > 0 || this.state !== 'PLAYING') return;
                this.airRaidWarning = 250; playAirRaidSiren();
            }

            nextLevel() {
                this.level++; 
                if (this.level > this.maxLevel) { 
                    this.state = 'VICTORY_SPEECH'; 
                    bgMusic.pause(); 
                    speechAudio.play().catch(e=>console.log("Audio blocked")); 
                    return; 
                }
                this.canvas.style.background = this.mapColors[this.level].sky;
                this.resetGame(false); this.state = 'MENU'; 
            }

            resetGame(fullReset = true) {
                if(fullReset) { this.level = 1; this.canvas.style.background = this.mapColors[1].sky; this.techLevel = 1; this.gold = 500; this.speechY = this.canvas.height; }
                else { this.gold += 1000; } 
                
                this.statueHp = 3000; this.enemyStatueHp = 3000 + (this.level * 2500); 
                this.units = []; this.enemies = []; this.floatingTexts = []; this.projectiles = []; this.particles = new ParticleSystem();
                this.isHiding = false; document.getElementById('btnBunker').style.background = "linear-gradient(145deg, #c0392b, #78281f)"; document.getElementById('btnBunker').innerText = "🕳️ LỆNH: CHUI HẦM BẢO TOÀN";
                this.airRaidWarning = 0; this.isEnemyBomberActive = false; this.airRaidTimer = 0; 
                this.transitionTimer = 0;
                
                this.ourEmergencyTriggered = false; this.enemyEmergencyTriggered = false;
                this.ourShieldTimer = 0; this.enemyShieldTimer = 0;
                
                this.goldMines.forEach(m => m.miner = null);
                this.updateUI();
            }

            setCommand(cmd) { this.currentCommand = cmd; this.isHiding = false; document.getElementById('btnBunker').style.background = "linear-gradient(145deg, #c0392b, #78281f)"; document.getElementById('btnBunker').innerText = "🕳️ LỆNH: CHUI HẦM BẢO TOÀN"; }
            addFloatingText(text, x, y, color = '#f1c40f', isBig=false) { this.floatingTexts.push({ text, x, y, alpha: 1.0, color, isBig }); }
            getCurrentPopulation() { let count = 0; this.units.forEach(u => { if (u.type === 'spearton') count += 3; else if (u.type === 'magikill') count += 5; else if (u.type === 'giant') count += 4; else count += 1; }); return count; }

            upgradeTech() {
                if (this.state !== 'PLAYING') return;
                if (this.gold >= 150 && this.techLevel < 3) {
                    this.gold -= 150; this.techLevel++;
                    this.units.forEach(u => { u.techLevel = this.techLevel; u.dmg = Math.floor(u.dmg * 1.3); u.maxHp = Math.floor(u.maxHp * 1.25); u.hp = u.maxHp; });
                    this.particles.emit(120, 200, '#2ecc71', 'spark', 50);
                    this.addFloatingText("⭐ NÂNG CẤP HỎA LỰC LEVEL " + this.techLevel, 120, 100, '#2ecc71', true);
                    this.updateUI();
                }
            }

            triggerSkill(type) {
                if (this.state !== 'PLAYING') return;
                if (type === 'earthquake' && this.gold >= 120) {
                    this.gold -= 120;
                    this.isPlaneActive = true; this.planeX = -100; this.screenShake = 50;
                    this.particles.emit(this.canvas.width / 2, this.canvas.height / 2, '#e74c3c', 'spark', 80);
                    this.enemies.forEach(e => { e.hp -= (200 * this.techLevel); this.particles.emit(e.x, e.y, '#e74c3c', 'blood', 15); this.addFloatingText("-" + (200 * this.techLevel), e.x, e.y, '#e74c3c', true); });
                }
            }

            spawnUnit(type) {
                if (this.state !== 'PLAYING') return;
                let costs = { miner: 30, swordwrath: 40, archidon: 50, spearton: 70, magikill: 100, giant: 160 };
                let pops = { miner: 1, swordwrath: 1, archidon: 1, spearton: 3, magikill: 5, giant: 4 };
                let stats = {
                    miner: { hp: 120, dmg: 8, range: 30, speed: 1.8, size: 0.95 },
                    swordwrath: { hp: 180, dmg: 26, range: 45, speed: 1.6, size: 1.0 },
                    archidon: { hp: 130, dmg: 35, range: 250, speed: 1.4, size: 1.0 },
                    spearton: { hp: 320, dmg: 45, range: 70, speed: 1.2, size: 1.2 },
                    magikill: { hp: 150, dmg: 65, range: 230, speed: 1.0, size: 1.05 },
                    giant: { hp: 900, dmg: 90, range: 280, speed: 0.7, size: 1.95 }
                }[type];

                if (this.gold >= costs[type] && this.getCurrentPopulation() + pops[type] <= 100) {
                    this.gold -= costs[type];
                    let unit = new GameObject(110, 160 + Math.random() * 220, type, false, {
                        hp: stats.hp * (1 + (this.techLevel - 1) * 0.25), dmg: stats.dmg * (1 + (this.techLevel - 1) * 0.3), range: stats.range, speed: stats.speed, size: stats.size
                    }, this.techLevel);

                    if (type === 'miner') {
                        let freeMine = this.goldMines.find(m => !m.miner);
                        if (freeMine) { freeMine.miner = unit; unit.mineTarget = freeMine; } else { unit.mineTarget = this.goldMines[0]; }
                    }
                    this.units.push(unit); this.particles.emit(unit.x, unit.y, '#3498db', 'spark', 15); this.updateUI();
                }
            }

            updateUI() {
                document.getElementById("levelText").innerText = this.level;
                // FIX LỖI MÁU ẢO (Dùng Math.ceil để hiển thị 1 nếu máu còn 0.1)
                document.getElementById("hpText").innerText = Math.ceil(this.statueHp);
                document.getElementById("enemyHpText").innerText = Math.ceil(this.enemyStatueHp);
                document.getElementById("goldText").innerText = Math.floor(this.gold);
                document.getElementById("popText").innerText = this.getCurrentPopulation();
                
                if(this.ourShieldTimer > 0) document.getElementById("ourShield").innerText = `(GIÁP TỬ THỦ: ${Math.ceil(this.ourShieldTimer/60)}s)`;
                else document.getElementById("ourShield").innerText = "";
                
                if(this.enemyShieldTimer > 0) document.getElementById("enemyShield").innerText = `(GIÁP TỬ THỦ: ${Math.ceil(this.enemyShieldTimer/60)}s)`;
                else document.getElementById("enemyShield").innerText = "";
            }

            drawEnvironment() {
                let env = this.mapColors[this.level];
                
                if(env.sun) {
                    this.ctx.fillStyle = "rgba(241, 196, 15, 0.9)"; this.ctx.shadowBlur = 50; this.ctx.shadowColor = "#f1c40f";
                    this.ctx.beginPath(); this.ctx.arc(100, 70, 35, 0, Math.PI*2); this.ctx.fill(); this.ctx.shadowBlur = 0;
                }
                if(env.moon) {
                    this.ctx.fillStyle = "#ecf0f1"; this.ctx.shadowBlur = 40; this.ctx.shadowColor = "#ecf0f1";
                    this.ctx.beginPath(); this.ctx.arc(120, 70, 30, 0, Math.PI*2); this.ctx.fill(); 
                    this.ctx.fillStyle = "rgba(21, 67, 96, 1)"; this.ctx.beginPath(); this.ctx.arc(132, 62, 25, 0, Math.PI*2); this.ctx.fill(); 
                    this.ctx.shadowBlur = 0;
                }

                this.ctx.fillStyle = env.mtn1;
                this.ctx.beginPath(); this.ctx.moveTo(0, 200);
                for(let i=0; i<=this.canvas.width; i+=100) { this.ctx.lineTo(i, 100 + Math.sin(i*0.01 + this.animFrame*0.005)*40); }
                this.ctx.lineTo(this.canvas.width, 250); this.ctx.lineTo(0, 250); this.ctx.fill();
                
                this.ctx.fillStyle = env.mtn2;
                this.ctx.beginPath(); this.ctx.moveTo(0, 250);
                for(let i=0; i<=this.canvas.width; i+=80) { this.ctx.lineTo(i, 150 + Math.cos(i*0.02 + this.animFrame*0.01)*50); }
                this.ctx.lineTo(this.canvas.width, 250); this.ctx.lineTo(0, 250); this.ctx.fill();

                this.ctx.fillStyle = "rgba(0,0,0,0.3)"; this.ctx.fillRect(0, 200, this.canvas.width, 220);

                if(env.clouds) {
                    this.ctx.fillStyle = "rgba(255, 255, 255, 0.7)";
                    this.clouds.forEach(c => {
                        c.x += c.speed; if (c.x > this.canvas.width + 100) c.x = -100;
                        this.ctx.beginPath(); this.ctx.arc(c.x, c.y, 25*c.scale, 0, Math.PI*2); this.ctx.fill();
                        this.ctx.beginPath(); this.ctx.arc(c.x+30*c.scale, c.y-20*c.scale, 35*c.scale, 0, Math.PI*2); this.ctx.fill();
                        this.ctx.beginPath(); this.ctx.arc(c.x+60*c.scale, c.y, 25*c.scale, 0, Math.PI*2); this.ctx.fill();
                    });
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
                if(env.lightning && Math.random() < 0.015) {
                    this.ctx.fillStyle = "rgba(255,255,255,0.6)"; this.ctx.fillRect(0,0,this.canvas.width, this.canvas.height);
                    this.screenShake = 15;
                }
            }
            
            drawRain() {
                if(this.mapColors[this.level].rain) {
                    this.ctx.strokeStyle = "rgba(174, 214, 241, 0.6)"; this.ctx.lineWidth = 2.5;
                    this.rain.forEach(r => {
                        r.y += r.speedY; r.x += r.speedX;
                        if (r.y > this.canvas.height) { r.y = -20; r.x = Math.random() * (this.canvas.width+500); }
                        this.ctx.beginPath(); this.ctx.moveTo(r.x, r.y); this.ctx.lineTo(r.x - r.speedX, r.y - r.speedY); this.ctx.stroke();
                    });
                }
            }

            drawBases() {
                this.ctx.shadowBlur = 15; this.ctx.shadowColor = "#000";
                this.ctx.fillStyle = "#5d4037"; this.ctx.fillRect(10, 150, 90, 270); 
                this.ctx.fillStyle = "#3e2723"; 
                this.ctx.fillRect(10, 130, 25, 30); this.ctx.fillRect(45, 130, 25, 30); this.ctx.fillRect(80, 130, 20, 30); 
                
                this.ctx.fillStyle = "#8d6e63"; this.ctx.beginPath(); if(this.ctx.roundRect) this.ctx.roundRect(90, 320, 30, 20, 5); else this.ctx.fillRect(90, 320, 30, 20); this.ctx.fill();
                this.ctx.fillStyle = "#795548"; this.ctx.beginPath(); if(this.ctx.roundRect) this.ctx.roundRect(105, 305, 25, 20, 5); else this.ctx.fillRect(105, 305, 25, 20); this.ctx.fill();
                
                if(this.ourShieldTimer > 0) {
                    this.ctx.shadowBlur = 40; this.ctx.shadowColor = "#3498db";
                    this.ctx.strokeStyle = `rgba(52, 152, 219, ${0.6 + Math.sin(this.animFrame*0.15)*0.4})`;
                    this.ctx.lineWidth = 10;
                    this.ctx.beginPath(); this.ctx.arc(50, 280, 160, -Math.PI/2, Math.PI/2); this.ctx.stroke();
                    this.ctx.shadowBlur = 0;
                }

                this.ctx.fillStyle = "#bdc3c7"; this.ctx.fillRect(50, 30, 5, 100);
                this.ctx.fillStyle = "#e74c3c"; 
                this.ctx.beginPath(); this.ctx.moveTo(55, 35); this.ctx.lineTo(105, 55 + Math.sin(this.animFrame*0.2)*12); this.ctx.lineTo(55, 85); this.ctx.fill();
                this.ctx.fillStyle = "#f1c40f"; 
                this.ctx.save(); this.ctx.translate(68, 58); this.ctx.beginPath();
                for(let i=0; i<5; i++) { this.ctx.lineTo(Math.cos((18+i*72)*Math.PI/180)*8, -Math.sin((18+i*72)*Math.PI/180)*8); this.ctx.lineTo(Math.cos((54+i*72)*Math.PI/180)*3.5, -Math.sin((54+i*72)*Math.PI/180)*3.5); }
                this.ctx.closePath(); this.ctx.fill(); this.ctx.restore();

                this.goldMines.forEach((m, idx) => {
                    this.ctx.fillStyle = "#f39c12"; this.ctx.beginPath(); this.ctx.arc(m.x, m.y, 18, 0, Math.PI * 2); this.ctx.fill();
                    this.ctx.fillStyle = "#e67e22"; this.ctx.beginPath(); this.ctx.arc(m.x-5, m.y+5, 14, 0, Math.PI * 2); this.ctx.fill();
                    this.ctx.fillStyle = "#fff"; this.ctx.font = "bold 11px 'Segoe UI'"; this.ctx.fillText("L" + (idx + 1), m.x - 9, m.y + 4);
                });

                let ex = this.canvas.width - 100;
                this.ctx.fillStyle = "#1c2833"; this.ctx.fillRect(ex, 150, 90, 270); 
                this.ctx.fillStyle = "#111"; this.ctx.fillRect(ex, 130, 25, 30); this.ctx.fillRect(ex+35, 130, 25, 30); this.ctx.fillRect(ex+70, 130, 20, 30); 
                
                this.ctx.strokeStyle = "#555"; this.ctx.lineWidth = 2;
                this.ctx.beginPath(); this.ctx.moveTo(ex-30, 350); this.ctx.lineTo(ex, 320); this.ctx.stroke();
                this.ctx.beginPath(); this.ctx.moveTo(ex-30, 320); this.ctx.lineTo(ex, 350); this.ctx.stroke();

                if(this.enemyShieldTimer > 0) {
                    this.ctx.shadowBlur = 40; this.ctx.shadowColor = "#e74c3c";
                    this.ctx.strokeStyle = `rgba(231, 76, 60, ${0.6 + Math.sin(this.animFrame*0.15)*0.4})`;
                    this.ctx.lineWidth = 10;
                    this.ctx.beginPath(); this.ctx.arc(ex+45, 280, 160, Math.PI/2, Math.PI*1.5); this.ctx.stroke();
                    this.ctx.shadowBlur = 0;
                }

                this.ctx.fillStyle = "#bdc3c7"; this.ctx.fillRect(ex+40, 30, 5, 100);
                this.ctx.fillStyle = "#000"; 
                this.ctx.beginPath(); this.ctx.moveTo(ex+40, 35); this.ctx.lineTo(ex-10, 55 + Math.sin(this.animFrame*0.2)*12); this.ctx.lineTo(ex+40, 85); this.ctx.fill();
            }

            drawMinimap() {
                this.ctx.fillStyle = "rgba(0, 0, 0, 0.6)"; this.ctx.strokeStyle = "#f1c40f"; this.ctx.lineWidth = 2;
                this.ctx.fillRect(this.canvas.width/2 - 150, 10, 300, 30); this.ctx.strokeRect(this.canvas.width/2 - 150, 10, 300, 30);
                
                this.ctx.fillStyle = "#3498db";
                this.units.forEach(u => {
                    if(u.type !== 'miner') { let mx = (this.canvas.width/2 - 150) + (u.x / this.canvas.width) * 300; this.ctx.fillRect(mx, 20, 3, 10); }
                });
                
                this.ctx.fillStyle = "#e74c3c";
                this.enemies.forEach(e => { let mx = (this.canvas.width/2 - 150) + (e.x / this.canvas.width) * 300; this.ctx.fillRect(mx, 20, 3, 10); });
            }

            drawMenuOverlay(title, subtitle, btnText, color) {
                this.ctx.fillStyle = "rgba(0, 0, 0, 0.85)"; this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
                this.ctx.fillStyle = color; this.ctx.font = "900 42px 'Segoe UI'"; this.ctx.textAlign = "center"; this.ctx.shadowBlur = 30; this.ctx.shadowColor = color;
                this.ctx.fillText(title, this.canvas.width / 2, this.canvas.height / 2 - 40); this.ctx.shadowBlur = 0;
                
                if (this.level === 1) subtitle = "MÀN 1: BẢO VỆ VÙNG GIẢI PHÓNG - Cẩn thận máy bay ném bom mỗi 60s!";
                else if (this.level === 2) subtitle = "MÀN 2: TẬP KÍCH BAN ĐÊM - Địch tử thủ (Dưới 50% HP) gọi viện binh!";
                else if (this.level === 3) subtitle = "MÀN 3: HOÀNG HÔN ĐẪM MÁU - Trận chiến sinh tử. Quân ta thủ thành GIẢM 90% DMG!";
                
                this.ctx.fillStyle = "#ecf0f1"; this.ctx.font = "italic 20px 'Segoe UI'";
                this.ctx.fillText(subtitle, this.canvas.width / 2, this.canvas.height / 2 + 10);
                this.ctx.fillStyle = "linear-gradient(145deg, #1b4f72, #0d283a)"; this.ctx.fillRect(this.canvas.width / 2 - 140, this.canvas.height / 2 + 50, 280, 50);
                this.ctx.fillStyle = "#f1c40f"; this.ctx.font = "bold 20px 'Segoe UI'";
                this.ctx.fillText(btnText, this.canvas.width / 2, this.canvas.height / 2 + 82); this.ctx.textAlign = "left";
            }
            
            drawVictorySpeech() {
                this.ctx.fillStyle = "#c0392b"; this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
                
                this.ctx.save(); this.ctx.translate(this.canvas.width/2, this.canvas.height/2); this.ctx.rotate(this.animFrame*0.005);
                this.ctx.fillStyle = "rgba(241, 196, 15, 0.3)"; this.ctx.beginPath();
                for(let i=0; i<5; i++) { this.ctx.lineTo(Math.cos((18+i*72)*Math.PI/180)*250, -Math.sin((18+i*72)*Math.PI/180)*250); this.ctx.lineTo(Math.cos((54+i*72)*Math.PI/180)*100, -Math.sin((54+i*72)*Math.PI/180)*100); }
                this.ctx.closePath(); this.ctx.fill(); this.ctx.restore();
                
                this.ctx.fillStyle = "#f1c40f"; this.ctx.font = "bold 26px 'Segoe UI'"; this.ctx.textAlign = "center";
                this.ctx.shadowBlur = 10; this.ctx.shadowColor = "#000";
                
                for(let i=0; i<this.speechLines.length; i++) { this.ctx.fillText(this.speechLines[i], this.canvas.width/2, this.speechY + i*45); }
                this.ctx.textAlign = "left"; this.ctx.shadowBlur = 0;
                
                this.speechY -= 0.6; 
                
                if(this.speechY < -200) {
                    this.ctx.fillStyle = "rgba(0,0,0,0.8)"; this.ctx.fillRect(this.canvas.width/2 - 100, this.canvas.height - 60, 200, 40);
                    this.ctx.fillStyle = "#fff"; this.ctx.font = "bold 16px 'Segoe UI'"; this.ctx.textAlign = "center";
                    this.ctx.fillText("BẤM ĐỂ CHƠI LẠI TỪ ĐẦU", this.canvas.width/2, this.canvas.height - 35); this.ctx.textAlign = "left";
                }
            }
            
            spawnEmergencyUnits(isEnemy) {
                let count = 30; 
                if(isEnemy) { count = this.level === 1 ? 30 : (this.level === 2 ? 40 : 60); }
                for(let i=0; i<count; i++) {
                    if (isEnemy) {
                        let types = ['goblin', 'orc', 'shadow_mage', 'giant']; let t = types[Math.floor(Math.random() * types.length)];
                        let levelMult = 1 + (this.level - 1) * 0.5; 
                        let stats = { goblin: { hp: 120*levelMult, dmg: 16*levelMult, range: 45, speed: 1.6, size: 0.95 }, orc: { hp: 250*levelMult, dmg: 30*levelMult, range: 50, speed: 1.2, size: 1.2 }, shadow_mage: { hp: 180*levelMult, dmg: 45*levelMult, range: 250, speed: 0.9, size: 1.05 }, giant: { hp: 750*levelMult, dmg: 70*levelMult, range: 280, speed: 0.6, size: 1.85 } }[t];
                        this.enemies.push(new GameObject(this.canvas.width - 130 + Math.random()*50, 160 + Math.random() * 220, t, true, stats));
                    } else {
                        let types = ['swordwrath', 'archidon', 'spearton']; let t = types[Math.floor(Math.random() * types.length)];
                        let stats = { swordwrath: { hp: 180, dmg: 26, range: 45, speed: 1.6, size: 1.0 }, archidon: { hp: 130, dmg: 35, range: 250, speed: 1.4, size: 1.0 }, spearton: { hp: 320, dmg: 45, range: 70, speed: 1.2, size: 1.2 } }[t];
                        this.units.push(new GameObject(130 - Math.random()*50, 160 + Math.random() * 220, t, false, { hp: stats.hp * (1 + (this.techLevel - 1) * 0.25), dmg: stats.dmg * (1 + (this.techLevel - 1) * 0.3), range: stats.range, speed: stats.speed, size: stats.size }, this.techLevel));
                    }
                }
            }

            run() {
                if (this.state === 'VICTORY_SPEECH') {
                    this.animFrame++; this.ctx.clearRect(0,0,this.canvas.width,this.canvas.height);
                    this.drawVictorySpeech();
                    requestAnimationFrame(() => this.run()); return;
                }

                if (this.statueHp <= 0 && this.state === 'PLAYING') { 
                    this.state = 'GAME_OVER'; 
                    this.drawMenuOverlay("💀 THÀNH TRÌ ĐÃ VỠ!", "Quân ta đã hy sinh anh dũng tại Màn " + this.level, "BẤM VÀO ĐÂY ĐỂ CHƠI LẠI", "#e74c3c"); 
                    return; 
                }
                
                // FIX LỖI MÁU ẢO KẸT MÀN
                if (this.enemyStatueHp <= 0 && this.state === 'PLAYING') {
                    this.state = 'TRANSITION';
                    this.transitionTimer = 180; // Dừng lại ngắm chiến thắng 3 giây trước khi qua màn
                    if (this.level >= this.maxLevel) {
                        this.addFloatingText("⭐ ĐẠI THẮNG MÙA XUÂN! ĐANG CHUYỂN CẢNH...", this.canvas.width/2-200, this.canvas.height/2, '#f1c40f', true);
                    } else {
                        this.addFloatingText("🎖️ CĂN CỨ ĐỊCH BỊ SAN PHẲNG!", this.canvas.width/2-150, this.canvas.height/2, '#2ecc71', true);
                    }
                }
                
                if (this.state === 'TRANSITION') {
                    this.transitionTimer--;
                    if (this.transitionTimer <= 0) {
                        this.nextLevel();
                    }
                }

                this.animFrame++; this.ctx.save();
                if (this.screenShake > 0) { this.screenShake--; this.ctx.translate((Math.random() - 0.5) * 20, (Math.random() - 0.5) * 20); }

                this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                this.drawEnvironment(); this.drawBases();

                if (this.state === 'MENU') { 
                    this.drawMenuOverlay("MÀN " + this.level + ": SẴN SÀNG CHIẾN ĐẤU", "", "BẤM ĐỂ XUẤT QUÂN", "#3498db"); 
                    this.ctx.restore(); requestAnimationFrame(() => this.run()); return; 
                }
                
                this.drawMinimap(); 
                
                if (this.ourShieldTimer > 0) this.ourShieldTimer--;
                if (this.enemyShieldTimer > 0) this.enemyShieldTimer--;
                
                let enemyMaxHp = 3000 + (this.level * 2500);
                if (this.enemyStatueHp <= enemyMaxHp/2 && !this.enemyEmergencyTriggered && this.state === 'PLAYING') {
                    this.enemyEmergencyTriggered = true; this.enemyShieldTimer = 900; 
                    this.spawnEmergencyUnits(true);
                    this.addFloatingText("ĐỊCH TỬ THỦ! VIỆN BINH ĐỔ BỘ", this.canvas.width - 250, 100, '#e74c3c', true);
                    this.screenShake = 30;
                }
                
                if (this.statueHp <= 1500 && !this.ourEmergencyTriggered && this.state === 'PLAYING') {
                    this.ourEmergencyTriggered = true; this.ourShieldTimer = 900;
                    this.spawnEmergencyUnits(false);
                    let shieldPct = this.level === 1 ? 50 : (this.level === 2 ? 70 : 90);
                    this.addFloatingText(`TA TỬ THỦ! GIẢM ${shieldPct}% SÁT THƯƠNG`, 150, 100, '#3498db', true);
                    this.screenShake = 30;
                }
                
                this.updateUI(); 

                this.airRaidTimer++;
                let targetFrames = this.level === 1 ? 3600 : (this.level === 2 ? 1800 : 900); 
                if (this.airRaidTimer >= targetFrames) { this.triggerAirRaidWarning(); this.airRaidTimer = 0; }
                if (this.airRaidWarning > 0) { 
                    this.ctx.fillStyle = "rgba(231, 76, 60, 0.2)"; this.ctx.fillRect(0,0,this.canvas.width,this.canvas.height);
                    this.addFloatingText("⚠️ BÁO ĐỘNG KHÔNG QUÂN!", this.canvas.width/2-100, 80, '#e74c3c', true);
                    this.airRaidWarning--; if (this.airRaidWarning === 1) { this.isEnemyBomberActive = true; this.enemyBomberX = -100; } 
                }

                if (this.isEnemyBomberActive) {
                    this.enemyBomberX += 14;
                    this.ctx.fillStyle = "#111"; this.ctx.shadowBlur = 20; this.ctx.shadowColor = "#e74c3c";
                    this.ctx.beginPath(); this.ctx.arc(this.enemyBomberX, 40, 35, 0, Math.PI*2); this.ctx.fill();
                    this.ctx.beginPath(); this.ctx.moveTo(this.enemyBomberX + 20, 40); this.ctx.lineTo(this.enemyBomberX - 35, 10); this.ctx.lineTo(this.enemyBomberX - 15, 40); this.ctx.fill();
                    this.ctx.shadowBlur = 0;
                    
                    if (this.enemyBomberX % 30 < 14) {
                        this.screenShake = 25; this.particles.emit(this.enemyBomberX - 20, 200 + Math.random()*200, '#e74c3c', 'spark', 40); 
                        this.particles.emit(this.enemyBomberX - 20, 200 + Math.random()*200, '#111', 'smoke', 20); 
                        this.units.forEach(u => {
                            if (!this.isHiding) { u.hp -= 300; this.particles.emit(u.x, u.y, '#900C3F', 'blood', 15); this.addFloatingText("-300 BOM", u.x, u.y, '#e74c3c'); } 
                            else { this.addFloatingText("An toàn", u.x, u.y-10, '#2ecc71'); }
                        });
                    }
                    if (this.enemyBomberX > this.canvas.width + 150) this.isEnemyBomberActive = false;
                }

                if (this.isPlaneActive) {
                    this.planeX += 15;
                    this.ctx.fillStyle = "#34495e"; this.ctx.shadowBlur = 20; this.ctx.shadowColor = "#f1c40f";
                    this.ctx.beginPath(); this.ctx.arc(this.planeX, 50, 30, 0, Math.PI*2); this.ctx.fill(); this.ctx.shadowBlur=0;
                    if (this.planeX % 30 < 15) { this.particles.emit(this.planeX, 60, '#f1c40f', 'spark', 30); }
                    if (this.planeX > this.canvas.width + 150) this.isPlaneActive = false;
                }

                this.projectiles.forEach((proj, idx) => { proj.updateAndDraw(this.ctx, this.particles); if (!proj.active) this.projectiles.splice(idx, 1); });
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
                                    let dx = 100 - u.x; let dy = 260 - u.y; let dist = Math.hypot(dx, dy);
                                    if (dist > 3) { u.x += (dx / dist) * moveSpeed; u.y += (dy / dist) * moveSpeed; }
                                    else {
                                        this.gold += u.goldBag || 15; u.goldBag = 0; u.state = 'going';
                                        this.particles.emit(100, 260, '#f1c40f', 'spark', 20); this.addFloatingText("+" + (15 * this.techLevel), 100, 260, '#f1c40f', true);
                                    }
                                }
                            }
                        } else {
                            let nearestEnemy = this.enemies.find(e => Math.abs(e.x - u.x) <= u.range);
                            if (nearestEnemy) {
                                if (u.attackCd > 0) u.attackCd--;
                                else { 
                                    if(u.type === 'archidon') this.projectiles.push(new Projectile(u.x, u.y-10, nearestEnemy, 'arrow', u.dmg, false));
                                    else if(u.type === 'magikill') this.projectiles.push(new Projectile(u.x, u.y-25, nearestEnemy, 'magic', u.dmg, false));
                                    else if(u.type === 'giant') { this.projectiles.push(new Projectile(u.x+40, u.y-25, nearestEnemy, 'cannon', u.dmg, false)); this.screenShake = 8; }
                                    else {
                                        nearestEnemy.hp -= u.dmg; this.particles.emit(nearestEnemy.x, nearestEnemy.y, '#c0392b', 'blood', 15); 
                                        this.addFloatingText("-" + Math.floor(u.dmg), nearestEnemy.x, nearestEnemy.y - 15, '#e74c3c'); 
                                    }
                                    u.attackCd = u.maxCd; 
                                }
                            } else {
                                let targetX = this.currentCommand === 'ATTACK' ? this.canvas.width - 130 : 250;
                                let distToBase = (this.canvas.width - 100) - u.x;
                                
                                if (this.currentCommand === 'ATTACK' && distToBase <= u.range) {
                                    if (u.attackCd > 0) u.attackCd--;
                                    else {
                                        let dmgMult = this.enemyShieldTimer > 0 ? 0.5 : 1; 
                                        let actualDmg = u.dmg * dmgMult;
                                        
                                        if(u.type === 'archidon' || u.type === 'magikill' || u.type === 'giant') {
                                            let pType = u.type === 'giant' ? 'cannon' : (u.type === 'archidon' ? 'arrow' : 'magic');
                                            this.projectiles.push(new Projectile(u.x, u.y-25, {x: this.canvas.width-100, y: 260, hp: 9999}, pType, actualDmg, false));
                                            if (u.type === 'giant') this.screenShake = 8;
                                        }
                                        // FIX MÁU ẢO ÉP VỀ 0
                                        this.enemyStatueHp = Math.max(0, this.enemyStatueHp - actualDmg); 
                                        setTimeout(() => { this.particles.emit(this.canvas.width - 100, 260, '#f1c40f', 'spark', 25); this.addFloatingText("-" + Math.floor(actualDmg), this.canvas.width - 100, 200 + Math.random()*50, '#f1c40f', true); }, 200);
                                        u.attackCd = u.maxCd; 
                                    }
                                } else if (u.x < targetX) { u.x += u.speed; }
                            }
                        }
                    }
                    u.draw(this.ctx, this.animFrame, this.isHiding); if (u.hp <= 0) { this.particles.emit(u.x, u.y, '#900C3F', 'blood', 25); this.particles.emit(u.x, u.y, '#333', 'debris', 5); this.units.splice(idx, 1); }
                });

                // LÍNH ĐỊCH
                this.enemies.forEach((e, idx) => {
                    let nearestUnit = this.units.find(u => u.type !== 'miner' && Math.abs(u.x - e.x) <= e.range);
                    if (nearestUnit && !this.isHiding) { 
                        if (e.attackCd > 0) e.attackCd--;
                        else { 
                            if(e.type === 'shadow_mage') this.projectiles.push(new Projectile(e.x, e.y-25, nearestUnit, 'magic', e.dmg, true));
                            else if(e.type === 'giant') { this.projectiles.push(new Projectile(e.x-40, e.y-25, nearestUnit, 'cannon', e.dmg, true)); this.screenShake = 8; }
                            else {
                                nearestUnit.hp -= e.dmg; this.particles.emit(nearestUnit.x, nearestUnit.y, '#c0392b', 'blood', 15); 
                                this.addFloatingText("-" + Math.floor(e.dmg), nearestUnit.x, nearestUnit.y - 15, '#c0392b'); 
                            }
                            e.attackCd = e.maxCd; 
                        }
                    } else {
                        let distToBase = e.x - 100; 
                        if (distToBase <= e.range) {
                            if (e.attackCd > 0) e.attackCd--;
                            else {
                                let dmgMult = 1;
                                if(this.ourShieldTimer > 0) { dmgMult = this.level === 1 ? 0.5 : (this.level === 2 ? 0.3 : 0.1); }
                                let actualDmg = e.dmg * dmgMult;
                                
                                if(e.type === 'shadow_mage' || e.type === 'giant') {
                                    let pType = e.type === 'giant' ? 'cannon' : 'magic';
                                    this.projectiles.push(new Projectile(e.x, e.y-25, {x: 100, y: 260, hp: 9999}, pType, actualDmg, true));
                                    if (e.type === 'giant') this.screenShake = 8;
                                }
                                // FIX MÁU ẢO ÉP VỀ 0
                                this.statueHp = Math.max(0, this.statueHp - actualDmg); 
                                setTimeout(() => { this.particles.emit(100, 260, '#e74c3c', 'spark', 25); this.addFloatingText("-" + Math.floor(actualDmg), 100, 200 + Math.random()*50, '#e74c3c', true); }, 200);
                                e.attackCd = e.maxCd; 
                            }
                        } else { e.x -= e.speed; }
                    }
                    e.draw(this.ctx, this.animFrame, false); 
                    if (e.hp <= 0) { this.particles.emit(e.x, e.y, '#7f8c8d', 'smoke', 25); this.particles.emit(e.x, e.y, '#333', 'debris', 5); this.enemies.splice(idx, 1); this.gold += (40 + this.level*15); this.addFloatingText("+" + (40 + this.level*15), e.x, e.y-20, '#f1c40f'); }
                });

                this.floatingTexts.forEach((ft, idx) => { 
                    ft.y -= 1.2; ft.alpha -= 0.02; 
                    this.ctx.fillStyle = ft.color; this.ctx.globalAlpha = Math.max(0, ft.alpha); 
                    this.ctx.font = ft.isBig ? "900 18px 'Segoe UI'" : "bold 13px 'Segoe UI'"; 
                    this.ctx.shadowBlur = 4; this.ctx.shadowColor = "#000";
                    this.ctx.fillText(ft.text, ft.x, ft.y); 
                    this.ctx.globalAlpha = 1.0; this.ctx.shadowBlur = 0;
                    if (ft.alpha <= 0) this.floatingTexts.splice(idx, 1); 
                });
                
                this.drawRain(); 
                this.ctx.restore(); requestAnimationFrame(() => this.run());
            }
        }

        const GameManager = new RTSGameManager();

        setInterval(() => {
            if (GameManager.state === 'PLAYING' && GameManager.enemyStatueHp > 0 && GameManager.enemies.length < 45) {
                let types = ['goblin', 'orc', 'shadow_mage', 'giant']; let t = types[Math.floor(Math.random() * types.length)];
                let levelMult = 1 + (GameManager.level - 1) * 0.5; 
                let stats = { goblin: { hp: 130*levelMult, dmg: 18*levelMult, range: 45, speed: 1.7, size: 0.95 }, orc: { hp: 270*levelMult, dmg: 32*levelMult, range: 50, speed: 1.3, size: 1.2 }, shadow_mage: { hp: 190*levelMult, dmg: 48*levelMult, range: 250, speed: 1.0, size: 1.05 }, giant: { hp: 800*levelMult, dmg: 75*levelMult, range: 280, speed: 0.6, size: 1.85 } }[t];
                GameManager.enemies.push(new GameObject(GameManager.canvas.width - 130, 160 + Math.random() * 220, t, true, stats));
            }
        }, 2500);

        GameManager.run();
    </script>
</body>
</html>
"""

st.components.v1.html(game_html, height=750, scrolling=False)
