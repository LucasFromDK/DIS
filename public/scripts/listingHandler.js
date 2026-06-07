import removeListing from "./removeListing.js";
import fetchProducts from "./pullListings.js";
import displayUserListings from "./userListings.js";

window.addEventListener('DOMContentLoaded', () => {
	if (window.location.pathname.endsWith('index') || window.location.pathname.endsWith('/')) {
		fetchProducts('.listing-container');
		console.log("Fetching products for marketplace listings.");
	} else if (window.location.pathname.endsWith('account')) {
		displayUserListings('.listing-container');
		console.log("Displaying user listings on account page.");
	}
});

// Expose fetchProducts and removeListing to the global scope for use in HTML.
window.fetchProducts = fetchProducts;
window.displayUserListings = displayUserListings;
window.removeListing = removeListing;