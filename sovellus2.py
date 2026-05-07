
## Datan esikäsittelyn sovellus Fingridin tai Entso-e:n apiohjelmalla haetulle datalle

## Aja komentoriviltä tai Pythonin Shellissä
## CC BY-NC-SA 4.0 (ks. käyttöohje)


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import sys


def valikko():
    print("Käytettävissä olevat toiminnot\n")
    print("1) Resoluutiomuunnokset\n2) Datan perustiedot ja keskilukuja\n3) Tutki ja täydennä puuttuva dataa")
    print("4) Piirrä kuvio\n5) Yhdistä dataa\n6) Tuotantoaste muuttujaksi\n7) Tallenna data\n0) Lopeta ohjelma\n")
    valintax = input("Anna valintasi numerolla: ").strip()
    viiva()
    return valintax

def viiva():
    print("\n--------------------------------------------------------------------------------------------------\n")
    return None

def kysy_mja():
    mja_nimi = input("Anna datassa olevan kohdemuuttujan nimi: ").strip()
    print()
    return mja_nimi

def nimea_value(dfx):
    if 'value' in dfx.columns:
        print("Minkä nimen annat 'value'-sarakkeelle?")
        mja_value = input("Anna sarakkeen nimi, esim. 'tuuli_t' tai 'aurinko_k': ").strip()
        dfx.rename(columns={'value': mja_value}, inplace=True)
        print("\n",dfx.head(),"\n")
    return dfx

def dt_indeksi(dfx):
    print("Aloitusaika laitetaan indeksiksi jatkoa varten.\n")
    print("Data muunnetaan UTC-ajasta Suomen aikaan, jos se ei ole siinä jo.\n")
    dfx["startTime"] = pd.to_datetime(dfx["startTime"], utc=True)
    dfx["startTime"] = dfx["startTime"].dt.tz_convert("Europe/Helsinki")
    if "endTime" in dfx.columns:
        dfx["endTime"] = pd.to_datetime(dfx["endTime"], utc=True, errors="coerce")
        dfx["endTime"] = dfx["endTime"].dt.tz_convert("Europe/Helsinki")
    dfx.set_index("startTime", inplace=True)
    dfx.sort_index(inplace=True)
    return dfx

def modified_info(dfx):
    print("Valmis:\n",dfx.head())
    print("\nMuokatun datan tutkiminen ja tallennus koneelle päävalikon kautta.")        
    viiva()
    return None

def joined_info(dfx):
    print("\nDatat on nyt yhdistetty.")
    print(dfx.head())
    print("\nYhdistetyn datan tallennus ja tutkiminen päävalikon kautta.")
    viiva()
    return None

def hae_data(filex):
    dfx = pd.read_csv(filex+".csv")
    print("\nAlunperin datasi",filex,"näyttää tältä (aikavälin alku ja loppu):\n")
    print(dfx.head(),"\n")
    print(dfx.tail()) 
    print()
    return dfx

def start(): 
    print("\n*** Tämä on datan esikäsittelyn sovellus Fingridin tai Entso-e:n apiohjelmalla haetulle datalle ***\n")
    print("Ensin haetaan data koneelta (data 1).\n")
    try:
        file = input("Anna csv-tiedoston nimi ilman päätettä ja tarvittaessa myös hakemistopolku: ").strip()
        dfx = hae_data(file)
    except Exception as e:
        print(f"\nTiedoston haku epäonnistui: {e}")
        print("Käynnistä ohjelma uudelleen.")
        viiva()
        sys.exit(1)
    return dfx

def valmisdf(dfx):
    print("Käyttövalmis data näyttää tältä:\n")
    print(dfx.head())
    viiva()
    return None

def nonlocalize(dfx):
    dfx.reset_index(inplace=True)
    dfx["startTime"] = dfx["startTime"].dt.tz_localize(None)
    if "endTime" in dfx.columns:
        dfx["endTime"] = dfx["endTime"].dt.tz_localize(None)
    return dfx

def kysy_file():
    print("\nAnna nimi tiedostolle johon muokattu data tallennetaan (mahd. myös hakemistopolku).")
    nimix = input("Nimi tiedostolle (ilman tiedostopäätettä): ").strip()
    return nimix

