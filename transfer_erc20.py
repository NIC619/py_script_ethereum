import json
import os

from web3 import Web3


# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/your_infura_access_token"))
priv_key = 'your_private_key'

DIR = os.path.dirname(__file__)
file_path = os.path.join(DIR, './ERC20.json')
contract = json.loads(open(file_path).read())
ERC20_ABI = contract["abi"]
contract = w3.eth.contract(abi=ERC20_ABI, address=DAI_ADDR)

receiver = "receiver_address"
amount = "receive token amount"
unsigned_transaction = USDCContract.functions.approve(receiver, amount).buildTransaction(
    {
        'gas': 300000,
        'gasPrice': Web3.toWei(5, 'gwei'),
        'nonce': w3.eth.getTransactionCount(Web3.toChecksumAddress("your_address")),
    }
)
print(unsigned_transaction)

signed = w3.eth.account.signTransaction(unsigned_transaction, priv_key)
print(signed)

tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(receipt)