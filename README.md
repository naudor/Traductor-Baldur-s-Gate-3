# Traducció al català de Baldur's Gate 3

Aquest projecte ofereix una **traducció no oficial al català** del videojoc *Baldur's Gate 3*, substituint l’idioma castellà del joc. La traducció s'aplica **reemplaçant el fitxer d’idioma original** per un fitxer `.pak` modificat.

## 🧭 Com utilitzar la traducció

1. Assegura’t que tens el joc configurat en **castellà**.
2. Ves a la ruta:
   ```
   C:\Steam\steamapps\common\Baldurs Gate 3\Data\Localization\Spanish
   ```
3. **Fes una còpia de seguretat** del fitxer original `Spanish.pak`.
4. Substitueix-lo pel fitxer `.pak` que trobaràs a la carpeta [`pak`](https://github.com/naudor/Traductor-Baldur-s-Gate-3/tree/main/pak) d’aquest repositori.

> ⚠️ Aquesta traducció **no es carrega com a mod**, sinó que **substitueix l’idioma castellà** directament.

---

## 📁 Estructura del repositori

- **`originals/`**  
  Fitxers resultants de desempaquetar el fitxer `Spanish.pak` original del joc. Serveixen com a referència base.

- **`descodificats/`**  
  Mateixos fitxers que `originals`, però **descodificats a format XML**, facilitant-ne la lectura i edició.

- **`traduccions-xml/`**  
  Fitxers XML **traduïts automàticament al català**.

- **`traduccions-loca/`**  
  Els mateixos fitxers traduïts, però **reconvertits al format `.loca`**, preparats per empaquetar.

- **`pak/`**  
  Conté el **fitxer final `Spanish.pak` traduït**, llest per substituir el fitxer d’idioma original del joc.

- **`traductor.py`**  
  Script en Python que **automatitza la traducció**. Utilitza el model d’IA **DeepSeek** per traduir automàticament totes les línies dels fitxers XML originals.

---

## 🤖 Traducció automàtica i correccions manuals

La traducció del joc ha estat **generada completament amb el model DeepSeek**, mitjançant l’script `traductor.py`. Tot i que el resultat és molt complet, el model ha comès errors de traducció que cal **corregir manualment**.

Per fer-ho:

1. Edita els fitxers XML de la carpeta `traduccions-xml` per corregir errors de traducció.
2. Converteix-los a format `.loca` utilitzant **LSLib Toolkit**.
3. Empaqueta els fitxers `.loca` en un nou fitxer `Spanish.pak`.

---

## 🛠️ Eina necessària: LSLib Toolkit

Per desempaquetar, descodificar, codificar i empaquetar els fitxers `.pak`, `.loca` i `.xml`, cal utilitzar:

🔧 **[LSLib Divinity Mod Tools (LSLib Toolkit)](https://github.com/Norbyte/lslib/releases)**

És una eina essencial per a la manipulació dels fitxers del joc.

---

## 📌 Estat del projecte

La traducció automàtica és **completa**, però **encara s’hi han de revisar i corregir errors**. Tota col·laboració per revisar, corregir o millorar el procés és molt benvinguda.
