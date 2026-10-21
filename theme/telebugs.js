/* Small enhancements to mdBook's native navigation. */
(() => {
    const appearanceMenu = document.getElementById("mdbook-theme-list");
    appearanceMenu.addEventListener("click", (event) => {
        if (event.target.closest("button.theme")) {
            document.getElementById("mdbook-theme-toggle").click();
        }
    });

    const activeLink = document.querySelector(".chapter a.active");
    const chapterNumber = activeLink?.querySelector("strong")?.textContent.trim().replace(/\.$/, "");
    if (chapterNumber) {
        const label = document.querySelector(".chapter-label");
        const formattedNumber = chapterNumber.includes(".") ? chapterNumber : chapterNumber.padStart(2, "0");
        if (label) label.textContent = `Chapter ${formattedNumber}`;
        activeLink.setAttribute("aria-current", "page");
    }

    const contentsToggle = document.getElementById("mdbook-sidebar-toggle");
    contentsToggle.addEventListener("click", () => {
        document.getElementById("mdbook-sidebar-toggle-anchor").click();
    });

    document.querySelector(".contents-close")?.addEventListener("click", () => {
        contentsToggle.click();
        contentsToggle.focus();
    });

    const contentsCheckbox = document.getElementById("mdbook-sidebar-toggle-anchor");
    const contents = document.getElementById("mdbook-sidebar");
    const mobileLayout = window.matchMedia("(max-width: 1079px)");
    const readingPage = document.getElementById("mdbook-page-wrapper");
    const masthead = document.querySelector(".site-masthead");
    const syncContentsHeight = () => {
        if (mobileLayout.matches || !contentsCheckbox.checked) return;
        // Fill the window both below the masthead and once the contents stick.
        const top = Math.max(20, contents.getBoundingClientRect().top);
        contents.style.setProperty("--contents-top", `${top}px`);
    };
    const syncContents = (event) => {
        contents.inert = !contentsCheckbox.checked;
        const drawerOpen = contentsCheckbox.checked && mobileLayout.matches;
        readingPage.inert = drawerOpen;
        masthead.inert = drawerOpen;
        // Keep checkbox activation and mdBook's inline visibility in sync.
        if (contentsCheckbox.checked) contents.style.removeProperty("display");
        syncContentsHeight();
        if (drawerOpen && event) document.querySelector(".contents-close").focus();
    };
    contentsCheckbox.addEventListener("change", syncContents);
    mobileLayout.addEventListener("change", syncContents);
    window.addEventListener("scroll", syncContentsHeight, { passive: true });
    window.addEventListener("resize", syncContentsHeight);
    syncContents();

    contents.addEventListener("click", (event) => {
        if (!mobileLayout.matches || !contentsCheckbox.checked ||
            event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey ||
            !event.target.closest("a[href]")) return;
        // In-page section links must reveal the reading page as well.
        contentsToggle.click();
        document.getElementById("mdbook-content").focus({ preventScroll: true });
    });

    contents.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && mobileLayout.matches && contentsCheckbox.checked) {
            contentsToggle.click();
            contentsToggle.focus();
        }
    });

    // mdBook's fold controls are anchors without an href. Give them button
    // semantics and the same keyboard interaction as the contents toggle.
    document.querySelectorAll(".chapter-fold-toggle").forEach((toggle) => {
        const chapter = toggle.closest(".chapter-item");
        const chapterLink = toggle.previousElementSibling;
        const updateExpanded = () => toggle.setAttribute("aria-expanded", chapter.classList.contains("expanded"));
        toggle.setAttribute("role", "button");
        toggle.setAttribute("aria-label", `Toggle ${chapterLink.textContent.trim()} sections`);
        updateExpanded();
        toggle.addEventListener("click", updateExpanded);
        toggle.addEventListener("keydown", (event) => {
            if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                toggle.click();
            }
        });
    });
})();
