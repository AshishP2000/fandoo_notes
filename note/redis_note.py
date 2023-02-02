import json

from note.redis_service import RedisCrud


class RedisNote:

    def __init__(self):
        self.redis = RedisCrud()

    def save(self, notes, user_id):
        note_dict = self.get(user_id)
        note_id = str(f'note_{notes.get("id")}')
        note_dict.update({note_id: notes})
        self.redis.setter(user_id, json.dumps(note_dict))

    def get(self, user_id):
        key = f'note_{user_id}'
        payload = self.redis.getter(key[5:6])
        return payload

    def delete(self, user_id, note_id):
        notes_dict = self.get(user_id)
        note = notes_dict.get(str(f'note_{note_id}'))
        if note is not None:
            notes_dict.pop(str(f'note_{note_id}'))
            self.redis.setter(user_id, json.dumps(notes_dict))


# if __name__ == '__main__':
#     r = RedisNote()
    # r.save({'id': 2, 'note_title': 'something', 'note_body': 'hi to everyone', 'user': 2}, 2)
    # r.delete(2, 2)
    # print(r.get(1))
    # print(r.redis.redis_client.keys("*"))
# user_1_note : {"id":1,"title_note":"some",""}
