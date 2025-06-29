from tqdm import tqdm
import xml.etree.ElementTree as ET
import os
import html
from openai import OpenAI
import json

# Configura l'API (DeepSeek via endpoint compatible amb OpenAI)
os.environ["OPENAI_API_KEY"] = "sk-5a41a61c2f7b4153bb7f7be2c6dd2c88"
client = OpenAI(base_url="https://api.deepseek.com")
MODEL_NAME = "deepseek-chat"
MIDA_BLOC = 50

def neteja_entrada(text: str) -> str:
    text = html.escape(text)
    text = text.replace("'", "’")
    return text

def restaura_sortida(text: str) -> str:
    text = html.unescape(text)
    return text.replace("’", "'")

def tradueix_bloc_de_línies(llista_frases: list[str]) -> list[str]:
    prompt_json = {
        "texts": [neteja_entrada(frase) for frase in llista_frases]
    }

    try:
        resposta = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ets un traductor professional del castellà al català. "
                        "Rebràs un objecte JSON amb una llista de frases sota la clau 'texts'. "
                        "Traduïx cada element del camp 'texts' i retorna un JSON amb la clau 'translations'. "
                        "El nombre d'elements traduïts ha de coincidir exactament amb l'original. "
                        "NO afegeixis explicacions."
                        "Instruccions especials:"
                        "Tradueix 'Corazón Sombrio' per 'Cor tenebrós', 'garracuerno' per 'Garracorna', 'azotamentes' per 'flagell de ments', 'risa' per 'rialla', 'mentonáculo' per 'mentonacle', "
                        "'a salvo' per 'fora de perill', 'Tarareo' per 'taral·leig', 'escueta' per 'concisa', 'en cuanto' per 'tant bon punt', 'amanezca' per 'surti el sol', 'ojo avizor' per 'ull viu'"
                        "'cambion' per 'metàmorf', 'juguetes' per 'juguines', 'Ojalá' per 'Tant de bo', 'impia' per 'impietosa', 'engendro' per 'abominació', 'ladrones' per 'lladres', 'sedienta' per 'assedegada'"
                        "'siervo' per 'vassall', 'podrida' per 'púdrida', 'labia' per 'eloqüència', 'cabeza hueca' per 'cap de suro', 'mente colmena' per 'ment enllaçada', 'nauseabunda' per 'repugnant'"
                        "'frasco' per 'flascó', 'conseguido' per 'aconseguit', 'diablillo' per 'dimoniet'', 'Jarro' per 'Gerra', 'piel robliza' per 'pell de roure', 'cáliz' per 'càliz', 'compañeros' per 'companys'"
                        "'trampilla' per 'trapa', 'pócima' per 'pòcima', 'jamas pense' per 'mai hauria pensat', 'al acecho' per 'a la guait', 'picaro' per 'brivall', 'salpicadura' per 'esquitx', 'pillan' per 'atrapen'"
                        "'me las piro' per 'foto el camp', 'empujoncito' per 'empenteta', 'bicho' per 'bestiola', 'hacha' per 'destral', 'te diviertes' per 'et diverteixes', 'pandilla' per 'colla', 'pilla' per 'agafa'"
                        "'lenyador' per 'llenyataire','sabe a' per 'te gust a ', 'hinchado' per 'inflat', 'conozco' per 'conec', 'pesadilla' per 'malson', 'acometida' per 'escomesa', 'tañido' per 'repic', 'enano' per 'nan'"
                        "'yelmo' per 'elm', 'rindete' per 'rendeix-te', 'estupendo' per 'fantàstic', 'ahínco' per 'afany', 'pastizal' per 'dineral', 'merecido' per 'merescut', 'manos a la obra' per 'anem per feina'"
                        "'usa' per 'utilitza', 'colinas' per 'turons', 'sendero' per 'camí', 'date prisa' per 'afanya't', 'se cuelan' per 's'escolen', 'macheta' per 'ganivet gros', 'en un santiamen' per 'en un instant'"
                        "'Lunar' per 'de la Lluna', 'pretendes' per 'pretens', 'bicho' per 'bestiola'"
                        "Si detectes que una paraula com 'cielo' s'utilitza com a mot carinyós, tradueix-la com 'rei' o 'carinyo', segons convingui. Si és literal, fes servir 'cel'."
                        "Quan es parli en el text original de 'saga' com a sinonim de 'bruja' tradueix-lo per 'bruixa'"
                        #"Respecta escrupolosament el gènere no binari de l'original. Si el text font usa recursos no binaries (com '-e', '-en'),"
                        #" adapta'l al català amb la mateixa convenció, prioritzant la intenció dels creadors sobre la normativa estàndard"
                    )
                },
                {
                    "role": "user",
                    "content": json.dumps(prompt_json, ensure_ascii=False)
                }
            ],
            temperature=0.5,
        )

        text_traduït = resposta.choices[0].message.content.strip()

        # Elimina capçaleres Markdown o restes decoratives
        línies = text_traduït.strip().splitlines()
        if línies and línies[0].strip().lower() in ("json", "```json"):
            línies = línies[1:]  # elimina la primera línia
            if línies and línies[-1].strip() == "```":
                línies = línies[:-1]  # elimina l'última línia si és el tancament del bloc
            text_traduït = "".join(línies).strip()

        linies_traduïdes = ["" for _ in llista_frases]
        try:
            traduccions_json = json.loads(text_traduït)
            traduïdes = traduccions_json.get("translations", [])
            for i, frase in enumerate(traduïdes):
                if i < len(linies_traduïdes):
                    linies_traduïdes[i] = restaura_sortida(frase.strip())
        except Exception as e:
            print(f"❌ Error interpretant la resposta JSON del model: {e}")
            print("📥 Resposta rebuda del model (bruta):")
            print(repr(text_traduït))

        for i, traduccio in enumerate(linies_traduïdes):
            if not traduccio.strip():
                frase_original = llista_frases[i]
                try:
                    resposta_retry = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "Ets un traductor professional del castellà al català. "
                                    "Tradueix la frase següent, conservant qualsevol etiqueta XML o caràcters especials. "
                                    "NO afegeixis cap comentari ni explicació."
                                )
                            },
                            {
                                "role": "user",
                                "content": neteja_entrada(frase_original)
                            }
                        ],
                        temperature=0.5,
                    )
                    retry_result = resposta_retry.choices[0].message.content.strip()
                    if retry_result:
                        linies_traduïdes[i] = restaura_sortida(retry_result)
                        print(f"🔁 Línia {i+1} re-traduïda correctament.")
                    else:
                        linies_traduïdes[i] = frase_original
                        print(f"⚠️ Línia {i+1} no traduïda. Frase original mantinguda:\n> {frase_original}")
                except Exception as e:
                    print(f"❌ Error al reintentar la línia {i+1}: {e}")
                    linies_traduïdes[i] = frase_original
                    print(f"⚠️ Línia {i+1} mantinguda original per error:\n> {frase_original}")

        return linies_traduïdes

    except Exception as e:
        print(f"⚠️ Error en traduir el bloc: {e}")
        return []

