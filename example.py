from src.masks import get_mask_account, get_mask_card_number

card = "7000792289606361"
account = "73654108430135874305"

print(get_mask_card_number(card))  # 7000 79** **** 6361
print(get_mask_account(account))  # **4305
