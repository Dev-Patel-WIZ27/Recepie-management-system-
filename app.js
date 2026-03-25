const API_URL = "https://recepie-backend-1jjc.onrender.com";

// Global State
const state = {
    user: null, 
    route: 'home', 
    ingredients: [],
    matchedRecipes: [],
    generatedOTP: null,
    userFamily: null,
    familyData: null,
    adminUsers: []
};

// Expanded Data (Ingredients remain static for UI picking)
const mockIngredients = {
    Vegetables: ['Tomato', 'Onion', 'Garlic', 'Potato', 'Carrot', 'Spinach', 'Bell Pepper', 'Broccoli', 'Mushroom', 'Zucchini', 'Corn', 'Cauliflower', 'Eggplant', 'Green Beans', 'Cabbage', 'Sweet Potato', 'Asparagus', 'Peas', 'Kale', 'Celery'],
    Pantry: ['Rice', 'Pasta', 'Flour', 'Sugar', 'Olive Oil', 'Salt', 'Black Pepper', 'Soy Sauce', 'Vinegar', 'Honey', 'Beans', 'Cumin', 'Paprika', 'Oats', 'Peanut Butter', 'Bread', 'Chicken Broth', 'Canned Tomatoes', 'Quinoa', 'Lentils'],
    Proteins: ['Chicken', 'Beef', 'Eggs', 'Tofu', 'Pork', 'Shrimp', 'Salmon', 'Bacon', 'Turkey', 'Tuna', 'Sausage', 'Lamb', 'Crab', 'Tempeh'],
    Dairy: ['Milk', 'Cheese', 'Butter', 'Yogurt', 'Heavy Cream', 'Parmesan', 'Cream Cheese', 'Sour Cream', 'Cheddar', 'Mozzarella', 'Ghee'],
    Fruits: ['Apple', 'Banana', 'Avocado', 'Lemon', 'Lime', 'Mango', 'Strawberries', 'Oranges', 'Blueberries', 'Grapes', 'Watermelon', 'Pineapple', 'Peach', 'Raspberries', 'Pear']
};

// Application Router
function render() {
    const root = document.getElementById('app');
    if (!document.getElementById('layout')) {
        root.innerHTML = `
            <div id="layout" class="container">
                <nav class="navbar glass">
                    <a href="#" class="logo" onclick="navigate('home')">
                        <i class="ph-fill ph-cooking-pot"></i> RecipeHero
                    </a>
                    <div class="nav-links">
                        <a class="nav-link active" id="nav-home" onclick="navigate('home')">Home</a>
                        <a class="nav-link" id="nav-pantry" onclick="navigate('pantry')">Pantry</a>
                        <a class="nav-link" id="nav-family" onclick="navigate('family')">Family</a>
                        <a class="nav-link" id="nav-admin" onclick="navigate('admin')" style="color:#d63031;"><i class="ph-bold ph-lock-key"></i> Admin</a>
                        <button class="btn btn-primary" id="nav-login" onclick="navigate('login')" style="padding: 8px 16px; font-size: 0.9rem;">Login</button>
                    </div>
                </nav>
                <main id="page-content"></main>
            </div>
        `;
    }

    updateNavState();
    const content = document.getElementById('page-content');
    
    switch(state.route) {
        case 'home': content.innerHTML = renderHome(); break;
        case 'login': content.innerHTML = renderLogin(); break;
        case 'pantry': content.innerHTML = renderPantry(); break;
        case 'family': content.innerHTML = renderFamily(); break;
        case 'admin': content.innerHTML = renderAdmin(); break;
        default: content.innerHTML = renderHome();
    }
}

window.navigate = async function(route) {
    const protectedRoutes = ['pantry', 'family', 'admin'];
    if (protectedRoutes.includes(route) && !state.user) {
        state.route = 'login';
    } else {
        if (route === 'admin') {
            const pass = prompt("Enter Owner Password:");
            if (!pass) return; // User cancelled
            window.adminSecret = pass;
        }
        state.route = route;
    }
    
    if (state.route === 'pantry') await fetchMatches();
    if (state.route === 'family' && state.userFamily) await fetchFamily();
    if (state.route === 'admin') await fetchAdminUsers();
    
    render();
};

