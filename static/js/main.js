// Search overlay
function openSearch(){
  const o=document.getElementById('search-overlay');
  o.classList.add('active');
  setTimeout(()=>document.getElementById('search-input').focus(),100);
  document.body.style.overflow='hidden';
}

function closeSearchBtn(){
  document.getElementById('search-overlay').classList.remove('active');
  document.body.style.overflow='';
}

function closeSearch(e){
  if(e.target===document.getElementById('search-overlay')) closeSearchBtn();
}

document.addEventListener('keydown',function(e){
  if(e.key==='Escape') closeSearchBtn();
});

// Mobile menu
function toggleMobile(){
  const m=document.getElementById('mobile-menu');
  m.classList.toggle('active');
}

const socialBar = document.getElementById("socialBar");
const socialToggle = document.getElementById("socialToggle");

socialToggle.addEventListener("click", () => {

    socialBar.classList.toggle("collapsed");
    const icon = socialToggle.querySelector("i");

    if (socialBar.classList.contains("collapsed")) {
        icon.classList.remove("fa-chevron-left");
        icon.classList.add("fa-chevron-right");

    } else {
        icon.classList.remove("fa-chevron-right");
        icon.classList.add("fa-chevron-left");
    }
});