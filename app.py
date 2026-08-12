import streamlit as st

st.set_page_config(
    page_title="Diet Creator",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: #f7fbf6;
}

.block-container {
    max-width: 1450px;
    padding: 0 3rem 2rem 3rem;
}

/* Navigation */
.navbar {
    background: white;
    padding: 18px 28px;
    border-radius: 0 0 18px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 3px 18px rgba(20, 80, 40, .08);
    margin-bottom: 25px;
}

.brand {
    font-size: 28px;
    font-weight: 800;
    color: #16833d;
}

.brand span {
    color: #f57c00;
}

.navlinks {
    display: flex;
    gap: 35px;
    color: #263238;
    font-weight: 600;
}

.navlinks .active {
    color: #16833d;
    border-bottom: 3px solid #16833d;
    padding-bottom: 7px;
}

.login {
    background: #16833d;
    color: white;
    padding: 11px 20px;
    border-radius: 10px;
    font-weight: 700;
}

/* Hero */
.hero {
    min-height: 330px;
    border-radius: 28px;
    padding: 55px;
    background: linear-gradient(115deg, #edf9e9 0%, #ffffff 52%, #fff1c9 100%);
    position: relative;
    overflow: hidden;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 52px;
    line-height: 1.12;
    color: #111;
    margin: 0;
    max-width: 620px;
}

.hero h1 span {
    color: #16833d;
}

.hero p {
    color: #4b5563;
    font-size: 18px;
    max-width: 550px;
    line-height: 1.7;
}

.hero-badge {
    display: inline-block;
    background: #16833d;
    color: white;
    padding: 13px 22px;
    border-radius: 12px;
    font-weight: 700;
    margin-top: 12px;
}

/* Cards */
.card {
    background: white;
    border-radius: 18px;
    padding: 22px;
    border: 1px solid #e6eee5;
    box-shadow: 0 5px 20px rgba(25, 80, 35, .06);
    height: 100%;
}

.card h3 {
    color: #16833d;
    margin-top: 0;
}

.metric {
    border-radius: 16px;
    padding: 20px;
    min-height: 115px;
}

.metric-green { background: #e8f8ed; }
.metric-blue { background: #e8f4ff; }
.metric-orange { background: #fff4df; }
.metric-pink { background: #ffeaf2; }

.metric-icon {
    font-size: 30px;
}

.metric-title {
    font-weight: 600;
    color: #52606d;
}

.metric-value {
    font-size: 24px;
    font-weight: 800;
}

/* Meal cards */
.meal {
    background: white;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #e8e8e8;
    box-shadow: 0 4px 15px rgba(0,0,0,.05);
    height: 100%;
}

.meal-head {
    color: white;
    padding: 12px;
    text-align: center;
    font-weight: 700;
}

.breakfast { background: #f59e0b; }
.snack { background: #16a34a; }
.lunch { background: #2196f3; }
.evening { background: #9333ea; }
.dinner { background: #ec407a; }

.meal-body {
    padding: 16px;
}

.food-image {
    width: 100%;
    height: 125px;
    object-fit: cover;
    border-radius: 12px;
    margin-bottom: 10px;
}

.food-list {
    color: #475569;
    font-size: 13px;
    line-height: 1.9;
}

.kcal {
    text-align: center;
    padding: 9px;
    border-radius: 9px;
    background: #f3f8f2;
    color: #16833d;
    font-weight: 800;
    margin-top: 12px;
}

/* Streamlit widgets */
div[data-testid="stButton"] button {
    background: linear-gradient(90deg, #16833d, #23a455);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 20px;
    font-weight: 700;
    width: 100%;
}

div[data-testid="stButton"] button:hover {
    background: linear-gradient(90deg, #0f6d31, #16833d);
    color: white;
}

.footer {
    background: #087b36;
    color: white;
    margin-top: 35px;
    padding: 25px;
    border-radius: 18px;
    text-align: center;
}

.small-note {
    color: #64748b;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# Navigation
st.markdown("""
<div class="navbar">
    <div class="brand">🌿 Diet <span>Creator</span></div>
    <div class="navlinks">
        <div class="active">Home</div>
        <div>About</div>
        <div>Diet Plans</div>
        <div>Nutrition</div>
        <div>Blog</div>
        <div>Contact</div>
    </div>
    <div class="login">♙ Login / Sign Up</div>
</div>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <h1>Create Your<br>Perfect <span>Diet Plan</span></h1>
    <p>
        Get a personalized diet plan based on your goals,
        preferences and lifestyle.
    </p>
    <div class="hero-badge">🥗 Eat Healthy • Live Healthy!</div>
</div>
""", unsafe_allow_html=True)

st.markdown("## 👤 Create Your Personalized Plan")

left, right = st.columns([1, 2.7], gap="large")

with left:
    st.markdown('<div class="card"><h3>👤 Your Information</h3>', unsafe_allow_html=True)

    name = st.text_input("Name", placeholder="Enter your name")
    age = st.number_input("Age", 10, 100, 22)
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    height = st.number_input("Height (cm)", 100, 220, 170)
    weight = st.number_input("Weight (kg)", 20, 200, 65)
    activity = st.selectbox(
        "Activity Level",
        ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"]
    )
    goal = st.selectbox(
        "Goal",
        ["Weight Loss", "Weight Maintenance", "Weight Gain"]
    )

    create = st.button("✨ Create My Diet Plan")

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    height_m = height / 100
    bmi = weight / (height_m * height_m)

    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_factor = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725
    }[activity]

    calories = bmr * activity_factor

    if goal == "Weight Loss":
        calories -= 400
    elif goal == "Weight Gain":
        calories += 350

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(f"""
        <div class="metric metric-green">
            <div class="metric-icon">🔥</div>
            <div class="metric-title">Daily Calories</div>
            <div class="metric-value">{calories:.0f} kcal</div>
            <small>Recommended</small>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown("""
        <div class="metric metric-blue">
            <div class="metric-icon">💧</div>
            <div class="metric-title">Water Intake</div>
            <div class="metric-value">2.5 L</div>
            <small>Per Day</small>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric metric-orange">
            <div class="metric-icon">🎯</div>
            <div class="metric-title">Goal</div>
            <div class="metric-value" style="font-size:18px">{goal}</div>
            <small>Personalized</small>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric metric-pink">
            <div class="metric-icon">⚖️</div>
            <div class="metric-title">BMI</div>
            <div class="metric-value">{bmi:.1f}</div>
            <small>{"Normal" if 18.5 <= bmi < 25 else "Check range"}</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🥗 Your Daily Diet Plan")

    meals = [
        ("🌅 Breakfast", "breakfast",
         "https://images.unsplash.com/photo-1517673400267-0251440c45dc?w=600",
         ["Oatmeal with nuts", "1 Boiled egg", "1 Banana", "Green tea"], "400 kcal"),
        ("🍎 Mid-Morning Snack", "snack",
         "https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?w=600",
         ["1 Apple", "10 Almonds", "Buttermilk"], "150 kcal"),
        ("🍛 Lunch", "lunch",
         "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=600",
         ["2 Multigrain rotis", "1 cup Dal", "Brown rice", "Salad & curd"], "550 kcal"),
        ("🥗 Evening Snack", "evening",
         "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600",
         ["Sprouts chaat", "Green tea", "1 Fruit"], "150 kcal"),
        ("🌙 Dinner", "dinner",
         "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600",
         ["2 Multigrain rotis", "Mixed vegetable sabzi", "Paneer / Tofu", "Salad"], "500 kcal")
    ]

    cols = st.columns(5, gap="small")

    for col, (title, cls, image, foods, kcal) in zip(cols, meals):
        with col:
            food_html = "".join([f"<div>✓ {food}</div>" for food in foods])
            st.markdown(f"""
            <div class="meal">
                <div class="meal-head {cls}">{title}</div>
                <div class="meal-body">
                    <img class="food-image" src="{image}">
                    <div class="food-list">{food_html}</div>
                    <div class="kcal">{kcal}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="card">
        <h3>💡 Tips for You</h3>
        <p>💧 Drink plenty of water throughout the day.</p>
        <p>🍎 Eat meals at regular intervals.</p>
        <p>🥦 Include vegetables and protein.</p>
        <p>🚫 Limit highly processed foods.</p>
        <p>😴 Get enough sleep and stay active.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
        <h3>📊 Nutrient Balance</h3>
        <p>🟠 Carbohydrates — <b>50%</b></p>
        <p>🟢 Proteins — <b>25%</b></p>
        <p>🔵 Healthy Fats — <b>25%</b></p>
        <hr>
        <p class="small-note">Balanced nutrition can support your daily energy needs.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
        <h3>🛡️ Disclaimer</h3>
        <p class="small-note">
        This diet planner is for general educational purposes only.
        It does not replace professional medical or nutritional advice.
        Consult a qualified dietitian or healthcare professional for
        personalized guidance.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    © 2026 Diet Creator &nbsp; | &nbsp; Privacy Policy &nbsp; | &nbsp;
    Terms of Service &nbsp; | &nbsp; Disclaimer
    <br><br>
    🌿 Eat Healthy • Live Healthy!
</div>
""", unsafe_allow_html=True)
