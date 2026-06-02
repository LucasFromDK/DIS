// Fetch /api/products and display them on the page
async function fetchProducts() {
  try {
    const response = await fetch('/api/products');
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const products = await response.json();
    console.log(products)
    displayProducts(products);
  } catch (error) {
    console.error('Error fetching products:', error);
  }
}

function displayProducts(products) {
  const container = document.querySelector('.listing-container');
  container.innerHTML = ''; // Clear existing listings
    products.forEach(product => {
    const listing = document.createElement('div');
    listing.classList.add('listing');
    listing.innerHTML = `<h3>${product.name}</h3>
                          <p>${product.description}</p>
                          <p>Price: ${product.price / 100} DKK</p>
                          <p>Amount: ${product.units}</p>
                          <p>Seller: ${product.sellername}</p>`;
    container.appendChild(listing);
  });
}

window.addEventListener('DOMContentLoaded', fetchProducts);