
from operator import le


class DnsResponse:
    def __init__(self, bytes, comment="") -> None:
        self.index = 0
        self.bytes = bytes
        self.comment = comment

        self.transaction_id = self.read(2)
        self.direction = self.read_bit_sequence([
            1, 
            4,
            1,
            1,
            1,
        ])
        self.request_type = "response" if self.direction[0]  == "1" else "request"
        self.question_count = int.from_bytes(self.read(2), "big") 
        self.answer_count = int.from_bytes(self.read(2), "big") 
        self.recursive_count = int.from_bytes(self.read(2), "big") 
        self.additional_records = int.from_bytes(self.read(2), "big") 

    def read_bit_sequence(self, sequence):
        assert sum(sequence) == 8
        value =  "{0:b}".format(self.bytes[self.index])
        self.index += 1
        response = []
        index = 0
        for i in sequence:
            val = value[index:index+i]
            if len(val) == 0:
                response.append("0")
            else:
                response.append(val)
            index += i
        self.index += 1
        return response

    def read(self, length):
        response = self.bytes[self.index:self.index + length]
        self.index += length
        return response

    def __str__(self) -> str:
        return """
            {comment}
            transaction_id: {transaction_id}
            direction : {direction}
            request_type: {request_type}
            question_count: {question_count}
            answer_count: {answer_count}
            recursive_count: {recursive_count}
            additional_records: {additional_records}
        """.format(
            comment=self.comment,
            transaction_id=self.transaction_id,
            direction=self.direction,
            request_type=self.request_type,
            question_count=self.question_count,
            answer_count=self.answer_count,
            recursive_count=self.recursive_count,
            additional_records=self.additional_records,
        )
    
    def __repr__(self) -> str:
        return self.__str__()
