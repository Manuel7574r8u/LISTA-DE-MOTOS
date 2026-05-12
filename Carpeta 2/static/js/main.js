console.log("Terminal de Motos iniciada con éxito");
console.warn("Acceso de desarrollador detectado");

window.onload = function() {

    const titulo = document.querySelector("h1");
    titulo.style.color = "orange";

    // BOTÓN CAMBIO MODO
    document.getElementById("modoBtn").onclick = function() {
        document.body.classList.toggle("cambio-modo");
    };

    // BOTÓN TEMA
    const botonTema = document.getElementById("temaBtn");

    botonTema.addEventListener("click", function() {
        document.body.classList.toggle("tema-claro");

        if(document.body.classList.contains("tema-claro")){
            botonTema.textContent = "Modo oscuro";
        } else {
            botonTema.textContent = "Modo claro";
        }
    });

    // Selecciona el modal (ventana flotante)
    const modal = document.getElementById("modal");
    
    // Selecciona el texto donde se mostrará el nombre de la moto
    const texto = document.getElementById("textoModal");

    // Selecciona todos los artículos (todas las motos)
    document.querySelectorAll("article").forEach(moto => {

        // Cuando haces click en una moto
        moto.onclick = function(){
            
            // Coge el texto del h3 dentro de la moto
            texto.textContent = this.querySelector("h3").textContent;
            
            // Muestra el modal
            modal.style.display = "block";
        }

    });

    // Cuando haces click en la X
    document.getElementById("cerrar").onclick = function(){
        
        // Oculta el modal
        modal.style.display = "none";
    };

};

// FUNCIÓN FILTRO
function filtrar(tipo){
    // selecciona todas las motos (todos los article)
    const motos = document.querySelectorAll("article");

    motos.forEach(moto => {
        const texto = moto.textContent;

        if(tipo === "todas" || texto.includes(tipo)){
            // asegurar que la clase de oculto se quite
            moto.classList.remove('hidden-moto');
        } else {
            // ocultar mediante clase (no rompe el centrado)
            moto.classList.add('hidden-moto');
        }

    });
}
