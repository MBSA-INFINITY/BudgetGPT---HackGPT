from db import users_collection
def handle_new_user(user_id):
    if user_details := users_collection.find_one({"user_id": user_id}, {"_id": 0}):
        return {"new_user": False}
    else:
        user_data = {
            "user_id": user_id,
            "balance": 0
        }
        users_collection.insert_one(user_data)
        return {"new_user": True}
    
def update_balance(user_id, transactions):
    amount = 0
    for transaction in transactions:
        if transaction.get("type").lower() == 'credit':
            amount+=transaction.get("cumulative_transaction_amount")
        else:
            amount-=transaction.get("cumulative_transaction_amount")
    users_collection.update_one({"user_id": user_id},{"$inc":{"balance": amount}})