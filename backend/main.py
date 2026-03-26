from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import random
import os
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

from backend import models
from backend.database import engine, get_db

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="RecipeHero API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seed DB Recipes Function
def seed_db(db: Session):
    if db.query(models.Recipe).count() == 0:
        mock_recipes = [
            {
                "title": "Tomato Basil Pasta", 
                "ingredients": ["Pasta", "Tomato", "Garlic", "Olive Oil", "Salt", "Parmesan", "Black Pepper"], 
                "instructions": "1. Boil pasta in salted water. 2. Sauté garlic in olive oil. 3. Add diced tomatoes and simmer. 4. Toss pasta with sauce and top with parmesan and pepper.",
                "calories": 450,
                "servings": 2,
                "image": "https://images.unsplash.com/photo-1473093226795-af9932fe5856?w=400", 
                "time": "20 mins"
            },
            {
                "title": "Garlic Butter Rice", 
                "ingredients": ["Rice", "Garlic", "Butter", "Salt"], 
                "instructions": "1. Cook rice as per package instructions. 2. Melt butter in a pan and sauté minced garlic. 3. Mix the garlic butter into the warm rice. 4. Season with salt.",
                "calories": 320,
                "servings": 1,
                "image": "https://images.unsplash.com/photo-1512058564366-18510beaabec?w=400", 
                "time": "25 mins"
            },
            {
                "title": "Veggie Stir Fry", 
                "ingredients": ["Carrot", "Bell Pepper", "Onion", "Tofu", "Soy Sauce", "Mushroom", "Zucchini"], 
                "instructions": "1. Chop all vegetables and tofu. 2. Heat oil in a wok. 3. Sauté veggies until tender-crisp. 4. Add tofu and soy sauce, stir well.",
                "calories": 280,
                "servings": 2,
                "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400", 
                "time": "15 mins"
            },
            {
                "title": "Chicken Potato Roast", 
                "ingredients": ["Chicken", "Potato", "Olive Oil", "Garlic", "Salt", "Asparagus"], 
                "instructions": "1. Preheat oven to 200°C. 2. Toss chicken, potatoes, and asparagus with oil and garlic. 3. Season with salt. 4. Roast for 35-40 mins until golden.",
                "calories": 550,
                "servings": 2,
                "image": "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?w=400", 
                "time": "40 mins"
            },
            {
                "title": "Avocado Toast", 
                "ingredients": ["Bread", "Avocado", "Lemon", "Salt", "Black Pepper", "Eggs"], 
                "instructions": "1. Toast the bread. 2. Mash avocado with lemon, salt, and pepper. 3. Spread on toast. 4. Top with a poached or fried egg.",
                "calories": 380,
                "servings": 1,
                "image": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=400", 
                "time": "10 mins"
            },
            {
                "title": "Mushroom Risotto", 
                "ingredients": ["Rice", "Mushroom", "Onion", "Garlic", "Butter", "Parmesan"], 
                "instructions": "1. Sauté onions and mushrooms in butter. 2. Add rice and stir. 3. Slowly add broth until absorbed. 4. Stir in parmesan and enjoy.",
                "calories": 420,
                "servings": 2,
                "image": "https://images.unsplash.com/photo-1476124369491-e7addf5db378?w=400", 
                "time": "45 mins"
            },
            {
                "title": "Honey Glazed Salmon", 
                "ingredients": ["Salmon", "Honey", "Soy Sauce", "Garlic", "Lemon"], 
                "instructions": "1. Mix honey, soy sauce, and garlic. 2. Pour over salmon and marinate for 15 mins. 3. Sear salmon in a pan until cooked through. 4. Serve with lemon slices.",
                "calories": 480,
                "servings": 2,
                "image": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400", 
                "time": "20 mins"
            },
            {
                "title": "Spinach Omelet", 
                "ingredients": ["Eggs", "Spinach", "Butter", "Salt", "Cheese"], 
                "instructions": "1. Sauté spinach in butter. 2. Whisk eggs and pour over spinach. 3. Add cheese and fold when set. 4. Season with salt.",
                "calories": 310,
                "servings": 1,
                "image": "https://images.unsplash.com/photo-1510693061483-1ce5dc967073?w=400", 
                "time": "15 mins"
            },
            {
                "title": "Chicken Alfredo", 
                "ingredients": ["Chicken", "Pasta", "Heavy Cream", "Garlic", "Parmesan", "Butter"], 
                "instructions": "1. Cook pasta and chicken separately. 2. Melt butter with garlic and cream. 3. Stir in parmesan to thicken. 4. Toss with chicken and pasta.",
                "calories": 650,
                "servings": 2,
                "image": "https://images.unsplash.com/photo-1645112411341-6c4fd023714a?w=400", 
                "time": "30 mins"
            },
            {
                "title": "Sweet Potato Fries", 
                "ingredients": ["Sweet Potato", "Olive Oil", "Salt", "Paprika"], 
                "instructions": "1. Cut sweet potatoes into wedges. 2. Toss with oil and spices. 3. Bake at 200°C for 25-30 mins until crispy.",
                "calories": 250,
                "servings": 1,
                "image": "https://images.unsplash.com/photo-1604152002388-7264a27bc25d?w=400", 
                "time": "30 mins"
            },
            {
                "title": "Classic Caesar Salad", 
                "ingredients": ["Lettuce", "Bread", "Parmesan", "Lemon", "Garlic", "Olive Oil"], 
                "instructions": "1. Chop lettuce and make croutons from bread. 2. Whisk lemon, garlic, and oil for dressing. 3. Toss all together with parmesan.",
                "calories": 300,
                "servings": 2,
                "image": "https://images.unsplash.com/photo-1550304943-4f24f54ddde9?w=400", 
                "time": "15 mins"
            },
            {
                "title": "Garlic Shrimp Scampi", 
                "ingredients": ["Shrimp", "Garlic", "Butter", "Lemon", "Pasta", "Salt"], 
                "instructions": "1. Boil pasta. 2. Sauté shrimp in butter and minced garlic. 3. Add lemon juice and toss with cooked pasta.",
                "calories": 420,
                "servings": 2,
                "image": "https://images.unsplash.com/photo-1533777324565-a040eb52facd?w=400", 
                "time": "20 mins"
            },
            {
                "title": "Roasted Vegetable Quinoa", 
                "ingredients": ["Quinoa", "Zucchini", "Bell Pepper", "Onion", "Olive Oil"], 
                "instructions": "1. Roast veggies with oil. 2. Cook quinoa separately. 3. Toss together for a healthy bowl.",
                "calories": 350,
                "servings": 2,
                "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400", 
                "time": "25 mins"
            },
            {
                "title": "Lentil Soup", 
                "ingredients": ["Lentils", "Carrot", "Onion", "Celery", "Tomato"], 
                "instructions": "1. Sauté veggies. 2. Add lentils and chopped tomatoes. 3. Simmer in water/broth until lentils are soft.",
                "calories": 320,
                "servings": 3,
                "image": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400", 
                "time": "40 mins"
            },
            {
                "title": "Caprese Salad", 
                "ingredients": ["Tomato", "Cheese", "Basil", "Olive Oil", "Salt"], 
                "instructions": "1. Slice tomatoes and fresh cheese. 2. Layer with basil leaves. 3. Drizzle with oil and season with salt.",
                "calories": 220,
                "servings": 1,
                "image": "https://images.unsplash.com/photo-1608897013039-887f21d8c804?w=400", 
                "time": "10 mins"
            },
            {
                "title": "Pesto Chicken Pasta", 
                "ingredients": ["Pasta", "Chicken", "Basil", "Garlic", "Parmesan", "Olive Oil"], 
                "instructions": "1. Cook pasta and chicken. 2. Blend basil, garlic, parmesan, and oil for pesto. 3. Toss all together.",
                "calories": 520,
                "servings": 2,
                "image": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=400", 
                "time": "25 mins"
            },
            {
                "title": "Egg Fried Rice", 
                "ingredients": ["Rice", "Eggs", "Onion", "Peas", "Soy Sauce"], 
                "instructions": "1. Scramble eggs. 2. Sauté veggies and add cooked rice. 3. Mix in soy sauce and scramble eggs.",
                "calories": 380,
                "servings": 1,
                "image": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400", 
                "time": "20 mins"
            }
        ]
        for r in mock_recipes:
            db.add(models.Recipe(**r))
        db.commit()

