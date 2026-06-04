import removeListing from "./removeListing.js";
import fetchProducts from "./pullListings.js";

window.addEventListener('DOMContentLoaded', fetchProducts);

// Expose fetchProducts and removeListing to the global scope for use in HTML.
window.fetchProducts = fetchProducts;
window.removeListing = removeListing;