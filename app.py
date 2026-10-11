import streamlit as st
import random

st.set_page_config(page_title="Game Chiến Tranh Pháo Đài", page_icon="🛡️")

st.title("🛡️ Chiến Tranh Phòng Thủ Pháo Đài")
st.markdown("Bảo vệ căn cứ của bạn khỏi các đợt tấn công của kẻ địch!")

if "hp" not in st.session_state:
    st.session_state.hp = 100
if "score" not in st.session_state:
    st.session_state.score = 0
if "enemies_left" not in st.session_state:
    st.session_state.enemies_left = 5

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="❤️ Máu Pháo Đài", value=f"{st.session_state.hp}%")
with col2:
    st.metric(label="🎯 Điểm Tiêu Diệt", value=st.session_state.score)
with col3:
    st.metric(label="⚠️ Địch Còn Lại", value=st.session_state.enemies_left)

st.markdown("---")

if st.session_state.hp > 0 and st.session_state.enemies_left > 0:
    st.subheader("Trận chiến đang diễn ra...")
    
    if st.button("🔥 BẮN ĐẠI BÁC!", type="primary", use_container_width=True):
        hit = random.choice([True, True, False])
        if hit:
            st.session_state.score += 10
            st.session_state.enemies_left -= 1
            st.success("💥 Bách phát bách trúng! Tiêu diệt được 1 tên địch.")
        else:
            st.warning("❌ Trượt mất rồi! Kẻ địch đang áp sát.")
            
        damage = random.randint(5, 15)
        st.session_state.hp = max(0, st.session_state.hp - damage)
        st.rerun()

if st.session_state.hp <= 0:
    st.error("💀 THẤT BẠI! Pháo Đài của bạn đã bị phá hủy hoàn toàn.")
    if st.button("🔄 Chơi Lại Từ Đầu"):
        st.session_state.hp = 100
        st.session_state.score = 0
        st.session_state.enemies_left = 5
        st.rerun()

elif st.session_state.enemies_left <= 0:
    st.balloons()
    st.success("🏆 CHIẾN THẮNG! Bạn đã quét sạch toàn bộ kẻ địch bảo vệ thành công căn cứ!")
    if st.button("🎮 Chơi Màn Mới"):
        st.session_state.hp = 100
        st.session_state.score += 50
        st.session_state.enemies_left = 8 + random.randint(1, 5)
        st.rerun()
