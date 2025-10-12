document.addEventListener("DOMContentLoaded", function () {

    if (typeof gsap !== "undefined") {
        gsap.from("form", { opacity: 0, y: -50, duration: 0.8, ease: "power2.out" });
        gsap.from("h1", { opacity: 0, y: -30, duration: 0.8, delay: 0.2 });

        const videoCards = document.querySelectorAll(".video-card");
        if (videoCards.length) {
            gsap.from(videoCards, { opacity: 0, y: 50, stagger: 0.1, duration: 0.6, ease: "power2.out" });
        }
    }

    const moodSelect = document.getElementById("mood");
    if (moodSelect) {
        moodSelect.addEventListener("change", function () {
            gsap.from(this, { backgroundColor: "#ffeb3b", duration: 0.4, repeat: 1, yoyo: true });
        });
    }

    const queryInput = document.getElementById("query");
    if (queryInput) {
        queryInput.addEventListener("focus", function () { gsap.to(this, { borderColor: "#2196f3", duration: 0.3 }); });
        queryInput.addEventListener("blur", function () { gsap.to(this, { borderColor: "#ccc", duration: 0.3 }); });
    }
});
