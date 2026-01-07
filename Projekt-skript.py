

import pandas as pd
import matplotlib.pyplot as plt

# 1. Skapa datasetet baserat på Spotify Q3 2025 siffrorna
data = {
    'Segment': ['Premium', 'Gratis (Annons)'],
    'Anvandare_Miljoner': [281, 446],
    'Intakter_Miljoner_EUR': [3826, 446],
    'Bruttomarginal_Procent': [33.2, 18.4]
}

df = pd.DataFrame(data)

# 2. Beräkna ARPU (Intäkt per användare per månad)
df['ARPU_EUR'] = (df['Intakter_Miljoner_EUR'] / df['Anvandare_Miljoner']) / 3

#==============================================================================================
# Graf 1: Värdet av en Spotify-kund (EUR per månad)
plt.figure(figsize=(8, 6))
bars1 = plt.bar(df['Segment'], df['ARPU_EUR'], color=["#22D661", '#191414'])

# Lägg till labels för EUR
for bar in bars1:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, f'{yval:.2f} €', 
             ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.title('Värdet av en Spotify-kund (EUR per månad)')
plt.ylabel('Euro (€)')
plt.ylim(0, df['ARPU_EUR'].max() * 1.2)
plt.show()

#==============================================================================================
# Graf 2: Bruttomarginal per segment (%)
plt.figure(figsize=(8, 6))
bars2 = plt.bar(df['Segment'], df['Bruttomarginal_Procent'], color=["#22D661", '#191414'])

# Lägg till labels för procent
for bar in bars2:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval}%', 
             ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.title('Bruttomarginal per segment (%)')
plt.ylabel('Procent (%)')
plt.ylim(0, 40)
plt.show()

#==============================================================================================
# Graf 3: Simulering av vinstpotential vid konvertering av gratisanvändare till premium
konverteringsgrad = 0.05 # 5% konverteringsgrad
antal_som_flyttas = df.loc[1, 'Anvandare_Miljoner'] * konverteringsgrad
vinst_premium_per_user = df.loc[0, 'ARPU_EUR'] * (df.loc[0, 'Bruttomarginal_Procent'] / 100)
vinst_gratis_per_user = df.loc[1, 'ARPU_EUR'] * (df.loc[1, 'Bruttomarginal_Procent'] / 100)

vinst_innan = (antal_som_flyttas * vinst_gratis_per_user)
vinst_efter = (antal_som_flyttas * vinst_premium_per_user)

kategorier = ['Vinst som Gratislyssnare', 'Vinst som Premium-kunder']
vinst_varden = [vinst_innan, vinst_efter]

plt.figure(figsize=(10, 6))
bars3 = plt.bar(kategorier, vinst_varden, color=['#191414', '#1DB954'])

for bar in bars3:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.1f} M EUR', 
             ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.title(f'Vinstpotential vid konvertering av {antal_som_flyttas:.1f} miljoner användare')
plt.ylabel('Månadsvinst (Miljoner EUR)')
plt.ylim(0, max(vinst_varden) * 1.2)
plt.show()

#==============================================================================================
import numpy as np
# Graf 4: Monte Carlo-simulering av vinstökning vid olika konverteringsgrader
# 1. Inställningar för simuleringen
antal_simuleringar = 10000
# Vi antar att konverteringen följer en normalfördelning med medelvärde 5% (0.05)
# och en standardavvikelse på 1% (0.01)
konverterings_scenarier = np.random.normal(0.05, 0.01, antal_simuleringar)

# 2. Beräkna vinstökning för varje scenario
# (vinst_premium_per_user - vinst_gratis_per_user) är vinstlyftet per person
vinstlyft_per_person = vinst_premium_per_user - vinst_gratis_per_user
totala_gratisanvandare = df.loc[1, 'Anvandare_Miljoner']

vinster = []
for k in konverterings_scenarier:
    antal_personer = totala_gratisanvandare * k
    vinster.append(antal_personer * vinstlyft_per_person)

# 3. Visualisera resultatet med ett Histogram (Seaborn-stil)
plt.figure(figsize=(10, 6))
plt.hist(vinster, bins=50, color='#1DB954', edgecolor='black', alpha=0.7)

# Lägg till en linje för medelvärdet
medel_vinst = np.mean(vinster)
plt.axvline(medel_vinst, color='red', linestyle='dashed', linewidth=2, label=f'Medel: {medel_vinst:.1f} M EUR')

plt.title('Simulering av vinstökning (10 000 scenarier)', fontsize=14)
plt.xlabel('Månadsvinstökning (Miljoner EUR)')
plt.ylabel('Antal utfall (Frekvens)')
plt.legend()
plt.show()

# 4. Statistisk analys för rapporten
print(f"Medelvärde: {medel_vinst:.2f} M EUR")
print(f"95% konfidensintervall: {np.percentile(vinster, 2.5):.2f} till {np.percentile(vinster, 97.5):.2f} M EUR")