function updateNavState() {
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    const activeLink = document.getElementById(`nav-${state.route}`);
    if (activeLink) activeLink.classList.add('active');
    
    const loginBtn = document.getElementById('nav-login');
    if (loginBtn) {
        if (state.user) {
            loginBtn.textContent = 'Logout';
            loginBtn.onclick = () => { state.user = null; state.userFamily = null; navigate('home'); };
            loginBtn.classList.replace('btn-primary', 'btn-secondary');
        } else {
            loginBtn.textContent = 'Login';
            loginBtn.onclick = () => navigate('login');
            loginBtn.classList.replace('btn-secondary', 'btn-primary');
        }
    }
}

// --- BACKEND API CALLS ---
async function fetchMatches() {
    try {
        const res = await fetch(`${API_URL}/recipes/match`, {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ ingredients: state.ingredients })
        });
        const data = await res.json();
        state.matchedRecipes = data.matches || [];
    } catch(e) { console.error(e); state.matchedRecipes = []; }
}

async function fetchFamily() {
    try {
        const res = await fetch(`${API_URL}/family/${state.userFamily}`);
        if(res.ok) {
            state.familyData = await res.json();
        } else {
            state.userFamily = null;
            state.familyData = null;
        }
    } catch(e) { console.error(e); }
}

// --- RENDERERS ---
function renderHome() {
    return `
        <div style="text-align: center; max-width: 800px; margin: 40px auto;">
            <div class="glass-3d" style="display: inline-block; padding: 10px 20px; color: var(--primary-color); border-radius: 30px; font-weight: 700; margin-bottom: 24px; font-size: 0.95rem;">
                🚀 The Smarter Way to Cook
            </div>
            <h1 class="hero-title" style="font-size: 4.5rem; margin-bottom: 24px; color: var(--text-dark); line-height: 1.1; font-weight: 800; text-shadow: 2px 2px 4px rgba(255,255,255,0.8);">
                Zero Waste.<br/>
                <span style="color: var(--primary-color);">Maximum Taste.</span>
            </h1>
            <p class="hero-subtitle" style="font-size: 1.3rem; color: var(--text-dark); font-weight: 500; margin-bottom: 40px; padding: 0 40px; text-shadow: 1px 1px 0px rgba(255,255,255,0.8);">
                Tell us what ingredients you have in your kitchen, and we'll instantly find delicious recipes you can make right now.
            </p>
            <div style="display: flex; gap: 20px; justify-content: center;">
                <button class="btn btn-primary glass-3d" style="font-size: 1.1rem; padding: 16px 36px; border-radius: 30px;" onclick="navigate('pantry')">
                    <i class="ph-bold ph-magic-wand"></i> Get Started Free
                </button>
            </div>
            
            <div style="margin-top: 80px;" class="glass-3d">
                <img src="https://images.unsplash.com/photo-1466637574441-749b8f19452f?ixlib=rb-4.0.3&w=1200&q=80" alt="Fresh ingredients" style="width: 100%; height: 400px; object-fit: cover; border-radius: calc(var(--radius-lg) - 2px);">
            </div>
        </div>
    `;
}

