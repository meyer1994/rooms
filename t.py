from rooms.models import RoomModel

RoomModel.create_table(
    wait=True, 
    billing_mode='PAY_PER_REQUEST',
)

room = RoomModel.get('nice')
print(room)
raise SystemExit

room = RoomModel.query('nice', limit=1)
print(room.total_count)
room = next(room)
print(room)
raise SystemExit

room = RoomModel('nice')
print(room)
room = room.save()
print(room)