def processa_fitxer_xml(nom_fitxer, num_linia_inicial):
    try:
        arbre = ET.parse(nom_fitxer)
        arrel = arbre.getroot()
        nom_fitxer_nou = nom_fitxer.replace('.xml', '_CAT.xml')
        log_path = nom_fitxer.replace('.xml', '_traduccio.log')
        log = open(log_path, 'w', encoding='utf-8')

        if os.path.exists(nom_fitxer_nou):
            arbre_nou = ET.parse(nom_fitxer_nou)
            arrel_nou = arbre_nou.getroot()
        else:
            arrel_nou = ET.Element(arrel.tag)

        elements = list(arrel.iter('content'))
        print(f"📊 Línies originals: {len(elements)}")
        total = len(elements)
        comptador = 0

        while comptador < total:
            if comptador < num_linia_inicial:
                comptador += 1
                continue

            bloc_actual = []
            elements_bloc = []
            i = 0
            while comptador + i < total and len(bloc_actual) < MIDA_BLOC:
                element = elements[comptador + i]
                if element.text and element.text.strip():
                    bloc_actual.append(element.text.strip())
                    elements_bloc.append(element)
                i += 1

            if not bloc_actual:
                comptador += i
                continue

            log.write(f"\n🔹 Bloc començat a línia {comptador} ({len(bloc_actual)} frases):\n")
            traduccions = tradueix_bloc_de_línies(bloc_actual)

            if not traduccions or len(traduccions) != len(bloc_actual):
                log.write(f"❌ Bloc descartat: {len(traduccions)} traduccions rebudes.\n")
                comptador += i
                continue

            linies_buides = sum(1 for t in traduccions if not t.strip())
            log.write(f"✅ Bloc acceptat. Línies buides: {linies_buides}\n")
            if len(traduccions) != len(bloc_actual):
                print(f"❌ Bloc començat a línia {comptador}: {len(bloc_actual)} originals vs {len(traduccions)} traduïdes")
            else:
                print(f"✅ Bloc començat a línia {comptador}: {len(bloc_actual)} frases traduïdes correctament")

            for idx, (elem_original, text_traduït) in enumerate(zip(elements_bloc, traduccions)):
                if not text_traduït.strip():
                    log.write(f"  ⚠️ Línia {idx + 1} buida. S'afegeix la frase original.\n")
                    text_traduït = elem_original.text.strip()

                nou_elem = ET.SubElement(arrel_nou, elem_original.tag)
                nou_elem.text = text_traduït
                for atribut, valor in elem_original.attrib.items():
                    nou_elem.set(atribut, valor)

            comptador += i

            xml_str = ET.tostring(arrel_nou, encoding='unicode')
            xml_str = xml_str.replace('</content>', '</content>\n')
            with open(nom_fitxer_nou, 'w', encoding='utf-8') as f:
                f.write('<?xml version="1.0" encoding="utf-8"?>\n')
                f.write(xml_str)

        log.close()
        print(f"✅ Fitxer completament traduït i desat com: {nom_fitxer_nou}")
        print(f"📄 Log de la traducció desat com: {log_path}")

        elements_traduits = list(arrel_nou.iter('content'))
        print(f"📊 Línies traduïdes: {len(elements_traduits)}")

        if len(elements_traduits) == len(elements):
            print("✅ Nombre de línies coincident entre l'original i el fitxer traduït.")
        else:
            print("❌ Atenció: el nombre de línies traduïdes no coincideix amb l'original!")
            print(f"➡️ Diferència: {len(elements)} originals vs {len(elements_traduits)} traduïdes")

    except Exception as e:
        print(f"❌ Error en processar el fitxer XML: {e}")

