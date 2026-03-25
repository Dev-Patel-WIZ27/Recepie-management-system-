from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import random
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

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
            {"title": "Tomato Basil Pasta", "ingredients": ["Pasta", "Tomato", "Garlic", "Olive Oil", "Salt", "Parmesan", "Black Pepper"], "image": "https://images.unsplash.com/photo-1621996316526-78b17b6a4a15?w=400", "time": "20 mins"},
            {"title": "Garlic Butter Rice", "ingredients": ["Rice", "Garlic", "Butter", "Salt"], "image": "https://images.unsplash.com/photo-1512058564366-18510beaabec?w=400", "time": "25 mins"},
            {"title": "Veggie Stir Fry", "ingredients": ["Carrot", "Bell Pepper", "Onion", "Tofu", "Soy Sauce", "Mushroom", "Zucchini"], "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400", "time": "15 mins"},
            {"title": "Chicken Potato Roast", "ingredients": ["Chicken", "Potato", "Olive Oil", "Garlic", "Salt", "Asparagus"], "image": "https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?w=400", "time": "40 mins"},
            {"title": "Avocado Toast", "ingredients": ["Bread", "Avocado", "Lemon", "Salt", "Black Pepper", "Eggs"], "image": "https://images.unsplash.com/photo-1588137378633-981eeff4711d?w=400", "time": "10 mins"},
            {"title": "Mushroom Risotto", "ingredients": ["Rice", "Mushroom", "Onion", "Garlic", "Butter", "Parmesan"], "image": "https://images.unsplash.com/photo-1476124369491-e7addf5db378?w=400", "time": "45 mins"},
            {"title": "Honey Glazed Salmon", "ingredients": ["Salmon", "Honey", "Soy Sauce", "Garlic", "Lime"], "image": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400", "time": "20 mins"},
            {"title": "Spinach Omelet", "ingredients": ["Eggs", "Spinach", "Butter", "Salt", "Cheese"], "image": "https://images.unsplash.com/photo-1510693061483-1ce5dc967073?w=400", "time": "15 mins"},
            {"title": "Chicken Alfredo", "ingredients": ["Chicken", "Pasta", "Heavy Cream", "Garlic", "Parmesan", "Butter"], "image": "https://images.unsplash.com/photo-1645112411341-6c4fd023714a?w=400", "time": "30 mins"},
            {"title": "Sweet Potato Fries", "ingredients": ["Sweet Potato", "Olive Oil", "Salt", "Paprika"], "image": "https://images.unsplash.com/photo-1604152002388-7264a27bc25d?w=400", "time": "30 mins"}
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
        # Check against placeholder values
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
    
    # Fallback to console output if missing credentials
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
    return {"status": "success", "user_id": user.id, "phone": user.phone, "name": user.name}

@app.post("/recipes/match")
def get_matching_recipes(req: MatchRequest, db: Session = Depends(get_db)):
    all_recipes = db.query(models.Recipe).all()
    matches = []
    
    if not req.ingredients:
        return {"matches": []}
        
    for r in all_recipes:
        match_count = len([ing for ing in r.ingredients if ing in req.ingredients])
        if match_count > 0:
            matches.append({
                "id": r.id,
                "title": r.title,
                "ingredients": r.ingredients,
                "image": r.image,
                "time": r.time,
                "matchCount": match_count
            })
            
    matches.sort(key=lambda x: x["matchCount"], reverse=True)
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
        "posts": [{"id": p.id, "author": p.author, "content": p.content, "time": m.time_posted} for p in group.posts]
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
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return {"status": "success", "users": [{"id": u.id, "phone": u.phone, "name": u.name} for u in users]}

