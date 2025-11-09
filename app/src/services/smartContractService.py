import os
import json
from web3 import Web3
from dotenv import load_dotenv
from app.src.models.commitTransaction import CommitTransaction

class SmartContractService:
    def __init__(self):
        load_dotenv()

        provider_url = os.getenv("WEB3_PROVIDER_URL", "http://127.0.0.1:8545")
        private_key = os.getenv("PRIVATE_KEY")
        contract_address = os.getenv("CONTRACT_ADDRESS")

        if not private_key:
            raise ValueError("Missing PRIVATE_KEY in environment variables")

        if not contract_address:
            raise ValueError("Missing CONTRACT_ADDRESS in environment variables")

        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        if not self.web3.is_connected():
            raise ConnectionError(f"Cannot connect to Web3 provider: {provider_url}")

        self.account = self.web3.eth.account.from_key(private_key)

        abi_path = os.path.join(os.path.dirname(__file__), "../resource/artifacts/TransactionLogger.json")
        abi_path = os.path.abspath(abi_path)

        with open(abi_path, "r") as f:
            artifact = json.load(f)

        self.contract = self.web3.eth.contract(
            address=self.web3.to_checksum_address(contract_address),
            abi=artifact["abi"]
        )

    def commitTransaction(self, commitTx: CommitTransaction):
        nonce = self.web3.eth.get_transaction_count(self.account.address)

        tx = self.contract.functions.commitTransaction(
            *commitTx.toSmartContractArgs()
        ).build_transaction({
            "from": self.account.address,
            "nonce": nonce,
            "gas": 3000000,
            "gasPrice": self.web3.to_wei("5", "gwei"),
        })

        signed_tx = self.account.sign_transaction(tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        return self.web3.to_hex(tx_hash)
