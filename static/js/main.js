

function toggleFiltersDisplay(){

    const filtersSec = document.getElementById('filters')
    if (filtersSec.classList.contains("hidden")){
        filtersSec.classList.remove("hidden")
    } else {
        filtersSec.classList.add("hidden")
    }

}
