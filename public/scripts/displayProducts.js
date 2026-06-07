export default async function displayProducts(container, products, signedInUserId) {
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

		if (product.price === 0) {
			price = 'Free';
		}

		listing.innerHTML = `<h3>${product.name}</h3>
                          <p>${product.description}</p>
                          <p>Price: ${price}</p>
                          <p>Amount: ${units}</p>
                          <p>Seller: ${product.sellername}</p>
                          <p>Listed: ${listingDate} </p>`
		// Check if Seller is the logged in user, if so, add a delete button to the listing.
		if (product.userid == signedInUserId) {
			// Button to delete the listing
			let deleteButton = document.createElement('button');
			deleteButton.classList.add('actionButton');
			deleteButton.innerText = 'Remove Listing';

			deleteButton.addEventListener('click', async () => {
				// Remove Listing Logic
				await removeListing(product.id);
			});

			listing.appendChild(deleteButton);
		} else if (product.units > 0) {
			// Button to buy the listing
			let buyButton = document.createElement('button');
			buyButton.classList.add('actionButton');
			buyButton.innerText = 'Buy Listing';

			buyButton.addEventListener('click', () => {
				// Buy Listing Logic
				window.location.href = `../buy-listing?pid=${product.id}`;
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