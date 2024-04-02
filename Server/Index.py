from PIL import Image
import streamlit as st

im = Image.open("icon.png")
st.set_page_config(
    page_title="Riassunto circolari",
    page_icon=im,
)
st.markdown("""- **Presentazione del Progetto Pepper**
  - **(Circolare n. 291)**
  - **Date e Orario:** Sabato 2 marzo, dalle ore 9.00 alle 11.00
  - **Luogo:** Aula Magna
  - **Destinatari:** Studenti, Docenti, Genitori, Personale ATA
  - **Sommario degli argomenti:**
    - La circolare comunica la presentazione del Progetto Pepper, che coinvolgerà gli studenti iscritti nell'Attività Extracurricolare relativa e tutta la classe 5PE. Questi studenti saranno impegnati nella presentazione del progetto alle RSA locali e ad altre autorità.
    - L'evento si svolgerà in Aula Magna dalle ore 9.00 alle 11.00.
    - La presentazione del Progetto Pepper è stata aggiunta all'Agenda degli studenti partecipanti.
    - I professori coinvolti direttamente nell'evento saranno i proff. Camplani, Lione, Pellegrini, e Spandre. Ci saranno variazioni riguardanti la sostituzione dei professori Lione e Pellegrini (dalle 9.00 alle 11.00) e del prof. Spandre (dalle 10.00 alle 11.00).""")