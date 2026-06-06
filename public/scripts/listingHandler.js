import removeListing from "./removeListing.js";
import fetchProducts from "./pullListings.js";
import displayUserListings from "./userListings.js";

window.addEventListener('DOMContentLoaded', () => {
	if (window.location.pathname.endsWith('index') || window.location.pathname.endsWith('/')) {
		fetchProducts('.listing-container');
	} else if (window.location.pathname.endsWith('account')) {
		displayUserListings('.listing-container');
	}
});

// Expose fetchProducts and removeListing to the global scope for use in HTML.
window.fetchProducts = fetchProducts;
window.removeListing = removeListing;