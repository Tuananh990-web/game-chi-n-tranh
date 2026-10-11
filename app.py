import streamlit as st

st.set_page_config(page_title="Stick War 2: Order Empire - Deluxe Edition", page_icon="⚔️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: white; }
    iframe { border-radius: 14px; box-shadow: 0 10px 35px rgba(0,0,0,0.95); }
    </style>
""", unsafe_allow_html=True)

st.title("⚔️ Stick War 2: Order Empire (Bản Làm Lại Chuẩn Stick War)")
st.markdown("Khai thác mỏ vàng, điều khiển các kỹ năng tuyệt chiêu (Spin Attack, Shield Wall, Earthquake, Volley) & càn quét Cổng Quỷ!")

game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Stick War 2 Remake</title>
    <style>
        body { margin: 0; background: #0a0a0a; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; overflow: hidden; }
        canvas { background: linear-gradient(to bottom, #193318, #264a23); border: 4px solid #3d2817; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.9); cursor: crosshair; display: block; margin: 4px auto; }
        .ui-panel { display: flex; justify-content: center; flex-wrap: wrap; gap: 6px; margin-top: 4px; }
        .cmd-panel { display: flex; justify-content: center; gap: 8px; margin-top: 4px; }
        button { background: #966d13; color: white; border: 2px solid #ffcc00; padding: 6px 10px; font-weight: bold; font-size: 11px; border-radius: 5px; cursor: pointer; transition: 0.2s; }
        button:hover { background: #b8860b; transform: scale(1.05); }
        .cmd-btn { background: #1f618d; border-color: #48c9b0; }
        .ability-btn { background: #8e44ad; border-color: #f1c40f; }
        .stats { font-size: 13px; font-weight: bold; color: #ffcc00; margin-bottom: 2px; }
    </style>
</head>
<body>

    <div class="stats">
        🏰 Máu Thành: <span id="hpText">2000</span> | 🔮 Cổng Quỷ: <span id="portalHpText">2000</span> | 💰 Vàng: <span id="goldText">350</span> | 👥 Dân số: <span id="popText">0</span>/100 | ⚔️ Lệnh: <span id="cmdText" style="color:#2ecc71;">TẤN CÔNG</span>
    </div>

    <canvas id="gameCanvas" width="960" height="410"></canvas>

    <div class="cmd-panel">
        <button class="cmd-btn" onclick="setCommand('ATTACK')">⚔️ TẤN CÔNG</button>
        <button class="cmd-btn" onclick="setCommand('DEFEND')">🛡️ PHÒNG THỦ</button>
        <button class="cmd-btn" onclick="setCommand('RETREAT')">🚩 RÚT VỀ THÀNH (HỒI 6 HP/S)</button>
        <button class="ability-btn" onclick="triggerGlobalSkill('spin')">🌀 BÃO KIẾM</button>
        <button class="ability-btn" onclick="triggerGlobalSkill('volley')">🏹 MƯA TÊN</button>
        <button class="ability-btn" onclick="triggerGlobalSkill('earthquake')">💥 ĐẬP ĐẤT CHOÁNG</button>
        <button onclick="toggleAudio()">🔊 Âm Thanh</button>
    </div>

    <div class="ui-panel">
        <button onclick="spawnUnit('miner')">⛏️ Miner (30g - 1 Pop)</button>
        <button onclick="spawnUnit('footman')">⚔️ Swordwrath (40g - 1 Pop)</button>
        <button onclick="spawnUnit('archer')">🏹 Archidon (50g - 1 Pop)</button>
        <button onclick="spawnUnit('lancer')">🗡️ Spearton (70g - 3 Pop)</button>
        <button onclick="spawnUnit('mage')">🧙 Magikill (100g - 5 Pop)</button>
        <button onclick="spawnUnit('giant')">🗿 Giant (160g - 4 Pop)</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let castleHp = 2000, castleMaxHp = 2000;
        let portalHp = 2000, portalMaxHp = 2000;
        let gold = 350;
        let currentCommand = 'ATTACK';

        let castleEnragedTimer = 0; // 15 giây
        let portalEnragedTimer = 0;

        let units = [];
        let enemies = [];
        let projectiles = [];
        let particles = [];
        let animFrame = 0;
        let audioEnabled = false, audioCtx = null;

        function toggleAudio() {
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            audioEnabled = !audioEnabled;
        }

        function playSound(freq, type, duration) {
            if (!audioEnabled || !audioCtx) return;
            try {
                let osc = audioCtx.createOscillator();
                let gain = audioCtx.createGain();
                osc.type = type; osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                gain.gain.setValueAtTime(0.04, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.start(); osc.stop(audioCtx.currentTime + duration);
            } catch(e) {}
        }

        function setCommand(cmd) {
            currentCommand = cmd;
            let txt = cmd === 'ATTACK' ? 'TẤN CÔNG' : (cmd === 'DEFEND' ? 'PHÒNG THỦ' : 'RÚT VỀ THÀNH');
            document.getElementById("cmdText").innerText = txt;
        }

        function getCurrentPopulation() {
            let count = 0;
            units.forEach(u => {
                if (u.type === 'lancer') count += 3;
                else if (u.type === 'mage') count += 5;
                else if (u.type === 'giant') count += 4;
                else count += 1;
            });
            return count;
        }

        function triggerGlobalSkill(type) {
            if (type === 'spin') {
                units.filter(u => u.type === 'footman').forEach(u => {
                    u.isSpinning = 60; // 60 frame xoay kiếm
                    createParticles(u.x, u.y, '#3498db', 15);
                });
                playSound(500, 'sawtooth', 0.4);
            } else if (type === 'volley') {
                for(let i=0; i<15; i++) {
                    projectiles.push({
                        x: 400 + Math.random()*300, y: 0,
                        targetY: 200 + Math.random()*150,
                        vx: 0, vy: 12, type: 'arrow'
                    });
                }
                playSound(800, 'sine', 0.3);
            } else if (type === 'earthquake') {
                units.filter(u => u.type === 'giant').forEach(u => {
                    enemies.forEach(e => {
                        if (Math.hypot(e.x - u.x, e.y - u.y) < 180) {
                            e.stunned = 90; // Choáng 1.5s
                            e.hp -= 40;
                        }
                    });
                    createParticles(u.x, u.y, '#8e44ad', 30);
                });
                playSound(120, 'sawtooth', 0.6);
            }
        }