function simulateSMS(phone, otp) {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        oscillator.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        oscillator.frequency.setValueAtTime(800, audioCtx.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(1200, audioCtx.currentTime + 0.1);
        gainNode.gain.setValueAtTime(0, audioCtx.currentTime);
        gainNode.gain.linearRampToValueAtTime(0.3, audioCtx.currentTime + 0.05);
        gainNode.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.5);
        oscillator.start();
        oscillator.stop(audioCtx.currentTime + 0.5);
    } catch(e) {}
    
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
        <div style="font-size: 2.2rem; color: #10b981;"><i class="ph-fill ph-chat-circle-text"></i></div>
        <div>
            <div style="font-size: 0.75rem; font-weight: 800; color: #636e72; letter-spacing: 1px;">MESSAGES • NOW</div>
            <div style="font-size: 1rem; font-weight: 600; color: #2d3436; margin-top: 4px;">RecipeHero Secure Code: <span style="font-size: 1.2rem; font-weight: 800; color: var(--primary-color);">${otp}</span></div>
            <div style="font-size: 0.8rem; color: #636e72; margin-top: 2px;">Use this code to verify your number.</div>
        </div>
    `;
    container.appendChild(toast);
    setTimeout(() => { if (toast.parentElement) toast.remove(); }, 6000);
}

function renderLogin() {
    return `
        <div class="glass glass-3d" style="max-width: 450px; margin: 60px auto; padding: 48px; position: relative;">
            <div style="text-align: center; margin-bottom: 32px;">
                <div style="width: 72px; height: 72px; background: linear-gradient(135deg, rgba(255,94,58,0.2), rgba(255,94,58,0.05)); color: var(--primary-color); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2.2rem; margin: 0 auto 16px;">
                    <i class="ph-fill ph-shield-check"></i>
                </div>
                <h2 style="font-size: 2rem; font-weight: 800;">Secure Login</h2>
                <p style="color: var(--text-dark); font-weight: 500; margin-top: 8px;">Enter your mobile number to receive a secure code.</p>
            </div>
            
            <div id="login-step-1">
                <div class="input-group">
                    <label>Your Name <span style="font-size: 0.8rem; opacity: 0.7;">(Optional)</span></label>
                    <input type="text" id="name-input" class="input-field" placeholder="e.g. Gordon Ramsay" autocomplete="off" style="margin-bottom: 24px;" />
                </div>
                <div class="input-group">
                    <label>Mobile Number</label>
                    <input type="tel" id="mobile-input" class="input-field" placeholder="e.g. 9876543210" autocomplete="off" />
                </div>
                <button id="send-otp-btn" class="btn btn-primary glass-3d" style="width: 100%; padding: 16px; font-size: 1.1rem;" onclick="handleSendOTP()">
                    Send Security Code <i class="ph-bold ph-paper-plane-right"></i>
                </button>
            </div>

            <div id="login-step-2" style="display: none;">
                <div class="input-group">
                    <label>Enter 4-digit OTP Code</label>
                    <input type="number" id="otp-input" class="input-field" placeholder="1234" autocomplete="off" />
                    <div id="otp-hint" style="margin-top: 10px; font-size: 1rem; color: var(--primary-color); font-weight: 800; display:none; background: rgba(255,255,255,0.9); padding: 8px; border-radius: 8px; text-align: center;"></div>
                </div>
                <button class="btn btn-primary glass-3d" style="width: 100%; padding: 16px; font-size: 1.1rem;" onclick="handleVerifyOTP()">
                    Verify & Login
                </button>
                <div style="text-align: center; margin-top: 24px;">
                    <a href="#" onclick="showStep1()" style="color: #636e72; text-decoration: none; font-size: 0.9rem; font-weight: 600;">
                        <i class="ph-bold ph-arrow-left"></i> Change mobile number
                    </a>
                </div>
            </div>
        </div>
    `;
}

window.handleSendOTP = async function() {
    const phone = document.getElementById('mobile-input').value.trim();
    if (phone.length > 2) {
        window.tempPhone = phone; 
        window.tempName = document.getElementById('name-input').value.trim();
        const otp = Math.floor(1000 + Math.random() * 9000).toString();
        state.generatedOTP = otp;
        
        const btn = document.getElementById('send-otp-btn');
        btn.innerHTML = '<i class="ph-bold ph-spinner ph-spin"></i> Generating securely...';
        btn.disabled = true;
        
        try {
            await fetch(`${API_URL}/auth/send-otp`, {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ phone: phone, otp: otp })
            });
        } catch(e) { console.warn("Backend unavailable."); }
        
        setTimeout(() => {
            document.getElementById('login-step-1').style.display = 'none';
            document.getElementById('login-step-2').style.display = 'block';
            
            // Removed the old mock toast simulator!
            const hint = document.getElementById('otp-hint');
            if (hint) {
                // If the user has Twilio credentials setup, the phone will get the text!
                // For safety during local dev we also log it.
                console.log(`Fallback OTP log -> ${otp}`);
                hint.innerHTML = `Test Mode! Your secure OTP code is:<br><span style="font-size:1.8rem; color:#ff5e3a; letter-spacing:4px; font-weight:900;">${otp}</span>`;
                hint.style.display = 'block';
                hint.style.background = 'rgba(255, 234, 167, 0.9)';
            }
        }, 1500);
    } else {
        alert("Please enter a valid mobile number.");
    }
}

window.showStep1 = function() {
    state.generatedOTP = null;
    document.getElementById('login-step-1').style.display = 'block';
    document.getElementById('login-step-2').style.display = 'none';
    document.getElementById('otp-input').value = '';
    const btn = document.getElementById('send-otp-btn');
    btn.innerHTML = 'Send Security Code <i class="ph-bold ph-paper-plane-right"></i>';
    btn.disabled = false;
    const hint = document.getElementById('otp-hint');
    if(hint) hint.style.display = 'none';
}

window.handleVerifyOTP = async function() {
    const otpInput = document.getElementById('otp-input').value.trim();
    if (state.generatedOTP && otpInput === state.generatedOTP) {
        try {
            const res = await fetch(`${API_URL}/auth/verify-otp`, {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ phone: window.tempPhone, otp: otpInput, name: window.tempName || null })
            });
            const data = await res.json();
            if(data.status === 'success') {
                state.user = { id: data.user_id, phone: data.phone };
            } else {
                state.user = { phone: window.tempPhone }; // fallback
            }
        } catch(e) {
            state.user = { phone: window.tempPhone }; // fallback local
        }
        state.generatedOTP = null;
        navigate('pantry');
    } else {
        alert("Incorrect OTP. Please check the simulated SMS notification and try again.");
    }
}

function renderPantry() {
    let ingHTML = '';
    for (const [category, items] of Object.entries(mockIngredients)) {
        ingHTML += `<div style="margin-bottom: 24px; text-align: left;">
            <h3 style="color: var(--text-dark); margin-bottom: 12px; font-size: 1.1rem; font-weight: 700;">${category}</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">`;
        items.forEach(item => {
            const isSelected = state.ingredients.includes(item);
            ingHTML += `<button onclick="toggleIngredient('${item}')" class="btn glass-3d ${isSelected ? 'btn-primary' : 'btn-secondary'}" style="padding: 10px 18px; font-size: 0.95rem; border-radius: 20px;">
                ${isSelected ? '<i class="ph-bold ph-check"></i> ' : ''}${item}
            </button>`;
        });
        ingHTML += `</div></div>`;
    }

    let matchedRecipesHTML = '';
    if (state.ingredients.length === 0) {
        matchedRecipesHTML = `<div style="text-align: center; color: var(--text-dark); font-weight: 500; padding: 40px; grid-column: span 2;">Select ingredients from your pantry to see what you can make!</div>`;
    } else if (state.matchedRecipes.length > 0) {
        state.matchedRecipes.forEach(r => {
            matchedRecipesHTML += `
                <div class="glass-3d" style="border-radius: var(--radius-md); overflow: hidden; display: flex; flex-direction: column; text-align: left; padding: 0;">
                    <img src="${r.image}" style="width: 100%; height: 180px; object-fit: cover;" alt="${r.title}">
                    <div style="padding: 20px;">
                        <h4 style="margin-bottom: 8px; font-size: 1.2rem; font-weight: 700;">${r.title}</h4>
                        <p style="font-size: 0.9rem; color: var(--text-dark); opacity: 0.8; margin-bottom: 16px;"><i class="ph-fill ph-clock"></i> ${r.time} • Mapped ${r.matchCount} ingredients</p>
                        <button class="btn btn-primary" style="width: 100%; padding: 12px; font-size: 1rem;">View Full Recipe</button>
                    </div>
                </div>
            `;
        });
    } else {
        matchedRecipesHTML = `<div style="text-align: center; color: var(--text-dark); padding: 40px; grid-column: span 2; font-weight: 500;">No recipes found for these ingredients. Try adding more!</div>`;
    }

    return `
        <div class="responsive-grid" style="gap: 40px; align-items: start;">
            <div class="glass glass-3d" style="padding: 40px;">
                <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 32px;">
                    <div style="font-size: 2.5rem; color: var(--primary-color);"><i class="ph-fill ph-basket"></i></div>
                    <h2 style="margin: 0; font-size: 2rem;">Smart Pantry</h2>
                </div>
                <div style="max-height: 600px; overflow-y: auto; padding-right: 12px;">
                    ${ingHTML}
                </div>
            </div>
            
            <div class="glass glass-3d" style="padding: 40px; background: rgba(255,255,255,0.85);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px;">
                    <h2 style="margin: 0; font-size: 2rem;">Cook Now (From DB)</h2>
                    <div style="font-size: 1.2rem; font-weight: 700; color: var(--primary-color); background: rgba(255,94,58,0.1); padding: 8px 16px; border-radius: 20px;">
                        ${state.ingredients.length} Selected
                    </div>
                </div>
                <div class="responsive-grid" style="gap: 24px; max-height: 600px; overflow-y: auto; padding-right: 12px;">
                    ${matchedRecipesHTML}
                </div>
            </div>
        </div>
    `;
}

