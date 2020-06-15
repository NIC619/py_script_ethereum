from web3 import Web3


# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/your_infura_access_token"))
priv_key = 'your_private_key'

nonce = w3.eth.getTransactionCount("your_address")
unsigned_transaction = {
    'to': "contract_address",
    'gas': 1500000,
    'data': "tx data(if any)",
    'gasPrice': 10*10**9,
    'nonce': nonce,
    'chainId': 1
}

signed = w3.eth.account.signTransaction(unsigned_transaction, priv_key)
print(signed)

receipt = w3.eth.sendRawTransaction(signed.rawTransaction)
print(receipt)