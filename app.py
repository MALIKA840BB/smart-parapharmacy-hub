import streamlit as st
import pandas as pd
import random

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Smart Parapharmacy Hub",
    page_icon="🌿",
    layout="wide"
)

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .main-title {
        font-size: 38px;
        color: #2E7D32;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .section-box {
        background-color: #F1F8E9;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2E7D32;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌿 Smart Parapharmacy & AI Skin Advisor Hub</div>', unsafe_allow_html=True)
st.write("---")

# --- SIDEBAR / NAVIGATION ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4320/4320351.png", width=100)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller vers :", ["🤖 AI Skin Advisor", "📦 Gestion du Stock", "📊 Tableau de Bord (KPIs)"])

# --- DATA SIMULÉE POUR LE STOCK ---
if 'products' not in st.session_state:
    st.session_state.products = [
        {"ID": "PR001", "Nom": "Crème Hydratante CeraVe", "Catégorie": "Visage", "Stock": 45, "Prix (DH)": 160},
        {"ID": "PR002", "Nom": "Sérum Vitamine C La Roche-Posay", "Catégorie": "Anti-âge", "Stock": 12, "Prix (DH)": 320},
        {"ID": "PR003", "Nom": "Écran Solaire Isdin Fusion Water", "Catégorie": "Solaire", "Stock": 8, "Prix (DH)": 210},
        {"ID": "PR004", "Nom": "Gel Nettoyant Bioderma Sebium", "Catégorie": "Nettoyant", "Stock": 60, "Prix (DH)": 140},
    ]

# ==========================================
# 1. PAGE : AI SKIN ADVISOR
# ==========================================
if page == "🤖 AI Skin Advisor":
    st.markdown('<div class="section-box"><h3>✨ Conseiller Capillaire & Cutané Intélligent (AI)</h3>'
                'Sélectionnez votre type de peau et vos préoccupations pour obtenir une routine personnalisée.</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        type_peau = st.selectbox("Quel est votre type de peau ?", ["Sèche", "Grasse", "Mixte", "Sensible", "Normale"])
        preoccupation = st.multiselect("Quelles sont vos préoccupations ?", ["Acné / Boutons", "Taches / Hyperpigmentation", "Rides / Relâchement", "Déshydratation", "Rougeurs"])
    
    with col2:
        budget = st.slider("Votre budget max pour un produit (DH) :", 50, 500, 250)
    
    if st.button("✨ Générer ma Routine Recommandée", type="primary"):
        st.write("### 📜 Votre Diagnostic & Recommandation AI :")
        
        # Logique de recommandation basique (Simulation AI)
        recommandations = []
        if "Acné / Boutons" in preoccupation or type_peau == "Grasse":
            recommandations.append("🧪 **Actif recommandé :** Acide Salicylique ou Niacinamide.")
            recommandations.append("🛍️ **Produit du Stock :** Gel Nettoyant Bioderma Sebium (140 DH)")
        if "Taches / Hyperpigmentation" in preoccupation:
            recommandations.append("🧪 **Actif recommandé :** Vitamine C ou Acide Azélaïque.")
            recommandations.append("🛍️ **Produit du Stock :** Sérum Vitamine C La Roche-Posay (320 DH)")
        if type_peau == "Sèche" or "Déshydratation" in preoccupation:
            recommandations.append("🧪 **Actif recommandé :** Acide Hyaluronique ou Céramides.")
            recommandations.append("🛍️ **Produit du Stock :** Crème Hydratante CeraVe (160 DH)")
            
        if not recommandations:
            recommandations.append("🧪 **Routine de Base :** Nettoyant doux + Crème hydratante + Protection Solaire SPF50.")
            recommandations.append("🛍️ **Produit du Stock :** Écran Solaire Isdin Fusion Water (210 DH)")
            
        for rec in recommandations:
            st.info(rec)
            
        st.success("💡 *Conseil AI : N'oubliez pas d'appliquer votre écran solaire toutes les 2 heures au Maroc !* 🇲🇦")

# ==========================================
# 2. PAGE : GESTION DU STOCK
# ==========================================
elif page == "📦 Gestion du Stock":
    st.markdown('<div class="section-box"><h3>📦 Inventaire & Suivi des Produits</h3>'
                'Visualisez, modifiez et ajoutez des articles à votre stock en temps réel.</div>', unsafe_allow_html=True)
    
    df = pd.DataFrame(st.session_state.products)
    
    # Alertes de rupture de stock
    low_stock = df[df['Stock'] <= 10]
    if not low_stock.empty:
        for idx, row in low_stock.iterrows():
            st.error(f"⚠️ **Alerte Stock Bas :** Le produit **{row['Nom']}** n'a plus que **{row['Stock']}** unités en réserve !")

    st.write("### 📋 Liste des Produits en Stock")
    st.dataframe(df, use_container_width=True)
    
    # Formulaire d'ajout
    with st.expander("➕ Ajouter un nouveau produit au catalogue"):
        with st.form("add_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                new_nom = st.text_input("Nom du produit :")
                new_cat = st.selectbox("Catégorie :", ["Visage", "Corps", "Solaire", "Nettoyant", "Anti-âge", "Cheveux"])
            with col2:
                new_stock = st.number_input("Quantité initiale :", min_value=0, value=10)
            with col3:
                new_prix = st.number_input("Prix de vente (DH) :", min_value=0, value=100)
                
            if st.form_submit_button("Enregistrer le produit"):
                if new_nom:
                    new_id = f"PR{random.randint(100, 999)}"
                    st.session_state.products.append({
                        "ID": new_id, "Nom": new_nom, "Catégorie": new_cat, "Stock": new_stock, "Prix (DH)": new_prix
                    })
                    st.success(f"✔️ Le produit **{new_nom}** a été ajouté avec l'ID {new_id} !")
                    st.rerun()
                else:
                    st.warning("Veuillez entrer un nom de produit valide.")

# ==========================================
# 3. PAGE : TABLEAU DE BORD (KPIS)
# ==========================================
elif page == "📊 Tableau de Bord (KPIs)":
    st.markdown('<div class="section-box"><h3>📊 Indicateurs de Performance (KPIs)</h3>'
                'Suivi financier et statistiques globales de la parapharmacie.</div>', unsafe_allow_html=True)
    
    df = pd.DataFrame(st.session_state.products)
    
    # Calculs des métriques
    total_produits = len(df)
    total_articles_stock = df['Stock'].sum()
    valeur_total_stock = (df['Stock'] * df['Prix (DH)']).sum()
    prix_moyen = df['Prix (DH)'].mean()
    
    # Affichage des KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Réf. uniques", total_produits)
    col2.metric("🔢 Total Articles", total_articles_stock)
    col3.metric("💰 Valeur du Stock", f"{valeur_total_stock:,} DH")
    col4.metric("📈 Prix Moyen", f"{prix_moyen:.2f} DH")
    
    st.write("---")
    
    # Graphiques d'analyse
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.write("📊 **Répartition du Stock par Catégorie**")
        cat_stock = df.groupby('Catégorie')['Stock'].sum()
        st.bar_chart(cat_stock)
        
    with col_chart2:
        st.write("💰 **Valeur financière du Stock par Produit**")
        df['Valeurs'] = df['Stock'] * df['Prix (DH)']
        st.bar_chart(data=df, x='Nom', y='Valeurs', color="#2E7D32")
