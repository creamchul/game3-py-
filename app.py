import streamlit as st
import random
from PIL import Image
import os
import pickle
from dataclasses import dataclass, field
from typing import List, Optional, Dict
import base64

# CSS 스타일 정의
def set_custom_style():
    st.markdown("""
    <style>
    .main {
        background-color: #f5f7ff;
        padding: 20px;
    }
    .stApp {
        max-width: 1000px;
        margin: 0 auto;
    }
    .creature-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        border-left: 5px solid #4CAF50;
        transition: transform 0.3s ease;
    }
    .creature-card:hover {
        transform: translateY(-5px);
    }
    .creature-title {
        font-size: 24px;
        font-weight: bold;
        color: #303F9F;
        margin-bottom: 10px;
    }
    .attribute-fire {
        color: #FF5722;
        font-weight: bold;
    }
    .attribute-water {
        color: #2196F3;
        font-weight: bold;
    }
    .attribute-grass {
        color: #4CAF50;
        font-weight: bold;
    }
    .attribute-electric {
        color: #FFC107;
        font-weight: bold;
    }
    .emotion-happy {
        color: #4CAF50;
        font-weight: bold;
    }
    .emotion-normal {
        color: #9E9E9E;
        font-weight: bold;
    }
    .emotion-sad {
        color: #2196F3;
        font-weight: bold;
    }
    .emotion-depressed {
        color: #673AB7;
        font-weight: bold;
    }
    .emotion-angry {
        color: #F44336;
        font-weight: bold;
    }
    .stat-label {
        font-weight: bold;
        color: #555;
    }
    .dialogue-box {
        background-color: #f9f9f9;
        border-left: 3px solid #9c27b0;
        padding: 10px 15px;
        margin: 10px 0;
        border-radius: 0 5px 5px 0;
        font-style: italic;
    }
    .interact-button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .interact-button:hover {
        background-color: #45a049;
    }
    footer {
        text-align: center;
        margin-top: 50px;
        color: #777;
    }
    </style>
    """, unsafe_allow_html=True)

# 캐릭터 클래스 정의
@dataclass
class Creature:
    name: str
    attribute: str
    emotion_value: int = 50  # 감정 수치 (0-100)
    level: int = 1
    exp: int = 0
    evolve_level: int = 5
    dialogues: Dict[str, Dict[str, str]] = field(default_factory=dict)
    
    @property
    def emotion(self):
        """감정 수치에 따른 감정 상태 반환"""
        if self.emotion_value >= 80:
            return "행복"
        elif self.emotion_value >= 50:
            return "평범"
        elif self.emotion_value >= 20:
            return "슬픔"
        else:
            return "우울"
    
    def get_dialogue(self):
        """현재 감정 상태에 맞는 대사 반환"""
        if self.name in self.dialogues and self.emotion in self.dialogues[self.name]:
            return self.dialogues[self.name][self.emotion]
        return f"{self.name}이(가) {self.emotion} 상태입니다."
    
    def interact(self):
        """캐릭터와 교감하기"""
        old_emotion = self.emotion
        
        # 감정 변화 (-10 ~ +15)
        emotion_change = random.randint(-10, 15)
        self.emotion_value = max(0, min(100, self.emotion_value + emotion_change))
        
        # 경험치 증가
        self.exp += 10
        
        # 대사 가져오기
        dialogue = self.get_dialogue()
        
        # 결과 메시지
        message = f"{self.name}의 감정이 {old_emotion}에서 {self.emotion}으로 변했습니다! (경험치 +10)"
        
        # 레벨업 체크
        if self.exp >= self.level * 20:
            self.level += 1
            message += f"\n레벨업! {self.name}의 레벨이 {self.level}이 되었습니다!"
            
            # 진화 체크
            if self.level >= self.evolve_level:
                message += f"\n🌟 {self.name}가 진화 레벨에 도달했습니다! 진화 완료! 🌟"
                
        return message, dialogue

# 캐릭터별 대사 정의
def get_default_dialogues():
    return {
        "피카츄": {
            "행복": "피카피카! 너랑 함께 있으면 정말 기뻐!",
            "평범": "피카~ 그럭저럭 괜찮아~",
            "슬픔": "피카... 왠지 오늘은 기분이 안 좋아...",
            "우울": "피...카... 나 혼자 남겨진 느낌이야..."
        },
        "꼬부기": {
            "행복": "꼬북꼬북! 물놀이 같이 하자!",
            "평범": "꼬북~ 오늘 날씨가 좋네~",
            "슬픔": "꼬북... 비가 오려나봐...",
            "우울": "꼬...북... 물이 너무 차가워..."
        },
        "이상해씨": {
            "행복": "이상~해! 햇살이 너무 좋아!",
            "평범": "이상~ 새싹이 자라고 있어",
            "슬픔": "이상... 햇빛이 부족해...",
            "우울": "이...상... 겨울이 너무 길어..."
        }
    }

# 세션 상태 초기화
def init_session_state():
    if 'creatures' not in st.session_state:
        # 기본 대사 가져오기
        default_dialogues = get_default_dialogues()
        
        # 기본 캐릭터 생성
        st.session_state.creatures = [
            Creature(
                name="피카츄", 
                attribute="전기", 
                emotion_value=random.randint(40, 90), 
                evolve_level=4, 
                dialogues=default_dialogues
            ),
            Creature(
                name="꼬부기", 
                attribute="물", 
                emotion_value=random.randint(30, 80), 
                evolve_level=5, 
                dialogues=default_dialogues
            ),
            Creature(
                name="이상해씨", 
                attribute="풀", 
                emotion_value=random.randint(20, 70), 
                evolve_level=6, 
                dialogues=default_dialogues
            ),
        ]
    
    if 'interaction_history' not in st.session_state:
        st.session_state.interaction_history = []

