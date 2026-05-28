document.addEventListener("DOMContentLoaded", () => {
	const ui = {
		actions: {
			backToTop: document.getElementById("backToTop"),
		},
	};

	initBackToTop(); // Trigger the back-to-top button functionality

	function initBackToTop() {
		ui.actions.backToTop.addEventListener("click", function () {
			window.scrollTo({
				top: 0,
				behavior: "smooth",
			});
		});
	}
});