window.toggleIngredient = async function(item) {
    if (state.ingredients.includes(item)) {
        state.ingredients = state.ingredients.filter(i => i !== item);
    } else {
        state.ingredients.push(item);
    }
    render(); // Immediate visual feedback
    await fetchMatches(); // Backend processing
    render(); // Final recipes update
}

window.createFamilyGroup = async function() {
    try {
        const res = await fetch(`${API_URL}/family/create`, {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ name: 'The Culinary Connect' })
        });
        const data = await res.json();
        if(data.status === 'success') {
            state.userFamily = data.code;
            
            // Add self as leader
            await fetch(`${API_URL}/family/member`, {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ name: 'You (Creator)', code: data.code, role: 'leader' })
            });

            alert(`Backend DB Success! You created the group. Invite code: ${data.code}. Share to let them join.`);
            await fetchFamily();
            render();
        }
    } catch(e) { alert("Backend error."); }
}

window.joinFamilyGroup = async function() {
    const code = document.getElementById('join-code').value.trim().toUpperCase();
    if (code.length > 5) {
        try {
            const res = await fetch(`${API_URL}/family/${code}`);
            if (res.ok) {
                state.userFamily = code;
                alert("You have successfully connected to the family group via the backend!");
                await fetchFamily();
                render();
            } else {
                alert("Database says: Family Group Code not found!");
            }
        } catch(e) { console.error(e); }
    } else {
        alert("Please enter a valid Family Group Code.");
    }
}