# 감정 이모티콘 가져오기
def get_emotion_emoji(emotion):
    if emotion == "행복":
        return "😊"
    elif emotion == "평범":
        return "😐"
    elif emotion == "슬픔":
        return "😢"
    elif emotion == "우울":
        return "😰"
    elif emotion == "화남":
        return "😡"
    return "😐"

# 속성 아이콘 가져오기
def get_attribute_icon(attribute):
    if attribute == "불":
        return "🔥"
    elif attribute == "물":
        return "💧"
    elif attribute == "풀":
        return "🌿"
    elif attribute == "전기":
        return "⚡"
    return "✨"

# 속성 스타일 클래스 가져오기
def get_attribute_class(attribute):
    if attribute == "불":
        return "attribute-fire"
    elif attribute == "물":
        return "attribute-water"
    elif attribute == "풀":
        return "attribute-grass"
    elif attribute == "전기":
        return "attribute-electric"
    return ""

# 감정 스타일 클래스 가져오기
def get_emotion_class(emotion):
    if emotion == "행복":
        return "emotion-happy"
    elif emotion == "평범":
        return "emotion-normal"
    elif emotion == "슬픔":
        return "emotion-sad"
    elif emotion == "우울":
        return "emotion-depressed"
    elif emotion == "화남":
        return "emotion-angry"
    return ""

# 경험치 바 표시
def render_exp_bar(creature):
    next_level_exp = creature.level * 20
    progress = min(1.0, creature.exp / next_level_exp)
    
    st.progress(progress)
    st.caption(f"경험치: {creature.exp}/{next_level_exp}")

# 감정 수치 바 표시
def render_emotion_bar(creature):
    emotion_color = "green" if creature.emotion_value >= 80 else \
                   "blue" if creature.emotion_value >= 50 else \
                   "orange" if creature.emotion_value >= 20 else "red"
    
    st.progress(creature.emotion_value / 100, emotion_color)
    st.caption(f"감정 수치: {creature.emotion_value}/100")

# 캐릭터 카드 렌더링
def render_creature_card(creature, index):
    st.markdown(f"""
    <div class="creature-card">
        <div class="creature-title">
            {creature.name} {get_attribute_icon(creature.attribute)} Lv.{creature.level}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # 속성 정보
        attribute_class = get_attribute_class(creature.attribute)
        st.markdown(f"""
        <span class="stat-label">속성:</span> 
        <span class="{attribute_class}">{creature.attribute} {get_attribute_icon(creature.attribute)}</span>
        """, unsafe_allow_html=True)
        
        # 감정 상태
        emotion_class = get_emotion_class(creature.emotion)
        st.markdown(f"""
        <span class="stat-label">감정:</span> 
        <span class="{emotion_class}">{creature.emotion} {get_emotion_emoji(creature.emotion)}</span>
        """, unsafe_allow_html=True)
        
        # 감정 수치 바
        render_emotion_bar(creature)
        
        # 캐릭터 대사
        st.markdown(f"""
        <div class="dialogue-box">
            "{creature.get_dialogue()}"
        </div>
        """, unsafe_allow_html=True)
        
        # 레벨과 경험치 바
        st.markdown(f"""
        <span class="stat-label">레벨:</span> {creature.level} / 진화 레벨: {creature.evolve_level}
        """, unsafe_allow_html=True)
        
        render_exp_bar(creature)
        
        # 진화 완료 메시지
        if creature.level >= creature.evolve_level:
            st.success(f"🌟 {creature.name}의 진화가 완료되었습니다! 🌟")
    
    with col2:
        # 교감하기 버튼
        if st.button(f"{get_emotion_emoji(creature.emotion)} 교감하기", key=f"interact_{index}"):
            message, dialogue = creature.interact()
            
            # 히스토리에 추가
            st.session_state.interaction_history.append(f"{message}\n{creature.name}: \"{dialogue}\"")
            if len(st.session_state.interaction_history) > 5:
                st.session_state.interaction_history.pop(0)
                
            st.success(message)
            st.info(f"{creature.name}: \"{dialogue}\"")
            st.rerun()

# 히스토리 표시
def render_history():
    if st.session_state.interaction_history:
        st.markdown("### 최근 활동")
        for i, message in enumerate(reversed(st.session_state.interaction_history)):
            st.info(message)

# 메인 함수
def main():
    st.set_page_config(
        page_title="감정 수집 게임", 
        page_icon="🎮",
        layout="wide"
    )
    
    # 커스텀 CSS 적용
    set_custom_style()
    
    # 세션 상태 초기화
    init_session_state()
    
    # 사이드바
    with st.sidebar:
        st.image("https://raw.githubusercontent.com/streamlit/streamlit/master/examples/data/monster-battle-cover.png", use_column_width=True)
        st.title("🎮 감정 수집 게임")
        st.markdown("감정을 가진 귀여운 캐릭터들을 수집하고, 캐릭터와 교감하면서 성장시키는 게임")
        
        # 히스토리 표시
        render_history()
        
        st.markdown("---")
        st.markdown("© 2023 감정 수집 게임. 모든 권리 보유.")
    
    # 메인 콘텐츠
    st.title("🏆 나의 캐릭터 컬렉션")
    
    # 캐릭터 목록을 카드 형태로 표시
    for i, creature in enumerate(st.session_state.creatures):
        render_creature_card(creature, i)

if __name__ == "__main__":
    main() 