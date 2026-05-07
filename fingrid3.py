## API client Fingridin avoimen datan palveluun GetDataSetData

## Hakee tiedot annettujen id-tunnisteiden mukaisista datoista
## tietyltä samalta aikaväliltä (startTime ja endTime) json-muodossa
## Muuntaa tiedot Pandasin data frameksi ja tallentaa koneellesi
## Tallennusvalinta CSV tai Excel (ks. käyttöohje)

## Aja komentoriviltä tai Pythonin Shellissä
## Tarvitset Pythonin ja Pandasin asennettuna
## sekä henkilökohtaisen API-avaimen Fingridin kehittäjäsivustolta


import requests
import pandas as pd
import time
import math
import sys

def intro():
    print("\n*** Muodostetaan API-pyyntö Fingridin avoimen datan palveluun ***\n")
    print("Anna pyydetty tieto ja paina enter.")
    print("Lopuksi saat ilmoituksen, että kaikki haut ja tallennukset on tehty -tai virhekoodin.\n ")

def valikko():
    print("\nValitse tallennusmuoto")
    print("1 = CSV (.csv, yhteensopiva esikäsittelysovelluksen kanssa)")
    print("2 = Excel (.xlsx)")
    valinta = input("Valintasi (numero): ").strip()
    return valinta

def start():
    print("Anna haettavan aikavälin alku ja loppu muodossa vvv-mm-dd, esim. 2025-12-31.")
    print("Voit halutessasi antaa myös kellonajat tyyliin 2025-12-31 14:00.\n")
    alku1 = input("Anna aikavälin aloitusaika: ").strip()
    alku = pd.Timestamp(alku1, tz='Europe/Helsinki')
    return alku

def end():
    loppu1 = input("Anna lopetusaika: ").strip()
    loppu = pd.Timestamp(loppu1, tz='Europe/Helsinki')
    return loppu

def kohteet():
    print("Mitä dataa haet?")
    print(" Tuulivoiman tuotanto, id: 75")
    print(" Tuulivoiman kapasiteetti, id: 268")
    print(" Aurinkovoiman tuotantoennuste, id: 248")
    print(" Aurinkovoiman kapasiteetti, id: 267\n")
    id_listx = input("Anna kaikkien haettavien datojen id:t välilyönnillä erotettuna: ").strip().split()
    return id_listx

def dt_fi(dfx):
    dfx["startTime"] = pd.to_datetime(dfx["startTime"], utc=True).dt.tz_convert("Europe/Helsinki")
    dfx["startTime"] = dfx["startTime"].dt.tz_localize(None)
    dfx["endTime"] = pd.to_datetime(dfx["endTime"], utc=True, errors="coerce").dt.tz_convert("Europe/Helsinki")
    dfx["endTime"] = dfx["endTime"].dt.tz_localize(None)
    return dfx

def paaohjelma():
    intro()
    avain = input("Anna henkilökohtainen API-avaimesi: ").strip()
    print()
    alku = start()
    loppu = end()
    print()
    id_list = kohteet()
    kumpi = valikko()

    if kumpi == "1": 
        print("\nTiedostot tallennetaan datan id:n mukaisella nimellä 'data_id' oletuksena samaan")
        print("kansioon jossa tämä ohjelma on. Jos haluat tallennuksen muualle, anna hakemistopolku.")
        print("Enterillä joka tapauksessa eteenpäin.")
        polku = input("Hakemistopolku (päättyen \): ").strip()

        for id in id_list: 
            datasetid = id
            url = "https://data.fingrid.fi/api/datasets/"+datasetid+"/data"
            params = {'startTime' : alku, 'endTime' : loppu, 'pageSize': 20000}
            headers = {'x-api-key' : avain, 'accept': 'application/json'}

            print("\nHaetaan dataa id:llä",id)
            print()
            
            all_data = []
            page = 1
            total = 1
            while page < total + 1:
                params["page"] = page
                response = requests.get(url, headers=headers, params=params)
            
                if response.status_code == 200:
                    print("Yhteys ok")
                else:
                    print("Virhekoodi:",response.status_code)
                    break
            
                data = response.json()
                if page == 1:
                    print("Haettavia rivejä on:", data["pagination"]["total"])
                    print("Tarvitaan sivuja:",data["pagination"]["total"]/params['pageSize'])
                    total = math.ceil(data["pagination"]["total"]/params['pageSize'])
            
                print("Haetaan sivu",page,"jolla on rivejä:", len(data["data"]))
                all_data.extend(data["data"])
                page = page + 1
                time.sleep(2)

            df = pd.DataFrame(all_data)

            print("Tallennettavien rivien ja sarakkeiden määrä:",df.shape)

            try:
                df.to_csv(polku+"data_"+datasetid+".csv", index=False)
                print(polku+"data_"+datasetid+".csv tallennettu.")
            except Exception as e:
                print(f"Tallennus epäonnistui: {e}")

        print("\nKaikki haut on tehty ja datat tallennettu.")

    elif kumpi == "2":
        print("\nAnna nimi Excel-tiedostolle johon data(t) tallennetaan (mahd. myös hakemistopolku).")
        nimi = input("Nimi tiedostolle (ilman tiedostopäätettä): ").strip()
        
        with pd.ExcelWriter(nimi+".xlsx", engine="openpyxl") as writer:

            for id in id_list: 
                datasetid = id
                url = "https://data.fingrid.fi/api/datasets/"+datasetid+"/data"
                params = {'startTime' : alku, 'endTime' : loppu, 'pageSize': 20000}
                headers = {'x-api-key' : avain, 'accept': 'application/json'}

                print("\nHaetaan dataa id:llä",id)
                print()
                
                all_data = []
                page = 1
                total = 1
                while page < total + 1:
                    params["page"] = page
                    response = requests.get(url, headers=headers, params=params)
                
                    if response.status_code == 200:
                        print("Yhteys ok")
                    else:
                        print("Virhekoodi:",response.status_code)
                        break
                
                    data = response.json()
                    if page == 1:
                        print("Haettavia rivejä on:", data["pagination"]["total"])
                        print("Tarvitaan sivuja:",data["pagination"]["total"]/params['pageSize'])
                        total = math.ceil(data["pagination"]["total"]/params['pageSize'])
                
                    print("Haetaan sivu",page,"jolla on rivejä:", len(data["data"]))
                       
                    all_data.extend(data["data"])
                    page = page + 1
                    time.sleep(2)

                df = pd.DataFrame(all_data)
                df = dt_fi(df)

                print("Tallennettavien rivien ja sarakkeiden määrä:",df.shape)

                try:        
                    df.to_excel(writer, sheet_name="data_"+datasetid, index=False)
                    print(f"Välilehti tallennettu nimellä data_{datasetid}.")
                except Exception as e:
                    print(f"Tallennus epäonnistui: {e}")

            print("\nKaikki hakutulokset on nyt tallennettu tiedostoon",nimi+".xlsx.")
        
    return None

## pääohjelman kutsu
try:
    paaohjelma()
except Exception as e:
    print(f"Virhe: {e}")
    sys.exit(1)


