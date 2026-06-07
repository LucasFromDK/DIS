let pid = new URLSearchParams(window.location.search).get('pid');
let amount = new URLSearchParams(window.location.search).get('amount');

async function getProduct() {
	const response = await fetch(`/api/product(${pid})`);
	if (!response.ok) {
		throw new Error('Network response was not ok');
	}
	const product = await response.json();
	return product;
}

async function setProductCheckout() {
	const product = await getProduct();
	if (window.location.pathname.endsWith('buy-listing')) {
		if (product.price === 0) {
			document.getElementById('product-info').innerHTML = `Fill out the form below to purchase 1 to ${product.units} units of ${product.name} for free.`;
			return;
		} else {
			document.getElementById('product-info').innerHTML = `Fill out the form below to purchase 1 to ${product.units} units of ${product.name} for ${product.price / 100} DKK each.`;
		}
	} else if (window.location.pathname.endsWith('success')) {
		if (product.price === 0) {
			document.getElementById('success-info').innerHTML = `Thank you for your purchase! <br> You have successfully purchased ${amount}x ${product.name} for free.`;
			return;
		} else {
			document.getElementById('success-info').innerHTML = `Thank you for your purchase! <br> You have successfully purchased ${amount}x ${product.name} for ${product.price / 100} DKK each, for a total of ${(product.price * amount) / 100} DKK.`;
		}
	}
}

window.addEventListener('DOMContentLoaded', setProductCheckout);