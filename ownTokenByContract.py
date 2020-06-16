from decimal import Decimal
import json
import os

from web3 import Web3


# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/your_infura_access_token"))
priv_key = 'your_private_key'

DIR = os.path.dirname(__file__)

# USDC contract
file_path = os.path.join(DIR, './ERC20.json')
contract = json.loads(open(file_path).read())
ERC20_ABI = contract["abi"]
USDC_ADDR = Web3.toChecksumAddress('USDC_address')
USDCContract = w3.eth.contract(abi=ERC20_ABI, address=USDC_ADDR)

# Me
addr = Web3.toChecksumAddress("your_address")
nonce = w3.eth.getTransactionCount(addr)
print("my ETH balance:", Web3.fromWei(w3.eth.getBalance(addr), 'ether'))
print("my USDC balance:", Web3.fromWei(USDCContract.functions.balanceOf(addr).call(), 'Lovelace'))
print("my nonce:", nonce)

# OwnTokenByContract contract
file_path = os.path.join(DIR, './OwnTokenByContract.json')
contract = json.loads(open(file_path).read())
OWN_TOKEN_BY_CONTRACT = contract["abi"]
OWN_TOKEN_BY_CONTRACT_ADDR = Web3.toChecksumAddress('deployed_contract_address')
OwnTokenByContractContract = w3.eth.contract(abi=OWN_TOKEN_BY_CONTRACT, address=OWN_TOKEN_BY_CONTRACT_ADDR)
print("OTBC USDC balance:", Web3.fromWei(USDCContract.functions.balanceOf(OWN_TOKEN_BY_CONTRACT_ADDR).call(), 'Lovelace'))
# print(OwnTokenByContractContract.functions.owner().call())

# value = Web3.toWei(1, 'ether')
value = Web3.toWei(1, 'Lovelace')
# Approve OwnTokenByContract contract
unsigned_transaction = USDCContract.functions.approve(
    OWN_TOKEN_BY_CONTRACT_ADDR,
    value,
).buildTransaction({'gas': 1500000, 'gasPrice': Web3.toWei(5, 'gwei'), 'nonce': w3.eth.getTransactionCount(addr)})
signed = w3.eth.account.signTransaction(unsigned_transaction, priv_key)
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(receipt)

# transferFrom USDC
unsigned_transaction = OwnTokenByContractContract.functions.transferFrom(
    USDC_ADDR,
    value,
).buildTransaction({'gas': 1500000, 'gasPrice': Web3.toWei(5, 'gwei'), 'nonce': w3.eth.getTransactionCount(addr)})
signed = w3.eth.account.signTransaction(unsigned_transaction, priv_key)
print(signed)
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(receipt)
print("OTBC USDC balance:", Web3.fromWei(USDCContract.functions.balanceOf(OWN_TOKEN_BY_CONTRACT_ADDR).call(), 'Lovelace'))

# transfer USDC
value = value // 2
unsigned_transaction = OwnTokenByContractContract.functions.transfer(
    USDC_ADDR,
    value,
).buildTransaction({'gas': 1500000, 'gasPrice': Web3.toWei(5, 'gwei'), 'nonce': w3.eth.getTransactionCount(addr)})
signed = w3.eth.account.signTransaction(unsigned_transaction, priv_key)
print(signed)
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(receipt)

# approve USDC
value = value // 2
unsigned_transaction = OwnTokenByContractContract.functions.approve(
    USDC_ADDR,
    value,
).buildTransaction({'gas': 1500000, 'gasPrice': Web3.toWei(5, 'gwei'), 'nonce': w3.eth.getTransactionCount(addr)})
signed = w3.eth.account.signTransaction(unsigned_transaction, priv_key)
print(signed)
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(receipt)

# transferFrom OwnTokenByContract contract
value = value // 2
unsigned_transaction = USDCContract.functions.transferFrom(
    OWN_TOKEN_BY_CONTRACT_ADDR,
    addr,
    value,
).buildTransaction({'gas': 1500000, 'gasPrice': Web3.toWei(5, 'gwei'), 'nonce': w3.eth.getTransactionCount(addr)})
signed = w3.eth.account.signTransaction(unsigned_transaction, priv_key)
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(receipt)
