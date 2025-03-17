from dataclasses import dataclass


@dataclass
class UserDTO:
    username: str
    password: str

    @classmethod
    def from_request(cls, data):
        return cls(
            username=data['username'],
            password=data['password']
        )