window.removeFamilyMember = async function(id) {
    if (confirm("Are you sure you want to completely remove this member from the database?")) {
        try {
            await fetch(`${API_URL}/family/member/${id}`, { method: 'DELETE' });
            await fetchFamily();
            render();
        } catch(e) {}
    }
}

window.addFamilyMember = async function() {
    const input = document.getElementById('new-member-input');
    const name = input.value.trim();
    if (name && state.userFamily) {
        try {
            await fetch(`${API_URL}/family/member`, {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ name: name, code: state.userFamily, role: 'member' })
            });
            await fetchFamily();
            render();
        } catch(e) {}
    } else {
        alert("Please enter a valid name.");
    }
}

function renderFamily() {
    if (!state.user) return ''; 

    if (!state.userFamily || !state.familyData) {
        return `
            <div class="glass glass-3d" style="max-width: 650px; margin: 40px auto; padding: 60px; text-align: center;">
                <div style="font-size: 4rem; color: var(--primary-color); margin-bottom: 24px;"><i class="ph-fill ph-house-line"></i></div>
                <h2 style="font-size: 2.8rem; margin-bottom: 16px; font-weight: 800;">Family DB Hub</h2>
                <p style="color: var(--text-dark); margin-bottom: 48px; font-size: 1.15rem; font-weight: 500;">Connect securely to the FastAPI Backend.</p>
                
                <div class="responsive-grid" style="gap: 32px; text-align: left;">
                    
                    <div class="glass" style="padding: 32px; border: 2px dashed rgba(255,94,58,0.5); border-radius: var(--radius-lg); transition: border 0.3s;">
                        <h3 style="margin-bottom: 16px; font-size: 1.5rem;">Create Data</h3>
                        <p style="font-size: 0.95rem; color: var(--text-dark); opacity: 0.8; margin-bottom: 32px; min-height: 48px;">Set up a new SQLite family entity.</p>
                        <button class="btn btn-primary glass-3d" style="width: 100%; font-size: 1.1rem; padding: 14px;" onclick="createFamilyGroup()"><i class="ph-bold ph-magic-wand"></i> Initialize Config</button>
                    </div>
                    
                    <div class="glass" style="padding: 32px; border: 2px solid rgba(255,255,255,0.8); border-radius: var(--radius-lg); background: rgba(255,255,255,0.4);">
                        <h3 style="margin-bottom: 16px; font-size: 1.5rem;">Join Config</h3>
                        <p style="font-size: 0.95rem; color: var(--text-dark); opacity: 0.8; margin-bottom: 24px; min-height: 48px;">Connect to an existing DB session via code.</p>
                        <input type="text" id="join-code" class="input-field glass-3d" placeholder="e.g. FAM-XYZ-1234" style="margin-bottom: 16px; text-transform: uppercase;">
                        <button class="btn btn-secondary glass-3d" style="width: 100%; font-size: 1.1rem; padding: 14px; background: white;" onclick="joinFamilyGroup()"><i class="ph-bold ph-sign-in"></i> Attach Group</button>
                    </div>
                    
                </div>
            </div>
        `;
    }

    let membersHTML = state.familyData.members.map(m => {
        const isYou = m.role === 'leader';
        return `
            <div class="${isYou ? 'glass-3d' : 'glass'}" style="padding: 10px 20px; border-radius: 30px; font-size: 1.05rem; font-weight: ${isYou ? '800' : '600'}; box-shadow: var(--shadow-sm); display: flex; align-items: center; gap: 8px; ${isYou ? 'background: linear-gradient(135deg, var(--primary-color), var(--primary-hover)); color: white;' : ''}">
                ${m.name}
                ${!isYou ? `<div onclick="removeFamilyMember('${m.id}')" style="cursor: pointer; opacity: 0.7; margin-left: 6px; display:flex; align-items:center; color: var(--text-dark);" title="Remove DB Member">❌</div>` : ''}
            </div>
        `;
    }).join('');

    let postsHTML = state.familyData.posts.map(p => `
        <div style="padding: 24px; border-bottom: 1px solid rgba(0,0,0,0.05); text-align: left;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 12px; align-items: center;">
                <strong style="color: var(--text-dark); font-size: 1.1rem; display: flex; align-items: center; gap: 12px;">
                    <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%); border-radius: 50%; color: white; display: flex; align-items: center; justify-content: center; font-size: 1rem; font-weight: 800; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                        ${p.author ? p.author.charAt(0) : 'U'}
                    </div>
                    ${p.author}
                </strong>
                <span style="font-size: 0.85rem; color: var(--text-dark); opacity: 0.6; font-weight: 600;">${p.time}</span>
            </div>
            <p style="color: var(--text-dark); font-size: 1.1rem; padding-left: 52px;">${p.content}</p>
        </div>
    `).join('');

    return `
        <div style="max-width: 900px; margin: 0 auto;">
            <div class="glass glass-3d" style="padding: 48px; text-align: center; margin-bottom: 40px; position: relative; overflow: hidden;">
                <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, transparent 60%); z-index: -1;"></div>
                <div style="font-size: 4rem; color: var(--primary-color); margin-bottom: 20px;"><i class="ph-fill ph-users-three"></i></div>
                <h2 style="margin-bottom: 12px; font-size: 2.8rem; font-weight: 800;">${state.familyData.groupName}</h2>
                <div style="font-size: 1rem; font-weight: 800; color: var(--primary-color); background: rgba(255,94,58,0.15); padding: 8px 20px; border-radius: 30px; display: inline-block; margin-bottom: 32px; letter-spacing: 1.5px; box-shadow: inset 2px 2px 4px rgba(255,255,255,0.8);">
                    LIVE DB CODE: ${state.userFamily}
                </div>
                
                <h3 style="margin-bottom: 16px; font-size: 1.2rem; color: var(--text-dark); font-weight: 700;">Dynamically Synced Members</h3>
                <div style="display: flex; justify-content: center; gap: 16px; margin-bottom: 32px; flex-wrap: wrap;">
                    ${membersHTML}
                </div>
                
                <div style="display: flex; gap: 12px; justify-content: center; align-items: center; background: rgba(255,255,255,0.5); padding: 24px; border-radius: var(--radius-md); max-width: 500px; margin: 0 auto; box-shadow: inset 2px 2px 6px rgba(0,0,0,0.05); border: 1px solid rgba(255,255,255,0.8);">
                    <input type="text" id="new-member-input" class="input-field glass-3d" placeholder="Insert into DB table..." style="margin-bottom: 0; flex: 1;">
                    <button class="btn btn-secondary glass-3d" style="padding: 14px 24px; font-size: 1.1rem; background: white;" onclick="addFamilyMember()"><i class="ph-bold ph-plus"></i> DB Add</button>
                </div>
            </div>

            <div class="glass glass-3d" style="overflow: hidden; padding: 0;">
                <div style="padding: 32px; border-bottom: 2px solid rgba(255,255,255,0.5); background: rgba(255,255,255,0.6);">
                    <h3 style="margin-bottom: 20px; text-align: left; font-size: 1.5rem;">Family Discussions / Logs</h3>
                    <div style="display: flex; gap: 16px;">
                        <input type="text" id="comment-input" class="input-field glass-3d" placeholder="Push a row into Posts table..." style="margin-bottom: 0; font-size: 1.1rem; padding: 16px;" />
                        <button class="btn btn-primary glass-3d" onclick="handleAddComment()" style="padding: 0 32px; font-size: 1.1rem;">Push Log</button>
                    </div>
                </div>
                <div id="posts-container" style="background: rgba(255,255,255,0.4);">
                    ${postsHTML}
                </div>
            </div>
        </div>
    `;
}

