// Carregar likes salvos
document.querySelectorAll(".like-btn").forEach(btn => {
    const id = btn.dataset.id;

    // Recupera estado salvo
    let savedLike = localStorage.getItem("like_" + id);
    let savedCount = localStorage.getItem("count_" + id) || 0;

    const countSpan = btn.querySelector(".like-count");
    countSpan.textContent = savedCount;

    if (savedLike === "1") {
        btn.classList.add("liked");
    }

    // Evento de clique
    btn.addEventListener("click", () => {
        let liked = btn.classList.contains("liked");
        let currentCount = parseInt(countSpan.textContent);

        if (!liked) {
            // Dá like
            btn.classList.add("liked");
            currentCount++;
            localStorage.setItem("like_" + id, "1");
        } else {
            // Remove o like
            btn.classList.remove("liked");
            currentCount--;
            localStorage.setItem("like_" + id, "0");
        }

        // Atualiza contador
        countSpan.textContent = currentCount;
        localStorage.setItem("count_" + id, currentCount);
    });
});
