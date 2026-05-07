
## Api-client ENTSO-E:n rajapintapalveluun

## Hakee Suomea koskevaa sähkön hintadataa tietyltä aikaväliltä (startTime ja endTime) 
## Muuntaa tiedot Pandasin data frameksi ja tallentaa csv:nä tai Excelinä omalle koneellesi 
## (ks. käyttöohje)
## Aja komentoriviltä tai Pythonin Shellissä
## Tarvitset Pythonin ja Pandasin sekä entsoe-py:n asennettuna
## sekä henkilökohtaisen api-avaimen Entso-e:n rajapintapalveluun


import requests
from entsoe import EntsoePandasClient
import pandas as pd

def valikko():
    print("\nValitse tallennusmuoto")
    print("1 = CSV (.csv, yhteensopiva esikäsittelysovelluksen kanssa)")
    print("2 = Excel (.xlsx)")
    valinta = input("Valintasi (numero): ").strip()
    return valinta
   
print("\n*** Muodostetaan API-pyyntö ENTSO-E:n avoimen datan palveluun ***\n")
print("Anna pyydetty tieto ja paina enter.")
print("Lopuksi saat ilmoituksen, että data on tallennettu koneellesi -tai virhekoodin.\n ")

api_key = input("Anna api-avain eli security token: ").strip()
client = EntsoePandasClient(api_key = api_key)

print("\nAnna haettavan aikavälin alku ja loppu muodossa vvv-mm-dd, esim. 2025-12-31.")
print("Voit halutessasi antaa myös kellonajat tyyliin 2025-12-31 14:00.\n")
alku = input("Anna aikavälin aloitusaika: ").strip()
loppu = input("Anna lopetusaika: ").strip()

kumpi = valikko()

print("\nAnna nimi tiedostolle johon haettu data tallennetaan (mahd. myös hakemistopolku).")
file = input("Nimi tiedostolle (ilman tiedostopäätettä): ").strip()

start = pd.Timestamp(alku, tz='Europe/Helsinki')
end = pd.Timestamp(loppu, tz='Europe/Helsinki')
country_code = 'FI'  

result_series = client.query_day_ahead_prices(country_code, start=start, end=end)

df = result_series.to_frame()
df.reset_index(inplace=True)
df.columns = ['startTime', 'price']
print("\nTallennettavien rivien ja sarakkeiden määrä:",df.shape)
print("Ensimmäiset rivit:")
print(df.head())
print()

if kumpi == "1": 
    try:
        df.to_csv(file+".csv",index=False)
        print(file+".csv tallennettu.\n")
    except Exception as e:
        print(f"\nTallennus epäonnistui: {e}")

elif kumpi == "2":
    df["startTime"] = df["startTime"].dt.tz_localize(None)
    try:
        with pd.ExcelWriter(file+".xlsx", engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="prices", index=False)
            print(file+".xlsx tallennettu.\n")
    except Exception as e:
        print(f"Tallennus epäonnistui: {e}")
        

                
        
