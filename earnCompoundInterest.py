from decimal import Decimal
import json
import os

from web3 import Web3

# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/your_infura_access_token"))
priv_key = 'your_private_key'

DIR = os.path.dirname(__file__)

# CETHER ABI
file_path = os.path.join(DIR, './CETHER.json')
contract = json.loads(open(file_path).read())
CETHER_ABI = contract["abi"]
# CTOKEN ABI
file_path = os.path.join(DIR, './CTOKEN.json')
contract = json.loads(open(file_path).read())
CTOKEN_ABI = contract["abi"]

# DAI contract
file_path = os.path.join(DIR, './ERC20.json')
contract = json.loads(open(file_path).read())
ERC20_ABI = contract["abi"]
DAI_ADDR = Web3.toChecksumAddress('DAI_address')
DAIContract = w3.eth.contract(abi=ERC20_ABI, address=DAI_ADDR)

# USDC contract
file_path = os.path.join(DIR, './ERC20.json')
contract = json.loads(open(file_path).read())
USDC_ADDR = Web3.toChecksumAddress('USDC_address')
USDCContract = w3.eth.contract(abi=ERC20_ABI, address=USDC_ADDR)

# Me
addr = Web3.toChecksumAddress("your_address")
nonce = w3.eth.getTransactionCount(addr)
print("my ETH balance:", Web3.fromWei(w3.eth.getBalance(addr), 'ether'))
print("my DAI balance:", Web3.fromWei(DAIContract.functions.balanceOf(addr).call(), 'ether'))
print("my USDC balance:", Web3.fromWei(USDCContract.functions.balanceOf(addr).call(), 'ether'))
print("my nonce:", nonce)

# EarnCOMPOUND contract
file_path = os.path.join(DIR, './EarnCompoundInterest.json')
contract = json.loads(open(file_path).read())
EARN_COMPOUND_ABI = contract["abi"]
EARN_COMPOUND_ADDR = Web3.toChecksumAddress('deployed_contract_address')
EarnCOMPOUNDContract = w3.eth.contract(abi=EARN_COMPOUND_ABI, address=EARN_COMPOUND_ADDR)
print("ECOMPOUND ETH balance:", Web3.fromWei(w3.eth.getBalance(EARN_COMPOUND_ADDR), 'ether'))
print("ECOMPOUND DAI balance:", Web3.fromWei(DAIContract.functions.balanceOf(EARN_COMPOUND_ADDR).call(), 'ether'))
print("ECOMPOUND USDC balance:", Web3.fromWei(USDCContract.functions.balanceOf(EARN_COMPOUND_ADDR).call(), 'ether'))
# print(EarnCOMPOUNDContract.functions.owner().call())

# cEther contract
CETHER_ADDR = Web3.toChecksumAddress("CETHER_address")
CETHERContract = w3.eth.contract(abi=CETHER_ABI, address=CETHER_ADDR)
# supply_rate = CETHERContract.functions.supplyRatePerBlock().call()
# print("cEther supply rate:", supply_rate)
underlying_balance = CETHERContract.functions.balanceOfUnderlying(EARN_COMPOUND_ADDR).call()
print("ECOMPOUND Ether balance:", Decimal(underlying_balance / 10 ** 18))
balance = CETHERContract.functions.balanceOf(EARN_COMPOUND_ADDR).call()
print("ECOMPOUND cEther balance:", balance)
print("cEther exg. rate:", CETHERContract.functions.exchangeRateCurrent().call())
# cDAI contract
CDAI_ADDR = Web3.toChecksumAddress("CDAI_address")
CDAIContract = w3.eth.contract(abi=CTOKEN_ABI, address=CDAI_ADDR)
# supply_rate = CDAIContract.functions.supplyRatePerBlock().call()
# print("cDAI supply rate:", supply_rate)
underlying_balance = CDAIContract.functions.balanceOfUnderlying(EARN_COMPOUND_ADDR).call()
print("ECOMPOUND DAI balance:", Decimal(underlying_balance / 10 ** 18 ))
balance = CDAIContract.functions.balanceOf(EARN_COMPOUND_ADDR).call()
print("ECOMPOUND cDAI balance:", balance)
print("cDAI exg. rate:", CDAIContract.functions.exchangeRateCurrent().call())
# cUSDC contract
CUSDC_ADDR = Web3.toChecksumAddress("CUSDC_address")
CUSDCContract = w3.eth.contract(abi=CTOKEN_ABI, address=CUSDC_ADDR)
# supply_rate = CUSDCContract.functions.supplyRatePerBlock().call()
# print("cUSDC supply rate:", supply_rate)
underlying_balance = CUSDCContract.functions.balanceOfUnderlying(EARN_COMPOUND_ADDR).call()
print("ECOMPOUND USDC balance:", Decimal(underlying_balance / 10 ** 6 ))
balance = CUSDCContract.functions.balanceOf(EARN_COMPOUND_ADDR).call()
print("ECOMPOUND cUSDC balance:", balance)
print("cUSDC exg. rate:", CUSDCContract.functions.exchangeRateCurrent().call())

