// Fetch /api/products and display them on the page
async function fetchProducts() {
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

    // Convert createdOn from Unix Timestamp to DD-MM HH:MM format.
    let listingDate = new Date(product.createdOn * 1000).toLocaleString("en-UK", {
      day: "2-digit",
      month: "long",
      hour: "2-digit",
      minute: "2-digit"
    });

    listing.innerHTML = `<h3>${product.name}</h3>
                          <p>${product.description}</p>
                          <p>Price: ${price}</p>
                          <p>Amount: ${units}</p>
                          <p>Seller: ${product.sellername}</p>
                          <p>Listed: ${listingDate} </p>`
                          // Check if Seller is the logged in user, if so, add a delete button to the listing.
                          if (product.sellerid == signedInUserId) {
                            // Button to delete the listing
                            let deleteButton = document.createElement('button');
                            deleteButton.classList.add('actionButton');
                            deleteButton.innerText = 'Remove Listing';

                            deleteButton.addEventListener('click', async () => {
                              // Remove Listing Logic
                              console.log(`Deleting listing with LID: ${product.id}`);
                            });

                            listing.appendChild(deleteButton);
                          } else if (product.units > 0) {
                            // Button to buy the listing
                            let buyButton = document.createElement('button');
                            buyButton.classList.add('actionButton');
                            buyButton.innerText = 'Buy Listing';

                            buyButton.addEventListener('click', () => {
                              // Buy Listing Logic
                              let sellerId = product.sellerid;
                              console.log(`Attempting to buy ${product.name} from ${product.sellername} (SID: ${sellerId}  LID: ${product.id})`);
                            });

                            listing.appendChild(buyButton);
                          } else {
                            let soldOutText = document.createElement('button');
                            soldOutText.classList.add('soldOutButton');
                            soldOutText.innerText = 'Sold Out';
                            listing.appendChild(soldOutText);
                          }
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
  return loggedInUser.id
}

window.addEventListener('DOMContentLoaded', fetchProducts);