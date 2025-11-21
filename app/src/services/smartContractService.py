import os
import json
from web3 import Web3
from dotenv import load_dotenv
from app.src.models.commitTransaction import CommitTransaction

class SmartContractService:
    def __init__(self):
        load_dotenv()

        provider_url = os.getenv("WEB3_PROVIDER_URL")
        private_key = os.getenv("PRIVATE_KEY")
        contract_address = os.getenv("CONTRACT_ADDRESS")

        if not provider_url:
            raise ValueError("Missing WEB3_PROVIDER_URL in .env")

        if not private_key:
            raise ValueError("Missing PRIVATE_KEY in .env")

        if not contract_address:
            raise ValueError("Missing CONTRACT_ADDRESS in .env")

        # Connect Web3
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        if not self.web3.is_connected():
            raise ConnectionError(f"Cannot connect to RPC: {provider_url}")

        # Wallet signer
        self.account = self.web3.eth.account.from_key(private_key)
        self.wallet_address = self.account.address

        # Load ABI
        abi_path = os.path.join(
            os.path.dirname(__file__),
            "../resource/artifacts/TransactionLogger.json"
        )
        abi_path = os.path.abspath(abi_path)

        with open(abi_path, "r") as f:
            artifact = json.load(f)

        self.contract = self.web3.eth.contract(
            address=self.web3.to_checksum_address(contract_address),
            abi=artifact["abi"]
        )

    def commitTransaction(self, tx: CommitTransaction):

        # Build function call
        function_call = self.contract.functions.commitTransaction(
            tx.user_id,
            tx.campaign_id,
            tx.transaction_id,
            tx.amount,
            tx.status,
            tx.message
        )

        # Build transaction object
        transaction = function_call.build_transaction({
            "from": self.wallet_address,
            "nonce": self.web3.eth.get_transaction_count(self.wallet_address),
            "gas": 350000,
            "gasPrice": self.web3.eth.gas_price,
            "chainId": 11155111  # Sepolia chain ID
        })

        # Sign
        signed_tx = self.web3.eth.account.sign_transaction(transaction, self.account.key)

        # Send
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        return self.web3.to_hex(tx_hash)