def actualitza_fitxer_traduït(nom_fitxer_original, nom_fitxer_traduït):
    try:
        arbre_original = ET.parse(nom_fitxer_original)
        arrel_original = arbre_original.getroot()
        elements_originals = list(arrel_original.iter('content'))

        if os.path.exists(nom_fitxer_traduït):
            arbre_traduït = ET.parse(nom_fitxer_traduït)
            arrel_traduït = arbre_traduït.getroot()
            contentuids_existents = {
                elem.attrib.get('contentuid'): elem.text.strip()
                for elem in arrel_traduït.iter('content')
                if elem.attrib.get('contentuid') and elem.text
            }
        else:
            arrel_traduït = ET.Element(arrel_original.tag)
            contentuids_existents = {}

        nous_elements = []
        nous_textos = []
        for elem in elements_originals:
            contentuid = elem.attrib.get('contentuid')
            text = elem.text.strip() if elem.text else ''
            if contentuid and contentuid not in contentuids_existents and text:
                nous_elements.append(elem)
                nous_textos.append(text)

        print(f"🔍 S'han detectat {len(nous_textos)} noves línies per traduir.")

        bloc_inici = 0
        while bloc_inici < len(nous_textos):
            bloc = nous_textos[bloc_inici:bloc_inici + MIDA_BLOC]
            elements_bloc = nous_elements[bloc_inici:bloc_inici + MIDA_BLOC]

            traduccions = tradueix_bloc_de_línies(bloc)
            if len(traduccions) != len(bloc):
                print(f"⚠️ Error de mida al bloc {bloc_inici}. Traduccions descartades.")
                bloc_inici += MIDA_BLOC
                continue

            for original, text_traduït in zip(elements_bloc, traduccions):
                nou_elem = ET.SubElement(arrel_traduït, original.tag)
                nou_elem.text = text_traduït
                for atribut, valor in original.attrib.items():
                    nou_elem.set(atribut, valor)

            bloc_inici += MIDA_BLOC

        xml_str = ET.tostring(arrel_traduït, encoding='unicode')
        xml_str = xml_str.replace('</content>', '</content>\n')
        with open(nom_fitxer_traduït, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write(xml_str)

        print(f"✅ Traducció actualitzada i desada com: {nom_fitxer_traduït}")
        print(f"📊 Línies noves traduïdes: {len(nous_textos)}")

    except Exception as e:
        print(f"❌ Error en actualitzar el fitxer de traducció: {e}")


# Exemple d'ús
nom_fitxer_original = 'D:\\Repositori\\Traductor-Baldur-s-Gate-3\\descodificats\\Localization\\Spanish\\Gender\\Neutral\\spanish_X_to_M.xml'
num_linia_inicial = 0
#processa_fitxer_xml(nom_fitxer_original, num_linia_inicial)
nom_fitxer_traduït = nom_fitxer_original.replace('.xml', '_CAT.xml')
actualitza_fitxer_traduït(nom_fitxer_original, nom_fitxer_traduït)
