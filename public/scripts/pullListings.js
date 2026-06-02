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
    container.classList.remove("loading")
    console.log(products)
    displayProducts(container, products);
  } catch (error) {
    console.error('Error fetching products:', error);
  }
}

function displayProducts(container, products) {
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
                          <p>Seller: ${product.sellername}</p>`;
    container.appendChild(listing);
  });
}

window.addEventListener('DOMContentLoaded', fetchProducts);