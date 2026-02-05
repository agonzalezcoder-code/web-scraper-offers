def filter_best_offers(offers):
    keywords = ["python", "developer"]
    return [
        offer for offer in offers
        if any(word in offer["title"].lower() for word in keywords)
    ]
