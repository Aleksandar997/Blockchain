import datetime
import json

class Peer:
    def __init__(self, address, date):
        self.address = address
        self.date = date

    def is_peer_active(self, compare_to):
        (compare_to - self.date).days < 1

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class PeerList(list):
    # def __init__(self):
    #     self = []

    def remove_inactive_peers(self):
        today = datetime.date.today()
        self = PeerList(filter(lambda p : p.is_peer_active(today), self))
        # return list(map(lambda p: p.address, active_peers))

    def __get_by_address(self, address) -> Peer:
        peers = list(filter(lambda p : p.address == address, self))
        if len(peers) == 0:
            return None
        return peers[0]

    def append_peer(self, address) -> Peer:
        today = datetime.date.today()
        peer = self.__get_by_address(address)
        last_peer = None
        if len(self) > 0:
            last_peer = self[-1]
        if peer == None:
            self.append(Peer(address, today))
        else:
            peer.date = today
        return last_peer

    # def get_addresses(self):
    #     return list(map(lambda p: p.address, self))