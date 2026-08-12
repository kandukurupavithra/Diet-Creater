import base64
import requests
import streamlit as st

st.set_page_config(page_title="Diet Creator", page_icon="🥗", layout="wide")

# ---------- STATE ----------
for key, default in {
    "logged_in": False,
    "signup": False,
    "diet_created": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ---------- HELPERS ----------
def secret(name):
    try:
        return st.secrets.get(name, "")
    except Exception:
        return ""

def calculate(age, gender, height, weight, activity, goal):
    bmi = weight / ((height / 100) ** 2)
    bmr = (10 * weight + 6.25 * height - 5 * age +
           (5 if gender == "Male" else -161))
    factor = {"Sedentary": 1.20, "Lightly Active": 1.375,
              "Moderately Active": 1.55, "Very Active": 1.725}[activity]
    calories = bmr * factor
    if goal == "Weight Loss":
        calories -= 400
    elif goal == "Weight Gain":
        calories += 350
    calories = max(1200, round(calories))
    protein = round(weight * (1.2 if goal == "Weight Loss" else
                              1.4 if goal == "Weight Gain" else 1.3))
    water = round(weight * 0.035, 1)
    return bmi, calories, protein, water

def detect_food(image):
    key = secret("OPENAI_API_KEY")
    if not key:
        return None
    try:
        from openai import OpenAI
        encoded = base64.b64encode(image.getvalue()).decode()
        client = OpenAI(api_key=key)
        result = client.responses.create(
            model="gpt-4.1-mini",
            input=[{"role": "user", "content": [
                {"type": "input_text",
                 "text": "Identify the main food in this image. Return only its common name. If unclear, return unknown."},
                {"type": "input_image",
                 "image_url": f"data:image/jpeg;base64,{encoded}"}
            ]}]
        )
        text = result.output_text.strip()
        return None if text.lower() == "unknown" else text
    except Exception:
        return None

def nutrition(food):
    key = secret("USDA_API_KEY")
    if not key:
        return None
    try:
        r = requests.post(
            "https://api.nal.usda.gov/fdc/v1/foods/search",
            params={"api_key": key},
            json={"query": food, "pageSize": 1},
            timeout=20)
        r.raise_for_status()
        foods = r.json().get("foods", [])
        if not foods:
            return None
        f = foods[0]
        ns = {x.get("nutrientName","").lower(): x.get("value",0) or 0
              for x in f.get("foodNutrients", [])}

        def val(term):
            for n, v in ns.items():
                if term in n:
                    return v
            return 0

        return {
            "name": f.get("description", food),
            "calories": val("energy"),
            "protein": val("protein"),
            "carbs": val("carbohydrate"),
            "fat": val("total lipid"),
            "fiber": val("fiber"),
            "a": val("vitamin a"), "c": val("vitamin c"),
            "d": val("vitamin d"), "e": val("vitamin e"),
            "k": val("vitamin k"), "calcium": val("calcium"),
            "iron": val("iron"), "potassium": val("potassium")
        }
    except Exception:
        return None

# ---------- STYLE ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
*{font-family:Poppins,sans-serif}
.stApp{background:linear-gradient(180deg,#f4fbf3,#fff)}
.block-container{max-width:1450px;padding:0 2.5rem 2rem}
.nav{background:white;border-radius:0 0 20px 20px;padding:18px 28px;
display:flex;justify-content:space-between;box-shadow:0 5px 25px #175b2212;margin-bottom:25px}
.logo{font-size:28px;font-weight:800;color:#16833d}.logo span{color:#f57c00}
.hero{padding:50px;border-radius:28px;background:linear-gradient(115deg,#e5f8e7,#fff,#fff0c9);margin-bottom:28px}
.hero h1{font-size:50px;line-height:1.1;margin:0}.hero h1 span{color:#16833d}
.hero p{max-width:650px;color:#596572;font-size:17px;line-height:1.7}
.card{background:white;border:1px solid #e3eee2;border-radius:20px;padding:22px;
box-shadow:0 7px 25px #175b220c}
.card h3{color:#16833d;margin-top:0}
.metric{padding:18px;border-radius:17px;min-height:105px}
.green{background:#e8f8ed}.blue{background:#e8f4ff}.orange{background:#fff4df}.pink{background:#ffeaf2}
.metric-value{font-size:21px;font-weight:800}.metric-title{color:#64748b;font-size:13px}
.meal{background:white;border:1px solid #e7e7e7;border-radius:17px;overflow:hidden;box-shadow:0 5px 18px #0000000c}
.meal-title{color:white;text-align:center;padding:12px 5px;font-weight:700}
.bf{background:#f59e0b}.sn{background:#16a34a}.ln{background:#2196f3}.ev{background:#9333ea}.di{background:#ec407a}
.meal-body{padding:14px}.food-img{width:100%;height:115px;object-fit:cover;border-radius:12px}
.foods{color:#475569;font-size:12px;line-height:1.9;margin-top:8px}
.kcal{background:#f0f8ef;color:#16833d;text-align:center;font-weight:800;padding:9px;border-radius:10px;margin-top:10px}
.login-card{max-width:500px;margin:8vh auto;background:white;border-radius:28px;padding:40px;
box-shadow:0 15px 50px #175b221f;border:1px solid #e3eee2}
.login-logo{text-align:center;font-size:35px;font-weight:800;color:#16833d}.login-logo span{color:#f57c00}
.footer{background:#087b36;color:white;border-radius:18px;text-align:center;padding:25px;margin-top:35px}
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN ----------
if not st.session_state.logged_in:
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-logo">🌿 Diet <span>Creator</span></div>', unsafe_allow_html=True)
    if not st.session_state.signup:
        st.markdown("<h2 style='text-align:center'>Welcome Back! 👋</h2>", unsafe_allow_html=True)
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password")
        if st.button("🔐 Login", use_container_width=True):
            if email.strip() and password.strip():
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Enter email and password.")
        if st.button("Create a new account", use_container_width=True):
            st.session_state.signup = True
            st.rerun()
    else:
        st.markdown("<h2 style='text-align:center'>Create Account ✨</h2>", unsafe_allow_html=True)
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        password = st.text_input("Create Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        if st.button("🚀 Sign Up", use_container_width=True):
            if not all([name.strip(), email.strip(), password.strip()]):
                st.error("Fill all fields.")
            elif password != confirm:
                st.error("Passwords do not match.")
            else:
                st.session_state.logged_in = True
                st.rerun()
        if st.button("Already have an account? Login", use_container_width=True):
            st.session_state.signup = False
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ---------- HEADER ----------
st.markdown("""
<div class="nav">
<div class="logo">🌿 Diet <span>Creator</span></div>
<div style="font-weight:600;color:#16833d">Home &nbsp; • &nbsp; Diet Plans &nbsp; • &nbsp; Nutrition</div>
<div style="font-weight:700;color:#16833d">✓ Logged In</div>
</div>
<div class="hero">
<h1>Create Your<br>Perfect <span>Diet Plan</span></h1>
<p>Personalized meals based on your body information and goal, plus camera food scanning for estimated protein, vitamins, minerals and calories.</p>
</div>
""", unsafe_allow_html=True)

# ---------- DIET CREATOR ----------
st.markdown("## 👤 Create Your Personalized Plan")
left, right = st.columns([1, 2.8], gap="large")

with left:
    st.markdown('<div class="card"><h3>👤 Your Information</h3>', unsafe_allow_html=True)
    name = st.text_input("Name", placeholder="Enter your name")
    age = st.number_input("Age", 10, 100, 22)
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    height = st.number_input("Height (cm)", 100, 220, 170)
    weight = st.number_input("Weight (kg)", 20, 200, 65)
    activity = st.selectbox("Activity Level",
        ["Sedentary","Lightly Active","Moderately Active","Very Active"])
    goal = st.selectbox("Goal", ["Weight Loss","Weight Maintenance","Weight Gain"])
    if st.button("✨ Create My Diet Plan", use_container_width=True):
        st.session_state.diet_created = True
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    bmi, calories, protein_target, water = calculate(age, gender, height, weight, activity, goal)
    cols = st.columns(4)
    metrics = [
        ("🔥","Daily Calories",f"{calories} kcal","green"),
        ("💧","Water Intake",f"{water} L","blue"),
        ("💪","Protein Target",f"{protein_target} g","orange"),
        ("⚖️","BMI",f"{bmi:.1f}","pink")]
    for c, (icon,title,val,cls) in zip(cols, metrics):
        with c:
            st.markdown(f'<div class="metric {cls}"><div>{icon}</div><div class="metric-title">{title}</div><div class="metric-value">{val}</div></div>', unsafe_allow_html=True)

    if st.session_state.diet_created:
        st.success(f"🎉 Your personalized plan is ready{', '+name if name else ''}!")
        if goal == "Weight Loss":
            meals=[
            ("🌅 Breakfast","bf","https://images.unsplash.com/photo-1517673400267-0251440c45dc?w=600",["Oats with milk","1 boiled egg","1 banana","Green tea"],"350 kcal"),
            ("🍎 Snack","sn","https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?w=600",["1 apple","8 almonds","Buttermilk"],"180 kcal"),
            ("🍛 Lunch","ln","https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=600",["2 multigrain rotis","Dal","Mixed vegetables","Curd + salad"],"500 kcal"),
            ("🥗 Evening","ev","https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600",["Sprouts chaat","Green tea","1 fruit"],"180 kcal"),
            ("🌙 Dinner","di","https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600",["2 rotis","Paneer / tofu","Vegetable sabzi","Salad"],"450 kcal")]
        elif goal == "Weight Gain":
            meals=[
            ("🌅 Breakfast","bf","https://images.unsplash.com/photo-1517673400267-0251440c45dc?w=600",["Oats with milk","2 eggs","Banana","Peanut butter"],"550 kcal"),
            ("🍎 Snack","sn","https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?w=600",["Banana shake","10 almonds","Dates"],"350 kcal"),
            ("🍛 Lunch","ln","https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=600",["3 rotis","Rice","Dal","Paneer","Curd"],"700 kcal"),
            ("🥗 Evening","ev","https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600",["Peanut chaat","Fruit","Milk"],"350 kcal"),
            ("🌙 Dinner","di","https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600",["3 rotis","Paneer / tofu","Vegetable sabzi","Curd"],"650 kcal")]
        else:
            meals=[
            ("🌅 Breakfast","bf","https://images.unsplash.com/photo-1517673400267-0251440c45dc?w=600",["Oats with milk","2 eggs","Banana","Green tea"],"450 kcal"),
            ("🍎 Snack","sn","https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?w=600",["Apple","10 almonds","Buttermilk"],"200 kcal"),
            ("🍛 Lunch","ln","https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=600",["2 rotis","Rice","Dal","Vegetables","Curd"],"600 kcal"),
            ("🥗 Evening","ev","https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600",["Sprouts chaat","Fruit","Green tea"],"200 kcal"),
            ("🌙 Dinner","di","https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600",["2 rotis","Paneer / tofu","Vegetable sabzi","Salad"],"550 kcal")]
        st.markdown("### 🥗 Your Personalized Daily Diet Plan")
        mealcols=st.columns(5)
        for col,(title,cls,img,foods,kcal) in zip(mealcols,meals):
            with col:
                items="".join(f"<div>✓ {x}</div>" for x in foods)
                st.markdown(f'<div class="meal"><div class="meal-title {cls}">{title}</div><div class="meal-body"><img class="food-img" src="{img}"><div class="foods">{items}</div><div class="kcal">{kcal}</div></div></div>',unsafe_allow_html=True)
    else:
        st.info("👈 Enter your details and click Create My Diet Plan.")

# ---------- FOOD SCANNER ----------
st.markdown("## 📸 Food Scanner & Nutrition")
a,b=st.columns([1,1.6],gap="large")
with a:
    st.markdown('<div class="card"><h3>📷 Scan Your Food</h3><p>Take a photo or upload food. AI can identify it and USDA can return estimated nutrients.</p></div>',unsafe_allow_html=True)
    camera=st.camera_input("Take a picture of your food")
    upload=st.file_uploader("Or upload a photo",type=["jpg","jpeg","png"])
    image=camera if camera else upload

with b:
    if image:
        st.image(image,caption="Food photo",width="stretch")
        detected=detect_food(image)
        if detected:
            st.success(f"🤖 Detected: {detected}")
            food=st.text_input("Food name",value=detected)
        else:
            st.info("If automatic recognition is unavailable, enter the food name below.")
            food=st.text_input("Food name",placeholder="Example: banana, rice, dal, paneer")
        if food:
            n=nutrition(food)
            if n:
                st.markdown(f"### 🧪 Nutrition: {n['name']}")
                r1=st.columns(4)
                for c,t,v in zip(r1,["🔥 Calories","💪 Protein","🍚 Carbs","🥑 Fat"],
                                  [f"{n['calories']:.0f} kcal",f"{n['protein']:.1f} g",f"{n['carbs']:.1f} g",f"{n['fat']:.1f} g"]):
                    c.metric(t,v)
                r2=st.columns(4)
                for c,t,v in zip(r2,["🟠 Vitamin A","🍊 Vitamin C","☀️ Vitamin D","🟢 Vitamin E"],
                                  [f"{n['a']:.1f} µg",f"{n['c']:.1f} mg",f"{n['d']:.1f} µg",f"{n['e']:.1f} mg"]):
                    c.metric(t,v)
                r3=st.columns(4)
                for c,t,v in zip(r3,["🟣 Vitamin K","🦴 Calcium","🩸 Iron","⚡ Potassium"],
                                  [f"{n['k']:.1f} µg",f"{n['calcium']:.1f} mg",f"{n['iron']:.1f} mg",f"{n['potassium']:.1f} mg"]):
                    c.metric(t,v)
                st.caption("Nutrition values are database estimates and vary with portion, recipe and preparation.")
            else:
                st.warning("Nutrition lookup failed. Check USDA_API_KEY in Streamlit Secrets.")
    else:
        st.markdown(
    "<div class='card'>"
    "<h3>🥦 Nutrition You'll See</h3>"
    "<p>🔥 Calories</p>"
    "<p>💪 Protein</p>"
    "<p>🍊 Vitamins A, C, D, E & K</p>"
    "<p>🦴 Calcium • 🩸 Iron • ⚡ Potassium</p>"
    "</div>",
    unsafe_allow_html=True
)

# ---------- FOOTER ----------
if st.button("🚪 Logout"):
    st.session_state.logged_in=False
    st.session_state.diet_created=False
    st.rerun()

st.markdown('<div class="footer">🌿 <b>Diet Creator</b><br>Eat Healthy • Live Healthy!<br><br>For general educational use; not a substitute for professional medical or nutrition advice.</div>',unsafe_allow_html=True)
