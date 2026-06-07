import displayUserListings from "./userListings.js";

export default async function removeListing(listingId) {
	let delistProduct = await fetch(`/api/products/delete(${listingId})`)
	if (!delistProduct.ok) {
		throw new Error('Network response was not ok');
	}
	// Check if Index or Account Page
	if (window.location.pathname === "/") {
		// Refresh Index Page Listings
		await fetchProducts(".listing-container");
	} else if (window.location.pathname === "/account") {
		// Refresh Account Page Listings
		await displayUserListings(".listing-container");
	}
}