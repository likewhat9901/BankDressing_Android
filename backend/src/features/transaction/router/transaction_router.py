from fastapi import APIRouter, Depends

from src.features.transaction.model.transaction import TransactionQuery, TransactionUpdate, TransactionListResponse
from src.features.transaction.service.transaction_service import fetch_transactions_data, modify_transaction


transaction_router = APIRouter(prefix="/transaction", tags=["거래내역"])


@transaction_router.get("/")
def get_transactions(query: TransactionQuery = Depends()) -> TransactionListResponse:
    """거래내역 목록 조회"""
    data_list, total_count = fetch_transactions_data(query)

    return TransactionListResponse(
        transactions=data_list,
        total_count=total_count,
        has_more=query.offset + len(data_list) < total_count
    )

@transaction_router.put("/{transaction_id}")
def update_transaction(transaction_id: int, update_data: TransactionUpdate):
    """거래내역 수정"""
    result = modify_transaction(transaction_id, update_data.to_repository_dict())
    return {"message": "거래내역이 수정되었습니다", "transaction": result}