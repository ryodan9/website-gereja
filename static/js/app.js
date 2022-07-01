// const container = document.querySelector('.container-ibadah')
// const kursi = document.querySelector('.row-kursi .kursi:not(.ditempati)')
// var element = document.getElementById('pesan')
// var kursis = document.querySelector('')

// populateUI()

// function populateUI(){
//     const kursiDipilih = JSON.parse(localStorage.getItem('kursiDipilih'))

//     if(kursiDipilih !== null && kursiDipilih.length > -1){
//         kursi.forEach((kursi, index) => {
//             if (kursiDipilih.indexOf(index) > -1){
//                 kursi.classList.add('dipilih');
//             }
//         });
//     }
// }

// container.addEventListener('click', e => {
//     if(
//         e.target.classList.contains('kursi')&&
//         !e.target.classList.contains('ditempati')
//     ){
//         e.target.classList.toggle('dipilih')
//     }
// });

function daftar()
{
    kursi = document.querySelector('.kursi');
    option = document.querySelector('option');
    kursi.classList.add('ditempati');
}