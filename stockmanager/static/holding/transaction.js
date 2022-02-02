// Loek van Steijn

// Makes the forms for buying/selling/adding funds/removing funds etc appear on click and stops transactions of negative cash or orders
window.addEventListener("click", function(e){
	if (document.getElementById("transaction_buy").contains(e.target) || document.getElementById("Buy").contains(e.target))
    {
  	    document.getElementById("transaction_buy").style.display = "block";
    }
    else
    {
  	    document.getElementById("transaction_buy").style.display = "none";
    }
	if (document.getElementById("transaction_sell").contains(e.target) || document.getElementById("Sell").contains(e.target))
    {
  	    document.getElementById("transaction_sell").style.display = "block";
    }
    else
    {
  	    document.getElementById("transaction_sell").style.display = "none";
    }
});

transactionb.addEventListener("click", () => {
	if (document.getElementById("numberb").value <= 0)
	{
		event.preventDefault()
	}
	if (document.getElementById("aprice").value <= 0)
	{
		event.preventDefault()
	}
});

transactions.addEventListener("click", () => {
	if (document.getElementById("numbers").value <= 0)
	{
		event.preventDefault()
	}
	if (document.getElementById("bprice").value <= 0)
	{
		event.preventDefault()
	}
});