@app.on_event("startup")
def on_startup():
    db = next(get_db())
    seed_db(db)

class OTPRequest(BaseModel):
    phone: str
    otp: str

class VerifyRequest(BaseModel):
    phone: str
    otp: str
    name: Optional[str] = None

class MatchRequest(BaseModel):
    ingredients: List[str]

class FamilyCreate(BaseModel):
    name: str

class MemberCreate(BaseModel):
    name: str
    code: str
    role: str = "member"

class PostCreate(BaseModel):
    author: str
    content: str
    time: str
    code: str

@app.post("/auth/send-otp")
def send_otp(req: OTPRequest, db: Session = Depends(get_db)):
    if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_PHONE_NUMBER:
        if "your_account_sid" not in TWILIO_ACCOUNT_SID.lower():
            try:
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                client.messages.create(
                    body=f"Your RecipeHero secure login OTP is: {req.otp}",
                    from_=TWILIO_PHONE_NUMBER,
                    to=req.phone
                )
                print(f"✅ Real SMS Dispatched via Twilio to {req.phone}!")
                return {"status": "success", "message": "SMS Dispatched via Twilio!"}
            except Exception as e:
                print(f"❌ Twilio Error: {e}")
                return {"status": "error", "message": str(e)}
    
    print(f"⚠️ SIMULATED SEND API (No Twilio Keys). OTP for {req.phone} is: {req.otp}")
    return {"status": "success", "message": f"Simulated OTP dispatch to {req.phone} (No Twilio keys). OTP: {req.otp}"}

