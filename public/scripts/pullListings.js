// Fetch /api/products and display them on the page
async function fetchProducts() {
  try {
    const container = document.querySelector('.listing-container');
    container.classList.add("loading")
    container.innerHTML = ''; // Clear existing listings
    const response = await fetch('/api/products');
    if (!response.ok) {
      container.innerText = await response.text();
      container.classList.remove("loading")
      throw new Error('Network response was not ok');
    }
    const products = await response.json();
    const signedInUserId = await getLoggedIn();
    container.classList.remove("loading")
    console.log(products)
    displayProducts(container, products, signedInUserId);
  } catch (error) {
    console.error('Error fetching products:', error);
  }
}

function displayProducts(container, products, signedInUserId) {
  products.forEach(product => {
    const listing = document.createElement('div');
    listing.classList.add('listing');

    let price = new Intl.NumberFormat("da-DK", { style: "currency", currency: "DKK" }).format(
      product.price / 100
    );

    let units = new Intl.NumberFormat("da-DK").format(
      product.units
    );

    listing.innerHTML = `<h3>${product.name}</h3>
                          <p>${product.description}</p>
                          <p>Price: ${price}</p>
                          <p>Amount: ${units}</p>
                          <p>Seller: ${product.sellername}</p>`
                          // Check if Seller is the logged in user, if so, add a delete button to the listing.
                          if (product.sellerid == signedInUserId) {
                            // Button to delete the listing
                            let deleteButton = document.createElement('button');
                            deleteButton.classList.add('deleteButton');
                            deleteButton.innerText = 'Remove Listing';
                            deleteButton.addEventListener('click', async () => {
                              // Remove Listing Logic
                              let listingId = product.id;
                              console.log(`Deleting listing with id: ${listingId}`);
                            });
                            listing.appendChild(deleteButton);
                          };
    container.appendChild(listing);
  });
}

// Helper function to get the logged in user.
async function getLoggedIn() {
  let loggedInUser = await fetch('/api/logged_in_user');
  if (!loggedInUser.ok) {
    throw new Error('Network response was not ok');
  }
  loggedInUser = await loggedInUser.json();
  console.log(loggedInUser)
  return loggedInUser.id
}

window.addEventListener('DOMContentLoaded', fetchProducts);