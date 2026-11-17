"""연습용 주문 API 1차 버전입니다. 일부러 결함 두 개를 넣었으므로 실제 서비스에 쓰지 않습니다."""
from fastapi import FastAPI, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Practice Orders API", version="1.0.0")

ORDERS = {1: {"id": 1, "total": 12000, "status": "paid"},
          2: {"id": 2, "total": 8500, "status": "shipped"}}


class Order(BaseModel):
    id: int
    total: int
    status: str


@app.get("/split")
def split(total: int, people: int):
    # 결함 1: people 이 0 이어도 막지 않아 ZeroDivisionError 로 500 이 납니다.
    return {"each": total // people}


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int = Path(examples=[1, 2])):
    order = ORDERS.get(order_id)
    if order is None:
        return JSONResponse({"detail": "not found"}, status_code=404)
    if order["status"] == "shipped":
        # 결함 2: 명세는 total 이 정수인데 문자열로 돌려줍니다.
        # JSONResponse 는 response_model 검사를 거치지 않아 그대로 나갑니다.
        return JSONResponse({**order, "total": f"{order['total']}.00"})
    return order
