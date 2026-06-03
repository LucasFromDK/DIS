export default async function removeListing(listingId) {
    let delistProduct = await fetch(`/api/products/delete(${listingId})`)
    if (!delistProduct.ok) {
        throw new Error('Network response was not ok');
    }
    fetchProducts();
}