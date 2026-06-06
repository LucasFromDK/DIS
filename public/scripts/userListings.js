import { getLoggedIn } from "./pullListings.js";
import displayProducts from "./displayProducts.js";

// Get Products using pullListings and display them using displayProducts but only those that belong to the logged in user.
export default async function displayUserListings(container) {
	try {
		const containerElement = document.querySelector(container);
		containerElement.classList.add("loading")
		containerElement.innerHTML = '';
		const response = await fetch('/api/products');

		if (!response.ok) {
			containerElement.innerText = await response.text();
			containerElement.classList.remove("loading")
			throw new Error('Network response was not ok');
		}
		const products = await response.json();
		const signedInUserId = await getLoggedIn();
		// Show Loading animation for 1 second.
		setTimeout(() => {
			containerElement.classList.remove("loading")
			const userProducts = products.filter(product => product.sellerid === signedInUserId);
			displayProducts(containerElement, userProducts, signedInUserId);
		}, 1000);
	} catch (error) {
		console.error('Error fetching products:', error);
	}
}