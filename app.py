import streamlit as st
import random
from PIL import Image
import os
import pickle
from dataclasses import dataclass, field
from typing import List, Optional
import base64

# 캐릭터 클래스 정의
@dataclass
class Creature:
    name: str
    attribute: str
    emotion: str
    level: int = 1
    exp: int = 0
    evolve_level: int = 5
    
    def interact(self):
        """캐릭터와 교감하기"""
        emotions = ["행복", "슬픔", "화남"]
        old_emotion = self.emotion
        self.emotion = random.choice(emotions)
        self.exp += 10
        
        message = f"{self.name}의 감정이 {old_emotion}에서 {self.emotion}으로 변했습니다! (경험치 +10)"
        
        # 레벨업 체크
        if self.exp >= self.level * 20:
            self.level += 1
            message += f"\n레벨업! {self.name}의 레벨이 {self.level}이 되었습니다!"
            
            # 진화 체크
            if self.level >= self.evolve_level:
                message += f"\n🌟 {self.name}가 진화 레벨에 도달했습니다! 진화 완료! 🌟"
                
        return message

# 세션 상태 초기화
def init_session_state():
    if 'creatures' not in st.session_state:
        # 기본 캐릭터 생성
        st.session_state.creatures = [
            Creature(name="피카츄", attribute="전기", emotion="행복", evolve_level=4),
            Creature(name="꼬부기", attribute="물", emotion="슬픔", evolve_level=5),
            Creature(name="이상해씨", attribute="풀", emotion="화남", evolve_level=6),
        ]

# 메인 함수
def main():
    st.set_page_config(page_title="감정 수집 게임", page_icon="🎮")
    
    # 세션 상태 초기화
    init_session_state()
    
    # 타이틀
    st.title("🎮 감정 수집 게임")
    st.subheader("감정을 가진 귀여운 캐릭터들을 수집하고, 캐릭터와 교감하면서 성장시키는 게임")
    
    # 캐릭터 목록 표시
    st.header("나의 캐릭터 목록")
    
    for i, creature in enumerate(st.session_state.creatures):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader(f"{creature.name}")
            
            # 캐릭터 정보 표시
            info_df = {
                "속성": [creature.attribute],
                "감정": [creature.emotion],
                "레벨": [creature.level],
                "경험치": [creature.exp],
                "진화 레벨": [creature.evolve_level]
            }
            st.dataframe(info_df)
            
            # 진화 완료 메시지
            if creature.level >= creature.evolve_level:
                st.success(f"🌟 {creature.name}의 진화가 완료되었습니다! 🌟")
        
        with col2:
            # 교감하기 버튼
            if st.button(f"{creature.name}와 교감하기", key=f"interact_{i}"):
                message = creature.interact()
                st.success(message)
                st.experimental_rerun()
    
    # 저작권 정보
    st.markdown("---")
    st.markdown("© 2023 감정 수집 게임. 모든 권리 보유.")

if __name__ == "__main__":
    main() 