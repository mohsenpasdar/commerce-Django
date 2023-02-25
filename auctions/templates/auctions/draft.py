# Check if the listing is closed:
    if listing.status == 'closed':
        if request.user == listing.winner:
            winner_message = 'Congratulations! You have won this auction.'
        elif (request.user == listing.seller) and listing.winner:
            winner_message = f"The auction has ended and {listing.winner.username} has won the auction with a bid of {highest_bid}!"
        elif (request.user != listing.seller) and listing.winner:
            winner_message = f'This auction has been won by {listing.winner.username}.'
        elif not listing.winner:
            winner_message = "The auction has ended but there were no bidders."
        else: 
            winner_message = None        
        return render(request, 'auctions/listing.html', {'listing': listing, 'winner_message': winner_message})