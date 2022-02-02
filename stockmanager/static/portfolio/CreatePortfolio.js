// Loek van Steijn
window.addEventListener("click", function(e){

	if (document.getElementById("form-portfolio").contains(e.target) || document.getElementById("create_portfolio").contains(e.target))
    {
  	    document.getElementById("form-portfolio").style.display = "block";
    }
    else
    {
  	    document.getElementById("form-portfolio").style.display = "none";
    }
});

window.addEventListener("click", function(e){

    if (document.getElementById("form-add-fund").contains(e.target) || document.getElementById("fundsa").contains(e.target))
    {
        document.getElementById("form-add-fund").style.display = "block";
    }
    else
    {
        document.getElementById("form-add-fund").style.display = "none";
    }
});

window.addEventListener("click", function(e){

    if (document.getElementById("form-remove-fund").contains(e.target) || document.getElementById("fundsr").contains(e.target))
    {
        document.getElementById("form-remove-fund").style.display = "block";
    }
    else
    {
        document.getElementById("form-remove-fund").style.display = "none";
    }
});

window.addEventListener("click", function(e){

    if (document.getElementById("form-add-reminder").contains(e.target) || document.getElementById("reminder").contains(e.target))
    {
        document.getElementById("form-add-reminder").style.display = "block";
    }
    else
    {
        document.getElementById("form-add-reminder").style.display = "none";
    }
});
