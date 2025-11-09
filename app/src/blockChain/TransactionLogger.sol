// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TransactionLogger {
    struct Transaction {
        string id;            // Mã donation / transaction từ BE
        address sender;       // Ví commit
        uint256 amount;       // Số tiền (ví dụ theo wei)
        string status;        // success / failed
        uint256 timestamp;    // thời điểm ghi
        string note;          // ghi chú ngắn, VD: "Donation for campaign 123"
    }

    mapping(string => Transaction) private transactions;

    event TransactionCommitted(string id, address sender, uint256 amount, string status, string note);

    function commitTransaction(
        string memory id,
        uint256 amount,
        string memory status,
        string memory note
    ) public {
        require(bytes(transactions[id].id).length == 0, "Transaction already exists");

        transactions[id] = Transaction({
            id: id,
            sender: msg.sender,
            amount: amount,
            status: status,
            timestamp: block.timestamp,
            note: note
        });

        emit TransactionCommitted(id, msg.sender, amount, status, note);
    }

    function getTransactionById(string memory id)
        public
        view
        returns (Transaction memory)
    {
        require(bytes(transactions[id].id).length != 0, "Transaction not found");
        return transactions[id];
    }
}
