import removeListing from "./removeListing.js";
import displayProducts from "./displayProducts.js";

// Fetch /api/products and display them on the page
export default async function fetchProducts() {
  try {
    const container = document.querySelector('.listing-container');
    container.classList.add("loading")
    container.innerHTML = ''; // Clear existing listings
    const response = await fetch('/api/products');
    let animFinished = false

    if (!response.ok) {
      container.innerText = await response.text();
      container.classList.remove("loading")
      throw new Error('Network response was not ok');
    }

    const products = await response.json();
    const signedInUserId = await getLoggedIn();

    // Show Loading animation for 1 second.
    setTimeout(() => {
      container.classList.remove("loading")
      console.log(products)
      displayProducts(container, products, signedInUserId);
    }, 1000);

  } catch (error) {
    console.error('Error fetching products:', error);
  }
}

// Helper function to get the logged in user.
async function getLoggedIn() {
  let loggedInUser = await fetch('/api/logged_in_user');
  if (!loggedInUser.ok) {
    throw new Error('Network response was not ok');
  }
  loggedInUser = await loggedInUser.json();
  return loggedInUser.id
}