def toiminnot(dfx):
    while True:
        valinta = valikko()
        if valinta == "1":
            print("Voit keskiarvoistaa valitsemasi muuttujan\n1) tunnin tai 2) päivän tasolle.")
            print("Huom. älä käytä jo yhdistetylle datalle -tulos on jokatapauksessa yksimuuttujainen data.\n")
            print("3) ei kumpikaan; paluu päävalikkoon\n")
            resol = input("Valintasi (numero): ").strip()
            print()
            if resol == "1":
                print("Keskiarvoistetaan kohdemuuttuja tunnin tasolle.\n")
                mja_resample = kysy_mja()
                if mja_resample not in dfx.columns:
                    print("Datassa ei ole muuttujaa nimellä",mja_resample)
                    viiva()
                else: 
                    df_hours = dfx[mja_resample].resample("h").mean()
                    dfx = df_hours.to_frame()
                    dfx.sort_index(inplace=True)
                    print("Alkuperäinen resoluutio on nyt korvattu tuntiresoluutiolla.\n")
                    modified_info(dfx)        
            elif resol == "2":
                print("Keskiarvoistetaan kohdemuuttuja päivän tasolle.\n")
                mja_resample2 = kysy_mja()
                if mja_resample2 not in dfx.columns:
                    print("Datassa ei ole muuttujaa nimellä",mja_resample2)
                    viiva()
                else:
                    df_hours = dfx[mja_resample2].resample("1D").mean()
                    dfx = df_hours.to_frame()
                    dfx.sort_index(inplace=True)
                    print("Alkuperäinen resoluutio on nyt korvattu päiväresoluutiolla.\n")
                    modified_info(dfx)
            else:
                print("Dataa ei muutettu.")
                viiva()
                            
        elif valinta == "2":
            print("Datarivien määrä, aikaväli ja datatyypit:\n")
            dfx.info()
            print()
            print("Keski- ja hajontalukuja:\n")
            print(dfx.drop(columns=['datasetId'], errors='ignore').describe(),"\n")
            print("Puuttuvan tiedon määrät (kaikki muuttujat):\n")
            print(dfx.isnull().sum())
            viiva()
                
        elif valinta == "3":
            print("Tarkastelu koskee valitsemasi muuttujan puuttuvia arvoja, jotka on merkattu puuttuvaksi (NaN).")
            print("Jos koko rivi aikaleimoineen puuttuu datasta, tietoa ei ole merkattu puuttuvaksi.\n")
            
            mja_miss = kysy_mja()
            if mja_miss not in dfx.columns:
                print("Datassa ei ole muuttujaa nimellä",mja_miss)
                viiva()
            elif dfx[mja_miss].isna().sum() == 0:
                print("Muuttujassa",mja_miss,"ei ole puuttuvaa tietoa.")
                viiva()
            else:
                print("Yhtäjaksoisuus: Alla vasemmalla peräkkäisten puuttuvien (NaN) tuntien määrä (ts. jakson pituus")
                print("datan resoluution mukaisessa aikayksikössä) ja oikealla kuinka monta tämänpituista jaksoa esiintyy")
                print("(frekvenssit).\n")
                
                miss = dfx[mja_miss].isnull()
                groups = (miss != miss.shift()).cumsum()
                gaps = dfx[miss].groupby(groups[miss])
                gap_lengths = gaps.size()
                print(gap_lengths.value_counts().sort_index())
                
                print("\nHaluatko paikata em. muuttujan puuttuvaa tietoa lineaarisella interpolaatiolla?")
                print("Paikkaaminen perustuu edeltäviin arvoihin, joten \"alkureunasta\" paikkaaminen ei onnistu.")
                fill = input("1 = kyllä, 2 = ei, valintasi: ").strip()
                if fill == "1":
                    print("\nKuinka monta peräkkäistä arvoa samassa sarakkeessa olet valmis paikkamaan?\n")
                    print("Jos paikkaat kaikki puuttuvat, niin anna maksimi jakson pituudesta edellä.")
                    fill_luku = int(input("Anna lukumäärä: ").strip())
                    dfx[mja_miss] = dfx[mja_miss].interpolate(method='linear', limit_direction='forward', limit=fill_luku)
                    print("\nData on nyt paikattu.")
                    print("Paikatun datan tallennus ja tutkiminen päävalikon kautta.")
                    viiva()
                else:
                    print("\nDataa ei muutettu.")
                    viiva()
                 
        elif valinta == "4":
            print("Minkä muuttujan muutosta ajassa haluat kuvata?\n")
            print("Voit peruuttaa antamalla minkä vaan merkin joka ei ole muuttujan nimi.")
            mja_plot = kysy_mja()
            if mja_plot not in dfx.columns:
                print("Datassa ei ole muuttujaa nimellä",mja_plot)
                viiva()
                continue
            else: 
                dfx[mja_plot].plot(figsize=(14,8))
                plt.xlabel("Aika")
                plt.title(f"{mja_plot}")
                plt.show()
                
        elif valinta == "5":
            print("Liitettävässä datassa (data 2) on oltava valmiina sama resoluutio kuin datassa 1.\n")
            print("Hae liitettävä data (data2) koneeltasi.")
            print("Voit peruuttaa päävalikkoon antamalla nimeksi 0 (nolla).\n")
            file2 = input("Anna csv-tiedoston nimi ilman päätettä ja tarvittaessa myös hakemistopolku: ").strip()
            if file2 == '0':
                viiva()
                continue
            else:
                try:
                    dfx2 = hae_data(file2)
                except Exception as e:
                    print(f"Tiedoston haku epäonnistui: {e}")
                    viiva()
                    continue
            dfx2 = nimea_value(dfx2)            
            dfx2 = dt_indeksi(dfx2)
            
            print("Voit nyt yhdistää päävalikossa käsittelemäsi datan (data 1) nyt koneelta hakemasi datan (data 2) kanssa.\n")
            print("Valitse yhdistämisen tapa:\n")
            print("1) Aikaleimat datan 1 mukaan (datasta 1 mukaan kaikki rivit).")
            print("2) Aikaleimat datan 2 mukaan (datasta 2 mukaan kaikki rivit).")
            print("3) Kaikki aikaleimat mukaan (molemmista datoista kaikki rivit yhdistettyyn dataan.)")
            print("4) Keskeytä ja palaa päävalikkoon\n")
            
            join = input("Valintasi: ").strip()
            if join == "1":
                df_yhd = dfx.join(dfx2, how="left", rsuffix="_2")
                df_outer = dfx.join(dfx2, how="outer", rsuffix="_2")
                missing = dfx2.index.difference(dfx.index)
                print("Datan 2 osalta",len(missing),"riviä jää pois yhdistetystä datasta.\n")
                dfx = df_yhd
                joined_info(dfx)
            elif join == "2":
                df_yhd = dfx.join(dfx2, how="right", rsuffix="_2")
                df_outer = dfx.join(dfx2, how="outer", rsuffix="_2")
                missing = dfx.index.difference(dfx2.index)
                print("Datan 1 osalta",len(missing),"riviä jää pois yhdistetystä datasta.\n")
                dfx = df_yhd
                joined_info(dfx)
            elif join == "3":
                dfx = dfx.join(dfx2, how="outer", rsuffix="_2")
                joined_info(dfx)
            else:
                print("\nDataa ei muutettu.")
                            
        elif valinta == "6":
            print("Voit tehdä uuden muuttujan tuotannon suhteesta (%) kapasiteettiin, jos datassasi on")
            print("nämä molemmat muuttujat samassa resoluutiossa.\n")
            aste = input("Haluatko jatkaa? 1 = kyllä, 2 = ei, valintasi: ").strip()
            
            if aste == "1":
                mja_t = input("\nAnna datassa olevan tuotantomuuttujan nimi: ").strip()
                mja_k = input("Anna datassa olevan kapasiteettimuuttujan nimi: ").strip()
                if mja_t not in dfx.columns or mja_k not in dfx.columns:
                    print("Tarkista muuttujien nimet.")
                    viiva()
                    continue
                zero_len = len(dfx[dfx[mja_k]==0])
                if zero_len > 0:
                    print("\nKapasiteettimuuttujassa on",zero_len,"rivillä arvo 0 (harhaanjohtavaa).")
                    print("Poistetaan nollat, tilalle puuttuva tieto (NaN), mikä mahdollistaa myös paikkaamisen.\n")
                    zero = input("1 = Hyväksy vaihto, 2  = Säilytä nollat. Valintasi: ").strip()
                    if zero == "1":
                        dfx.replace({mja_k: {0: np.nan}}, inplace=True)
                        print("Nollan tilalla on nyt puuttuva tieto (NaN).\n")
                    else:
                        pass
                print()           
                dfx["tuotantoaste"] = np.where(
                dfx[mja_k] != 0,
                dfx[mja_t].clip(lower=0) / dfx[mja_k] * 100,
                np.nan)
                modified_info(dfx)
            else:
                viiva()
                continue
            
        elif valinta == "7":
            print("Valitse tallennusmuoto")
            print("1 = CSV (.csv), 2 = Excel (.xlsx)")
            print("3 = Peruuta päävalikkoon.")
            save = input("Valintasi (numero): ").strip()

            if save == "1":
                nimi = kysy_file()
                try:
                    dfx.to_csv(nimi+".csv", index=True)
                    print()
                    print(nimi+".csv tallennettu.")
                    viiva()
                except Exception as e:
                    print(f"\nTallennus epäonnistui: {e}")
            elif save == "2":
                dfx = nonlocalize(dfx)
                nimi = kysy_file()
                try:
                    with pd.ExcelWriter(nimi+".xlsx", engine="openpyxl") as writer:
                        dfx.to_excel(writer, sheet_name="preprocessed", index=False)
                        print()
                        print(nimi+".xlsx tallennettu.")
                        viiva()
                except Exception as e:
                    print(f"Tallennus epäonnistui: {e}")
            else:
                viiva()
                continue
            
        elif valinta == "0":
            print("Kiitos ohjelman käytöstä.")
            viiva()
            break
        else:
            print("Syötä toimintoa vastaava numero.")
            viiva()
    return None

def paaohjelma():
    df = start()    
    df = nimea_value(df)  
    df = dt_indeksi(df) 
    valmisdf(df)
    toiminnot(df)
    return None



## pääohjelman kutsu
try:
    paaohjelma()
except Exception as e:
    print(f"Virhe: {e}")
    sys.exit(1)