# mint cDAI with earnCompound contract
unsigned_transaction = EarnCOMPOUNDContract.functions.mintERC20(
    CDAI_ADDR,
    DAI_ADDR,
    DAIContract.functions.balanceOf(EARN_COMPOUND_ADDR).call(),
).buildTransaction({'gas': 1500000, 'gasPrice': Web3.toWei(5, 'gwei'), 'nonce': w3.eth.getTransactionCount(addr)})
signed = w3.eth.account.signTransaction(unsigned_transaction, priv_key)
print(signed)
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(receipt)
print("ECOMPOUND DAI balance:", Web3.fromWei(DAIContract.functions.balanceOf(EARN_COMPOUND_ADDR).call(), 'ether'))
balance = CDAIContract.functions.balanceOf(EARN_COMPOUND_ADDR).call()
print("ECOMPOUND cDAI balance:", balance)

# redeem cDAI with earnCompound contract
unsigned_transaction = EarnCOMPOUNDContract.functions.redeemERC20(
    CDAI_ADDR,
    CDAIContract.functions.balanceOf(EARN_COMPOUND_ADDR).call(),
).buildTransaction({'gas': 1500000, 'gasPrice': Web3.toWei(5, 'gwei'), 'nonce': w3.eth.getTransactionCount(addr)})
signed = w3.eth.account.signTransaction(unsigned_transaction, priv_key)
print(signed)
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(receipt)
print("ECOMPOUND DAI balance:", Web3.fromWei(DAIContract.functions.balanceOf(EARN_COMPOUND_ADDR).call(), 'ether'))
balance = CDAIContract.functions.balanceOf(EARN_COMPOUND_ADDR).call()
print("ECOMPOUND cDAI balance:", balance)

# mint cUSDC with earnCompound contract
unsigned_transaction = EarnCOMPOUNDContract.functions.mintERC20(
    CUSDC_ADDR,
    USDC_ADDR,
    USDCContract.functions.balanceOf(EARN_COMPOUND_ADDR).call(),
).buildTransaction({'gas': 1500000, 'gasPrice': Web3.toWei(5, 'gwei'), 'nonce': w3.eth.getTransactionCount(addr)})
signed = w3.eth.account.signTransaction(unsigned_transaction, priv_key)
print(signed)
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(receipt)
print("ECOMPOUND USDC balance:", Web3.fromWei(USDCContract.functions.balanceOf(EARN_COMPOUND_ADDR).call(), 'ether'))
balance = CUSDCContract.functions.balanceOf(EARN_COMPOUND_ADDR).call()
print("ECOMPOUND cUSDC balance:", balance)

# redeem cUSDC with earnCompound contract
unsigned_transaction = EarnCOMPOUNDContract.functions.redeemERC20(
    CUSDC_ADDR,
    CUSDCContract.functions.balanceOf(EARN_COMPOUND_ADDR).call(),
).buildTransaction({'gas': 1500000, 'gasPrice': Web3.toWei(5, 'gwei'), 'nonce': w3.eth.getTransactionCount(addr)})
signed = w3.eth.account.signTransaction(unsigned_transaction, priv_key)
print(signed)
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(receipt)
print("ECOMPOUND USDC balance:", Web3.fromWei(USDCContract.functions.balanceOf(EARN_COMPOUND_ADDR).call(), 'lovelace'))
balance = CUSDCContract.functions.balanceOf(EARN_COMPOUND_ADDR).call()
print("ECOMPOUND cUSDC balance:", balance)

# withdraw Dai
unsigned_transaction = EarnCOMPOUNDContract.functions.withdraw().buildTransaction({'gas': 1500000, 'gasPrice': Web3.toWei(5, 'gwei'), 'nonce': w3.eth.getTransactionCount(addr)})
signed = w3.eth.account.signTransaction(unsigned_transaction, priv_key)
print(signed)
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(receipt)
print("ECOMPOUND DAI balance:", Web3.fromWei(DAIContract.functions.balanceOf(EARN_COMPOUND_ADDR).call(), 'ether'))
print("my DAI balance:", Web3.fromWei(DAIContract.functions.balanceOf(addr).call(), 'ether'))

# Withdraw Ether
unsigned_transaction = EarnCOMPOUNDContract.functions.withdrawEther().buildTransaction({'gas': 1500000, 'gasPrice': Web3.toWei(5, 'gwei'), 'nonce': w3.eth.getTransactionCount(addr)})
signed = w3.eth.account.signTransaction(unsigned_transaction, priv_key)
print(signed)
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(receipt)
print("my ETH balance:", Web3.fromWei(w3.eth.getBalance(addr), 'ether'))
