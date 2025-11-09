import os, json
from web3 import Web3

class SmartContractService:
    def __init__(self):
        provider_url = os.getenv("WEB3_PROVIDER_URL", "http://127.0.0.1:8545")
        private_key = os.getenv("PRIVATE_KEY")
        contract_address = os.getenv("CONTRACT_ADDRESS")

        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.account = self.web3.eth.account.from_key(private_key)

        with open("artifacts/TransactionLogger.json") as f:
            artifact = json.load(f)

        self.contract = self.web3.eth.contract(
            address=contract_address,
            abi=artifact["abi"]
        )

    def commit_transaction(self, id, amount, status, note):
        nonce = self.web3.eth.get_transaction_count(self.account.address)
        tx = self.contract.functions.commitTransaction(
            id, int(amount), status, note
        ).build_transaction({
            "from": self.account.address,
            "nonce": nonce,
            "gas": 3000000,
            "gasPrice": self.web3.to_wei("5", "gwei"),
        })
        signed_tx = self.account.sign_transaction(tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.web3.to_hex(tx_hash)
