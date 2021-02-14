class DatabaseConfig:
    MONGO_URL = "mongodb://localhost:27017/"
    DATABASE_NAME = "orderbookdb"
    ORDER_BOOK_COL = "orders"
    TRANSACTION_COL = "transactions"
    MAX_POOLING = 100  # Connection-Pool/DB replica
    TIME_OUT = 3 * 1000  # 3 sec
    USER_NAME = ""
    PASSWORD = "SOME TOKEN"


