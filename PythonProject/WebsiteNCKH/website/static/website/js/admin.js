document.getElementById("date").innerHTML = new Date().toDateString();

const search = document.getElementById('search'),
      searchBtn = document.getElementById('search-btn'),
      searchClose = document.getElementById('searchclose')
searchBtn.addEventListener('click', () =>{
   search.classList.add('show-search')
})
searchClose.addEventListener('click', () =>{
   search.classList.remove('show-search')
})