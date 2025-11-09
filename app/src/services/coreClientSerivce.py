class CoreClientSerivce:
    def handleTransaction(self, tx):
        import random
        if random.random() > 0.1:
            return {"success": True}
        return {"success": False, "error": "Simulated network error"}