window.handleAddComment = async function() {
    const input = document.getElementById('comment-input');
    const content = input.value.trim();
    if (content && state.userFamily) {
        try {
            const author = state.familyData.members.find(m => m.role === 'leader')?.name || "User";
            await fetch(`${API_URL}/family/post`, {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ author, content, time: "Just now", code: state.userFamily })
            });
            await fetchFamily();
            render();
        } catch(e) {}
    }
}

async function fetchAdminUsers() {
    try {
        const res = await fetch(`${API_URL}/admin/users?secret=${window.adminSecret || ''}`);
        if (res.ok) {
            const data = await res.json();
            state.adminUsers = data.users || [];
        } else {
            alert("Incorrect Password or Access Denied!");
            window.adminSecret = null;
            state.route = 'home';
            render();
        }
    } catch(e) { console.error(e); }
}

function renderAdmin() {
    if (!state.user) return ''; 
    let tableRows = (state.adminUsers || []).map(u => `
        <tr>
            <td style="padding: 12px; border-bottom: 1px solid rgba(0,0,0,0.1); font-family: monospace;">${u.id}</td>
            <td style="padding: 12px; border-bottom: 1px solid rgba(0,0,0,0.1); font-weight: 800; color: var(--primary-color);">${u.phone}</td>
            <td style="padding: 12px; border-bottom: 1px solid rgba(0,0,0,0.1);">${u.name || '<span style="opacity:0.5; font-style:italic;">Not provided</span>'}</td>
        </tr>
    `).join('');

    return `
        <div class="glass glass-3d" style="max-width: 800px; margin: 40px auto; padding: 40px; text-align: left;">
            <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 32px;">
                <div style="font-size: 2.5rem; color: #d63031;"><i class="ph-fill ph-lock-key"></i></div>
                <h2 style="margin: 0; font-size: 2.2rem;">Owner Dashboard</h2>
            </div>
            <p style="color: var(--text-dark); margin-bottom: 32px; font-size: 1.1rem; font-weight: 500;">Welcome back! Here is a live feed of everyone who has securely registered and saved their phone number to your database.</p>
            
            <div style="background: rgba(255,255,255,0.6); padding: 8px; border-radius: var(--radius-lg); box-shadow: inset 0 2px 10px rgba(0,0,0,0.05);">
                <table style="width: 100%; text-align: left; border-collapse: collapse;">
                    <thead>
                        <tr style="background: rgba(0,0,0,0.05);">
                            <th style="padding: 16px; border-top-left-radius: 8px;">User ID</th>
                            <th style="padding: 16px;">Phone Number</th>
                            <th style="padding: 16px; border-top-right-radius: 8px;">Name (Optional)</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${tableRows.length > 0 ? tableRows : '<tr><td colspan="3" style="text-align:center; padding: 32px; font-weight: 600;">No users have registered yet.</td></tr>'}
                    </tbody>
                </table>
            </div>
        </div>
    `;
}

document.addEventListener('DOMContentLoaded', () => { render(); });
