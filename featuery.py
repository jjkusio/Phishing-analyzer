import xgboost as xgb
import matplotlib.pyplot as plt
import pandas as pd

def plot_importance(model_path, title, color):
    # Wczytujemy model
    model = xgb.XGBClassifier()
    model.load_model(model_path)
    
    # Pobieramy ważność (używamy 'gain', bo najlepiej pokazuje realny wpływ na decyzję)
    importances = model.get_booster().get_score(importance_type='gain')
    
    # Tworzymy DataFrame i sortujemy
    df_imp = pd.DataFrame(list(importances.items()), columns=['Feature', 'Importance'])
    df_imp = df_imp.sort_values(by='Importance', ascending=True)
    
    # Rysujemy
    plt.barh(df_imp['Feature'], df_imp['Importance'], color=color)
    plt.title(title)
    plt.xlabel('Importance (Gain)')

# Tworzymy okno z dwoma wykresami
plt.figure(figsize=(15, 10))

# Wykres dla modelu STATYCZNEGO
plt.subplot(1, 2, 1) # Lewa strona
plot_importance("static_model.json", "Ważność cech: MODEL STATYCZNY", "skyblue")

# Wykres dla modelu DYNAMICZNEGO
plt.subplot(1, 2, 2) # Prawa strona
plot_importance("dynamic_model.json", "Ważność cech: MODEL DYNAMICZNY", "salmon")

plt.tight_layout()
plt.show()