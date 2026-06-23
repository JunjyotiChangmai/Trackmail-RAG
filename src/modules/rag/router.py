from fastapi import APIRouter, HTTPException, status
from src.modules.rag.schemas import QueryRequest, QueryResponse
from src.modules.rag.services import rag_service

router = APIRouter(prefix="/rag", tags=["RAG Application"])

@router.post("/query", response_model=QueryResponse, status_code=status.HTTP_200_OK)
async def query_rag(payload: QueryRequest):
    try:
        answer = await rag_service.get_answer(payload.question)
        return QueryResponse(question=payload.question, answer=answer)
    except ValueError as val_err:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(val_err))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error processing RAG query: {str(e)}")