@app.post("/auth/verify-otp")
def verify_otp(req: VerifyRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.phone == req.phone).first()
    if not user:
        user = models.User(phone=req.phone, name=req.name)
        db.add(user)
        db.commit()
    elif req.name and not user.name:
        user.name = req.name
        db.commit()
    db.refresh(user)
    
    login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    login_record = models.LoginRecord(
        phone=req.phone, 
        name=req.name or user.name, 
        timestamp=login_time
    )
    db.add(login_record)
    db.commit()

    return {"status": "success", "user_id": user.id, "phone": user.phone, "name": user.name}

@app.post("/recipes/match")
def get_matching_recipes(req: MatchRequest, db: Session = Depends(get_db)):
    all_recipes = db.query(models.Recipe).all()
    matches = []
    
    if not req.ingredients:
        return {"matches": []}
        
    user_ingredients = {ing.strip().lower() for ing in req.ingredients}
        
    for r in all_recipes:
        recipe_ingredients_raw = r.ingredients
        if isinstance(recipe_ingredients_raw, str):
            try:
                import json
                recipe_ingredients = json.loads(recipe_ingredients_raw)
            except:
                recipe_ingredients = []
        else:
            recipe_ingredients = recipe_ingredients_raw or []

        normalized_recipe_ingredients = [ing.strip().lower() for ing in recipe_ingredients]
        matched_items = [ing for ing in normalized_recipe_ingredients if ing in user_ingredients]
        match_count = len(matched_items)
        
        if match_count > 0:
            total_count = len(recipe_ingredients)
            missing_count = total_count - match_count
            completeness = match_count / total_count if total_count > 0 else 0
            
            matches.append({
                "id": r.id,
                "title": r.title,
                "ingredients": recipe_ingredients,
                "instructions": r.instructions,
                "calories": r.calories,
                "servings": r.servings,
                "image": r.image,
                "time": r.time,
                "matchCount": match_count,
                "missingCount": missing_count,
                "completeness": completeness
            })
            
    matches.sort(key=lambda x: (x["matchCount"], x["completeness"], -x["missingCount"]), reverse=True)
    return {"matches": matches}

@app.post("/family/create")
def create_group(req: FamilyCreate, db: Session = Depends(get_db)):
    code = 'FAM-' + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4)) + '-' + str(random.randint(1000, 9999))
    group = models.FamilyGroup(name=req.name, code=code)
    db.add(group)
    db.commit()
    db.refresh(group)
    return {"status": "success", "code": group.code, "group_name": group.name}

@app.get("/family/{code}")
def get_group(code: str, db: Session = Depends(get_db)):
    group = db.query(models.FamilyGroup).filter(models.FamilyGroup.code == code).first()
    if not group:
        raise HTTPException(status_code=404, detail="Family Group not found")
        
    return {
        "groupName": group.name,
        "code": group.code,
        "members": [{"id": m.id, "name": m.name, "role": m.role} for m in group.members],
        "posts": [{"id": p.id, "author": p.author, "content": p.content, "time": p.time_posted} for p in group.posts]
    }

@app.post("/family/member")
def add_member(req: MemberCreate, db: Session = Depends(get_db)):
    group = db.query(models.FamilyGroup).filter(models.FamilyGroup.code == req.code).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    member = models.FamilyMember(name=req.name, role=req.role, group_id=group.id)
    db.add(member)
    db.commit()
    db.refresh(member)
    return {"status": "success", "member_id": member.id}

@app.delete("/family/member/{member_id}")
def remove_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(models.FamilyMember).filter(models.FamilyMember.id == member_id).first()
    if not member:
        return {"status": "not_found"}
    db.delete(member)
    db.commit()
    return {"status": "success"}

@app.post("/family/post")
def add_post(req: PostCreate, db: Session = Depends(get_db)):
    group = db.query(models.FamilyGroup).filter(models.FamilyGroup.code == req.code).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
        
    post = models.Post(author=req.author, content=req.content, time_posted=req.time, group_id=group.id)
    db.add(post)
    db.commit()
    return {"status": "success"}

@app.get("/admin/users")
def get_all_users(secret: str = None, db: Session = Depends(get_db)):
    if not ADMIN_PASSWORD or secret != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Forbidden")
    records = db.query(models.LoginRecord).order_by(models.LoginRecord.id.desc()).all()
    return {"status": "success", "users": [{"id": r.id, "phone": r.phone, "name": r.name, "timestamp": r.timestamp} for r in records]}

# Static file serving
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app.mount("/assets", StaticFiles(directory=root_path), name="assets")

@app.get("/")
@app.get("/login")
@app.get("/pantry")
@app.get("/family")
def serve_index():
    return FileResponse(os.path.join(root_path, "index.html"))

@app.get("/{filename}")
def serve_file(filename: str):
    file_path = os.path.join(root_path, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"detail": "Not Found"}
