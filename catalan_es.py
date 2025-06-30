import streamlit as st
import random
import json
import datetime
from typing import Dict, List, Tuple

# Configuración de la página
st.set_page_config(
    page_title="🏴󠁥󠁳󠁣󠁴󠁿 Entrenador de Verbos Catalanes",
    page_icon="🏴󠁥󠁳󠁣󠁴󠁿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS para adaptabilidad móvil
st.markdown("""
<style>
    /* Estilos generales para dispositivos móviles */
    @media (max-width: 768px) {
        .main > div {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        /* Aumentar el tamaño de botones en móviles */
        .stButton > button {
            height: 3rem;
            font-size: 1.1rem;
        }
        
        /* Mejorar visualización de métricas */
        [data-testid="metric-container"] {
            border: 1px solid #e0e0e0;
            padding: 0.5rem;
            border-radius: 0.5rem;
            margin-bottom: 0.5rem;
        }
        
        /* Estilos para tarjetas de verbos */
        .verb-card {
            background: linear-gradient(135deg, #ff6b6b 0%, #feca57 50%, #48ca8b 100%);
            color: white;
            padding: 2rem 1rem;
            border-radius: 1rem;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .verb-title {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .verb-translation {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 1rem;
        }
        
        .pronoun-display {
            font-size: 1.8rem;
            font-weight: bold;
            margin: 1rem 0;
            background: rgba(255,255,255,0.2);
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            display: inline-block;
        }
        
        .answer-display {
            font-size: 2rem;
            font-weight: bold;
            background: rgba(255,255,255,0.9);
            color: #2d5e3e;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
    }
    
    /* Para pantallas grandes */
    @media (min-width: 769px) {
        .verb-card {
            background: linear-gradient(135deg, #ff6b6b 0%, #feca57 50%, #48ca8b 100%);
            color: white;
            padding: 3rem 2rem;
            border-radius: 1rem;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        }
        
        .verb-title {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .verb-translation {
            font-size: 1.4rem;
            opacity: 0.9;
            margin-bottom: 1.5rem;
        }
        
        .pronoun-display {
            font-size: 2rem;
            font-weight: bold;
            margin: 1.5rem 0;
            background: rgba(255,255,255,0.2);
            padding: 0.8rem 1.5rem;
            border-radius: 0.5rem;
            display: inline-block;
        }
        
        .answer-display {
            font-size: 2.5rem;
            font-weight: bold;
            background: rgba(255,255,255,0.9);
            color: #2d5e3e;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 1.5rem 0;
        }
    }
    
    /* Ocultar elementos estándar de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mejorar visualización del selectbox en móviles */
    .stSelectbox > div > div {
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Datos de verbos catalanes
VERBS = {
    'ser': {'translation': 'ser', 'type': 'irregular'},
    'estar': {'translation': 'estar', 'type': 'irregular'},
    'tenir': {'translation': 'tener', 'type': 'irregular'},
    'fer': {'translation': 'hacer', 'type': 'irregular'},
    'dir': {'translation': 'decir', 'type': 'irregular'},
    'anar': {'translation': 'ir', 'type': 'irregular'},
    'veure': {'translation': 'ver', 'type': 'irregular'},
    'donar': {'translation': 'dar', 'type': 'regular-ar'},
    'saber': {'translation': 'saber', 'type': 'irregular'},
    'voler': {'translation': 'querer', 'type': 'irregular'},
    'parlar': {'translation': 'hablar', 'type': 'regular-ar'},
    'viure': {'translation': 'vivir', 'type': 'irregular'},
    'menjar': {'translation': 'comer', 'type': 'regular-ar'},
    'beure': {'translation': 'beber', 'type': 'irregular'},
    'treballar': {'translation': 'trabajar', 'type': 'regular-ar'},
    'estudiar': {'translation': 'estudiar', 'type': 'regular-ar'},
    'arribar': {'translation': 'llegar', 'type': 'regular-ar'},
    'sortir': {'translation': 'salir', 'type': 'irregular'},
    'venir': {'translation': 'venir', 'type': 'irregular'},
    'poder': {'translation': 'poder', 'type': 'irregular'},
    'portar': {'translation': 'llevar', 'type': 'regular-ar'},
    'deixar': {'translation': 'dejar', 'type': 'regular-ar'},
    'trobar': {'translation': 'encontrar', 'type': 'regular-ar'},
    'pensar': {'translation': 'pensar', 'type': 'irregular'},
    'sentir': {'translation': 'sentir', 'type': 'irregular'},
    'córrer': {'translation': 'correr', 'type': 'regular-re'},
    'llegir': {'translation': 'leer', 'type': 'irregular'},
    'escriure': {'translation': 'escribir', 'type': 'irregular'},
    'obrir': {'translation': 'abrir', 'type': 'irregular'},
    'tancar': {'translation': 'cerrar', 'type': 'regular-ar'}
}

PRONOUNS = ['jo', 'tu', 'ell/ella', 'nosaltres', 'vosaltres', 'ells/elles']

CONJUGATIONS = {
    'present': {
        'ser': ['sóc', 'ets', 'és', 'som', 'sou', 'són'],
        'estar': ['estic', 'estàs', 'està', 'estem', 'esteu', 'estan'],
        'tenir': ['tinc', 'tens', 'té', 'tenim', 'teniu', 'tenen'],
        'fer': ['faig', 'fas', 'fa', 'fem', 'feu', 'fan'],
        'dir': ['dic', 'dius', 'diu', 'diem', 'dieu', 'diuen'],
        'anar': ['vaig', 'vas', 'va', 'anem', 'aneu', 'van'],
        'veure': ['veig', 'veus', 'veu', 'veiem', 'veieu', 'veuen'],
        'donar': ['dono', 'dones', 'dona', 'donem', 'doneu', 'donen'],
        'saber': ['sé', 'saps', 'sap', 'sabem', 'sabeu', 'saben'],
        'voler': ['vull', 'vols', 'vol', 'volem', 'voleu', 'volen'],
        'parlar': ['parlo', 'parles', 'parla', 'parlem', 'parleu', 'parlen'],
        'viure': ['visc', 'vius', 'viu', 'vivim', 'viviu', 'viuen'],
        'menjar': ['menjo', 'menges', 'menja', 'mengem', 'mengeu', 'mengen'],
        'beure': ['bec', 'beus', 'beu', 'bevem', 'beveu', 'beuen'],
        'treballar': ['treballo', 'treballes', 'treballa', 'treballem', 'treballeu', 'treballen'],
        'estudiar': ['estudio', 'estudies', 'estudia', 'estudiem', 'estudieu', 'estudien'],
        'arribar': ['arribo', 'arribes', 'arriba', 'arribem', 'arribeu', 'arriben'],
        'sortir': ['surto', 'surts', 'surt', 'sortim', 'sortiu', 'surten'],
        'venir': ['vinc', 'véns', 'véu', 'venim', 'veniu', 'vénen'],
        'poder': ['puc', 'pots', 'pot', 'podem', 'podeu', 'poden'],
        'portar': ['porto', 'portes', 'porta', 'portem', 'porteu', 'porten'],
        'deixar': ['deixo', 'deixes', 'deixa', 'deixem', 'deixeu', 'deixen'],
        'trobar': ['trobo', 'trobes', 'troba', 'trobem', 'trobeu', 'troben'],
        'pensar': ['penso', 'penses', 'pensa', 'pensem', 'penseu', 'pensen'],
        'sentir': ['sento', 'sents', 'sent', 'sentim', 'sentiu', 'senten'],
        'córrer': ['corro', 'corres', 'corre', 'correm', 'correu', 'corren'],
        'llegir': ['llegeixo', 'llegeixes', 'llegeix', 'llegim', 'llegiu', 'llegeixen'],
        'escriure': ['escric', 'escrius', 'escriu', 'escrivim', 'escriviu', 'escriuen'],
        'obrir': ['obro', 'obres', 'obre', 'obrim', 'obriu', 'obren'],
        'tancar': ['tanco', 'tanques', 'tanca', 'tanquem', 'tanqueu', 'tanquen']
    },
    'indefinit': {
        'ser': ['fui', 'fores', 'fou', 'fórem', 'fóreu', 'foren'],
        'estar': ['estigui', 'estigues', 'estigué', 'estiguérem', 'estiguéreu', 'estigueren'],
        'tenir': ['tingui', 'tingues', 'tingué', 'tinguérem', 'tinguéreu', 'tingueren'],
        'fer': ['fiu', 'feres', 'féu', 'férem', 'féreu', 'feren'],
        'dir': ['digui', 'digues', 'digué', 'diguérem', 'diguéreu', 'digueren'],
        'anar': ['anì', 'anares', 'anà', 'anàrem', 'anàreu', 'anaren'],
        'veure': ['viu', 'veres', 'véu', 'vérem', 'véreu', 'veren'],
        'donar': ['donì', 'donares', 'donà', 'donàrem', 'donàreu', 'donaren'],
        'saber': ['sapigui', 'sapigues', 'sapigué', 'sapiguérem', 'sapiguéreu', 'sapigueren'],
        'voler': ['volgui', 'volgues', 'volgué', 'volguérem', 'volguéreu', 'volgueren'],
        'parlar': ['parlì', 'parlares', 'parlà', 'parlàrem', 'parlàreu', 'parlaren'],
        'viure': ['visquí', 'visques', 'visqué', 'visquérem', 'visquéreu', 'visqueren'],
        'menjar': ['menjì', 'menjares', 'menjà', 'menjàrem', 'menjàreu', 'menjaren'],
        'beure': ['beguí', 'begues', 'begué', 'beguérem', 'beguéreu', 'begueren'],
        'treballar': ['treballì', 'treballares', 'treballà', 'treballàrem', 'treballàreu', 'treballaren'],
        'estudiar': ['estudiì', 'estudiares', 'estudià', 'estudiàrem', 'estudiàreu', 'estudiaren'],
        'arribar': ['arribì', 'arribares', 'arribà', 'arribàrem', 'arribàreu', 'arribaren'],
        'sortir': ['sortí', 'sortires', 'sortí', 'sortírem', 'sortíreu', 'sortiren'],
        'venir': ['vinguí', 'vingues', 'vingué', 'vinguérem', 'vinguéreu', 'vingueren'],
        'poder': ['pogui', 'pogues', 'pogué', 'poguérem', 'poguéreu', 'pogueren'],
        'portar': ['portì', 'portares', 'portà', 'portàrem', 'portàreu', 'portaren'],
        'deixar': ['deixì', 'deixares', 'deixà', 'deixàrem', 'deixàreu', 'deixaren'],
        'trobar': ['trobì', 'trobares', 'trobà', 'trobàrem', 'trobàreu', 'trobaren'],
        'pensar': ['pensì', 'pensares', 'pensà', 'pensàrem', 'pensàreu', 'pensaren'],
        'sentir': ['sentí', 'sentires', 'sentí', 'sentírem', 'sentíreu', 'sentiren'],
        'córrer': ['corrí', 'correres', 'corré', 'corrérem', 'corréreu', 'correren'],
        'llegir': ['llegí', 'llegires', 'llegí', 'llegírem', 'llegíreu', 'llegiren'],
        'escriure': ['escriví', 'escrivires', 'escriví', 'escrivírem', 'escrivíreu', 'escriviren'],
        'obrir': ['obrí', 'obrires', 'obrí', 'obrírem', 'obríreu', 'obriren'],
        'tancar': ['tanquì', 'tanquares', 'tanqué', 'tanquàrem', 'tanquàreu', 'tanquaren']
    },
    'futur': {
        'ser': ['seré', 'seràs', 'serà', 'serem', 'sereu', 'seran'],
        'estar': ['estaré', 'estaràs', 'estarà', 'estarem', 'estareu', 'estaran'],
        'tenir': ['tindré', 'tindràs', 'tindrà', 'tindrem', 'tindreu', 'tindran'],
        'fer': ['faré', 'faràs', 'farà', 'farem', 'fareu', 'faran'],
        'dir': ['diré', 'diràs', 'dirà', 'direm', 'direu', 'diran'],
        'anar': ['aniré', 'aniràs', 'anirà', 'anirem', 'anireu', 'aniran'],
        'veure': ['veuré', 'veuràs', 'veurà', 'veurem', 'veureu', 'veuran'],
        'donar': ['donaré', 'donaràs', 'donarà', 'donarem', 'donareu', 'donaran'],
        'saber': ['sabré', 'sabràs', 'sabrà', 'sabrem', 'sabreu', 'sabran'],
        'voler': ['voldré', 'voldràs', 'voldrà', 'voldrem', 'voldreu', 'voldran'],
        'parlar': ['parlaré', 'parlaràs', 'parlarà', 'parlarem', 'parlareu', 'parlaran'],
        'viure': ['viuré', 'viuràs', 'viurà', 'viurem', 'viureu', 'viuran'],
        'menjar': ['menjaré', 'menjaràs', 'menjarà', 'menjarem', 'menjareu', 'menjaran'],
        'beure': ['beuré', 'beuràs', 'beurà', 'beurem', 'beureu', 'beuran'],
        'treballar': ['treballaré', 'treballaràs', 'treballarà', 'treballarem', 'treballareu', 'treballaran'],
        'estudiar': ['estudiaré', 'estudiaràs', 'estudiarà', 'estudiarem', 'estudiareu', 'estudiaran'],
        'arribar': ['arribaré', 'arribaràs', 'arribarà', 'arribarem', 'arribareu', 'arribaran'],
        'sortir': ['sortiré', 'sortiràs', 'sortirà', 'sortirem', 'sortireu', 'sortiran'],
        'venir': ['vindré', 'vindràs', 'vindrà', 'vindrem', 'vindreu', 'vindran'],
        'poder': ['podré', 'podràs', 'podrà', 'podrem', 'podreu', 'podran'],
        'portar': ['portaré', 'portaràs', 'portarà', 'portarem', 'portareu', 'portaran'],
        'deixar': ['deixaré', 'deixaràs', 'deixarà', 'deixarem', 'deixareu', 'deixaran'],
        'trobar': ['trobaré', 'trobaràs', 'trobarà', 'trobarem', 'trobareu', 'trobaran'],
        'pensar': ['pensaré', 'pensaràs', 'pensarà', 'pensarem', 'pensareu', 'pensaran'],
        'sentir': ['sentiré', 'sentiràs', 'sentirà', 'sentirem', 'sentireu', 'sentiran'],
        'córrer': ['correré', 'correràs', 'correrà', 'correrem', 'correreu', 'correran'],
        'llegir': ['llegiré', 'llegiràs', 'llegirà', 'llegirem', 'llegireu', 'llegiran'],
        'escriure': ['escriuré', 'escriuràs', 'escriurà', 'escriurem', 'escriureu', 'escriuran'],
        'obrir': ['obriré', 'obriràs', 'obrirà', 'obrirem', 'obrireu', 'obriran'],
        'tancar': ['tancaré', 'tancaràs', 'tancarà', 'tancarem', 'tancareu', 'tancaran']
    },
    'imperfet': {
        'ser': ['era', 'eres', 'era', 'érem', 'éreu', 'eren'],
        'estar': ['estava', 'estaves', 'estava', 'estàvem', 'estàveu', 'estaven'],
        'tenir': ['tenia', 'tenies', 'tenia', 'teníem', 'teníeu', 'tenien'],
        'fer': ['feia', 'feies', 'feia', 'fèiem', 'fèieu', 'feien'],
        'dir': ['deia', 'deies', 'deia', 'dèiem', 'dèieu', 'deien'],
        'anar': ['anava', 'anaves', 'anava', 'anàvem', 'anàveu', 'anaven'],
        'veure': ['veia', 'veies', 'veia', 'vèiem', 'vèieu', 'veien'],
        'donar': ['donava', 'donaves', 'donava', 'donàvem', 'donàveu', 'donaven'],
        'saber': ['sabia', 'sabies', 'sabia', 'sabíem', 'sabíeu', 'sabien'],
        'voler': ['volia', 'volies', 'volia', 'volíem', 'volíeu', 'volien'],
        'parlar': ['parlava', 'parlaves', 'parlava', 'parlàvem', 'parlàveu', 'parlaven'],
        'viure': ['vivia', 'vivies', 'vivia', 'vivíem', 'vivíeu', 'vivien'],
        'menjar': ['menjava', 'menjaves', 'menjava', 'menjàvem', 'menjàveu', 'menjaven'],
        'beure': ['bevia', 'bevies', 'bevia', 'bevíem', 'bevíeu', 'bevien'],
        'treballar': ['treballava', 'treballaves', 'treballava', 'treballàvem', 'treballàveu', 'treballaven'],
        'estudiar': ['estudiava', 'estudiaves', 'estudiava', 'estudiàvem', 'estudiàveu', 'estudiaven'],
        'arribar': ['arribava', 'arribaves', 'arribava', 'arribàvem', 'arribàveu', 'arribaven'],
        'sortir': ['sortia', 'sorties', 'sortia', 'sortíem', 'sortíeu', 'sortien'],
        'venir': ['venia', 'venies', 'venia', 'veníem', 'veníeu', 'venien'],
        'poder': ['podia', 'podies', 'podia', 'podíem', 'podíeu', 'podien'],
        'portar': ['portava', 'portaves', 'portava', 'portàvem', 'portàveu', 'portaven'],
        'deixar': ['deixava', 'deixaves', 'deixava', 'deixàvem', 'deixàveu', 'deixaven'],
        'trobar': ['trobava', 'trobaves', 'trobava', 'trobàvem', 'trobàveu', 'trobaven'],
        'pensar': ['pensava', 'pensaves', 'pensava', 'pensàvem', 'pensàveu', 'pensaven'],
        'sentir': ['sentia', 'senties', 'sentia', 'sentíem', 'sentíeu', 'sentien'],
        'córrer': ['corria', 'corries', 'corria', 'corríem', 'corríeu', 'corrien'],
        'llegir': ['llegia', 'llegies', 'llegia', 'llegíem', 'llegíeu', 'llegien'],
        'escriure': ['escrivia', 'escrivies', 'escrivia', 'escrivíem', 'escrivíeu', 'escrivien'],
        'obrir': ['obria', 'obries', 'obria', 'obríem', 'obríeu', 'obrien'],
        'tancar': ['tancava', 'tancaves', 'tancava', 'tancàvem', 'tancàveu', 'tancaven']
    }
}

RULES = {
    'present': {
        'title': 'Presente (Present)',
        'content': '''
**Verbos regulares -AR:**
Raíz + -o, -es, -a, -em, -eu, -en
*Ejemplo: parlar → parlo, parles, parla, parlem, parleu, parlen*

**Verbos regulares -RE:**
Raíz + -o, -es, -e, -em, -eu, -en
*Ejemplo: córrer → corro, corres, corre, correm, correu, corren*

**Verbos regulares -IR:**
Raíz + -o, -s, -∅, -im, -iu, -en
*Ejemplo: sortir → surto, surts, surt, sortim, sortiu, surten*

**Verbos irregulares** tienen formas especiales de conjugación.
        '''
    },
    'indefinit': {
        'title': 'Pretérito Indefinido (Pretèrit Indefinit)',
        'content': '''
**Verbos regulares -AR:**
Raíz + -ì, -ares, -à, -àrem, -àreu, -aren
*Ejemplo: parlar → parlì, parlares, parlà, parlàrem, parlàreu, parlaren*

**Verbos regulares -RE:**
Raíz + -í, -eres, -é, -érem, -éreu, -eren
*Ejemplo: córrer → corrí, correres, corré, corrérem, corréreu, correren*

**Verbos regulares -IR:**
Raíz + -í, -ires, -í, -írem, -íreu, -iren
*Ejemplo: sortir → sortí, sortires, sortí, sortírem, sortíreu, sortiren*

**Uso:** Acciones completadas en el pasado.
        '''
    },
    'futur': {
        'title': 'Futuro (Futur)',
        'content': '''
**Todos los verbos regulares:**
Infinitivo + -é, -às, -à, -em, -eu, -an
*Ejemplo: parlar → parlaré, parlaràs, parlarà, parlarem, parlareu, parlaran*
*Ejemplo: córrer → correré, correràs, correrà, correrem, correreu, correran*
*Ejemplo: sortir → sortiré, sortiràs, sortirà, sortirem, sortireu, sortiran*

**Raíces irregulares:**
tenir → tindr-, fer → far-, dir → dir-, voler → voldr-, etc.

**Uso:** Acciones en el futuro, planes, suposiciones.
        '''
    },
    'imperfet': {
        'title': 'Imperfecto (Imperfet)',
        'content': '''
**Verbos -AR:**
Raíz + -ava, -aves, -ava, -àvem, -àveu, -aven
*Ejemplo: parlar → parlava, parlaves, parlava, parlàvem, parlàveu, parlaven*

**Verbos -RE/-IR:**
Raíz + -ia, -ies, -ia, -íem, -íeu, -ien
*Ejemplo: córrer → corria, corries, corria, corríem, corríeu, corrien*
*Ejemplo: sortir → sortia, sorties, sortia, sortíem, sortíeu, sortien*

**Excepciones:** ser (era...), anar (anava...), veure (veia...)

**Uso:** Acciones repetidas en el pasado, descripciones.
        '''
    }
}

# Inicialización del estado de la sesión con guardado automático
def init_session_state():
    # Inicialización de variables principales
    if 'current_verb' not in st.session_state:
        st.session_state.current_verb = ''
    if 'current_pronoun_index' not in st.session_state:
        st.session_state.current_pronoun_index = 0
    if 'current_tense' not in st.session_state:
        st.session_state.current_tense = 'present'
    if 'is_revealed' not in st.session_state:
        st.session_state.is_revealed = False
    if 'recent_combinations' not in st.session_state:
        st.session_state.recent_combinations = []
    
    # Inicialización de estadísticas con autoguardado
    if 'stats' not in st.session_state:
        st.session_state.stats = {
            'total': 0,
            'today': 0,
            'last_date': datetime.date.today().isoformat(),
            'combinations': {},
            'session_start': datetime.datetime.now().isoformat()
        }

def update_stats():
    """Actualización de estadísticas considerando un nuevo día"""
    today = datetime.date.today().isoformat()
    if st.session_state.stats['last_date'] != today:
        st.session_state.stats['today'] = 0
        st.session_state.stats['last_date'] = today

def save_progress():
    """Guardado automático del progreso en session_state"""
    # En Streamlit session_state se guarda automáticamente en la sesión del navegador
    # Adicionalmente podemos mostrar notificación de guardado
    pass

def get_next_combination():
    """Obtención de la siguiente combinación verbo-pronombre"""
    attempts = 0
    while attempts < 100:
        verb = random.choice(list(VERBS.keys()))
        pronoun_index = random.randint(0, 5)
        combination = f"{verb}-{pronoun_index}-{st.session_state.current_tense}"
        
        if combination not in st.session_state.recent_combinations or attempts > 50:
            if verb in CONJUGATIONS[st.session_state.current_tense]:
                st.session_state.recent_combinations.append(combination)
                if len(st.session_state.recent_combinations) > 20:
                    st.session_state.recent_combinations.pop(0)
                return verb, pronoun_index
        attempts += 1
    
    # Fallback
    available_verbs = list(CONJUGATIONS[st.session_state.current_tense].keys())
    return available_verbs[0], 0

def next_verb():
    """Transición al siguiente verbo"""
    verb, pronoun_index = get_next_combination()
    st.session_state.current_verb = verb
    st.session_state.current_pronoun_index = pronoun_index
    st.session_state.is_revealed = False
    save_progress()

def reveal_answer():
    """Mostrar respuesta y actualizar estadísticas"""
    if not st.session_state.is_revealed:
        st.session_state.is_revealed = True
        
        # Actualizamos estadísticas
        st.session_state.stats['total'] += 1
        st.session_state.stats['today'] += 1
        
        combination = f"{st.session_state.current_verb}-{st.session_state.current_pronoun_index}-{st.session_state.current_tense}"
        if combination not in st.session_state.stats['combinations']:
            st.session_state.stats['combinations'][combination] = 0
        st.session_state.stats['combinations'][combination] += 1
        
        save_progress()

def reset_progress():
    """Reiniciar progreso"""
    st.session_state.stats = {
        'total': 0,
        'today': 0,
        'last_date': datetime.date.today().isoformat(),
        'combinations': {},
        'session_start': datetime.datetime.now().isoformat()
    }
    st.session_state.recent_combinations = []
    save_progress()

# Aplicación principal
def main():
    init_session_state()
    update_stats()
    
    # Título
    st.title("🏴󠁥󠁳󠁣󠁴󠁿 Entrenador de Verbos Catalanes")
    st.caption("Aprende conjugaciones de verbos catalanes en diferentes tiempos")
    
    # Estadísticas en formato compacto
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Total", st.session_state.stats['total'])
    with col2:
        st.metric("🎯 Hoy", st.session_state.stats['today'])
    with col3:
        unique_combinations = len(st.session_state.stats['combinations'])
        st.metric("✨ Únicos", unique_combinations)
    
    # Control
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reiniciar progreso", use_container_width=True):
            reset_progress()
            st.success("¡Progreso reiniciado!")
            st.rerun()
    
    with col2:
        if st.button("🎯 Siguiente verbo", key="next_main", use_container_width=True):
            next_verb()
            st.rerun()
    
    # Selección de tiempo
    st.subheader("🕒 Selecciona el tiempo:")
    tense_names = {
        'present': 'Presente',
        'indefinit': 'Pretérito Indefinido', 
        'futur': 'Futuro',
        'imperfet': 'Imperfecto'
    }
    
    selected_tense = st.selectbox(
        "Tiempo:",
        options=list(tense_names.keys()),
        format_func=lambda x: tense_names[x],
        index=list(tense_names.keys()).index(st.session_state.current_tense),
        label_visibility="collapsed"
    )
    
    if selected_tense != st.session_state.current_tense:
        st.session_state.current_tense = selected_tense
        next_verb()
        st.rerun()
    
    # Inicializamos verbo si es necesario
    if not st.session_state.current_verb:
        next_verb()
    
    # Tarjeta con verbo
    st.markdown("---")
    
    # Verificamos que el verbo existe en el tiempo seleccionado
    if (st.session_state.current_verb in CONJUGATIONS[st.session_state.current_tense] and
        st.session_state.current_verb in VERBS):
        
        verb_info = VERBS[st.session_state.current_verb]
        
        # Tarjeta del verbo con diseño bonito
        st.markdown(f"""
        <div class="verb-card">
            <div class="verb-title">{st.session_state.current_verb}</div>
            <div class="verb-translation">{verb_info['translation']}</div>
            <div style="font-size: 1rem; opacity: 0.8; margin-bottom: 1rem;">
                {tense_names[st.session_state.current_tense]}
            </div>
            <div class="pronoun-display">
                {PRONOUNS[st.session_state.current_pronoun_index]}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Botón para mostrar respuesta o respuesta
        if not st.session_state.is_revealed:
            if st.button("🔍 Mostrar respuesta", key="reveal", use_container_width=True, type="primary"):
                reveal_answer()
                st.rerun()
        else:
            # Mostramos respuesta
            conjugation = CONJUGATIONS[st.session_state.current_tense][st.session_state.current_verb][st.session_state.current_pronoun_index]
            
            st.markdown(f"""
            <div class="answer-display">
                ✅ {conjugation}
            </div>
            """, unsafe_allow_html=True)
            
            # Botón del siguiente verbo
            if st.button("➡️ Siguiente verbo", key="next_after_reveal", use_container_width=True, type="primary"):
                next_verb()
                st.rerun()
    else:
        st.error("❌ Error: verbo no encontrado en la base de datos")
        if st.button("🔄 Obtener nuevo verbo", use_container_width=True):
            next_verb()
            st.rerun()
    
    # Reglas de conjugación
    st.markdown("---")
    with st.expander("📚 Reglas de conjugación"):
        rule = RULES[st.session_state.current_tense]
        st.markdown(f"### {rule['title']}")
        st.markdown(rule['content'])
    
    # Instrucciones de uso
    with st.expander("ℹ️ Cómo usar"):
        st.markdown("""
        ### 📱 Pasos simples:
        1. **Selecciona el tiempo** para estudiar
        2. **Mira el verbo** y el pronombre  
        3. **Piensa en la conjugación correcta**
        4. **Presiona "Mostrar respuesta"** para verificar
        5. **Pasa al siguiente verbo**
        
        ### 💾 Progreso:
        - Tu progreso se guarda automáticamente en el navegador
        - Las estadísticas se actualizan en tiempo real
        - Los datos se conservan entre sesiones
        
        ### 📱 Uso móvil:
        - La aplicación está optimizada para dispositivos móviles
        - Botones ampliados para fácil pulsación
        - Diseño adaptativo para diferentes pantallas
        """)
    
    # Información sobre guardado (en pie de página)
    st.markdown("---")
    st.caption("💾 El progreso se guarda automáticamente en tu navegador")

if __name__ == "__main__":
    main()