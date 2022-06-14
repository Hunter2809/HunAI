from __future__ import annotations


class AIUser:
    def __init__(
        me, payload: dict[str, str]
    ) -> None:  # Example: {"_id":493451846543998977,"name":"Hunter","age":"16"}
        me.id = payload["_id"] # Getting the id variable from above
        pred_items = list(payload.items()) # Example ((name, Hunter), (age, 16))
        me.pred_items = me.cleanup_pred_items(pred_items)
    
    def cleanup_pred_items(me, payload: list[tuple[str, str]]):
        items = list(payload)
        for index, pred in enumerate(items):
            if pred[0].startswith("_") and pred[0] != "_id":
                del items[index]
        return iter(items)
    
    def get_predicate(me, name: str):
        for key, value in me.pred_items:
            if key == name:
                return value

    def set_predicate(me, key: str, value: str):
        for index, pair in enumerate(me.pred_items):
            if pair[0] == key:
                list(me.pred_items)[index] = (key, value)
                break

    def __iter__(me):
        return me

    def __next__(me):
        return next(me.pred_items)

    def __repr__(me) -> str:
        return f"<User ID={me.id} with {len(tuple(me.pred_items))-1} predicates>"

    def __str__(me) -> str:
        return me.id

    def __int__(me) -> int:
        return int(me.id)
