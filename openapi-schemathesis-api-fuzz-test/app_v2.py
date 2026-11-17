"""연습용 주문 API 2차 버전입니다. 1차의 결함 두 개를 고쳤습니다."""
from fastapi import FastAPI, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Practice Orders API", version="1.0.1")

ORDERS = {1: {"id": 1, "total": 12000, "status": "paid"},
          2: {"id": 2, "total": 8500, "status": "shipped"}}


class Order(BaseModel):
    id: int
    total: int
    status: str


@app.get("/split")
def split(total: int = Query(ge=0, le=1_000_000_000),
          people: int = Query(ge=1, le=1000)):
    # 수정 1: 범위를 명세에 적어 0 은 422 로 거절됩니다.
    return {"each": total // people}


@app.get("/orders/{order_id}", response_model=Order,
         responses={404: {"description": "없는 주문"}})
def get_order(order_id: int = Path(examples=[1, 2])):
    order = ORDERS.get(order_id)
    if order is None:
        return JSONResponse({"detail": "not found"}, status_code=404)
    # 수정 2: 모든 상태에서 명세대로 total 을 정수로 돌려줍니다.
    return order
