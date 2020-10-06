// Pisah ribuan dengan titik
function convertRupiah(x) {
    x = x.toString().replace('Rp', '')
    let parts = x.split(",");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    return 'Rp'+parts.join(",");
}
// update total harga 
function updateRupiah(element, value) {
    $(element).text(convertRupiah(value))
}

$('document').ready(function (){
    // init
    // convert semua harga ke format rupiah
    $(this).find(".convert-rupiah").each(function () {
        updateRupiah(this, $(this).text())
    });

})