<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
/* ===== RESET ===== */
html, body {
    margin: 0;
    padding: 0;
    height: 100%;
}

/* ===== BARRA DE PROGRESSO ===== */
#scroll-progress-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 6px; /* altura da barra */
    background-color: rgba(255, 255, 255, 0.1);
    z-index: 9999;
}

#scroll-progress-bar {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #ff0000, #ff4d4d);
    transition: width 0.05s linear;
}

/* ===== CONTEÚDO DE EXEMPLO ===== */
.content {
    padding: 40px;
    line-height: 1.8;
}
</style>
</head>

<body>

<!-- BARRA DE PROGRESSO -->
<div id="scroll-progress-container">
    <div id="scroll-progress-bar"></div>
</div>

<!-- CONTEÚDO -->
<div class="content">
    <h1>Página de Exemplo</h1>

    <p>Role a página para ver a barra preenchendo.</p>

    <!-- Simulação de página longa -->
    <p>Lorem ipsum dolor sit amet.</p>
    <p style="height: 3000px;"></p>
</div>

<script>
/* ===== SCRIPT DA BARRA DE PROGRESSO ===== */
window.addEventListener("scroll", () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;

    document.getElementById("scroll-progress-bar").style.width = scrollPercent + "%";
});
</script>

</body>
</html>
